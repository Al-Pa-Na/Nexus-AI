# Nexus AI 🤖

Nexus AI is a conversational agent that leverages Large Language Models (LLMs) to create an intuitive, natural language interface for web automation. It is designed to replace the process of manual clicking and filtering with simple, high-level commands, demonstrated here on the Internshala website.

## Key Features

* **Dual-Tool AI Agent:** The agent is equipped with two distinct tools and intelligently chooses the correct one based on the user's command:
    1.  **Internship Scraper:** Finds and filters internship listings.
    2.  **Chat Scraper:** Downloads and searches through personal chat messages.
* **Natural Language Understanding:** Utilizes the **Google Gemini API** to parse plain English commands, understand user intent, and extract necessary parameters like keywords and locations.
* **Live Web Automation:** Employs **Playwright** to run a headless browser, log in securely, navigate dynamic web pages, and scrape data in real-time.
* **Database Integration:** Scraped data is saved into a persistent **SQLite database**, allowing for data retention and a more robust application architecture.

## Tech Stack

* **Backend:** Python, Flask
* **AI:** Google Gemini API
* **Web Automation:** Playwright
* **Database:** SQLite

## Technical Highlights

A key challenge addressed during development was building a resilient web scraper capable of handling the target website's frequently changing HTML structure. This was solved by implementing robust, fallback selectors and required a deep dive into browser debugging tools. The project also demonstrates a stable application setup, overcoming common Python dependency conflicts through the use of virtual environments.

---

## Getting Started

To get Nexus AI running on a local machine, follow these steps.

#### 1. Prerequisites

* Python 3.11+ installed on your system.
* A Google AI API Key.

#### 2. Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Al-Pa-Na/Nexus-AI.git](https://github.com/Al-Pa-Na/Nexus-AI.git)
    cd Nexus-AI
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    py -3.11 -m venv venv
    venv\Scripts\activate.bat
    ```

3.  **Install all dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright's browsers:**
    ```bash
    playwright install
    ```

5.  **Set up the environment file:**
    * Create a file named `.env` in the project root.
    * Add your API key: `GOOGLE_API_KEY="YOUR_API_KEY_HERE"`

6.  **Initialize the database:**
    Run this command once to create the `database.db` file.
    ```bash
    python database.py
    ```

7.  **Run the one-time login setup:**
    This will open a browser window to log in to Internshala and save the session.
    ```bash
    python setup.py
    ```

#### 3. Run the Application

Start the Flask web server:
```bash
python app.py
```
Then, open your browser and go to `http://127.0.0.1:5000`.
