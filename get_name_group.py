import json
from os import listdir
import subprocess


ROOT = 'final_annotation'

with open('data/name_2_source.json', 'r') as f:
    name_2_source = json.loads(f.read())


source_2_file = {}
for file in listdir(ROOT):
    user_name = file.split('-')[0]
    # name_2_file[user_name] = file
    if source_2_file.get(name_2_source[user_name]) is None:
        source_2_file[name_2_source[user_name]] = []
    
    source_2_file[name_2_source[user_name]].append(file)


for key in source_2_file:
    print(source_2_file[key])
    if len(source_2_file[key]) == 2:
        # source_2_file[key][0]
        subprocess.run(['python', 'compute_agreement.py', "--file1", f'{ROOT}/{source_2_file[key][0]}', "--file2", f'{ROOT}/{source_2_file[key][1]}'])
    elif len(source_2_file[key]) > 2:
        for i in range(len(source_2_file[key])):
            for j in range(i+1, len(source_2_file[key])):
                subprocess.run(['python', 'compute_agreement.py', "--file1", f'{ROOT}/{source_2_file[key][i]}', "--file2", f'{ROOT}/{source_2_file[key][j]}'])
    else:
        continue
