# 项目模块概览

本仓库用于复现 **ChineseEEG 数据集** 的完整流程：让被试默读中文小说，同时用 128 通道 EGI 脑电仪和 Tobii Glasses 3 眼动仪同步记录脑电与眼动数据，并支持后续的 EEG-文本对齐与语义解码分析。

项目整体划分为 **四大模块**，外加一套 Docker 环境部署方案，各模块职责与关键脚本如下。

## 一、材料准备模块：`novel_segmentation_and_text_embeddings`

> 负责把原始小说文本加工成实验所需的刺激材料，并生成对应的文本嵌入。

- **`cut_chinese_novel.py`** — 刺激材料准备脚本
  - 将 `.txt` 格式的中文小说按句子/单元切分，输出适合 PsychoPy 呈现的 `.xlsx` 文件。
  - 支持按章节断点（`--divide_nums`）把整本小说拆成多个部分，便于分次实验（如更换眼动仪电池）。
  - 输入要求：文件以 `Ch0`（前言）开头，后续各章以 `Ch+章节号` 标记。
  - 输出三类文件：整本书 `segmented_Chinese_novel.xlsx`、单次 run `segmented_Chinese_novel_run_xx.xlsx`、以及用于屏幕呈现的 `_display.xlsx`。
- **`embedding.py`** — 文本嵌入生成脚本
  - 使用预训练语言模型 `bert-base-chinese`，为每行刺激文本生成统一长度的嵌入向量。
  - 输入即分段输出文件 `segmented_Chinense_novel_run_xx.xlsx`（非 display 版本），逐行生成嵌入；与对齐脚本读取同一份文本，确保行序一致。
  - 按 run 组织，以 `.npy` 格式保存，供后续对齐与解码分析使用。

## 二、实验模块：`experiment`

> 负责正式实验的运行：文本刺激呈现 + 同步控制 EGI 脑电仪与 Tobii Glasses 3 眼动仪。

- **`play_novel.py`** — 主实验脚本（基于 PsychoPy 编写，实验环境须为 Python 3.10）
  - 支持多种运行模式，可自由选择是否连接 EGI 设备（`--add_mark`）与眼动仪（`--add_eyetracker`）。
  - 实验流程：眼动校准（若启用）→ 练习阅读（仅首次会话）→ 正式阅读 → 章节间休息，休息后重新校准。
  - 呈现方式：每页三行、每行不超过 10 个汉字（不含标点），中间行高亮作为注视焦点，逐字按设定时长高亮，被试需跟随高亮阅读。
  - 同步打标（EEG Markers）：`EYES/EYEE`（眼动起止）、`CALS/CALE`（校准起止）、`BEGN/STOP`（EGI 起止）、`CH01...`（章节开始）、`ROWS/ROWE`（行起止）、`PRES/PREE`（前言起止），用于后续 EEG 与文本的精确对齐。
  - 内置自定义校准流程，通过眼动-屏幕坐标转换公式计算校准误差，未达阈值则自动重校准。

## 三、数据预处理模块：`data_preprocessing_and_alignment`

> 负责对原始 EEG 数据进行预处理，并将 EEG 分段与对应文本、文本嵌入对齐。

- **`preprocessing.py`** — EEG 预处理主脚本（依赖 MNE、mne-bids、pybv）
  - 预处理流水线：数据分段 → 降采样 + 陷波滤波 → 带通滤波（0.5–80 Hz 与 0.5–30 Hz 两版）→ 坏导插值/坏段标记 → ICA（infomax，默认 20 个分量）去除眼电、心电、肌电等伪迹 → 平均参考。
  - 全程支持 MNE 图形界面手动干预（剔除 ICA 分量、选择坏通道、标记坏段、检查结果）。
  - 原始数据与预处理后数据均按 **BIDS 格式** 保存。
- **`align_eeg_with_sentence.py`** — EEG 与文本/嵌入对齐脚本
  - 输入：`.vhdr` EEG 文件、对应 run 的小说 `.xlsx`、对应 run 的文本嵌入 `.npy`。
  - 输出：按 marker 切分出的 `cut_eeg_data` 分段、对应的 `texts` 与 `text_embeddings`。
  - **对齐用的是“处理后的分段文本”，不是原始小说**：
    - `texts` 直接读取分段文件 `segmented_Chinense_novel_run_xx.xlsx`（从第 2 行起读第 1 列，首个单元格为章节号，用于定位起始 marker `CH0X`），与 `embedding.py` 生成嵌入时读取的是**同一份文件**，保证三者按行一一对应。
    - 该文本已按屏幕呈现行切分（每行 ≤10 个汉字），且**纯标点行已被剔除**（此类行不呈现在屏幕中央行，无对应 EEG 分段）。
    - 用的是**非 display 版本** `_run_xx.xlsx`；`_display.xlsx` 仅用于 `play_novel.py` 的屏幕呈现，不参与对齐。
- 同目录辅助脚本：`convert_eeg_to_bids.py`（BIDS 转换）、`utils.py`（公共工具）、`forward.py` / `inverse.py`（正/逆模型相关）。

## 四、环境部署模块：`docker`

> 提供一键复现实验/处理环境的 Docker 方案，降低环境配置门槛。

- **Dockerfile** — 基于 `ubuntu:22.04` 构建镜像 `mouxinyu/eeg_dataset`，预装全部依赖、项目代码与带 GUI 的 PyCharm。
- **README.md** — Windows 环境下的完整部署教程：
  - 安装 WSL2 → 安装 Docker Desktop → 安装 VcXsrv（提供 GUI）→ `docker pull mouxinyu/eeg_dataset` → `docker run` 创建并进入容器。
  - 容器内置 `root` / `mynewuser` 两个用户，推荐使用 `mynewuser`，通过挂载（`-v`）与宿主机交换文件。

## 模块间协作流程

```
原始小说(.txt)
   │  cut_chinese_novel.py          （模块一：材料准备）
   ▼
分段刺激材料: segmented_Chinense_novel_run_xx.xlsx（已切行、剔除纯标点行）
   │
   ├──► embedding.py ──► 文本嵌入(.npy)        （模块一：同源分段文本生成嵌入）
   │
   ▼
play_novel.py                        （模块二：实验）
   │  呈现 _display.xlsx 刺激 + 打标，采集 EEG(EGI) 与眼动(Tobii)
   ▼
原始 EEG ──► preprocessing.py ──► 预处理后 BIDS 数据
   │                                  （模块三：预处理）
   ▼
align_eeg_with_sentence.py           （模块三：对齐）
   │  用同一份分段文本(_run_xx.xlsx) + 文本嵌入 + marker 切分 EEG
   ▼
后续分析（语义对齐 / 语义解码）
```

> 各模块详细说明、参数设置与运行命令，请参见对应目录下的 `README.md`。
