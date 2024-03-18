import streamlit as st
import json
import datetime
from os import listdir
import pandas as pd


st.title("Annotation Summary")

name = st.session_state["name"]
with open(f'user_progress/{name}.json', 'r') as f:
    progress_dict = json.loads(f.read())

this_group_id = len(list(listdir('configs'))) - 2
with open(f'data/group_{this_group_id}.json', 'r') as f:
    origin_dict = json.loads(f.read())

report_dict = {
    "page_id": [],
    "doc_id": [],
    "num_event_added": [],
    "num_event_deleted": [],
    "current_num_event": [],
    "origin_num_event": []
}
for i in range(len(progress_dict)):
    new_events = []
    for j in range(len(progress_dict[i]['event_list'])):
        if progress_dict[i]['checkboxes'][j]:
            new_events.append(progress_dict[i]['event_list'][j])
    new_set = set(new_events)
    old_set = set(origin_dict[i]['event_list'])
    deleted = len(old_set-new_set)
    added = len(new_set-old_set)

    report_dict["page_id"].append(i)
    report_dict["doc_id"].append(progress_dict[i]['doc_id'])
    report_dict['num_event_added'].append(added)
    report_dict['num_event_deleted'].append(deleted)
    report_dict['current_num_event'].append(len(new_events))
    report_dict['origin_num_event'].append(len(old_set))

report_df = pd.DataFrame.from_dict(report_dict)
report_df.to_excel(f'annotate_stats/{name}.xlsx')
report_df.to_csv(f'annotate_stats/{name}.csv')

if "doc_id" in report_df.columns:
    # report_df = report_df.drop("doc_id")
    report_df = report_df.drop(columns="doc_id")

st.dataframe(report_df, hide_index=True)


prolific_id =  st.text_input('Conclude the annotation by telling us your prolific ID', max_chars=24)
if len(prolific_id)== 24:
    st.write("The payment code is: **CSCL76JH**")
    this_time = str(datetime.datetime.now())
    with open('logs/user_finish_log.csv', 'a+') as f:
        f.write(f'{prolific_id}, {name}, {this_time}\n')
elif len(prolific_id)>0:
    st.error("Please enter a valid prolific ID")

