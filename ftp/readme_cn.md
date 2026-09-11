# ChineseEEG：用于语义对齐与神经解码的中文语料 EEG 数据集

## 简介

"ChineseEEG"（中文语料 EEG 数据集）包含 10 名被试的高密度 EEG 数据以及同步采集的眼动数据，每名被试默读中文文本约 11 小时。该数据集还包含在不同参数设置下生成的预处理 EEG 传感器级数据，为研究者提供了多样化的选择。此外，我们还提供了使用 BERT-base-chinese 模型（一种专为中文设计的预训练 NLP 模型）对中文文本材料编码得到的嵌入向量，帮助研究者探索 NLP 模型文本嵌入与大脑信息表征之间的对齐关系。

## 被试概况

数据集共使用 10 名被试的数据（年龄 18-24 岁，平均 20.68 岁，其中 5 名男性）。无被试报告有神经或精神疾病史。所有被试均为右利手，且视力正常或矫正后正常。

## 实验材料

实验材料由两部中文小说组成，均属儿童文学体裁。第一部是 **The Little Prince**（《小王子》），第二部是 **Garnett Dream**（《格兰特之梦》）。

对于 **The Little Prince**，其序言（preface）被用作练习阅读阶段的材料。小说正文随后用于正式阅读阶段的七次（session）实验。前六次 session 各包含小说的 4 个章节，第七次 session 包含最后两个章节。

对于 **Garnett Dream**，前 18 个章节用于正式阅读阶段的 18 次 session，每次 session 包含一个完整章节。

为在实验中正确地在屏幕上呈现文本，每次 session 的内容被切分为一系列单元（unit），每个单元不超过 10 个汉字。这些切分后的内容以 Excel（.xlsx）格式保存，供后续使用。在实验中，每次 session 内容中三个相邻的单元会分三行显示在屏幕上，其中中间一行被高亮，供被试阅读。

综上，ChineseEEG 数据集中共使用了 115,233 个字符（**The Little Prince** 中 24,324 个，**Garnett Dream** 中 90,909 个）作为实验刺激，其中包含 2,985 个唯一字符。

原始小说和切分后的小说保存在 `derivatives/novels` 文件夹中。`novels` 文件夹下的 `segmented_novel` 文件夹中包含两类 Excel 文件：一类文件名以 "display" 结尾，另一类不带该后缀。前者存储已切分的单元；后者则包含按照实验呈现格式重新组合后的单元。以 "display" 结尾的文件将用于支持相关代码的执行，以便在实验中实现有效的刺激呈现。

生成这两类文件的代码以及实验呈现的代码可在 GitHub 仓库中找到：https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing。

## 实验流程

被试的任务是阅读一部小说，需要保持头部静止，并让目光停留在屏幕上移动的高亮（红色）汉字上，按照程序设定的节奏阅读。被试需要在单次 session 内的多个 run 中读完整部小说。每个 run 分为两个阶段：眼动仪校准阶段和阅读阶段。

眼动仪校准阶段位于每个 run 的开头，要求被试将目光保持在注视点上，注视点会依次出现在屏幕的四个角和中心位置。

在阅读阶段，屏幕首先显示当前章节的序号。随后文本出现，每页三行，确保每行不超过十个汉字（不含标点）。每一页中，中间一行被高亮作为焦点，上下两行以较低强度作为背景显示。中间行的每个字符依次以红色高亮显示 0.35 秒，被试需要跟随高亮提示阅读小说内容。

关于实验设置和流程的详细信息，请参阅我们的论文：https://doi.org/10.1101/2024.02.08.579481。

## 标记（Markers）

为了在实验过程中精确地将 EEG 片段与单个字符对应起来，我们在 EEG 数据中标记了触发（trigger）。

EYES：眼动仪开始记录

EYEE：眼动仪停止记录

CALS：眼动仪校准开始

CALE：眼动仪校准结束

BEGN：EGI 开始记录

STOP：EGI 停止记录

CHxx：特定章节的开始（数字对应章节号）

ROWS：一行的开始

ROWE：一行的结束

PRES：序言的开始

PREE：序言的结束

## 数据记录

原始 EEG 数据的采样率为 1 kHz，而滤波数据和预处理数据的采样率为 256 Hz。

### 数据结构

数据集按照 EEG-BIDS 规范并使用 MNE-BIDS 包进行组织。数据集包含一些常规 BIDS 文件、10 名被试的数据文件夹以及一个 derivatives 文件夹。独立文件提供了数据集的概览：i) dataset_description.json 是一个 JSON 文件，描述数据集的信息，如名称、数据集类型和作者；ii) participants.tsv 包含被试信息，如年龄、性别和利手；iii) participants.json 描述 participants.tsv 中各列的属性；iv) README.md 包含数据集的详细介绍。

每名被试的文件夹包含两个文件夹，分别命名为 ses-LittlePrince 和 ses-GarnettDream，分别存储该被试阅读两部小说的数据。这两个文件夹各自包含一个 eeg 文件夹和一个 sub-xx_scans.tsv 文件。tsv 文件包含每个文件的扫描时间信息。eeg 文件夹包含多个 run 的源原始 EEG 数据、通道和标记事件文件。每个 run 包含一个 eeg.json 文件，其中涵盖该 run 的详细信息，如采样率和通道数量。事件存储在 events.tsv 中，包含 onset 和 event ID。由于 EEG-BIDS 不正式兼容 .mff 格式，EEG 数据已从原始元文件格式（.mff 文件）转换为 BrainVision 格式（.vhdr、.vmrk 和 .eeg 文件）。

derivatives 文件夹包含六个子文件夹：eyetracking_data、filtered_0.5_80、filtered_0.5_30、preproc、novels 和 text_embeddings。eyetracking_data 文件夹包含所有眼动数据。每份眼动数据以 .zip 文件格式保存，其中眼动轨迹和其他参数（如采样率）保存在不同的文件中。filtered_0.5_80 文件夹和 filtered_0.5_30 文件夹分别包含经过 0.5-80 Hz 和 0.5-30 Hz 带通滤波预处理步骤的数据。这些数据适合有特定需求、希望对 ICA 和重参考等后续预处理步骤进行自定义处理的研究者。preproc 文件夹包含使用完整预处理流程处理过的最小预处理 EEG 数据。与根目录下被试的原始数据文件夹相比，它包含四类额外的文件：i) bad_channels.json 包含在坏通道剔除阶段标记的坏通道。ii) ica_components.npy 存储 ICA 阶段所有独立成分的值。iii) ica_components.json 包含在 ICA 中被剔除的独立成分（ICA 随机种子固定，因此结果可复现）。iv) ica_components_topography.png 是所有独立成分的拓扑图图片，其中被剔除的成分以灰色标注。novels 文件夹包含原始和切分后的文本刺激材料。原始小说以 .txt 格式保存，与每次实验 run 对应的切分小说以 Excel（.xlsx）文件保存。text_embeddings 文件夹包含两部小说的嵌入向量。与每次实验 run 对应的嵌入向量以 NumPy（.npy）文件存储。

关于结构的概览，请参阅我们的论文：https://doi.org/10.1101/2024.02.08.579481。

### 预处理

对于 derivatives 文件夹中的预处理数据，我们只做了最小限度的预处理，以保留尽可能多的有用信息。预处理步骤包括数据分段、降采样、滤波、坏通道插值、ICA 和平均重参考。

在数据分段阶段，我们只保留实验正式阅读阶段的数据。根据数据采集阶段的事件标记，我们对数据进行分段，去除了与正式实验无关的部分，如校准和序言阅读。为尽量减少后续滤波步骤对信号首尾的影响，在正式阅读阶段开始前额外保留了 10 秒数据。随后，信号被降采样至 256 Hz。

接下来，应用 50 Hz 陷波滤波器以去除信号中的工频噪声。然后，我们对信号执行带通 overlap-add FIR 滤波，以消除低频直流分量和高频噪声。这里提供了两个版本的滤波数据。第一个的滤波频带为 0.5-80 Hz，第二个的滤波频带为 0.5-30 Hz。研究者可根据自身具体需求选择合适的版本。滤波之后，我们对坏通道进行了插值。

随后对数据应用独立成分分析（ICA），采用 infomax 算法。独立成分的数量设为 20，以确保它们包含大部分信息，同时数量不至于过多而增加人工处理的负担。我们剔除了明显的噪声成分，如眼电（EOG）和心电（ECG）。最后，使用平均方法对数据进行了重参考。

预处理的详细信息可参阅我们的论文：https://doi.org/10.1101/2024.02.08.579481。

### 文本嵌入

数据集提供了使用预训练语言模型 BERT-base-Chinese 计算的两部小说的嵌入向量。在实验过程中，每行显示的文本包含 n 个汉字。BERT-base-Chinese 模型处理这 n 个汉字，得到大小为 (n, 768) 的嵌入，其中 n 表示汉字数量，768 表示嵌入的维度。为确保不同长度的显示行具有相同形状的嵌入，对嵌入的第一维取平均，将每个实例的嵌入尺寸标准化为 (1, 768)。

### 缺失数据

由于技术原因，部分原始数据丢失：

- EEG：

  - Sub-09 ses-LittlePrince run 1-3

  - Sub-14 ses-GranettDream run 9

  - Sub-15 ses-GranettDream run 12

  - Sub-07 ses-GranettDream run 18（由 run 19 替代）
      注意：Sub-07 ses-GranettDream run 19 读取的是 GranettDream 的第 19 章而非第 18 章。


- 眼动数据：
  - Sub-08 ses-LittlePrince run 1-2


由于数据质量不佳或其他原因，部分预处理数据丢失：

- 在 0.5-30 Hz 滤波版本中：

  - Sub-15 ses-LittlePrince run 1-7

  - Sub-15 ses-GranettDream run 1, 2, 3, 7, 10, 16


- 在 0.5-80 Hz 滤波版本中：

  - Sub-13 ses-LittlePrince run 4, 5

  - Sub-15 ses-LittlePrince run 1-7

  - Sub-13 ses-GranettDream run 14

  - Sub-15 ses-GranettDream run 1, 2, 3, 7, 10, 16


## 使用说明

如果你想进一步了解该数据集，包括我们预处理步骤中的详细参数设置，或如何将文本与 EEG 片段对齐，请参阅我们的论文：https://doi.org/10.1101/2024.02.08.579481。你可以在 GitHub 仓库中找到文本呈现、数据处理及其他功能的相关代码：https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing。

参考文献
----------

Appelhoff, S., Sanderson, M., Brooks, T., Vliet, M., Quentin, R., Holdgraf, C., Chaumon, M., Mikulan, E., Tavabi, K., Höchenberger, R., Welke, D., Brunner, C., Rockhill, A., Larson, E., Gramfort, A. and Jas, M. (2019). MNE-BIDS: Organizing electrophysiological data into the BIDS format and facilitating their analysis. Journal of Open Source Software 4: (1896). https://doi.org/10.21105/joss.01896

Pernet, C. R., Appelhoff, S., Gorgolewski, K. J., Flandin, G., Phillips, C., Delorme, A., Oostenveld, R. (2019). EEG-BIDS, an extension to the brain imaging data structure for electroencephalography. Scientific Data, 6, 103. https://doi.org/10.1038/s41597-019-0104-8
