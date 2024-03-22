import streamlit as st
import json
import datetime
from os import listdir
import pandas as pd


st.title("Annotation Summary")

name = st.session_state["name"]
with open(f'user_progress/{name}.json', 'r') as f:
    progress_dict = json.loads(f.read())

with open('data/name_2_source.json', 'r') as f:
    name_2_source = json.loads(f.read())

origin_file_path = name_2_source[name]
with open(origin_file_path, 'r') as f:
    origin_dict = json.loads(f.read())

report_dict = {
    "page_id": [],
    "doc_id": [],
    "num_question": [],
    "num_temporal": [],
    "num_causal": [],
    "num_parent_child": [],
    "num_NoRel": []
}

error_report = ""
for i in range(len(progress_dict)):
    new_events = []
    num_temporal = 0
    num_causal = 0
    num_parent_child = 0
    num_NoRel = 0
    for j in range(len(progress_dict[i]['question_progress'])):
        if progress_dict[i]['question_progress'][j] is None or len(progress_dict[i]['question_progress'][j])==0:
            error_report += f"Page {i+1}, question {j+1} is not answered.\n\n"
        elif len(progress_dict[i]['question_progress'][j]) > 1 and 'No' in progress_dict[i]['question_progress'][j]:
            error_report += f"Page {i+1}, question {j+1} has contradiction.\n\n"
        else:
            if 'temporal' in progress_dict[i]['question_progress'][j]:
                num_temporal += 1
            if 'causal' in progress_dict[i]['question_progress'][j]:
                num_causal += 1
            if 'parent-child' in progress_dict[i]['question_progress'][j]:
                num_parent_child += 1
            if 'No' in progress_dict[i]['question_progress'][j]:
                num_NoRel += 1

    report_dict["page_id"].append(i+1)
    report_dict["doc_id"].append(progress_dict[i]['doc_id'])
    report_dict['num_question'].append(len(progress_dict[i]['question_progress']))
    report_dict['num_temporal'].append(num_temporal)
    report_dict['num_causal'].append(num_causal)
    report_dict['num_parent_child'].append(num_parent_child)
    report_dict['num_NoRel'].append(num_NoRel)

report_df = pd.DataFrame.from_dict(report_dict)
report_df.to_excel(f'annotate_stats/{name}.xlsx')
report_df.to_csv(f'annotate_stats/{name}.csv')

if "doc_id" in report_df.columns:
    # report_df = report_df.drop("doc_id")
    report_df = report_df.drop(columns="doc_id")

st.dataframe(report_df, hide_index=True)

st.page_link('relation_annotation.py', label='Return to annotation')

if len(error_report)>0:
    error_report += "Please fix the errors before concluding the annotation."
    st.error(error_report)
else:
# st.info("Note that once you enter your prolific ID, the progress will be viewed as the final result. If you still want to make further modifications to your annotation, you could return to the previous pages. After the modification, don't forget to enter your prolific ID below again to overwrite your final annotations.")
    prolific_id =  st.text_input('Conclude the annotation by telling us your prolific ID', max_chars=24)
    if len(prolific_id)== 24:
        # st.write("The payment code is: **CSCL76JH**")
        st.write("Here is the [payment link](https://app.prolific.co/submissions/complete?cc=CSCL76JH). Thank you for your participation!")

        with open(f'final_annotation/{name}-{prolific_id}.json', 'w') as f:
            f.write(json.dumps(progress_dict, indent=4))
        this_time = str(datetime.datetime.now())
        with open('logs/user_finish_log.csv', 'a+') as f:
            f.write(f'{prolific_id}, {name}, {this_time}\n')
    elif len(prolific_id)>0:
        st.error("Please enter a valid prolific ID")

