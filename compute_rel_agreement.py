import json
from argparse import ArgumentParser
from sklearn.metrics import cohen_kappa_score


LABEL_MAPPING = {'No': 0, 'temporal': 1, 'causal': 2, 'parent-child': 3}


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file1', type=str, required=True)
    parser.add_argument('--file2', type=str, required=True)
    args = parser.parse_args()

    with open(args.file1, 'r') as f:
        file1 = json.load(f)

    with open(args.file2, 'r') as f:
        file2 = json.load(f)
    
    user_id1 = args.file1.split('/')[-1].split('-')[0]
    user_id2 = args.file2.split('/')[-1].split('-')[0]
    prolific_id1 = args.file1.split('/')[-1].split('-')[1].split('.')[0]
    prolific_id2 = args.file2.split('/')[-1].split('-')[1].split('.')[0]

    # annotated_list1 = []
    # annotated_list2 = []
    for i in range(len(file1)):
        if file1[i]['doc_id'] == file2[i]['doc_id']:
            doc_id = file1[i]['doc_id']

            annotated_list1 = []
            annotated_list2 = []

            rel_list1 = []
            
            rel_list2 = []

            rel_binary1 = []
            rel_binary2 = []
            for j in range(len(file2[i]['question_progress'])):
                this_answer = file1[i]['question_progress'][j][0]
                rel_list1.append(LABEL_MAPPING[this_answer])
                this_answer = file2[i]['question_progress'][j][0]
                rel_list2.append(LABEL_MAPPING[this_answer])

                if "No" not in file1[i]['question_progress'][j]:
                    rel_binary1.append(j)
                if "No" not in file2[i]['question_progress'][j]:
                    rel_binary2.append(j)
            
            inter_rel_binary = set(rel_binary1).intersection(set(rel_binary2))
            if len(rel_binary1) == 0 and len(rel_binary2) == 0:
                f1_binary = 1
                iou_binary = 1
            elif len(rel_binary1) == 0 or len(rel_binary2) == 0:
                f1_binary = 0
                iou_binary = 0
            else:
                f1_binary = len(inter_rel_binary) * len(inter_rel_binary) / (len(rel_binary1) * len(rel_binary2))
                iou_binary = len(inter_rel_binary) / (len(rel_binary1) + len(rel_binary2) - len(inter_rel_binary))


            this_kappa = cohen_kappa_score(rel_list1, rel_list2, labels=[0, 1, 2, 3])
            total_events = len(rel_list1)
            # print(cohen_kappa_score(annotated_list1, annotated_list2, labels=[0, 1]))
            # print('----------------------------------')
            with open('logs/user_rel_agreement_doc.csv', 'a+') as f:
                f.write(f"{doc_id}\t{user_id1}\t{prolific_id1}\t{user_id2}\t{prolific_id2}\t{this_kappa}\t{f1_binary}\t{iou_binary}\t{total_events}\n")
    
    # kappa = cohen_kappa_score(annotated_list1, annotated_list2, labels=[0, 1])
    # total_events = len(annotated_list1)
    # event_1 = sum(annotated_list1)
    # event_2 = sum(annotated_list2)
    # with open('logs/user_agreement.csv', 'a+') as f:
    #     #f.write(f"{user_id1},{prolific_id1},{user_id2},{prolific_id2},{kappa}\n")
    #     f.write(f"{user_id1}\t{prolific_id1}\t{user_id2}\t{prolific_id2}\t{kappa}\t{total_events}\t{event_1}\t{event_2}\n")
    # print("Total number of Events:")
    # print()
    # print("User 1 Events:")
    # print(sum(annotated_list1))
    # print("User 2 Events:")
    # print(sum(annotated_list2))
    # print("Cohen's Kappa Score:")
    # print(kappa)

