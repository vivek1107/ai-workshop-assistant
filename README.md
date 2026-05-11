# AI Workshop Assistant: Meeting Notes & Action Tracker

A lightweight, local-first AI workflow app that turns raw meeting notes or workshop transcripts into:

- Executive summary
- Key discussion points
- Decisions made
- Action items with owner, due date, and priority
- Risks and open questions
- Follow-up email draft
- Downloadable Markdown report

Built with:

- Python
- Streamlit
- Ollama
- Open-source local LLMs such as Llama 3.2

## Why this project is useful

This project is designed for consulting, pre-sales, architecture, and client workshop scenarios.

It helps demonstrate how AI can support:

- meeting summarization
- client discovery
- follow-up automation
- workshop documentation
- consulting productivity

## Prerequisites

1. Install Python 3.10 or above
2. Install Ollama from https://ollama.com
3. Pull a local model:

```bash
ollama pull llama3.2:3b
```

If your laptop is low on memory, try:

```bash
ollama pull llama3.2:1b
```

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

If activation is blocked, run:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## How to use

1. Paste raw meeting notes into the text box.
2. Select the Ollama model in the sidebar.
3. Click "Generate Meeting Summary".
4. Review structured output.
5. Download the Markdown report.
