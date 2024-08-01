import streamlit as st
# from countdown_component import countdown
from authentication import authorize, authorized
from utils import get_llm, log_message, get_img_html
from settings import APP_NAME, FILES_DIR, SCRIPT_DIR, DELIBERATION_TIME
from game_data import policy
from chat import initialize_chat_history, add_message, process_message, prologue_sequence

# set Streamlit session state
if 'show_timer' not in st.session_state:
    st.session_state.show_timer = False
if 'show_vote' not in st.session_state:
    st.session_state.show_vote = False
if 'show_notes' not in st.session_state:
    st.session_state.show_notes = False
if 'show_materials' not in st.session_state:
    st.session_state.show_materials = False
if 'show_commands' not in st.session_state:
    st.session_state.show_commands = False

@st.dialog("Material", width="large")
def show_material_details(material):
    st.subheader(material['title'])
    st.write(material['content'])
    if st.button("Close"):
        st.rerun()

def show_material(material):
    with st.expander(material["title"]):
        col_image, col_notes = st.columns([2, 3], gap="medium", vertical_alignment="center")
        with col_image:
            st.html(get_img_html(
                "img/cover1.jpg", 
                # width="100px", 
                centered=True, 
                styles="height: 200px; margin: 0px; padding: 0px"
            ))
            if st.button("Read", key=f"inspect_{material['title']}", use_container_width=True):
                show_material_details(material)
            if st.button(":star2: Summarize", key=f"summarize_{material['title']}", type='primary', use_container_width=True):
                st.write("Summary: ...")
        with col_notes:
            st.text_area("Notes", placeholder="Notes", key=f"notes_{material['title']}", height=300, label_visibility="collapsed")

def show_materials(materials):
    # st.html("<h3 style='text-align: center;'>Materials</h3>")
    col1, col2 = st.columns([1, 1], gap="large", vertical_alignment="top")
    for i, material in enumerate(materials):
        if i % 2 == 0:
            col = col1
        else:
            col = col2
        with col:
            show_material(material)

def show_sidebar():
    if st.session_state.show_timer:
        st.sidebar.html(f"<div style='text-align: center; color: red; font-weight: bold; font-size: 48pt; margin: 0px; padding: 0px'>🕑 4:00</div>")

    if st.session_state.show_vote:
        proposal = policy["proposal"]
        st.sidebar.html(f"<hr style='padding-top: 0px; margin-bottom: 2em; margin-top: 0px;'><div>Proposal</div><h3 style='margin: 0 0 1em 0; padding: 0'>{proposal}</h3><div style='text-align: center; font-weight: bold; font-size: 16pt; margin-top: 0em; margin-bottom: 0em; padding: 0px'>Vote</div>")
        col1, col2 = st.sidebar.columns([1, 1], gap="medium", vertical_alignment="top")
        with col1:
            if st.button(":thumbsup:", key=f"support", type='primary', use_container_width=True):
                st.write("Supporting")
        with col2:
            if st.button(":thumbsdown:", key=f"oppose", type='primary', use_container_width=True):
                st.write("Opposing")        
        st.sidebar.html("<hr style='padding: 0px; margin-top: 1em; margin-bottom: 1em'><div style='height: 0.2em;'></div>")

    if st.session_state.show_notes:
        st.sidebar.html("<div style='text-align: center; font-weight: bold; font-size: 16pt; margin-top: 0em; margin-bottom: 0em; padding: 0px'>Notes</div>")
        st.sidebar.text_area("Notes", placeholder="Pros\n\nCons", key=f"notes", height=250, label_visibility="collapsed")
    
def show_chat():
    col_avatar, col_chat = st.columns([2, 6], gap="large", vertical_alignment="top")
    with col_avatar:
        st.html(get_img_html("img/athena.jpg", centered=True, styles="width: 100px; margin-top: 0em; margin-bottom: 0em; padding: 0px"))
        st.html("<div style='text-align: center; font-weight: bold; font-size: 16pt; margin-top: 0em; margin-bottom: 0em; padding: 0px'>🌟 Athena</div>")
        if st.session_state.get('show_commands', False):
            st.html("<div style='height: 1.33em;'></div>")
            if st.button(":star2: Identify Pros and Cons", key=f"proscons", type='primary', use_container_width=True):
                add_message("human", "Can you identify the pros and cons of the current policy proposal?")
                st.rerun()
            if st.button(":star2: Make recommendation", key=f"recommendation", type='primary', use_container_width=True):
                add_message("human", "Based on the available information, what is your recommendation for this policy decision?")
                st.rerun()

    with col_chat:
        messages = st.container(height=300)
        with messages:
            for message in st.session_state.messages:
                avatar = "img/athena.jpg" if message.type == "ai" else None
                st.chat_message(message.type, avatar=avatar).write(message.content)

        # Display "Continue" button or chat input based on prologue completion
        if not st.session_state.prologue_complete:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("Continue", key="continue_prologue", type='primary', use_container_width=True):
                    st.session_state.prologue_complete = prologue_sequence()
                    st.rerun()
        else:
            prompt = st.chat_input("", key="chat_input")
            if prompt:
                add_message("human", prompt)
                ai_response = process_message(prompt)
                add_message("ai", ai_response)
                st.rerun()




authorize()
if authorized():
    initialize_chat_history()
    show_chat()
    show_sidebar()

    st.html("<div style='height: 4em;'></div>")
    
    # Materials section
    if st.session_state.show_materials:
        materials = policy.get("materials", [])
        show_materials(materials)
