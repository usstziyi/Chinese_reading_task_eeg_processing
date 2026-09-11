BrainVision（Brain Products 的 Brain Vision Core Data Format）采用**三文件结构**，三者**同目录、同基名、扩展名不同**，且必须成套存在。

## 主文件 / 辅助文件

| 文件 | 角色 | 内容 | 是否必需 |
|------|------|------|----------|
| **`.vhdr`** | **主文件（入口）** | 文本 INI 格式的**头文件**：采样率、通道数、通道名/单位、数据文件与 marker 文件名、二进制格式等 | 必需 |
| `.vmrk` | 辅助 | 文本 INI 格式的**标记文件**：所有事件/触发（类型、描述、位置、时长） | 必需（MNE 会无条件打开它） |
| `.eeg` | 辅助 | **二进制信号数据本体**（也可为 `.dat`） | 必需 |

读数据时**必须从 `.vhdr` 入手**，MNE 的 `read_raw_brainvision()` 只接受头文件；传 `.eeg` 或 `.vmrk` 会报错：

[brainvision.py#L529-L535](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/.venv/Lib/site-packages/mne/io/brainvision/brainvision.py#L529-L535)

```python
ext = op.splitext(hdr_fname)[-1]
if ext not in (".vhdr", ".ahdr"):
    raise OSError("The header file must be given to read the data, not a file with extension ...")
```

## `.vhdr` 里如何指向另外两个文件

关键在 `[Common Infos]` 段的 `DataFile=` 和 `MarkerFile=`：

```
Brain Vision Data Exchange Header File Version 1.0
[Common Infos]
Codepage=UTF-8
DataFile=sub-07_task-reading_eeg.eeg      ← 指向数据文件
MarkerFile=sub-07_task-reading_eeg.vmrk   ← 指向标记文件
DataFormat=BINARY
DataOrientation=MULTIPLEXED
NumberOfChannels=129
SamplingInterval=3906.25                  ← 单位微秒，sfreq = 1e6 / 该值 ≈ 256 Hz
[Binary Infos]
BinaryFormat=IEEE_FLOAT_32
[Channel Infos]
Ch1=E1,,1,µV
Ch2=E2,,1,µV
...
```

MNE 就是靠这两行拼出另外两个文件的路径：

[brainvision.py#L559-L562](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/.venv/Lib/site-packages/mne/io/brainvision/brainvision.py#L559-L562)

```python
path = op.dirname(hdr_fname)
data_fname = op.join(path, cfg.get(cinfostr, "DataFile"))
mrk_fname = op.join(path, cfg.get(cinfostr, "MarkerFile"))
```

**含义**：文件名是相对 `.vhdr` 所在目录记录的——所以要整体移动/改名时，三个文件必须一起保持同名同目录，否则引用会断。

## `.vmrk` 里的标记格式

每条标记一行 `Mk序号=类型,描述,位置,大小,通道号`：

```
[Marker Infos]
Mk1=New Segment,,1,1,0,20240101120000000000
Mk2=Stimulus,CH01,1500,0,0
Mk3=Stimulus,ROWS,1600,0,0
```

字段含义（MNE 解析逻辑见 [brainvision.py#L296-L313](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/.venv/Lib/site-packages/mne/io/brainvision/brainvision.py#L296-L313)）：

| 字段 | 说明 |
|------|------|
| 类型 | `Stimulus` / `Response` / `Comment` / `New Segment` |
| 描述 | 标记内容（可空），可含 `\1` 转义的逗号 |
| 位置 | **采样点索引，1-indexed**（MNE 会减 1） |
| 大小 | 时长（采样点），0 表示瞬时 |
| 通道号 | 关联通道，0 表示无 |

MNE 读进来后组合成 annotations，描述为 `类型/描述`：

[brainvision.py#L361-L367](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/.venv/Lib/site-packages/mne/io/brainvision/brainvision.py#L361-L367)

```python
onset = np.array(onset, dtype=float) / sfreq
duration = np.array(duration, dtype=float) / sfreq
description = [f"{t}/{d}" for t, d in zip(type_, description)]
annotations = Annotations(onset=onset, duration=duration, description=description, ...)
```

所以 `Mk2=Stimulus,CH01,...` 在 MNE 里就是 description 为 `Stimulus/CH01` 的 annotation。第一条 `New Segment` 只用来确定记录时间（`meas_date`），随后会被跳过。

## 变体

- **数据文件扩展名**：除 `.eeg` 外也可能是 `.dat`（向量化导出）；MNE 以 `.vhdr` 里 `DataFile=` 指定的实际文件名为准，不写死扩展名。
- **`.ahdr` / `.amrk`**：其他厂商（如 Brain Products 的 NeurOne 导出）用的变体头文件，`.vhdr` 不存在时 MNE 会回退到 `.ahdr`（[brainvision.py#L346-L349](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/.venv/Lib/site-packages/mne/io/brainvision/brainvision.py#L346-L349)）。
- **ASCII 格式**：`DataFormat=ASCII` 时数据文件是文本而非二进制（MNE 支持有限）。

## 写回时的对应关系

导出时 MNE 会把 annotations 反向写进 `.vmrk`，描述前缀决定类型（[export/_brainvision.py#L125-L146](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/.venv/Lib/site-packages/mne/export/_brainvision.py#L125-L146)）：

- `Stimulus/S...` → 类型 `Stimulus`
- `Response/R...` → 类型 `Response`
- 其余 → 类型 `Comment`

## 与本项目的关系

本项目把 EGI `.mff` 转成 BrainVision 以满足 BIDS 要求，用的是 `mne_bids`：

[convert_eeg_to_bids.py#L43-L55](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/data_preprocessing_and_alignment/convert_eeg_to_bids.py#L43-L55)

```python
write_raw_bids(raw, bids_path, format='BrainVision', allow_preload=True, overwrite=True)
```

即最终目录里每个 run 是 `..._eeg.vhdr`（主文件）+ `..._eeg.vmrk`（标记）+ `..._eeg.eeg`（数据）三件套；原来的 EGI 触发/标注就落在 `.vmrk` 中。这与 README 所说的"转换为 .vhdr / .vmrk / .eeg 文件"一致。