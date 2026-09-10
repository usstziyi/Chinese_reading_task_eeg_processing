## 提出组织：不是某个官方标准机构，而是「社区 + INCF 孵化」

BIDS 全称 **Brain Imaging Data Structure**（最早叫 **OBIDS**，Open Brain Imaging Data Structure），它不是 ISO/IEEE 这类官方标准组织制定的，而是**科研社区驱动的开放标准**：

- **发起**：2015 年 1 月，在斯坦福大学举行的一次 **INCF（International Neuroinformatics Coordinating Facility，国际神经信息学协调机构）** 资助的数据共享工作组会议上提出。
- **主要推动者**：**Krzysztof (Chris) Gorgolewski**，之后由他牵头维护。
- **正式发布**：2016 年 6 月在 *Scientific Data* 期刊上发表论文（Gorgolewski et al., 2016），标志标准的首个正式版本。
- **被认可**：**INCF 于 2018 年正式背书（endorse）BIDS 为其标准之一**。INCF 本身就是一个专门做「开放、FAIR 神经科学」的标准组织。
- **治理结构**：从 **2019 年 10 月起**，项目改由 **Steering Group（指导委员会）** 领导，并由 **Maintainers Group（维护者团队）** 负责标准的日常维护，采用公开的治理与投票决策流程。

## 扩展机制：BEP

标准不是一次成型的，新增模态靠 **BEP（BIDS Extension Proposal，BIDS 扩展提案）** 推动，由 BEP Working Group / Leads Group 负责，走社区讨论 + 投票流程合入主规范。EEG 对应的就是 **EEG-BIDS** 扩展——也就是你这份代码在用的那部分。

## 这个标准面向什么

**面向神经影像数据的「组织方式 + 命名规则 + 元数据描述」**，核心目标有四个：

1. **数据共享**：让不同实验室、不同设备产出的数据能被别人直接读懂、复用（配合 OpenNeuro 这类公开数据平台）。
2. **机器可读**：用统一的 `sub-/ses-/task-/run-` 命名 + JSON 元数据，让软件能自动解析，而不是靠人工翻文档。
3. **可复现 & 自动化验证**：有了规范就能写 **bids-validator** 自动校验数据集是否合规，避免"格式说不清"的问题。
4. **覆盖多模态**：不止 MRI/fMRI，还扩展到 **EEG、MEG、iEEG、PET、DWI、ASL** 等——你的项目正是 EEG 场景。

## 对应到你代码里的体现

```
sub-07/ses-LittlePrince/eeg/sub-07_ses-LittlePrince_task-reading_run-1_eeg.vhdr
sub-07/.../..._eeg.json        ← BIDS 要求的元数据 sidecar
sub-07/.../..._channels.tsv    ← 通道信息表
```

[convert_eeg_to_bids.py](file:///d:/AI/copilot/copilot-worktrees/Chinese_reading_task_eeg_processing/usstziyi-musical-happiness/data_preprocessing_and_alignment/convert_eeg_to_bids.py) 里的 `BIDSPath` 生成目录/文件名、`write_raw_bids` 落盘、`make_dataset_description` 写数据集描述，全都是在**遵循 BIDS 规范**；而 `raw.info["line_freq"] = line_freq`（[L48](file:///d:/AI/copilot/copilot-worktrees/Chinese_reading_task_eeg_processing/usstziyi-musical-happiness/data_preprocessing_and_alignment/convert_eeg_to_bids.py#L48)）也是因为 **BIDS 强制要求 EEG 数据声明工频**。

## 一句话总结

BIDS 是 **INCF 孵化、社区驱动、2016 年正式发布、2019 年起由 Steering Group 治理** 的开放数据组织标准；它面向**所有神经影像模态的数据共享、自动解析与可复现**，不隶属于任何单一机构。

Sources:
- [BIDS Governance and Decision Making](https://bids.neuroimaging.io/collaboration/governance.html)
- [The Past, Present, and Future of the Brain Imaging Data Structure (BIDS)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10516110/)
- [INCF — Standards and Best Practices](https://incf.org/)
- [The OpenNeuro resource for sharing of neuroscience data](https://pmc.ncbi.nlm.nih.gov/articles/PMC8550750/)