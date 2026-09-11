import mne
import numpy as np
import openpyxl
import csv
import argparse
from utils import read_eeg_brainvision




def align_eeg_with_sentence(eeg_path, novel_xlsx_path, text_embedding_path, montage_name='GSN-HydroCel-128'):
    '''

    :param eeg_path: BrainVision files of the eeg
    :param novel_xlsx_path: path to the corresponding run of the novel
    :param text_embedding_path: path to the corresponding run of the text embeddings
    :return: cut_eeg_data, texts, text_embeddings in alignment. cut_eeg_data is a list containing all
             the cut eeg divided by the markers.
    '''

    eeg, events, event_id = read_eeg_brainvision(eeg_path, montage_name)

    text_embeddings = np.load(text_embedding_path)

    wb = openpyxl.load_workbook(novel_xlsx_path)
    wsheet = wb.active
    texts = []



    for i in range(2, wsheet.max_row + 1):
        texts.append((wsheet.cell(row=i, column=1)).value)

    start_chapter = int(texts[0])


    if start_chapter < 10:
        start_marker = 'CH0' + str(start_chapter)
    else:
        start_marker = 'CH' + str(start_chapter)


    start_marker_id = event_id[start_marker]
    events_start_chapter_index = np.where(events[:, 2] == start_marker_id)[0][0]

    eeg_data = eeg.get_data()



    ROWS_id = event_id['ROWS']
    ROWE_id = event_id['ROWE']


    rows_onset = []
    rowe_onset = []

    for event in events[events_start_chapter_index:]:
        if event[2] == ROWS_id:
            rows_onset.append(event[0])

    for event in events[events_start_chapter_index:]:
        if event[2] == ROWE_id:
            rowe_onset.append(event[0])




    cut_eeg_data = []

    for i in range(0, len(rows_onset)):

        start_time = rows_onset[i]
        end_time = rowe_onset[i]

        cut_eeg_data.append(eeg_data[:, start_time:end_time])


    return cut_eeg_data, texts, text_embeddings


def save_alignment(output_path, cut_eeg_data, texts, text_embeddings):
    '''
    把对齐结果落盘为一个 .npz 文件。

    各 EEG 分段长度不一致，无法直接堆成一个数组，所以用 object 数组保存；
    读回时需要显式允许 pickle，例如：

        with np.load(output_path, allow_pickle=True) as data:
            cut_eeg_data = list(data['segments'])
            texts = list(data['texts'])
            text_embeddings = data['text_embeddings']

    :param output_path: 输出路径，不以 .npz 结尾时会自动补上
    :param cut_eeg_data: align_eeg_with_sentence 返回的 EEG 分段列表
    :param texts: 与分段一一对应的文本列表
    :param text_embeddings: 与分段一一对应的文本嵌入
    '''
    if not output_path.endswith('.npz'):
        output_path += '.npz'

    # 分段形状不一致，直接用 np.array 会触发广播错误，需先建好 object 数组再逐个填入
    segments = np.empty(len(cut_eeg_data), dtype=object)
    segments[:] = cut_eeg_data

    np.savez_compressed(
        output_path,
        segments=segments,
        texts=np.array(texts, dtype=object),
        text_embeddings=text_embeddings,
    )

    print(f'alignment saved to {output_path}')


def main():
    parser = argparse.ArgumentParser(description='Parameters that can be changed')
    parser.add_argument('--eeg_path', type=str, default=r'sub-07_ses-LittlePrince_task-reading_run-01_eeg.vhdr')
    parser.add_argument('--novel_xlsx_path', type=str, default=r'segmented_Chinense_novel_run_1.xlsx')
    parser.add_argument('--text_embedding_path', type=str, default=r'LittlePrince_text_embedding_run_1.npy')
    parser.add_argument('--output_path', type=str, default=r'alignment_run_1.npz',
                        help='path of the .npz file used to save the alignment result')

    args = parser.parse_args()

    cut_eeg_data, texts, text_embeddings = align_eeg_with_sentence(
        eeg_path=args.eeg_path, novel_xlsx_path=args.novel_xlsx_path,
        text_embedding_path=args.text_embedding_path)

    save_alignment(args.output_path, cut_eeg_data, texts, text_embeddings)

    print(f'{len(cut_eeg_data)} segments, {len(texts)} texts, '
          f'{text_embeddings.shape} embeddings')


if __name__ == '__main__':
    main()
