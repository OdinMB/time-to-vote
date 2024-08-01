# countdown_component.py
import os
import streamlit.components.v1 as components

import math
import time
from time import mktime
from datetime import datetime, timedelta

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "countdown",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("countdown", path=build_dir)

def countdown(key=None):
    component_value = _component_func(key=key, default=0)
    return component_value

if not _RELEASE:
    import streamlit as st

    st.subheader("Countdown Timer Component")

    if st.button("Set Timer (30 seconds)"):
        _component_func(command="set_time", seconds=30)

    if st.button("Start/Pause"):
        _component_func(command="start")

    if st.button("Reset"):
        _component_func(command="reset")

    result = countdown()
    if result:
        if result.get("event") == "finished":
            st.success("Countdown finished!")