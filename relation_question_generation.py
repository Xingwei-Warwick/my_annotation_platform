import json
from argparse import ArgumentParser
import random


def create_questions(event_list):
    question_list = []
    for i in range(len(event_list)):
        for j in range(i+1, len(event_list)):
            question_list.append(f"Is ({event_list[i]}) related to ({event_list[j]})?")
    
    return question_list

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--path", type=str, required=True, help="Input file path")
    parser.add_argument("--split", type=int, default=1)
    args = parser.parse_args()

    with open(args.path, 'r') as f:
        data = json.load(f)
    
    for i in range(len(data)):
        checkbox = data[i]['checkboxes']
        event_list = []
        for j in range(len(checkbox)):
            if checkbox[j]:
                event_list.append(data[i]['event_list'][j])


        question_list = create_questions(event_list)
        data[i]['question_list'] = question_list
        data[i].pop('checkboxes', None)
        data[i].pop('event_list', None)
        data[i]['question_progress'] = [None for _ in range(len(question_list))]

    file_name = args.path.split('/')[-1]
    if args.split == 1:   
        with open(f"rel_questions/{file_name}", 'w') as f:
            json.dump(data, f, indent=4)
    else:
        data_split_list = []
        for i in range(len(data)):
            data_split = [[] for _ in range(args.split)]
            for q in data[i]['question_list']:
                digit = random.randint(0, args.split-1)
                data_split[digit].append(q)
            data_split_list.append(data_split)
        
        for i in range(args.split):
            out_data = []
            for j in range(len(data)):
                this_page = data[j].copy()
                this_page['question_list'] = data_split_list[j][i]
                this_page['question_progress'] = [None for _ in range(len(data_split_list[j][i]))]
                out_data.append(this_page)
            out_name = file_name.replace('.json', f'_{i+1}.json')
            with open(f"rel_questions/{out_name}", 'w') as f:
                json.dump(out_data, f, indent=4)

        

