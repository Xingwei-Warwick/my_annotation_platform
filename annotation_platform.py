import yaml
import json
from yaml.loader import SafeLoader
from utils import text_preprocess
import extra_streamlit_components as stx
import streamlit as st
import streamlit_authenticator as stauth


def save_cache_callback(box_idx, p_id, check_box_list, name):
    with open(f'user_progress/{name}.json', 'r') as f:
        progress_data = json.load(f)
    progress_data[p_id]['checkboxes'] = check_box_list
    progress_data[p_id]['checkboxes'][box_idx] = not progress_data[p_id]['checkboxes'][box_idx]
    with open(f'user_progress/{name}.json', 'w') as f:
        f.write(json.dumps(progress_data, indent=4))


def submit():
    st.session_state.submit_text = st.session_state.input_text
    st.session_state.input_text = ""


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
        st.page_link("pages/guideline.py", label="Guideline")
    
    if page_select != st.session_state.get('current_page', 1):
        st.session_state['current_page'] = page_select
        st.rerun()
    
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
        st.page_link('pages/conclusion.py', label='Conclude the Annotation')



    event_selection_list = []
    for i, event in enumerate(progress_data[page_select - 1]['event_list']):
        # event_selection_list.append(st.sidebar.checkbox(event, value=True, key=f'event_{i}'))

        choose_checkbox = progress_data[page_select - 1]['checkboxes'][i]
        event_selection_list.append(
            st.sidebar.checkbox(event, 
                                value=choose_checkbox, 
                                key=f'event_{i}', 
                                on_change=save_cache_callback, 
                                kwargs={
                                    'box_idx': i, 
                                    'p_id': page_select-1, 
                                    'check_box_list': progress_data[page_select - 1]['checkboxes'], 
                                    'name': name
                                    }
                                )
                            )


    # progress_data[page_select-1]['checkboxes'] = event_selection_list
    # with open(f'user_progress/{name}.json', 'w') as f:
    #     f.write(json.dumps(progress_data, indent=4))
    if "submit_text" not in st.session_state:
        st.session_state.submit_text = ""

    new_event =  st.sidebar.text_input('Enter a new event you want to add', placeholder='subject; predicate; object', max_chars=150, key='input_text', on_change=submit)
    if len(st.session_state.submit_text) > 0:
        if st.session_state.submit_text in progress_data[page_select - 1]['event_list']:
            st.session_state.submit_text = ""
            # st.sidebar.error('This event already exists')
            
        elif len(st.session_state.submit_text.split(';'))>1:
            progress_data[page_select - 1]['event_list'].append(st.session_state.submit_text)
            progress_data[page_select - 1]['checkboxes'].append(True)
            with open(f'user_progress/{name}.json', 'w') as f:
                f.write(json.dumps(progress_data, indent=4))
            length = len(progress_data[page_select - 1]['event_list'])
            # event_selection_list.append(st.sidebar.checkbox(new_event, value=True, key=f'event_{length - 1}'))
            st.rerun()
            # new_event = ''
        else:
            st.sidebar.error('Please enter an event with at least a subject and a predicate')
    
    