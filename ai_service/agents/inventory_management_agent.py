"""
Inventory Management Agent: Manages medicine stock and auto-ordering.
"""
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from ai_service.memories.simple_memory import SimpleMemory
from ai_service.prompts.inventory_management_prompt import inventory_management_prompt
import os
from dotenv import load_dotenv

load_dotenv()

# Simple in-memory medicine inventory
INVENTORY_DB = {
    "Paracetamol": 50,
    "Ibuprofen": 30,
    "Amoxicillin": 20
}

def normalize_medicine_name(medicine: str) -> str:
    """Normalize medicine name for consistent inventory lookup."""
    return medicine.strip().title()

@tool
def get_medicine_stock(medicine: str) -> int:
    """Get current stock for a medicine."""
    medicine = normalize_medicine_name(medicine)
    return INVENTORY_DB.get(medicine, 0)

@tool
def update_medicine_stock(medicine: str, quantity: int) -> str:
    """Update stock for a medicine."""
    medicine = normalize_medicine_name(medicine)
    INVENTORY_DB[medicine] = INVENTORY_DB.get(medicine, 0) + quantity
    return f"Stock for {medicine} updated to {INVENTORY_DB[medicine]}"

@tool
def auto_order_medicine(medicine: str, threshold: int = 10) -> str:
    """Auto-order medicine if below threshold."""
    medicine = normalize_medicine_name(medicine)
    stock = INVENTORY_DB.get(medicine, 0)
    if stock < threshold:
        INVENTORY_DB[medicine] += 50  # Simulate order
        return f"Auto-ordered 50 units of {medicine}. New stock: {INVENTORY_DB[medicine]}"
    return f"Stock sufficient: {stock} units"

@tool
def prescribe_medicine(medicine: str, quantity: int) -> str:
    """Prescribe a medicine to a patient: reduces stock by quantity, and auto-orders if stock falls below threshold (10 units)."""
    medicine = normalize_medicine_name(medicine)
    current_stock = INVENTORY_DB.get(medicine, 0)
    if current_stock < quantity:
        return f"Insufficient stock for {medicine}. Only {current_stock} units available."
    INVENTORY_DB[medicine] = current_stock - quantity
    response = f"Prescribed {quantity} units of {medicine}. Remaining stock: {INVENTORY_DB[medicine]}."
    # Auto-order if below threshold
    if INVENTORY_DB[medicine] < 10:
        auto_order_msg = auto_order_medicine.run(medicine)
        response += f" {auto_order_msg}"
    return response

llm = ChatOpenAI(
    model_name="gpt-4-turbo-preview",
    temperature=0.2,
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)

tools = [get_medicine_stock, update_medicine_stock, auto_order_medicine, prescribe_medicine]

inventory_management_agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=inventory_management_prompt
)

inventory_management_executor = AgentExecutor(
    agent=inventory_management_agent,
    tools=tools,
    memory=SimpleMemory(),
    verbose=True
)
