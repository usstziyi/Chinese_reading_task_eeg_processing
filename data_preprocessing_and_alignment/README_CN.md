# EEG 预处理与对齐文档

本文档说明了我们的 EEG 预处理流水线，以及如何使用我们的代码处理 EEG 数据。此外，还提供了我们数据集的说明供参考。

另外，我们还提供了将 EEG 数据、文本和文本嵌入进行对齐的代码。

## 数据预处理流水线

在这里，我们对数据进行预处理，以最大程度地去除明显伪迹。我们的预处理流水线总览如下图所示。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/processing_pipeline.png)

我们的处理流程包括以下步骤：

#### 数据分段

我们会在有效时间范围前后保留一小段时间。我们将通过参照 EEG 标记来定位切分位置。详细信息可参见 `preprocessing.py` 中的 `cut_single_eeg` 方法。在我们的流程中，我们将有效范围之前保留的时间设置为 10 秒。

#### 重采样与陷波滤波

在 ICA 之前，我们会先进行一些基本步骤，包括对数据进行降采样并滤除工频。在我们的设置中，重采样频率设为 256 Hz，工频设为 50 Hz。

#### 滤波

我们将使用带通滤波器对数据进行滤波以去除伪迹。在我们的处理中，我们做了两个版本的滤波，一个通带设置为 0.5-80 Hz，另一个设置为 0.5-30 Hz。

#### 坏通道插值与坏段标记

然后我们将使用 `MNE` 包中实现的方法对坏通道进行插值。我们还会将看起来像坏段的片段用 "bad" 标签标记出来，以供参考。这可以在 GUI 中完成，我们稍后会解释。

#### ICA

我们使用 ICA 去除眼电、心电、肌电伪迹以及其他可能的伪迹。在我们自己的处理中，我们将参数 `ica_n_component` 设置为 20，以确保能发现所有可能的伪迹。我们使用 `infomax` 算法。你可以自行更改这些参数。关于如何更改参数的详细信息将在代码部分说明。

#### 重参考

最后，我们对数据进行重参考。在我们的实现中，我们使用 "average"（平均）方法。

## 代码

### 环境要求

我们推荐使用 Python 3.10，这是我们自己使用的设置。

需要 `MNE`、`mne-bids`、`pybv` 这三个包。可以使用以下命令获取：

```
conda install --channel=conda-forge mamba
mamba create --override-channels --channel=conda-forge mne
```

```
pip install --upgrade mne-bids[full]
```

```
pip install pybv
```

**请确保使用上述命令安装了完整的 `mne` 包，否则你将无法正确使用 MNE 方法的 GUI。支持 GUI qt-browser 需要 `MNE` 版本 >= 1.0。** 推荐使用 `pybv`==0.7.5。更多信息请参阅以下页面：https://mne.tools/stable/install/manual_install.html#manual-install、https://mne.tools/mne-bids/stable/install.html、https://pybv.readthedocs.io/en/stable/。

### 代码用法

在代码 `preprocessing.py` 中，你可以更改给定参数以按自己的设置对数据进行预处理，并将**原始数据和预处理后的数据以 BIDS 格式保存**。

该代码将首先切分 EEG 数据。在有效 EEG 段开始前会保留一小段时间。你可以使用参数 `remaining_time_at_beginning` 指定该时间。切分后，代码将运行主要的预处理流水线。在整个预处理过程中，会出现三个 GUI 阶段。第一个阶段显示所有 ICA 分量源。你可以通过点击分量来排除想要剔除的分量。第二个阶段显示带通滤波后的数据。在此阶段，你可以像在第一阶段中那样通过点击通道来选择坏通道。你还可以通过用 "bad" 标签标注来屏蔽可能的坏段。最后一个阶段将显示重参考之后的数据，这是预处理的最后一步。在此阶段，你可以检查预处理后的数据是否满足你的需求。

参数的详细信息如下：

| 参数                       | 类型  | 说明                                                            |
| -------------------------- | ----- | --------------------------------------------------------------- |
| eeg_path                   | str   | 未处理 EEG 的数据路径                                            |
| sub_id                     | str   | 被试 ID 的字符串。如果 ID 只有一位数，请在前面补 0。              |
| ses                        | str   | 描述当前数据会话的字符串。保存文件时它将包含在文件名中。          |
| task                       | str   | 描述当前数据任务的字符串。保存文件时它将包含在文件名中。          |
| run                        | int   | 表示数据 run 编号的整数。                                        |
| raw_data_root              | str   | 原始数据的路径，也是整个数据集的根目录。                          |
| filtered_data_root         | str   | 滤波后数据的路径。                                               |
| processed_data_root        | str   | 预处理后数据的路径。                                             |
| dataset_name               | str   | 数据集名称，将保存在 dataset_description.json 中。                |
| author                     | str   | 数据集的作者。                                                   |
| line_freq                  | float | 数据的工频。将数据保存为 BIDS 格式时需要。默认为 50。              |
| start_chapter              | str   | 当前 EEG 数据中第一章的 EEG 标记字符串。例如，如果 EEG 从第 1 章开始，则该参数应为 'CH01'。 |
| low_pass_freq              | float | 滤波器的低通频率                                                |
| high_pass_freq             | float | 滤波器的高通频率                                                |
| resample_freq              | float | 滤波器的重采样频率                                              |
| remaining_time_at_beginning | float | 有效 EEG 段开始前保留的时间                                      |
| montage_name               | str   | EEG 的导联排布（montage）                                        |
| ica_method                 | str   | 使用哪种 ICA 方法。参见 mne 教程了解详细信息                      |
| ica_n_components           | int   | 使用多少个 ICA 分量。参见 mne 教程了解详细信息                    |
| rereference                | str   | 想要使用的重参考方法                                              |

## 数据集

你可以通过 Openneuro 平台（https://openneuro.org/datasets/ds004952）或通过 Science Data Bank（ScienceDB）平台中的 ChineseNeuro Symphony 社区（CHNNeuro）（https://doi.org/10.57760/sciencedb.CHNNeuro.00007）访问我们的数据集。

我们的数据按照 BIDS 标准格式的要求进行格式化，如下图所示。

我们数据结构的详细格式可以在我们的论文中找到：https://doi.org/10.1101/2024.02.08.579481。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/structure_new.png)

## 手动处理标准

示例名称：subject_04_eeg_01

ICA 示例图：

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/ica_topo.png)

需要剔除的分量：

ICA001：该分量在前额区域存在局部最大值，这是眨眼伪迹的典型特征。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/ica_001.png)

ICA006：该分量可能代表眼动或眼球扫视伪迹，因为它在头皮前额和两侧表现出局部最大值。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/ica_006.png)

ICA010：该分量可能与眼动和心电伪迹有关，因为它在前额区域和耳朵附近表现出局部最大值。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/ica_010.png)

ICA007：该分量可能在时间上与心电伪迹有关，因为其特征是耳朵附近有显著的极大值。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/ica_007.png)

ICA015：该分量可能在时间上与心电伪迹有关，因为它在头皮边缘表现出特征性极大值。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/ica_015.png)

## 数据对齐

这里我们提供脚本 `align_eeg_with_sentence.py`，用于获取 EEG 及其对齐的文本和文本嵌入。你只需为该方法指定三个参数：

| 参数                | 类型 | 说明                                        |
| ------------------- | ---- | ------------------------------------------- |
| eeg_path            | str  | 你的 `.vhdr` EEG 文件的路径                 |
| novel_xlsx_path     | str  | 对应 run 的小说的路径                       |
| text_embedding_path | str  | 对应 run 的文本嵌入的路径                   |

该方法将返回三个变量：`cut_eeg_data`、`texts` 和 `text_embeddings`。`cut_eeg_data` 是一个列表，包含按标记切分的 EEG 分段。`texts` 包含与切分出的 EEG 分段对应的文本，`text_embeddings` 包含由预训练语言模型生成的对应文本嵌入。

**注意：由于实验过程中的特殊情况，LangWangMeng 会话中的被试 07 在第 18 次 run 中未按原定计划阅读第 18 章的内容，而是改读了第 19 章的内容作为替代。因此，在该特定情况下，第 18 次 run 的 EEG 数据与第 18 个文本嵌入文件之间没有直接对应关系。**
