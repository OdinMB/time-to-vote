# chat.py

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain.tools import BaseTool
from pydantic import Field
import streamlit as st
from utils import get_llm
from game_data import policy
from typing import List, Dict, Any
from time import time, sleep

# Define tools
class MaterialsTool(BaseTool):
    name = "Materials"
    description = "Use this tool to access policy materials"
    materials: List[Dict[str, Any]] = Field(default_factory=list)

    def __init__(self):
        super().__init__()
        self.materials = policy.get("materials", [])

    def _run(self, query: str) -> str:
        # Simple implementation - return all materials
        return str(self.materials)

class NotesTool(BaseTool):
    name = "Notes"
    description = "Use this tool to access the senator's notes"

    def _run(self, query: str) -> str:
        # Access notes from session state
        main_notes = st.session_state.get("notes", "")
        material_notes = {k: v for k, v in st.session_state.items() if k.startswith("notes_")}
        return f"Main notes: {main_notes}\nMaterial notes: {material_notes}"

tools = [
    MaterialsTool(),
    NotesTool()
]

# Initialize LLM and agent
llm = get_llm(large=True, max_tokens=2000, temperature=0.0)
prompt = hub.pull("hwchase17/react-chat")

# Modify the prompt to fit the context of the game
game_prompt = prompt.partial(
    system_message="""You are Athena, an AI assistant helping a senator make policy decisions. 
    You have access to policy materials and the senator's notes. 
    Provide helpful insights and guide the senator through the decision-making process."""
)

agent = create_react_agent(llm, tools, game_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def unlock_feature(feature):
    st.session_state[feature] = True

def prologue_sequence():
    messages = [
        ("ai", "Good morning, Senator. I trust you've had your coffee already. We have a pressing matter at hand. In response to yesterday's terrible incident, your party has called for an emergency meeting to improve AI safety.", ""),
        ("ai", "The meeting is scheduled to commence in precisely 4 hours. That's 4 minutes in our accelerated timeline. Allow me to start the countdown for you.", "show_timer"),
        ("ai", "You're expected to open the discussion on a proposal to improve cybersecurity for national infrastructure. The party will be looking to you to either support or oppose the proposal. No pressure, of course.", "show_vote"),
        ("ai", "Your research team has compiled a comprehensive set of data and materials. They should provide valuable insights into the matter at hand.", "show_materials"),
        ("ai", "I have access to your notepads and will consider whatever you record there.", "show_notes"),
        ("ai", "As always, I'm at your service, Senator. Shall we dive into the materials?", "show_commands"),
    ]

    if 'prologue_index' not in st.session_state:
        st.session_state.prologue_index = 0

    if st.session_state.prologue_index < len(messages):
        role, content, unlocked_feature = messages[st.session_state.prologue_index]
        add_message(role, content)
        if unlocked_feature:
            unlock_feature(unlocked_feature)
        st.session_state.prologue_index += 1
        if st.session_state.prologue_index < len(messages):
            return False
    return True

# Modify the initialize_chat_history function
def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if 'prologue_complete' not in st.session_state:
        st.session_state.prologue_complete = False
        prologue_sequence()
        st.rerun()




def add_message(role, content):
    if role == "human":
        st.session_state.messages.append(HumanMessage(content=content))
    elif role == "ai":
        st.session_state.messages.append(AIMessage(content=content))

def get_chat_history():
    return "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.messages])

def process_message(user_input):
    try:
        chat_history = get_chat_history()
        response = agent_executor.invoke(
            {
                "input": user_input,
                "chat_history": chat_history
            }
        )
        return response['output']
    except Exception as e:
        return f"I apologize, but an error occurred: {str(e)}. Please try again or contact support if the issue persists."

# Export the functions
__all__ = ['initialize_chat_history', 'add_message', 'process_message']