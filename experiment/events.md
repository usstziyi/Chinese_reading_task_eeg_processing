11 种（README 的标记表也是 11 项）。其中 10 个是固定字符串，第 11 个是 `CH`+章节号 的动态标记。

Now let me build the table with code locations.

Event list (README L118-128 ✓ all match):
1. EYES — 眼动开始录制 — 发 2 次: L155, L1304
2. EYEE — 眼动结束录制 — L96, L1745
3. CALS — 校准开始 — L244
4. CALE — 校准结束 — L311
5. BEGN — EGI 开始记录 — L147, L601, L1282
6. STOP — EGI 停止记录 — L100, L983, L1244, L1847
7. CH01/CHxx — 章节开始 — L1041, L1691
8. ROWS — 行开始 — L507, L1069, L1707
9. ROWE — 行结束 — L526, L1129, L1727
10. PRES — 前言开始 — L365
11. PREE — 前言结束 — L537

Commented out (未启用): STRT (L506, L1706), SENTENCE_END (L1127, L1725).

Additional notes:
- 这些标记全部由 `eci_client.send_event()` 发送，也就是**打进 EEG 记录**（经 Net Station），用于后续对齐眼动与 EEG、定位文本。README L113 有说明。
- ROWS 只在每行第一个字时发（`if count == 1`），ROWE 在该行最后一个字高亮结束后发（`if count == main_row_words_len_without_punc`）。
- CH 标记的编码：章节号是个位数 → `CH01`..`CH09`；两位数 → `CH10`..`CH40`（正文最多 40 章，见 L1536-L1541 的判断）。README 写的是 CH01 这个形式。
- BEGN/STOP 成对出现，构成一个记录段；每段末尾 STOP，休息后重新 connect 再 BEGN。
- 眼动仪本身（g3.recorder）不用这些标记，它只有机上录制的起停；EYES/EYEE 是把它的事件标在 EEG 时间轴上的。

I should present the answer concisely: a table, then notes. And mention the count clearly: 11 种（10 固定 + CH 系列）。

Wait: is CH01 a family counting as 1 kind? README lists it as one entry "CH01：Beginning of specific chapter (Numbers correspond with chapters)". So 11 entries in the README table. I'll say 11 种，其中 10 个固定 + 1 个动态章节族。

Let me write.
通读全文，`eci_client.send_event()` 共发出 **11 种**事件（10 个固定字符串 + 1 个动态章节标记），与 README 的标记表（[README_CN.md#L118-L128](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/README_CN.md#L118-L128)）完全对应：

| # | 事件 | 含义 | 发送位置 |
|---|---|---|---|
| 1 | `BEGN` | EGI 开始记录（每段开头） | [L147](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L147)、[L601](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L601)、[L1282](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1282) |
| 2 | `STOP` | EGI 停止记录（每段结尾） | [L100](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L100)、[L983](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L983)、[L1244](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1244)、[L1847](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1847) |
| 3 | `EYES` | 眼动开始录制 | [L155](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L155)、[L1304](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1304) |
| 4 | `EYEE` | 眼动结束录制 | [L96](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L96)、[L1745](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1745) |
| 5 | `CALS` | 校准开始 | [L244](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L244) |
| 6 | `CALE` | 校准结束 | [L311](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L311) |
| 7 | `PRES` | 前言开始 | [L365](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L365) |
| 8 | `PREE` | 前言结束 | [L537](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L537) |
| 9 | `ROWS` | 一行开始高亮 | [L507](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L507)、[L1069](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1069)、[L1707](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1707) |
| 10 | `ROWE` | 一行高亮结束 | [L526](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L526)、[L1129](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1129)、[L1727](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1727) |
| 11 | `CH0x` / `CHxx` | 某章节开始（数字=章节号） | [L1041](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1041)、[L1691](file:///c:/Users/15221/AI/TraeWok/Chinese_reading_task_eeg_processing/experiment/play_novel.py#L1691) |
