# 中文语料 EEG 数据集构建与高级语义解码

## 简介

利用丰富文本刺激构建的脑电图（EEG）数据集可以增进我们对大脑如何编码语义信息的理解，并有助于脑机接口（BCI）中的语义解码。针对中文语言刺激 EEG 数据集稀缺的问题，我们提出了 ChineseEEG 数据集——一个高密度 EEG 数据集，并辅以同步的眼动记录。该数据集在 10 名被试默读两本知名小说约 11 小时中文文本的过程中采集完成。该数据集提供了长时间跨度的 EEG 记录，以及预处理后的 EEG 传感器级数据，和由预训练自然语言处理（NLP）模型提取的阅读材料语义嵌入。

**关于我们数据集的更详细信息，请查阅我们在 bioRxiv 上的预印本论文：[ChineseEEG: A Chinese Linguistic Corpora EEG Dataset for Semantic Alignment and Neural Decoding](https://www.biorxiv.org/content/10.1101/2024.02.08.579481v1)。**

**你可以通过中国神经交响乐社区（CHNNeuro）在科学数据银行平台（[https://doi.org/10.57760/sciencedb.CHNNeuro.00007](https://doi.org/10.57760/sciencedb.CHNNeuro.00007)）或通过 Openneuro（[https://openneuro.org/datasets/ds004952](https://openneuro.org/datasets/ds004952)）访问我们的数据集。**

本仓库包含复现我们论文中实验和数据处理流程所需的全部代码。它旨在为基于中文语料构建 EEG 数据集提供一个全面的范式，并期望促进基于 EEG 的语义解码和脑机接口相关技术的发展。

项目主要分为四个模块。`novel_segmentation_and_text_embeddings` 文件夹中的脚本 `cut_chinese_novel.py` 包含从源材料准备刺激材料的代码。experiment 模块中的脚本 `play_novel.py` 包含实验代码，包括文本刺激呈现以及对 EGI 设备和 Tobii Glasses 3 眼动仪的控制。`data_preprocessing_and_alignment` 模块中的脚本 `preprocessing.py` 包含对 EEG 数据进行预处理的主要代码。同一模块中的脚本 `align_eeg_with_sentence.py` 包含将 EEG 分段与相应文本内容和文本嵌入对齐的代码。`docker` 模块包含部署和运行代码所需的 Docker 镜像，以及如何使用 Docker 进行环境部署的教程。关于每个模块的详细信息，请参阅相应模块中的 README 文档。

## 流水线

我们的 EEG 记录与预处理流水线如下：

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/pipeline_english.png)

## 设备

### EEG 记录：EGI Geodesic EEG 400 系列

在实验过程中，EEG（脑电图）数据由配备 Geodesic Sensor Net 的 `128 通道` EEG 系统采集（EGI Inc., Eugene, OR, USA，[Geodesic EEG System 400 series (egi.com)](https://www.egi.com/clinical-division/clinical-division-clinical-products/ges-400-series)）。该设备的导联排布系统为 `GSN-HydroCel-128`。我们以 1000 Hz 的采样率记录数据。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/egi_montage.png)

EGI 的带 Geodesic Sensor Net (GSN) 的 128 通道 EEG 系统是一种精密的脑活动记录工具，专为高分辨率神经科学研究设计。该系统具有均匀分布的传感器阵列，提供完整的头皮覆盖，无需插值即可实现详细的空间数据采集。配合先进的 Net Amps 400 放大器和直观的 Net Station 5 软件，它能提供低噪声、高灵敏度的 EEG 数据采集和强大的数据分析能力，是动态和不断扩展的研究环境的理想选择。

### 眼动追踪：Tobii Pro Glasses 3

我们使用 Tobii Pro Glasses 3（[Tobii Pro Glasses 3 | Latest in wearable eye tracking - Tobii](https://www.tobii.com/products/eye-trackers/wearables/tobii-pro-glasses-3)）记录被试的眼动轨迹，以检查他们是否遵循了实验指导，即他们的视线应随着红色高亮文本移动。

Tobii Pro Glasses 3 是先进的穿戴式眼动仪。它能够捕获真实世界环境中的自然观看行为，从第一人称视角提供强有力的洞察。该设备具有 16 个照明器和集成在防刮镜片中的四个眼球相机、一个广角场景相机和一个内置麦克风，能够全面捕获被试行为和环境背景。其眼动追踪在不同人群中均可靠，不受眼睛颜色或形状的影响。Tobii Pro Glasses 3 以 50 Hz 或 100 Hz 的高采样率工作，并支持单点校准程序。

## 实验

在实验的准备阶段，我们首先为被试佩戴脑电帽和眼动仪，与屏幕保持 67 cm 的距离。我们强调被试在实验过程中应保持头部不动，且视线应跟随图中所示的红色高亮文本。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/screen.png)

在确保被试完全理解指导后，我们开始实验流程。首先进行眼动校准阶段，然后是练习阅读阶段，最后是正式阅读阶段。每个正式阅读阶段持续约 30 分钟。实验设置如下：

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/exp_layout.png)

## 使用说明

通常，你可以按照以下步骤执行代码来准备实验材料、进行实验以及开展后续数据分析。

### 环境设置

首先，请确保你的代码运行环境已正确设置。你可以选择为此创建 Docker 容器，或直接在个人电脑上安装所需包。

如果你选择使用 Docker，可以参考[这里](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/docker/README.md)提供的详细教程。如果你计划在本地环境中安装包，所需包及其对应版本信息可以在项目根目录下的 [requirement.txt](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/requirements.txt) 文件中找到。

### 实验材料准备

此步骤主要涉及准备实验所需的文本阅读材料。你需要首先将材料转换为下面所示的特定格式（文件名为 `Chinese_novel.txt`）：

```
Ch0
This is the preface of the novel
Ch1
Chapter 1 of the novel
Ch2
Chapter 2 of the novel
...
...
...
```

然后运行位于 `novel_segmentation` 文件夹中的 `cut_Chinese_novel.py` 脚本对小说文本进行句子切分：

```
python cut_Chinese_novel.py --divide_nums=<chapter numbers of the cutting point> --Chinese_novel_path=<path to your .txt file of the novel>
```

我们已将实验中使用的文本材料上传到 `text materials` 发行版，包括两本知名小说的中文版本，**《小王子》** 和 **《琅琊榜·浪浪梦》**（Garnett Dream）。

关于格式要求和脚本执行命令的详细信息，请访问 [novel_segmentation_and_text_embeddings](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/tree/main/novel_segmentation_and_text_embeddings) 模块了解更多详情。

### 实验

一旦我们获得了切分成特定格式的文本材料，我们就可以使用 `experiment` 模块中的 `play_novel.py` 运行实验程序。该程序将按照特定的实验范式呈现这些文本材料，并记录被试的 EEG 和眼动数据。运行程序前，请确保文本材料的路径已正确设置，且 EEG 和眼动设备已正确连接。使用以下命令运行程序：

```
python play_novel.py --add_mark --add_eyetracker  --preface_path=<your preface path> --host_IP=<host IP> --egi_IP=<egi IP> --eyetracker_hostname=<eyetracker serial number> --novel_path=<your novel path> --isFirstSession
```

关于具体实验范式、相关参数设置等详细信息，请参阅 [experiment](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/tree/main/experiment) 模块。

### 数据预处理

在完成所有被试的实验数据采集后，我们可以使用 `data_preprocessing` 模块中的 `preprocessing.py` 进行数据预处理。我们的预处理流程包括一系列步骤，如数据分段、降采样、滤波、坏通道插值、独立成分分析（ICA）和重参考。在坏通道插值和 ICA 阶段，我们实现了自动化算法，但也提供了手动干预的选项以确保准确性。所有这些方法的参数都可以通过调整代码中的设置来修改。

关于预处理流程、代码说明和参数设置的详细信息，请参阅 [data_preprocessing](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/tree/main/data_preprocessing) 模块。

### 文本嵌入

我们提供阅读材料的嵌入。每次 run 中的文本刺激都有对应的嵌入文件，以 `.npy` 格式保存。这些文本嵌入为一系列后续研究奠定了基础，包括 EEG 和文本数据在表征空间中的对齐分析，以及 EEG 语言解码等任务。关于详细信息，请参阅 [novel_segmentation_and_text_embeddings](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/tree/main/novel_segmentation_and_text_embeddings) 模块。

### 数据对齐

当你拥有文本、文本嵌入和各 run 的 EEG 数据后，你可以将它们对齐以进行后续分析。我们提供代码将 EEG 数据与其对应的文本和嵌入对齐。关于详细信息，请参阅 [data_preprocessing_and_alignment](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/tree/main/data_preprocessing_and_alignment) 模块。

## 致谢

- [Mou Xinyu](https://github.com/12485953) - 项目所有部分的编码者、数据处理。

- [He Cuilin](https://github.com/CuilinHe) - 实验执行者、数据处理。

- [Tan Liwei](https://github.com/tanliwei09) - 实验执行者、数据处理。

- [Zhang Jianyu](https://github.com/ionaaaa) - 中文语料切分和 EEG 随机掩码的编码者。

- [Tian Yan](https://github.com/Bryantianyan) - 实验执行者

- [Chen Yizhe]() - 实验仪器调试

  如果您对本项目有任何疑问，欢迎随时联系我们！！！

## 合作者
- [Wu Haiyan](https://github.com/haiyan0305) - 澳门大学

- [Liu Quanying] - 南方科技大学

- [Wang Xindi](https://github.com/sandywang)

- [Wang Qing] - 上海交通大学

- [Chen Zijiao] - 新加坡国立大学

- [Yang Yu-Fang] - 柏林自由大学

- [Hu Chuanpeng] - 南京师范大学

- [Xu Ting] - 儿童心智研究所整合发育神经科学中心，纽约

- [Cao Miao] - 斯威本科技大学

- [Liang Huadong](https://github.com/Romantic-Pumpkin) - 科大讯飞股份有限公司

## 基金支持

本工作主要得到天桥脑科学研究院（TCCI）MindD 项目、澳门科学技术发展基金（FDCT）[0127/2020/A3, 0041/2022/A]、广东省自然科学基金（2021A1515012509）、深圳市港澳科技创新项目（C 类）（SGDX2020110309280100）以及澳门大学 SRG（SRG2020-00027-ICI）的支持。我们还要感谢所有在研究助理招募和数据收集方面提供一般支持的研究助理。
