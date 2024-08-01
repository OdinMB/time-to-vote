import streamlit as st
from settings import APP_NAME, AIDIGEST_PAGE, FEEDBACK_PAGE, DEVELOPER
from utils import get_img_html
# from game_data import policy

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

    div[data-testid="stExpander"] > details > summary > span > div > p {
        font-weight: bold;
    }
        
    div[data-testid="stChatMessage"] {
        padding-top: 0.5em;
        padding-bottom: 0.5em;
        margin-top: 0em;
        margin-bottom: -0.7em;
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