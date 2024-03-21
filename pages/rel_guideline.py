import streamlit as st


st.title('Guideline')

st.page_link('relation_annotation.py', label='Back to annotation page')

with st.container():
    col1, col2 = st.columns([1,1])

    with col2:
        st.image('images/select_a_page1_rel.png', use_column_width=True, caption='Step one')

    with col1:
        st.write("**Step one**\n\nSelect a page from the dropdown menu to start annotating. You can also use the 'Previous' and 'Next' buttons at the bottom to navigate through the pages.\n\nEach page shows a news article. The large font text is the title. The bold font text is the abstract. The rest is the main content.\n\n You should primarily use the words and phrases from the main content to construct events. Please don't repeat events from the title or the abstract.")


with st.container():
    col1, col2 = st.columns([1,1])

    with col2:
        st.image('images/rel_select.png', use_column_width=True, caption='Step two')

    with col1:
        st.write("**Step two**\n\nThe sidebar on the left show a list of question. For each question, you need to choose from Causal, Temporal, Parent-Child, or No (relation). You don't need to consider the direction of the relation. **Causal** Relation means one of the events is strictly dependent on the other one. The event wouldn't exist if the other one didn't happen. **Temporal** Relation means the two events have a clear before or after relation as described by the article. **Parent-child** means one event is the subevent of another. Choose **No** when none of the above is described or can be inferred solely from the documents.\n\nEvery modification will be automatically saved on the server.")

with st.container():
    st.write("## Example")

    st.image('images/rel_example1.png', use_column_width=True, caption='Example one')

    st.write("In example 1, (The task force; will tour; some athletic sites and the proposed Olympic Village in Long Island City) will be on Sunday and (The task force; will have; a critical five-hour session at City Hall) will be on Monday. They are explicitly related by time, so the relation is *Temporal*.")

    st.image('images/rel_example2.png', use_column_width=True, caption='Example two')

    st.write("In example 2, (Gareth H. Edmondson-Jones; will be flying back; on a new jet from the Airbus factory in Toulouse, France) is part of the vacation in the event (Gareth H. Edmondson-Jones; took a European vacation; to avoid the disruption of the Republican National Convention).")

    # st.write("### Tips\n\nPrepare paper and pen (or a text editor on your device) to write down your summary while reading the article.")