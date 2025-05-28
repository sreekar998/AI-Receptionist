"""
Appointment Scheduler Agent: Manages scheduling, notifications, and slot assignment.
"""
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from ai_service.memories.simple_memory import SimpleMemory
from ai_service.prompts.appointment_scheduler_prompt import appointment_scheduler_prompt
from ai_service.agents.case_generator_agent import PATIENT_DB
import os
from dotenv import load_dotenv

load_dotenv()

APPOINTMENT_DB = {}

@tool
def find_free_slot(date: str) -> str:
    """Find a free 20-30 min slot for a given date."""
    slots = APPOINTMENT_DB.get(date, [])
    for i in range(9, 17):
        slot = f"{i}:00-{i}:30"
        if slot not in slots:
            return slot
    return "No free slots available"

@tool
def schedule_appointment(pid: str, date: str) -> str:
    """Schedule an appointment for a patient."""
    slot = find_free_slot.invoke({"date": date})
    if slot == "No free slots available":
        return slot
    APPOINTMENT_DB.setdefault(date, []).append(slot)
    PATIENT_DB[pid]["visits"].append(date)
    return f"Appointment scheduled for {pid} on {date} at {slot}"

@tool
def send_appointment_notification(pid: str, date: str) -> str:
    """Send appointment notification to patient."""
    patient = PATIENT_DB.get(pid)
    if not patient:
        return "Patient not found"
    return f"Notification sent to {patient['phone']} for appointment on {date}"

llm = ChatOpenAI(
    model_name="gpt-4-turbo-preview",
    temperature=0.2,
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)

tools = [find_free_slot, schedule_appointment, send_appointment_notification]

appointment_scheduler_agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=appointment_scheduler_prompt
)

appointment_scheduler_executor = AgentExecutor(
    agent=appointment_scheduler_agent,
    tools=tools,
    memory=SimpleMemory(),
    verbose=True
)

