# Supervisor Project

Supervisor is an AI-powered automation platform designed to streamline healthcare operations such as appointment scheduling, inventory management, and case generation. It leverages agent-based architecture and integrates with LLMs (Large Language Models) to provide intelligent, context-aware automation for clinics and hospitals.

## Features

- **Appointment Scheduler Agent**: Automates patient appointment scheduling and management.
- **Inventory Management Agent**: Tracks medicine stock, handles prescriptions, and auto-orders medicines when stock is low.
- **Case Generator Agent**: Assists in generating and managing patient case records.
- **Supervisor Agent**: Orchestrates and coordinates between specialized agents.

```

## Getting Started

### Prerequisites
- Python 3.11+
- [Poetry](https://python-poetry.org/docs/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   ```
2. **Install dependencies:**
   ```bash
   poetry install
   ```
3. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in required values (e.g., `OPENAI_API_KEY`).

4. **Run the application:**
   ```bash
   poetry run python app/main.py
   ```

## Development

- Agents are implemented in `ai_service/agents/`.
- Prompts for LLMs are in `ai_service/prompts/`.
- Business logic and API endpoints are in `app/`.

### Running the Streamlit Application

1.  **Start the Streamlit application:**

    ```bash
    streamlit run app/main.py
    ```

    This will launch the Streamlit application in your default web browser.

