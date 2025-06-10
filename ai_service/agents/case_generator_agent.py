"""
Case Generator Agent: Handles patient intake and CRUD and classification.
"""
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from ai_service.memories.simple_memory import SimpleMemory
from ai_service.prompts.case_generator_prompt import case_generator_prompt
import os
from dotenv import load_dotenv

load_dotenv()

PATIENT_DB = {}

@tool
def create_patient_record(name: str, address: str, date: str, age: int, marital_status: str, sex: str, phone: str) -> str:
    """Create a new patient record."""
    pid = f"P{len(PATIENT_DB)+1}"
    PATIENT_DB[pid] = {
        "name": name, "address": address, "date": date, "age": age,
        "marital_status": marital_status, "sex": sex, "phone": phone, "visits": []
    }
    return f"Patient record created with ID: {pid}"

@tool
def get_patient_record(pid: str) -> dict:
    """Retrieve a patient record by ID."""
    return PATIENT_DB.get(pid, {})

@tool
def update_patient_record(pid: str, field: str, value: str) -> str:
    """Update a field in a patient record."""
    if pid in PATIENT_DB:
        PATIENT_DB[pid][field] = value
        return f"Updated {field} for {pid}"
    return "Patient not found"

@tool
def classify_patient(pid: str) -> str:
    """Classify as new or follow-up based on visit history."""
    patient = PATIENT_DB.get(pid)
    if not patient:
        return "Patient not found"
    return "Follow-up" if patient["visits"] else "New case"

llm = ChatOpenAI(
    model_name="gpt-4-turbo-preview",
    temperature=0.2,
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)

tools = [create_patient_record, get_patient_record, update_patient_record, classify_patient]

case_generator_agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=case_generator_prompt
)

case_generator_executor = AgentExecutor(
    agent=case_generator_agent,
    tools=tools,
    memory=SimpleMemory(),
    verbose=True
)
