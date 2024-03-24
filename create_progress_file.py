import json
from os import listdir
import random


"""user_file = []
for file in listdir("data/selected_files_4_annotation"):
    with open(f"data/selected_files_4_annotation/{file}", "r") as f:
        user_file.append(json.load(f))


with open("data/user1.json", "w") as f:
    f.write(json.dumps(user_file, indent=4))"""

with open('data/selected_files_4_annotation_event_ranking.json', 'r') as f:
    caevo_event_ranking = json.loads(f.read())


user_file = []
count = 0
for file in listdir("data/selected_files_4_annotation"):
    if file.endswith(".json"):
        with open(f"data/selected_files_4_annotation/{file}", "r") as f:
            this_page = json.load(f)
            # user_file.append(json.load(f))
        
        new_event_list = []
        for event in this_page['event_list']:
            if len(event.split(';'))>1:
                new_event_list.append(event)
        
        if len(new_event_list) == 0:
            continue

        caevo_event_list = []
        for event, _ in caevo_event_ranking[this_page['doc_id']]:
            add_event = event.replace('Subj: ', '').replace('Obj: ', '')
            caevo_event_list.append((add_event, 'caevo'))
            if len(caevo_event_list) >= len(new_event_list):
                break
        
        llm_event_list = [(event, 'llm') for event in new_event_list]

        al_event_list = caevo_event_list + llm_event_list
        random.shuffle(al_event_list)

        event_list, source_list = zip(*al_event_list)
        this_page['event_list'] = event_list
        this_page['source'] = source_list

        this_page['checkboxes'] = [True for _ in this_page['event_list']]
        user_file.append(this_page)
        if len(user_file) >= 5:
            with open(f"data/group_{count}.json", "w") as f:
                f.write(json.dumps(user_file, indent=4))
            count += 1
            user_file = []