import streamlit as st
import layout
import datetime
#from IPython.display import Image, display

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        .main {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)


myInvestment = layout.Investment()
graph = myInvestment.make_builder()

object_update = {}

st.title('Investment Graph')
form_container = st.container()
result_container = st.container()

form_col, graph_col = st.columns([4,2])

with form_container:
    with form_col:
        with st.form(key='user'):
            name = st.text_input('Name')
            dob = st.date_input(
                "Select your date of birth:",
                value=datetime.date(1989, 5, 13),  # default selected date
                min_value=datetime.date(1900, 1, 1),  # earliest selectable date
                max_value=datetime.date(2030, 12, 31)  # latest selectable date
            )

            capital = st.number_input('Capital')
            country = st.selectbox('Select a Country:', ['Ghana', 'Germany'])
            interest = st.selectbox('Industry interested in:', ['Service', 'Manufacturing'])
            submission = st.form_submit_button(label='Submit')

            if submission:
                with st.spinner('Generating, please wait'):
                    object_update = graph.invoke(
                        {'name': name, 'dob': dob, 'capital': capital,
                         'country': country,
                         'interest': interest})
    with graph_col:
        graph_img = graph.get_graph().draw_mermaid_png()
        st.image(image=graph_img, caption='The AI thinking Graph',  width=350)


st.divider()

q_col, ans_col = st.columns(2)

with result_container:
    data_col, bs_col = st.columns([2, 4])
    with bs_col:
        bs_placeholder = st.empty()

    with data_col:
        for key, val in object_update.items():
            if key != 'business_case':
                with q_col:
                    st.write(key)
                with ans_col:
                    st.write(val)
            else:
                bs_placeholder.subheader('Business Case')
                bs_placeholder.write(object_update['business_case'])


