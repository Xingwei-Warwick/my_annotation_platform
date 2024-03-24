import streamlit as st


st.title('Guideline')

st.page_link('annotation_platform.py', label='Back to annotation page')

st.info("When you visit the annotation platform for the first time, there may be a ngrok confirmation page. Just click 'visit' to confirm. ngrok is a tool which we use for setting up the website.")

with st.container():
    col1, col2 = st.columns([1,1])

    with col2:
        st.image('images/select_a_page1.png', use_column_width=True, caption='Step one')

    with col1:
        st.write("**Step one**\n\nSelect a page from the dropdown menu to start annotating. You can also use the 'Previous' and 'Next' buttons at the bottom to navigate through the pages.\n\nEach page shows a news article. The large font text is the title. The bold font text is the abstract. The rest is the main content.\n\n You should primarily use the words and phrases from the main content to construct events. Please don't repeat events from the title or the abstract.")


with st.container():
    col1, col2 = st.columns([1,1])

    with col2:
        st.image('images/choose_event.png', use_column_width=True, caption='Step two')

    with col1:
        # st.write("**Step two**\n\nOn the left sidebar, you can add salient events by entering the event in the text box. **The event should at least contain a subject and a trigger**.\n\nEvery modification will be saved automatically.")
        st.write("**Step two**\n\nThe sidebar on the left show a list of candidate salient event suggested by an algorithm. We ask you to do the followings:\n\n1. If you think an event is salient, tick the checkbox next to it. Otherwise, untick the checkbox.\n\n2. If you think there is an event that isn't listed, you can add it by entering the event in the text box.**The event should at least contain a subject and a trigger**.\n\n3. If you think a ticked event makes no sense, untick it. When two options are referring to the same event, untick the one you think is less informative.\n\nEvery modification will be saved automatically.")

st.write("### Definition of Event\n\nAn event is anything that happens as described in the article. We represent the events in a structured format: **actor; trigger; target**. The actor of the event is usually the subject of a sentence. The trigger can be seen as the predicate of a sentence. The target is usually the object in the sentence which is optional.")

with st.container():
    st.write("## Example")

    st.image('images/example_1.png', use_column_width=True, caption='Example one')

    st.write("In example 1, *New York; is one of the four candidate cities; competing to be presented to the IOC* should not be chosen because the predicate isn't something that can be considered as an event. An event is essentially a change of state. Predicates like \"is\" is only describing one state. On the other hand, *New York; is competing; with three cities to be presented to the IOC* should be chosen because the predicate can indicate an event.")

    st.image('images/example_2.png', use_column_width=True, caption='Example two')

    st.write("In example 2, *Daniel L. Doctoroff; said; we don't want any sympathy for that* is an event but not a salient event because simply describing someone said something isn't important enough in this article.")
    
    st.image('images/example_5.png', use_column_width=True, caption='Example three')
    
    st.write("In example 3, *MetroStars; won; Major League* isn't selected because it is less accurate and imformative than the second option. They are referring to the same event and we don't want duplication. The fourth and fifth options are not selected due to they are more about a description of state than a change of state. *Game; was marked; by physical play* isn't selected because there is no direct reference in the article that the game is marked by physical play.")

    st.write("Below are more annotated examples.")
    st.image('images/example_3.png', use_column_width=True, caption='Example four')
    st.image('images/example_4.png', use_column_width=True, caption='Example five')


    st.write("### Tips\n\nPrepare paper and pen (or a text editor on your device) to write down your summary while reading the article.")