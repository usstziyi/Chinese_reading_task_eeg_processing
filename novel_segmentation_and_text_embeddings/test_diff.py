# -*- coding: utf-8 -*-
import sys, os, re
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from cut_chinese_novel import cut_paragraph as new_cut


def old_cut_paragraph(paragraph):
    """重建改动前的实现，用于对比"""
    sentences = re.split(r"(。|！|？|”|；)", paragraph)
    sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2])]
    for i in range(len(sentences)):
        if sentences[i][0] in ['。', '！', '？', '”', '；']:
            sentences[i - 1] += sentences[i][0]
            sentences[i] = sentences[i][1:]
    sentences = list(filter(lambda x: x != '', sentences))
    sentences = [s.strip().replace('\n', '').replace(' ', '') for s in sentences]
    sentences = [s for s in sentences if s]
    return sentences


tests = [
    '请别让我再这么忧伤：赶快写信告诉我，他又回来了……',
    '第一句。请别让我再这么忧伤：赶快写信告诉我，他又回来了……',
    '“你到底想说什么？”他问。请别让我再这么忧伤：赶快写信告诉我，他又回来了……',
]
for t in tests:
    print('输入:', repr(t))
    print('  old:', old_cut_paragraph(t))
    print('  new:', new_cut(paragraph=t))
    print()
