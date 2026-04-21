# AI Agent - Multi-Model Chatbot

## Introduction
Welcome! This project is a simple but powerful **Multi-Model Chatbot**.

Instead of asking just one AI a question, it asks multiple AI **worker models** for their answers, then a single **judge model** reviews all responses and returns the best combined answer.

By collecting different perspectives first, then synthesizing them, you often get a more accurate and complete final response.

## How It Works
Imagine a panel of experts:

1. Each expert gives their own answer (the **worker models**).
2. A team leader gathers those answers, resolves contradictions, and produces a final summary (the **judge model**).

This project uses **OpenRouter**, which provides access to many models through a single API.

## Prerequisites (What You Need Before Starting)
No coding experience? No problem—follow these steps.

### 1. Install Python
Python is required to run this project.

- Go to [python.org](https://www.python.org/)
- Download the latest version for your operating system.
- Run the installer.
- **Important:** check the box **“Add Python to PATH”** during installation.

### 2. Get an OpenRouter API Key
Your API key is a private credential the script uses to request model responses.

- Create an account at [OpenRouter](https://openrouter.ai/)
- Open the **Keys / API Keys** section.
- Generate a new API key.
- Save it securely and do not share it publicly.

### 3. Add Your API Key to the Code
Open `ai-agent.py` in a text editor and find:

```python
api_key="your-openrouter-key-here"
```

Replace `your-openrouter-key-here` with your real key, keeping quotes intact.

## Setting Up and Running the Code
Open Terminal (or Command Prompt / PowerShell on Windows) in the project folder.

### Step 1: Install required packages

```bash
pip install -r requirement.txt
```

### Step 2: Run the chatbot

```bash
python ai-agent.py
```

You should see: **“Multi-Model Chatbot started!”**

Now enter questions and receive synthesized answers.

## Exploring the Code (`ai-agent.py`)
Python comments begin with `#` and are for humans (ignored by the interpreter).

### High-level flow
- **Initialization:** create the OpenRouter client with your API key.
- **Model selection:** define `worker_models` and `judge_model`.
- **Infinite loop:** `while True` keeps the chatbot running until you type `quit` or `exit`.
- **Gathering answers:** a `for` loop sends your question to each worker model and collects responses.
- **Synthesis:** worker outputs are combined and sent to the judge model, which returns one final answer.

Enjoy exploring AI!
