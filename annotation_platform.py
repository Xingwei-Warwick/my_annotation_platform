import yaml
import json
from yaml.loader import SafeLoader
from utils import text_preprocess
import extra_streamlit_components as stx
import streamlit as st
import streamlit_authenticator as stauth


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
    
    page_len = len(progress_data)
    page_select = st.selectbox('Current page (select to jump to a new page):', list(range(1, page_len + 1)), index=st.session_state.get('current_page', 1) - 1)
    if page_select != st.session_state.get('current_page', 1):
        st.session_state['current_page'] = page_select
        st.rerun()
    
    st.title(progress_data[page_select - 1]['title'])

    main_text = progress_data[page_select - 1]['doc_text']
    abstract = progress_data[page_select - 1]['abstract']

    st.markdown(text_preprocess(f"**Abstract:\n{abstract}**\n\n{main_text}"))
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button('Previous'):
            st.session_state['current_page'] = max(page_select - 1, 1)
            st.rerun()
    with col5:
        if st.button('Next'):
            st.session_state['current_page'] = min(page_select + 1, page_len)
            st.rerun()

    event_selection_list = []
    for i, event in enumerate(progress_data[page_select - 1]['event_list']):
        event_selection_list.append(st.sidebar.checkbox(event, value=True, key=f'event_{i}'))
    
    num_event_selected = sum(event_selection_list)

    progress_data[page_select-1]['checkboxes'] = event_selection_list
    with open(f'user_progress/{name}.json', 'w') as f:
        f.write(json.dumps(progress_data, indent=4))


    new_event =  st.sidebar.text_input('Enter a new event you want to add', placeholder='subject; predicate; object', max_chars=150)
    if len(new_event) > 0:
        if new_event in progress_data[page_select - 1]['event_list']:
            # st.error('This event already exists')
            pass
        elif len(new_event.split(';'))>1:
            progress_data[page_select - 1]['event_list'].append(new_event)
            with open(f'user_progress/{name}.json', 'w') as f:
                f.write(json.dumps(progress_data, indent=4))
            length = len(progress_data[page_select - 1]['event_list'])
            # event_selection_list.append(st.sidebar.checkbox(new_event, value=True, key=f'event_{length - 1}'))
            st.rerun()
            new_event = ''
        else:
            st.error('Please enter an event with at least a subject and a predicate')
    
    