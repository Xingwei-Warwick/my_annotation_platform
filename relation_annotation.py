import yaml
import json
from yaml.loader import SafeLoader
from utils import text_preprocess
import streamlit as st
import streamlit_authenticator as stauth


def save_cache_callback(box_idx, p_id, check_box_list, name):
    with open(f'user_progress/{name}.json', 'r') as f:
        progress_data = json.load(f)
    progress_data[p_id]['question_progress'] = check_box_list
    progress_data[p_id]['question_progress'][box_idx] = st.session_state[f'relation_{box_idx}']
    with open(f'user_progress/{name}.json', 'w') as f:
        f.write(json.dumps(progress_data, indent=4))


with open('configs/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login(max_concurrent_users=1)

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    # authenticator.logout()
    # st.success(f'Welcome *{st.session_state["name"]}*')
    
    # st.title('Some content')

    name = st.session_state["name"]
    with open(f'user_progress/{name}.json', 'r') as f:
        progress_data = json.load(f)
    
    head_col1, head_col2 = st.columns([4,1])
    page_len = len(progress_data)
    with head_col1:
        page_select = st.selectbox('Current page (select to jump to a new page):', list(range(1, page_len + 1)), index=st.session_state.get('current_page', 1) - 1)
    with head_col2:
        authenticator.logout()
        st.page_link("pages/rel_guideline.py", label="Guideline")
    
    if page_select != st.session_state.get('current_page', 1):
        st.session_state['current_page'] = page_select
        st.rerun()

    if page_select == 1:
        st.info("Please click the guidline link above to view the annotation guidelines and examples 👆")
    
    st.title(progress_data[page_select - 1]['title'])

    main_text = progress_data[page_select - 1]['doc_text']
    abstract = progress_data[page_select - 1]['abstract']

    st.markdown(text_preprocess(f"**Abstract:\n{abstract}**\n\n{main_text}"))

    col1, col2 = st.columns([4,1])

    with col1:
        if st.button('Previous'):
            st.session_state['current_page'] = max(page_select - 1, 1)
            st.rerun()
    with col2:
        if st.button('Next'):
            st.session_state['current_page'] = min(page_select + 1, page_len)
            st.rerun()
    if page_select == len(progress_data):
        st.write("Congrates! You have reached the last page. Please click the link below to get the payment code.")
        st.page_link('pages/rel_conclusion.py', label='Conclude the Annotation')


    rel_selection_list = []
    for i, question in enumerate(progress_data[page_select - 1]['question_list']):
        # event_selection_list.append(st.sidebar.checkbox(event, value=True, key=f'event_{i}'))
        relation_progress = progress_data[page_select - 1]['question_progress'][i]
        rel_selection_list.append(st.sidebar.multiselect(text_preprocess(f'({i+1}) {question}'), 
                                                         ['No', 'temporal', 'causal', 'parent-child'], 
                                                         default=relation_progress, 
                                                         key=f'relation_{i}',
                                                         on_change=save_cache_callback, 
                                                        kwargs={
                                                            'box_idx': i, 
                                                            'p_id': page_select-1, 
                                                            'check_box_list': progress_data[page_select - 1]['question_progress'], 
                                                            'name': name
                                                            }
                                                        )
                                                        )
    
    empty_question = False
    conflict = []
    for i, ins in enumerate(rel_selection_list):
        if len(ins) == 0:
            empty_question = True
        elif len(ins) > 1 and 'No' in ins:
            conflict.append(i+1)

    if empty_question:
        st.warning("Please select an answer for each question")
    
    if len(conflict) > 0:
        ids = ', '.join([str(x) for x in conflict])
        st.error(f"Contradictory answers are selected for the following questions: {ids}")
    

    


    
    