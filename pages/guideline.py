import streamlit as st


st.title('Guideline')

st.page_link('annotation_platform.py', label='Back to annotation page')

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
        st.write("**Step two**\n\nThe sidebar on the left show a list of candidate salient event suggested by an algorithm. We ask you to do the followings:\n\n1. If you think an event is salient, tick the checkbox next to it. Otherwise, untick the checkbox.\n\n2. If you think there is an event that is not listed, you can add it by entering the event in the text box. **The event should at least contain a subject and a trigger**.")

with st.container():
    st.write("## Example")

    st.image('images/example_1.png', use_column_width=True, caption='Example one')

    st.write("In example 1, *New York; is one of the four candidate cities; competing to be presented to the IOC* should not be chosen because the predicate is not something that can be considered as an event. On the other hand, *New York; is competing; with three cities to be presented to the IOC* should be chosen because the predicate can indicate an event.")

    st.image('images/example_2.png', use_column_width=True, caption='Example two')

    st.write("In example 2, *Daniel L. Doctoroff; said; we don't want any sympathy for that* is not a salient event because simply describing someone said something is not important enough in this article.")

    st.write("### Tips\n\nPrepare paper and pen (or a text editor on your device) to write down your summary while reading the article.")