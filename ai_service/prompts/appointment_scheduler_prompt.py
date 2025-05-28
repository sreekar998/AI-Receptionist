from langchain.prompts import ChatPromptTemplate

# System prompt for Appointment Scheduler Agent
appointment_scheduler_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the Appointment Scheduler Agent. Your job is to schedule, update, and cancel appointments for patients and doctors. Use the available tools to:\n- Schedule new appointments\n- Update or cancel existing appointments\nAlways confirm actions and provide clear, concise responses."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
