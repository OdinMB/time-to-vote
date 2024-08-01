import streamlit as st
from settings import APP_NAME, AIDIGEST_PAGE, FEEDBACK_PAGE, DEVELOPER
from utils import get_img_with_href

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title=APP_NAME + " - AI Digest", 
    page_icon="img/favicon-32x32.png",
    layout="wide", 
    initial_sidebar_state="expanded", 
    menu_items=None
)

# st.logo(
#     image="img/logo.webp", 
#     # link=AIDIGEST_PAGE,
# )

# --- PAGE SETUP ---
app_page = st.Page(
    page="views/start.py",
    title="Study materials",
    icon=":material/assignment_turned_in:",
    default=True,
)
manual_page = st.Page(
    page="views/manual.py",
    title="Manual",
    icon=":material/assignment:",
)
explanation_page = st.Page(
    page="views/explanation.py",
    title="Technical explanation",
    icon=":material/developer_board:",
)

# --- NAVIGATION ---
pg = st.navigation([app_page])
#     {
#         "Research": [app_page],
#         "Documentation": [manual_page, explanation_page],
#     }
# )
pg.run()


st.sidebar.html("<div style='height: 1em;'></div>")

### Timer
st.sidebar.html(f"<div style='text-align: center; color: red; font-weight: bold; font-size: 48pt; margin: 0px; padding: 0px'>🕑 2:36</div>")
st.sidebar.html("<div style='height: 0.5em;'></div>")
    

# mimic the look of  a chat history with an AI chatbot on the sidebar
athena_html = get_img_with_href("img/athena.jpg", "", "100px", True, "margin-top: 0em; margin-bottom: 0em; padding: 0px")
st.sidebar.html(athena_html)
st.sidebar.html("<div style='text-align: center; font-weight: bold; font-size: 16pt; margin-top: 0em; margin-bottom: 0.5em; padding: 0px'>Athena</div>")

st.sidebar.info("Welcome, Senator! How can I help you today?")
st.sidebar.warning("Hi Athena. I need help with the new policy proposals.")
st.sidebar.info("Sure thing! I can help you with that. What do you need help with?")
# text input field
user_input = st.sidebar.text_input(label="You:", value="", disabled=True)


# logo_html = get_img_with_href("img/AppLogo.jpg", AIDIGEST_PAGE, "200px", True, "margin-top: 0.5em; margin-bottom: 0.5em")
# st.sidebar.html(logo_html)

# st.sidebar.html(f"<h2 style='text-align: center; padding-top: 0; margin-top: 0;'>{APP_NAME}</h2>")

# st.sidebar.markdown(f"""\
#     [AI Digest]({AIDIGEST_PAGE})  
#     [Feedback]({FEEDBACK_PAGE})  

#     ---                    
# """)

# st.sidebar.info(f"""\
#     Developer: {DEVELOPER}  
# """)

# --- STYLES ---
st.html("""\
<style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 325px;
        max-width: 325px;
    }
        
    .stButton>button {
        /* border-radius: 100px; */
    }
    div[data-testid="stTabs"] > div > div > div > button > div > p {
        font-size: 18px;
    }
        
    div[data-testid="stSidebarCollapseButton"] {
        display: none;
    }
    div[data-testid="stSidebarHeader"] {
        display: none;
    }
    section.main {
        padding-top: 0;
        margin-top: -35px;
    }

    div[data-testid="stSidebarHeader"] > a > img, 
    div[data-testid="collapsedControl"] > a > img, 
    div[data-testid="stSidebarHeader"] > img, 
    div[data-testid="collapsedControl"] > img {
        height: auto;
        width: 90px;
        margin-top: 10px
    }
    div[data-testid="stSidebarHeader"] > a > img,
        div[data-testid="stSidebarHeader"] > img {
            margin-left: 90px;
    }
            
    @media screen and (max-width: 767px) {
        .hide-on-mobile {
            display: none;
        }
    }
    @media screen and (min-width: 768px) {
        .hide-on-large_screen {
            display: none;
        }
    }
    .centered {
        text-align: center;
        width: 100%;
    }
</style>
""")