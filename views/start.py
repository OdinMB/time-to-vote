import streamlit as st

import math
import time
from time import mktime
from datetime import datetime, timedelta

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import HumanMessage
from typing import List, Dict
import json

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

# from countdown_component import countdown

from authentication import authorize, authorized
from utils import get_llm, get_embedding, log_message
from settings import APP_NAME, FILES_DIR, SCRIPT_DIR, DELIBERATION_TIME
from game_data import policies

# Create a JSON output parser
json_parser = JsonOutputParser()

# sample LLM function
def generate_something(query: str) -> List[str]:
    prompt_template = """\
    Query: {query}
    Generate 3 responses.
    Format your response as a JSON object that specifies a list 'variations'.
    """

    formatted_prompt = prompt_template.format(query=query, variations=variations)
    # log_message(formatted_prompt)

    messages = [HumanMessage(content=formatted_prompt)]
    model = get_llm(large=False, max_tokens=2000, temperature=0.0)
    response = model.invoke(messages)

    log_message(f"Variations: {response.content}")
    variations = json_parser.parse(response.content)['variations']
    return variations


# --- "main" ---

authorize()

@st.dialog("Material", width="large")
def show_material_details(material):
    st.subheader(f"{material['title']}")
    st.write(f"{material['content']}")
    if st.button("Close"):
        st.rerun()

if authorized():
    # Create tabs for each policy
    policy_tabs = st.tabs([f"{policy['icon']} {policy['tab']}" for policy in policies])

    for i, (tab, policy) in enumerate(zip(policy_tabs, policies)):
        with tab:
            policy_key = f"policy_{policy['policy_id']}"

            # Display policy proposal
            st.html(f"<div style=''>Proposal</div><h4 style='margin: 0; padding: 0'>{policy["proposal"]}</h4>")
            # col1, col2 = st.columns([3, 5], gap="large", vertical_alignment="top")
            # with col1:
            #     st.markdown("##### Proposal")
            # with col2:
            #     st.markdown(f"#### {policy["proposal"]}")

            st.html("<div style='height: 1em;'></div>")

            col1, col2 = st.columns([3, 5], gap="large", vertical_alignment="center")
            with col1:
                st.markdown("##### Athena")
            with col2:
                inner_col1, inner_col2, inner_col3 = st.columns([3, 3, 2])
                with inner_col1:
                    if st.button(":star2: Identify Pros and Cons", key=f"proscons_{policy_key}", type='primary', use_container_width=True):
                        st.write("Doing stuff")
                with inner_col2:
                    if st.button(":star2: Make recommendation", key=f"recommendation_{policy_key}", type='primary', use_container_width=True):
                        st.write("Doing stuff")
            
            col1, col2 = st.columns([3, 5], gap="large", vertical_alignment="top")
            with col1:
                st.markdown("##### Notes")
            with col2:
                st.text_area("Notes", placeholder="Pros\n\nCons", key=f"notes_{policy_key}", height=150, label_visibility="collapsed")

            col1, col2 = st.columns([3, 5], gap="large", vertical_alignment="center")
            with col1:
                st.markdown("##### My stance")
            with col2:
                st.radio("My stance", options=["Oppose", "Haven't Decided Yet", "Support"], index=1, horizontal=True, key=f"opinion_{policy_key}", label_visibility="collapsed")

            st.html("<div style='height: 2em;'></div>")

            # st.html("<h3 style='text-align: center;'>Materials</h3>")

            # Materials section
            materials = policy.get("materials", [])
            for material in materials:
                col_title, col_notes = st.columns([3, 5], gap="large", vertical_alignment="center")
                with col_title:
                    st.markdown(f"##### {material["title"]}")
                    inner_col1, inner_col2, inner_col3 = st.columns([2, 4, 5])
                    with inner_col1:
                        if st.button("Read", key=f"inspect_{policy_key}_{material['title']}", use_container_width=True):
                            show_material_details(material)
                    with inner_col2:
                        if st.button(":star2: Summarize", key=f"summarize_{policy_key}_{material['title']}", type='primary', use_container_width=True):
                            st.write("Summary: ...")
                with col_notes:
                    st.text_area("Notes", placeholder="Notes", key=f"notes_{policy_key}_{material['title']}", height=100, label_visibility="collapsed")