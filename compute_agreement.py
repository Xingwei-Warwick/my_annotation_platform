import json
from argparse import ArgumentParser
from sklearn.metrics import cohen_kappa_score




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
            # print(file1[i]['doc_id'])
            doc_id = file1[i]['doc_id']

            annotated_list1 = []
            annotated_list2 = []

            event_list1 = []
            for j in range(len(file1[i]['checkboxes'])):
                if file1[i]['checkboxes'][j]:
                    event_list1.append(file1[i]['event_list'][j].lower())
            
            event_list2 = []
            for j in range(len(file2[i]['checkboxes'])):
                if file2[i]['checkboxes'][j]:
                    event_list2.append(file2[i]['event_list'][j].lower())
            
            event_set1 = set(event_list1)
            event_set2 = set(event_list2)
            print("User 1 Events:")
            print(len(event_set1))
            print("User 2 Events:")
            print(len(event_set2))

            diff_set1 = event_set1 - event_set2
            diff_set2 = event_set2 - event_set1

            if len(diff_set1) > 0:
                annotated_list1 += [1] * len(event_list1)
                annotated_list2 += [0] * len(event_list1)
            
            if len(diff_set2) > 0:
                annotated_list1 += [0] * len(event_list2)
                annotated_list2 += [1] * len(event_list2)
            
            inter_set = event_set1.intersection(event_set2)
            if len(inter_set) > 0:
                annotated_list1 += [1] * len(inter_set)
                annotated_list2 += [1] * len(inter_set)
            f1 = len(inter_set) * len(inter_set) / (len(event_set1) * len(event_set2))
            iou = len(inter_set) / (len(event_set1) + len(event_set2) - len(inter_set))

            # print(annotated_list1)
            # print(annotated_list2)
            # print("Total number of Events:")
            # print(len(annotated_list1))
            event_1 = sum(annotated_list1)
            event_2 = sum(annotated_list2)
            total_events = len(annotated_list1)

            this_kappa = cohen_kappa_score(annotated_list1, annotated_list2, labels=[0, 1])
            # print(cohen_kappa_score(annotated_list1, annotated_list2, labels=[0, 1]))
            # print('----------------------------------')
            with open('logs/user_agreement_doc.csv', 'a+') as f:
                f.write(f"{doc_id}\t{user_id1}\t{prolific_id1}\t{user_id2}\t{prolific_id2}\t{this_kappa}\t{f1}\t{iou}\t{total_events}\t{event_1}\t{event_2}\n")
    
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

