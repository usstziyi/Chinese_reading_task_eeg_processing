# 基于中文语料的滚动显示项目

## 简介

本项目旨在基于**中文语料**进行**实时高亮逐字阅读**任务，同时记录被试的脑电（EEG）和眼动（eye-tracking）数据。采集的数据可用于 EEG 语言解码及相关研究。

## 设备型号

EGI：128 通道

眼动仪：Tobii Glasses 3

## 环境

**本项目必须基于 Python 3.10 版本运行！** 你可以使用 Anaconda 创建新环境来运行本项目。命令如下：

```
conda create -n psychopy_tobii python=3.10
```

然后激活该环境以安装我们所需的包：

```
conda activate psychopy_tobii
```

### PsychoPy

整个实验程序基于 PsychoPy 编写。你可以通过命令行使用以下命令下载 PsychoPy，也可以从 PsychoPy 官网下载：https://www.psychopy.org/。

```
pip install psychopy
```

PsychoPy 有两种模式：builder 和 coder。在本项目中，我们使用 coder 模式来实现实验。

### g3pylib

本项目使用 g3pylib，这是一个用于 Tobii Glasses 3 的 Python 客户端库。你可以按照这里的说明安装该包：https://github.com/tobiipro/g3pylib

首先克隆该包：

```
git clone https://github.com/tobiipro/g3pylib.git
```

```
cd g3pylib
```

然后在克隆包的路径下使用以下命令安装：

```
pip install .
```

### egi-pynetstation

egi-pynetstation 是一个 Python 包，用于通过 Python API 控制 EGI 的 NetStation EEG 放大器接口。使用以下命令安装：

```
pip install egi-pynetstation
```

关于该包的更多信息，请访问此网站：https://github.com/nimh-sfim/egi-pynetstation

## 代码说明

在开始实验之前，你应当先使用 `novel_segmentation` 部分中的 `cut_Chinese_novel.py` 将小说切分为我们要求的格式。详细说明请参阅该部分的 README。

如果已经成功完成切分，你可以运行 `PlayNovel.py` 开始主实验。

### 主实验

#### 主要流程

`PlayNovel.py` 用于运行基于 PsychoPy 的主实验。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/screen.png)

程序包含多种模式，你可以选择是否连接 EGI 和眼动仪进行实验。实验流程主要包括眼动校准（若选择眼动模式）、练习阅读、正式阅读以及章节间的休息。在阅读过程中，小说将以每页三行的形式呈现在屏幕上，每行不超过十个汉字（不含标点符号）。每页的中间行将被高亮作为注视焦点，上下两行则以降低强度显示作为背景。中间行的每个字将按一定时长依次高亮，要求被试跟随高亮提示阅读小说内容。各种参数（如单字高亮时长、高亮颜色等）都可以通过修改相应设置来调整。

#### 参数

下面将详细说明各参数。注意，你必须将**加粗**参数修改为你自己的设置，否则可能出现错误和计算不准确。

| 参数                          | 类型  | 默认值                               | 用途                                                          |
| ----------------------------- | ----- | ------------------------------------ | ------------------------------------------------------------- |
| highlight_color               | str   | 'red'                                | 字符的高亮颜色                                                |
| add_eyetracker                | bool  | True                                 | 是否连接眼动仪                                                |
| add_mark                      | bool  | True                                 | 是否连接 EGI 设备                                             |
| shift_time                    | float | 0.35                                 | 高亮字符的切换时间                                            |
| **host_IP**                   | str   | '10.10.10.42'                        | Net Station 的 IP 地址（运行本实验的电脑）                    |
| **egi_IP**                    | str   | '10.10.10.51'                        | EGI 设备的 IP 地址                                            |
| **eyetracker_hostname**       | str   | "TG03B-080202024891"                 | 眼动仪的序列号                                                |
| novel_path                    | str   | "segmented_Chinese_novel_main.xlsx"  | 你想播放的 `.xlsx` 格式小说的路径                             |
| preface_path                  | str   | "segmented_Chinese_novel_preface.xlsx" | 你想播放的 `.xlsx` 格式前言的路径                            |
| fullscreen                    | bool  | True                                 | 是否设置为全屏                                                |
| rest_period                   | int   | 3                                    | 章节间隔休息                                                  |
| force_rest_time               | int   | 15                                   | 强制休息时间                                                  |
| **distance_screen_eyetracker** | float | 73                                   | 屏幕中心到眼动仪中心的距离（厘米）                            |
| **screen_width**              | float | 54                                   | 屏幕宽度                                                      |
| **screen_height**             | float | 30.375                               | 屏幕高度                                                      |
| **screen_width_height_ratio** | float | 16/9                                 | 屏幕宽高比                                                    |
| **eyetracker_width_degree**   | float | 95                                   | 眼动相机水平扫描范围（度，两侧合计）                          |
| **eyetracker_height_degree**  | float | 63                                   | 眼动相机垂直扫描范围（度，两侧合计）                          |
| isFirstSession                | bool  | True                                 | 是否为实验的第一个会话，决定是否在正式实验前显示前言          |

**注意**：如前一节所述，我们可能会多次运行此脚本，以依次呈现小说的每个部分。每次运行程序时，你都需要指定参数 "isFirstSession"，让程序知道这是否是第一次播放。如果值为 "True"，程序将在正式阅读开始前播放前言进行练习阅读。如果为 "False"，将跳过练习阅读部分，直接从正文开始。

#### EEG 标记（Markers）

如果在实验中使用 EGI 设备记录 EEG 信号，我们的程序会在相应的时间点放置标记。这些标记将帮助你对齐眼动记录和 EEG 信号，以及定位与 EEG 特定分段对应的文本。

标记的详细信息如下：

```
EYES: Eyetracker starts to record
EYEE: Eyetracker stops recording
CALS: Eyetracker calibration starts
CALE: Eyetracker calibration stops
BEGN: EGI starts to record
STOP: EGI stops recording
CH01：Beginning of specific chapter (Numbers correspond with chapters)
ROWS: Beginning of a row
ROWE: End of a row
PRES：Beginning of the preface
PREE：End of the preface
```

#### 校准坐标转换

在该实验程序中，我们设计了自定义校准流程。一个圆点将依次出现在屏幕的四个角和中心，每个位置停留 5 秒。被试需要注视圆点中心以完成校准。对于每个圆点，我们记录被试注视数据的中间和后半段（3s 到 4s），并计算平均注视点作为被试的平均注视中心。然后，我们将平均注视点与圆点的实际中心位置进行比较，以计算误差。通过对所有五个圆点的误差取平均，得到最终的校准误差。如果最终误差低于预定误差阈值，则认为校准成功。如果校准不成功，实验程序将自动返回校准阶段并重复该过程，直到校准完成。

为了对齐眼动仪和 PsychoPy 程序的坐标系，以获得注视点在屏幕上的实际位置，我们利用几何关系推导出了眼动仪坐标系与 PsychoPy 坐标系之间的转换公式。该公式在校准过程中应用。具体关系如下：

```math
x_{\text{eyetracker}} = (\frac{{W \cdot x_{\text{psychopy}}}}{{d \cdot r \cdot \tan(\text{width\_degree/2})}} + 1 )  \cdot \frac{1}{2}
```

```math
y_{\text{eyetracker}} = (1 - \frac{{H \cdot y_{\text{psychopy}}}}{{d \cdot \tan(\text{height\_degree/2})}} )\cdot \frac{1}{2}
```

其中：
```math
(x_{eyetracker}, y_{eyetracker}) \ is \ the \ coordinate \ in \ the \ eyetracker\ coordinate \ system
```

```math
(x_{psychopy}, y_{psychopy}) \ is \ the \ coordinate \ in \ the \ psychopy\ coordinate \ system
```

```math
W \ : \ the \ width \ of \ the \ screen
```

```math
H \ : \ the \ height \ of \ the \ screen
```

```math
r \ : \ the \ ratio \ of \ the \ width \ to \ the \ height
```

```math
width\_degree \ : \ the\ horizontal\ scanning\ range\ of\ the\ eyetracking \ camera\ in\ degree\ ( both \ sides \ together)
```

```math
height\_degree \ : \ the\ vertical\ scanning\ range\ of\ the\ eyetracking \ camera\ in\ degree\ ( both \ sides \ together)
```

## 实验流程

实验设置如下：

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/exp_layout.png)

下面是从零开始启动项目（以小说《小王子》为例）的操作步骤和示例。

### 激活环境

首先，激活我们之前设置的环境，然后进入项目所在目录。

```
conda activate psychopy_tobii
cd <your_path_to_project>
```

### 小说切分

以符合格式要求的 `.txt` 小说文件为输入（格式要求可在“代码说明”部分的“句子切分”小节中找到）。指定参数将文本切分为若干部分。运行 `cut_Chinese_novel.py`，你将获得相应数量的 `.xlsx` 文件。这里，我们将小说切分为 4 个正文部分，共得到 5 个文件（4 个正文部分和 1 个前言部分）。

```
python cut_Chinese_novel.py --divide_num=8,16,24 --Chinese_novel_path=xiaowangzi_main_text.txt
```

### 主实验

- 首先，连接 EGI 设备和眼动仪。
- 接下来，调整参数并运行主程序。在变量 `novel_path` 和 `preface_path` 中分别设置正文和前言部分的路径。调整参数 `add_mark` 和 `add_eyetracker` 决定是否连接 EGI 和眼动仪。将 `host_IP`、`egi_IP` 和 `eyetracker_hostname` 改为你自己设备的 IP 地址。在第一次运行时将 `isFirstSession` 设为 True，以包含练习会话。其他可调参数可在“代码说明”下“主实验”的“参数”部分中找到。注意，你可能需要根据你自己的设置修改一些尺寸和距离相关参数。在后续运行中，将 `novel_path` 改为读取小说的不同部分，并将 `isFirstSession` 设为 False。

```
python play_novel.py --add_mark --add_eyetracker  --preface_path=<your preface path> --host_IP=<host IP> --egi_IP=<egi IP> --eyetracker_hostname=<eyetracker serial number> --novel_path=<your novel path> --isFirstSession
```

下面是我们自己的设置示例：

```
第一次运行：
python PlayNovel.py --add_mark --add_eyetracker  --preface_path=segmented_Chinense_novel_preface_display.xlsx --host_IP=10.10.10.42 --egi_IP=10.10.10.51 --eyetracker_hostname=TG03B-080202024891 --novel_path=segmented_Chinense_novel_run_1_display.xlsx --isFirstSession

第二次运行：
python PlayNovel.py --add_mark --add_eyetracker  --preface_path=segmented_Chinense_novel_preface_display.xlsx --host_IP=10.10.10.42 --egi_IP=10.10.10.51 --eyetracker_hostname=TG03B-080202024891 --novel_path=segmented_Chinense_novel_run_2_display.xlsx

...
```

- **在强制休息期间，EGI 系统将被断开。** ***此时，你需要在被试继续实验前重启 EGI 系统，确保其处于运行状态，否则程序会崩溃！！！***
- **在每个实验会话结束时，需要为被试的脑电帽补充生理盐水，并更换眼动仪的电池以确保充足的电量。启动并重新连接眼动仪，然后重启 EGI 系统。** ***切记不要在实验期间（包括休息期间）断开眼动仪或更换其电池，否则可能导致程序崩溃！！！***
- 实验的主要流程包括：校准 - 前言会话（仅在第一部分）- 正式阅读 - 休息（包括强制休息和被试主动发起的休息）。每次休息后都会重新校准。

  - 校准

    **注意：当校准多次失败时，主试可以选择跳过校准，直接进入阅读部分，方法是在校准失败提示页按键盘上的右箭头键。**

  - 前言阅读

  - 正式阅读

  - 休息

    **在被试继续实验前，重启 EGI 系统以确保其处于运行状态**
