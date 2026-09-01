# Docker 教程

## 简介

本内容旨在帮助不熟悉 Python 环境配置的研究者。虽然每个部分的 `README` 文档都已经列出了所需包及其版本，我们仍然提供一个包含项目全部依赖的 Docker 镜像，以简化环境配置过程。Docker 可以在 Linux、Windows 或 macOS 计算机上运行一个虚拟容器，容器中包含一个应用程序及其依赖。因此，用户只需按照本教程下载 Docker、拉取镜像并运行容器，即可轻松搭建运行代码所需的环境。

Docker 的两个核心概念是 `images`（镜像）和 `containers`（容器）。Docker `image` 是用于构建容器的只读模板，用于存储和传输应用程序。Docker `container` 是运行应用程序的标准化的、封装好的环境，可以看作是运行在宿主机上的一个独立的操作系统。在实践中，我们首先拉取一个镜像，然后使用它构建我们自己的容器，并在容器中进行运行代码等操作。

我们的 Docker 镜像 [mouxinyu/eeg_dataset](https://hub.docker.com/r/mouxinyu/eeg_dataset) 基于 [ubuntu:22.04](https://hub.docker.com/_/ubuntu)，并包含从 [GitHub 仓库](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing) 拉取的项目代码。此外，镜像中还配置了支持图形用户界面的 [Pycharm](https://www.jetbrains.com/pycharm/download/?section=linux)，使用户可以在运行容器时通过 GUI 进行操作，避免复杂的命令行编辑。dockerfile 的源码位于 `docker` 目录中。

**下面的教程将详细介绍如何在 Windows 操作系统上使用 Docker 应用我们的镜像**。其他操作系统的使用方法会略有不同，这里不做详细说明。

如果你想了解更多关于 Docker 的信息，可以浏览它的[官方网站](https://www.docker.com/)。

## 分步教程

### Docker 安装

关于如何在 Windows 系统上下载 Docker 的详细说明，建议参考官方文档中的[综合指南](https://docs.docker.com/desktop/install/windows-install/)。这里我们给出简要说明。

#### WSL 安装

在下载 Docker 之前，请确保你的系统上已安装适用于 Linux 的 Windows 子系统（WSL）。我们建议按照[官方说明](https://learn.microsoft.com/en-us/windows/wsl/install)确保 WSL 正常工作。下面，我们提供一个简化的安装过程和一些重要命令供你参考。

你可以通过打开命令行界面并执行以下命令来安装 WSL：

```
wsl --install
```

请确保 WSL 的默认版本设置为 WSL2。你可以通过执行以下命令指定默认版本：

```
wsl --set-default-version 2
```

你还可以通过以下命令查看 Windows 计算机上已安装的 Linux 发行版列表：

```
wsl -l -v
```

WSL 的其他基本命令可以在其[官方文档](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)中找到。

#### Docker 安装

在确认 WSL 已正确安装后，你可以继续安装 Docker。请安装与你操作系统相对应的版本。Windows 系统的安装路径见[这里](https://docs.docker.com/desktop/install/windows-install/)。

按照文档中的说明完成下载步骤后，双击打开 Docker Desktop，你将看到如下界面。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/docker.png)

### VcXsrv 安装

Docker 默认不提供 GUI。为了解决这个问题，我们需要在 Windows 宿主机上安装 VcXsrv（该方案也适用于 Mac）。请从[这里](https://sourceforge.net/projects/vcxsrv/)提供的官方网站下载。

下载完成后，双击安装。安装完成后，从开始菜单打开 VcXsrv（安装后名为 Xlaunch）。如果在开始菜单中找不到，可以使用搜索功能定位它。打开后，将出现一个设置页面。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/vcxsrv_1.png)

只需保持默认设置并点击"下一步"，直到结束，然后点击"完成"启动 VcXsrv。启动后，你可以在 Dock 中看到如下图标，表示启动成功。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/vcxsrv_2.png)

### 拉取镜像

现在，我们将通过从 [Docker Hub](https://hub.docker.com/) 拉取镜像来部署我们的环境，并运行它以创建容器。

首先，请确保你已经成功启动了 Docker Desktop，并且按照之前的说明打开了 VcXsrv。接下来，打开命令行界面，输入以下命令从 Docker Hub 拉取所需镜像：

```
docker pull mouxinyu/eeg_dataset
```

输入此命令后按回车键执行。如果在命令行中看到如下响应，则表示镜像已成功拉取：

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/image.png)

### 运行容器

接下来，我们可以使用刚刚拉取的镜像创建容器。你可以通过执行以下命令创建容器：

```
docker run --name eeg_dataset_container -it -v <path/to/your/windows/mount/point>:<path/to/your/container/mount/point> mouxinyu/eeg_dataset
```

相关参数的解释如下：

- --name：该参数指定要创建的容器的名称，之后我们可以使用该名称来引用特定容器。
- -it：该命令以交互模式运行容器，并为容器分配一个伪终端。
- -v：该命令将宿主机上的一个文件系统地址挂载到容器内对应的地址，允许容器和宿主机之间的文件交换。使用 `:` 分隔两个系统上的路径，左侧为宿主机上的路径，右侧为容器内的路径，建议设置为 `/home/mynewuser/mount`。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/docker_run.png)

容器默认有两个用户，一个是 `root` 用户，另一个是名为 `mynewuser` 的用户。进入容器时，默认情况下你在 `root` 用户下的 `/opt/pycharm/bin` 目录中。

我们建议你在大多数操作时切换到 `mynewuser` 用户，可以使用以下命令切换用户：

```
su mynewuser
```

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/su.png)

#### GUI

在 `/opt/pycharm/bin` 中，输入以下命令打开 Pycharm 的 GUI 界面：

```
sh pycharm.sh
```

如果你成功运行了 GUI，将出现如下界面：

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/pycharm_1.png)

确认用户协议并进入 pycharm 界面：

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/pycharm_2.png)

选择中间部分的 'Open' 选项，并选择 `home/mynewuser/Chinese_reading_task_eeg_processing` 打开项目。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/pycharm_3.png)

在这里，选择 'Trust Project' 打开项目。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/pycharm_4.png)

通常，Pycharm 会自动检测项目文件夹中的虚拟环境 `eeg_dataset_env` 并自动配置（如果是第一次设置该环境，可能需要一些时间）。但是，如果 Pycharm 没有自动识别该环境，你可以按照下面的步骤手动配置：

点击 Pycharm 页面右下角，选择 `Add New Interpreter --> Add Local Interpreter`。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/pycharm_5.png)

在 PyCharm 设置界面中，从左侧边栏选择 `Virtualenv Environment`。然后在 `Environment` 部分选择 `Existing` 选项以指定一个已存在的环境。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/pycharm_6.png)

然后选择 `/home/mynewuser/Chinese_reading_task_eeg_processing/eeg_dataset_env/bin/python3.10` 作为解释器。按 `OK` 配置环境。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/pycharm_7.png)

现在，你可以在 PyCharm 中编辑和运行代码了。

注意：如果你打算使用 `matplotlib` 包进行绘图，请在代码文件的最开头插入以下代码行：

```
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tkinter as tk
```

但是，如果你使用 `mne` 包内的集成绘图功能，则可以忽略此步骤。

#### 命令行

如果你熟悉 Linux 命令行操作，也可以使用命令行执行相应操作。我们已经为你配置了 vim 编辑器等工具。需要注意的是，命令行操作只能在 GUI 关闭时进行。

### 挂载

要在宿主机和容器之间交换文件，你需要使用 Docker 的挂载功能。请将你想保存的文件写入容器中的挂载点（如果你按照我们之前的建议操作，这个挂载点应该在 `/home/mynewuser/mount`）。然后，这些文件将出现在宿主机的指定位置。同样，你可以将宿主机上的文件放在其挂载点，然后在容器内的挂载点访问这些文件。我们强烈建议你使用挂载功能加载和写入数据，以避免内存问题或其他可能的问题。

### 退出

我们可以使用 `exit` 命令从 `mynewuser` 用户切换回 `root` 用户，同样，在 `root` 用户下使用 `exit` 命令可以退出容器。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/exit.png)

### 其他 Docker 命令

如果你已经关闭了容器，并希望重新进入容器的命令行界面，可以按照以下步骤操作。首先，使用以下命令查看系统中所有现有的容器：

```
docker ps -a
```

该命令将显示所有容器，包括已停止的容器。

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/ps.png)

接下来，使用以下命令启动已停止的容器并进入其命令行界面：

```
docker start eeg_dataset_container
docker exec -it eeg_dataset_container /bin/bash
```

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/restart.png)

### 注意事项

使用 WSL 和 Docker 时，请确保你的系统有足够的内存空间。此外，在某些情况下，你可能需要连接 VPN 才能访问外部网络。如果你的内存不足或未连接 VPN，可能会遇到卡顿或命令无响应等问题。
