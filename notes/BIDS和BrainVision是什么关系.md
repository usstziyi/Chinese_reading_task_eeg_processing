一句话：**BIDS 是"目录组织与元数据规范"，BrainVision 是"一种具体的数据文件格式"**——前者是容器和规则，后者是能装进这个容器的一种数据。两者不是同一层面的东西，不是竞争关系。

## 打比方

- **BIDS** ≈ 图书馆的编目规范：书怎么编号、放哪个书架、每本书要配哪些卡片（`sub-XX_ses-YY_task-ZZ_...` 命名 + `_eeg.json`、`_events.tsv` 等侧车文件）。
- **BrainVision** ≈ 书的装帧格式：内容实际以什么形式印在纸上（`.vhdr` + `.vmrk` + `.eeg`）。

同一套 BIDS 目录里，数据本体可以是好几种格式之一（BrainVision、EDF、EEGLAB `.set`、FIF…），BIDS 只管**怎么摆、怎么命名、附哪些元数据文件**。

## 具体关系

| | BIDS | BrainVision |
|---|---|---|
| 是什么 | 数据组织标准（目录结构 + 命名约定 + JSON/TSV 侧车） | 数据存储格式（三文件：头/标记/二进制） |
| 管什么 | 文件放哪、叫什么名、有哪些配套元数据 | 信号与标记怎么编码进文件 |
| 层次 | 外层"容器/规范" | 内层"被承载的格式之一" |
| 谁依赖谁 | 不依赖具体格式（但限定可选格式列表） | 不关心你是否用 BIDS |

**关键点：BIDS 对 EEG 只接受若干被认可的格式**，BrainVision 是其中最主流的一个。`.mff` 不在这份正式列表内，所以本项目必须先把 EGI 的 `.mff` 转成 BrainVision 才能合规——这正是 README 里那句话的原因。

## BIDS 在 BrainVision 三件套之外还要求什么

放在 BIDS 目录里时，除三件套外还必须有：

```
sub-07/ses-LittlePrince/eeg/
├── sub-07_ses-LittlePrince_task-reading_run-1_eeg.vhdr   ← 主文件
├── sub-07_ses-LittlePrince_task-reading_run-1_eeg.vmrk
├── sub-07_ses-LittlePrince_task-reading_run-1_eeg.eeg
├── sub-07_ses-LittlePrince_task-reading_run-1_eeg.json   ← 采集元数据（采样率等）
├── ..._channels.tsv                                      ← 通道信息
├── ..._events.tsv / _events.json                         ← 事件表
└── ..._coordsystem.json、_electrodes.tsv                  ← 电极/坐标
```

注意这里有个**职责重叠**要注意：

- BrainVision 自己的 `.vmrk` 存标记；
- BIDS 另外要求一份 `_events.tsv`（列为 `onset`、`duration`、`trial_type`…）。

也就是说同样的事件信息会**同时存在于两处**：`.vmrk`（格式内部）和 `_events.tsv`（BIDS 规范要求）。文件名的实体部分（`sub-07_ses-..._run-1`）是三件套共用的基名。

## 落到本项目

转换就是"**把 .mff 数据放进 BIDS 容器，并选 BrainVision 作为内部格式**"：

[convert_eeg_to_bids.py#L43-L55](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/data_preprocessing_and_alignment/convert_eeg_to_bids.py#L43-L55)

```python
write_raw_bids(raw, bids_path, format='BrainVision', allow_preload=True, overwrite=True)
```

- `format='BrainVision'` → 决定**内层格式**（写 `.vhdr/.vmrk/.eeg`）
- `bids_path` / `write_raw_bids` → 负责**外层 BIDS 规范**（目录、命名、`_eeg.json`、`_channels.tsv`、`_events.tsv` 等）

反过来说，用 `mne_bids.read_raw_bids()` 读时，它按 BIDS 规范定位到那个 `.vhdr`，再用 BrainVision 读取器解析三件套——**BIDS 负责"找到并配上元数据"，BrainVision 负责"解码数据本体"**。