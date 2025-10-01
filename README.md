# Nexus AI 🤖

Nexus AI is a sophisticated conversational agent designed to serve as a natural language interface for web automation. It leverages a Large Language Model (LLM) to parse user commands, understand intent, and execute complex tasks on a target website, effectively bridging the gap between human language and browser-level actions.

## Key Features

* **Semantic Command Parsing:** Powered by GPT-4o, the agent moves beyond simple keyword matching to understand the full semantic meaning of a user's request, including context and multiple parameters (e.g., job title, location, and time frame).

* **Dynamic Tool Use:** Implements a Model-Context-Protocol approach where the LLM dynamically selects the appropriate Python function (e.g., `search`, `filter`) and populates its arguments based on the user's command. This makes the agent's capabilities easily extendable.

* **Robust Browser Automation:** Utilizes a persistent Playwright context to perform actions reliably, handling login sessions and mimicking human interaction patterns to navigate modern web platforms effectively.

* **Structured Data Extraction:** Intelligently scrapes specified data points from web pages and organizes them into structured formats (`.csv`) for immediate use and analysis.

## Technical Architecture

The agent operates on a modular architecture that separates language understanding from execution.

1.  **Interface Layer (main.py):** A command-line interface (CLI) captures the user's raw text command.

2.  **LLM Core (OpenAI API):** The user's command, along with a manifest of available tools (`tools.py`), is sent to the GPT-4o model. The LLM acts as the core processor, parsing the command and returning a structured JSON object specifying which function to call and what arguments to use.

3.  **Execution Layer (main.py):** This layer interprets the JSON object from the LLM and calls the corresponding Python function.

4.  **Automation Layer (scraper.py):** This layer contains the low-level Playwright functions that interact directly with the web browser to perform the requested tasks.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A valid OpenAI API key

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Al-Pa-Na/Nexus-AI.git](https://github.com/Al-Pa-Na/Nexus-AI.git)
    cd Nexus-AI
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright browsers:**
    ```bash
    playwright install
    ```

4.  **Set up environment variables:**
    - Create a `.env` file and add your OpenAI API key: `OPENAI_API_KEY="your_secret_api_key_here"`

5.  **Run one-time session setup:**
    ```bash
    python setup.py
    ```

### Usage

Start the agent and input your commands at the prompt:
```bash
python main.py
```
