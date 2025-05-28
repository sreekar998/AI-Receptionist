"""
Supervisor Agent: Routes user input to the correct agent and manages parallel execution if needed.
"""
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from ai_service.agents.case_generator_agent import case_generator_executor
from ai_service.agents.appointment_scheduler_agent import appointment_scheduler_executor
from ai_service.agents.inventory_management_agent import inventory_management_executor
import os
from dotenv import load_dotenv

load_dotenv()

AGENT_MAP = {
    "case": case_generator_executor,
    "appointment": appointment_scheduler_executor,
    "inventory": inventory_management_executor
}

SYSTEM_PROMPT = """
You are the Supervisor Agent for a healthcare receptionist system. Based on the user's request, route the task to one of the following agents:
- Case Generator Agent (for patient intake, CRUD, classification)
- Appointment Scheduler Agent (for appointments)
- Inventory Management Agent (for medicine stock)
Reply only with the agent name and a short reason, e.g.:
[case] Reason: patient registration
[appointment] Reason: schedule appointment
[inventory] Reason: check medicine
"""

import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4-turbo-preview",
    temperature=0.2,
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)

def route_to_agent(user_input: str):
    """Decide which agent to use and execute the task."""
    # Ask LLM to pick agent
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    agent_decision = llm.invoke(messages).content
    if "case" in agent_decision:
        return AGENT_MAP["case"].invoke({"input": user_input})
    elif "appointment" in agent_decision:
        return AGENT_MAP["appointment"].invoke({"input": user_input})
    elif "inventory" in agent_decision:
        return AGENT_MAP["inventory"].invoke({"input": user_input})
    else:
        return {"output": "Sorry, I could not determine the correct agent for your request."}
