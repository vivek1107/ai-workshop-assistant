# AI Workshop Assistant: Meeting Notes & Action Tracker

A lightweight, local-first AI workflow app that converts raw meeting notes or workshop transcripts into structured, actionable outputs.

## What It Generates

- Executive summary
- Key discussion points
- Decisions made
- Action items with owner, due date, and priority
- Risks and open questions
- Follow-up email suggestions
- Downloadable Markdown report

## Why I Built This

In consulting, architecture, and pre-sales discussions, valuable information is often captured in unstructured notes. This project explores how AI can help convert those notes into clear summaries, decisions, risks, and follow-up actions.

The goal is to demonstrate a practical AI workflow that improves clarity, accountability, and follow-up after meetings or workshops.

## Tech Stack

- Python
- Streamlit
- Ollama
- Local open-source LLM such as Llama 3.2

## Use Cases

- Client discovery workshops
- Architecture discussions
- Pre-sales meetings
- Internal project reviews
- Consulting productivity workflows

## How to Run

1. Install Python 3.10 or above.
2. Install Ollama.
3. Pull a local model such as Llama 3.2.
4. Install project dependencies from `requirements.txt`.
5. Run the Streamlit app from the project folder.
6. Paste sample meeting notes and generate the structured output.

## Future Enhancements

- PDF/DOCX transcript upload
- CSV export for action items
- Microsoft Teams transcript support
- Azure OpenAI version
- LangGraph-based workflow version

## Note

This is a learning and portfolio project focused on practical AI workflow automation. It uses sample notes only and does not include any confidential or client-specific information.
