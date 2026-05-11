import json
from datetime import datetime
from typing import Any, Dict

import streamlit as st
import ollama


DEFAULT_MODEL = "llama3.2:3b"


SYSTEM_PROMPT = """
You are an AI Meeting Notes and Action Tracker assistant for enterprise consulting and pre-sales teams.

Your job is to transform raw meeting notes into a structured, executive-ready summary.

Return ONLY valid JSON with this exact structure:

{
  "meeting_title": "short title",
  "executive_summary": "brief summary in 4-6 lines",
  "key_discussion_points": ["point 1", "point 2"],
  "decisions_made": ["decision 1", "decision 2"],
  "action_items": [
    {
      "action": "clear action",
      "owner": "owner if known, otherwise TBD",
      "due_date": "due date if known, otherwise TBD",
      "priority": "High/Medium/Low"
    }
  ],
  "risks_and_open_questions": ["risk or question 1", "risk or question 2"],
  "follow_up_email": "professional email draft to send after the meeting"
}

Rules:
- Do not invent names, dates, or commitments.
- If owner or due date is missing, use "TBD".
- Keep business tone professional and concise.
- Prioritize clarity, accountability, and next steps.
- If the notes are about cloud, AI, Azure, architecture, security, governance, or FinOps, reflect that in the summary.
"""


def call_ollama_model(notes: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """
    Calls a local Ollama model and asks it to return structured meeting output as JSON.
    """
    user_prompt = f"""
Please analyze the following meeting notes and extract structured meeting outputs.

MEETING NOTES:
{notes}
"""

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        options={
            "temperature": 0.2
        },
        format="json"
    )

    content = response["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "meeting_title": "Meeting Summary",
            "executive_summary": content,
            "key_discussion_points": [],
            "decisions_made": [],
            "action_items": [],
            "risks_and_open_questions": [],
            "follow_up_email": "Could not generate a structured follow-up email because the model response was not valid JSON."
        }


def generate_markdown_report(result: Dict[str, Any]) -> str:
    """
    Converts structured JSON output into a clean Markdown report.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    md = []
    md.append(f"# {result.get('meeting_title', 'Meeting Summary')}")
    md.append("")
    md.append(f"Generated: {now}")
    md.append("")
    md.append("## Executive Summary")
    md.append(result.get("executive_summary", "No summary generated."))
    md.append("")

    md.append("## Key Discussion Points")
    for item in result.get("key_discussion_points", []):
        md.append(f"- {item}")
    md.append("")

    md.append("## Decisions Made")
    decisions = result.get("decisions_made", [])
    if decisions:
        for item in decisions:
            md.append(f"- {item}")
    else:
        md.append("- No explicit decisions captured.")
    md.append("")

    md.append("## Action Items")
    actions = result.get("action_items", [])
    if actions:
        md.append("| Action | Owner | Due Date | Priority |")
        md.append("|---|---|---|---|")
        for action in actions:
            md.append(
                f"| {action.get('action', 'TBD')} "
                f"| {action.get('owner', 'TBD')} "
                f"| {action.get('due_date', 'TBD')} "
                f"| {action.get('priority', 'Medium')} |"
            )
    else:
        md.append("- No action items captured.")
    md.append("")

    md.append("## Risks and Open Questions")
    risks = result.get("risks_and_open_questions", [])
    if risks:
        for item in risks:
            md.append(f"- {item}")
    else:
        md.append("- No risks or open questions captured.")
    md.append("")

    md.append("## Follow-Up Email Draft")
    md.append(result.get("follow_up_email", "No follow-up email generated."))
    md.append("")

    return "\n".join(md)


def main():
    st.set_page_config(
        page_title="AI Meeting Notes & Action Tracker",
        page_icon="📝",
        layout="wide"
    )

    st.title("📝 AI Meeting Notes & Action Tracker")
    st.caption(
        "A lightweight local AI assistant for turning workshop or meeting notes into summaries, decisions, actions, risks, and follow-up emails."
    )

    with st.sidebar:
        st.header("Settings")
        model = st.text_input("Ollama model", value=DEFAULT_MODEL)
        st.info(
            "Tip: Start with llama3.2:3b. If your laptop is low on RAM, try llama3.2:1b."
        )

        st.markdown("### Example command")
        st.code("ollama pull llama3.2:3b", language="bash")

    sample_text = """Client workshop notes:
- Client wants to explore AI assistant for internal knowledge retrieval.
- Current documents are spread across Enterprise Data sources.
- Robert from Security team is concerned about data leakage and access control.
- John from Architecture team prefers Azure OpenAI and Azure AI Search.
- Marry from Data Analytics team mentioned that business need a POC in 10 weeks (5 sprints of 2 weeks each)
- Solution Architect (Vivek) to prepare high-level architecture by Friday.
- Jennifer from Client team to provide sample documents next week.
- Open question: whether private endpoints are required for all services.
- Cost estimation should include model selection, token usage, and search index sizing.
"""

    notes = st.text_area(
        "Paste meeting notes or workshop transcript",
        value=sample_text,
        height=300,
        placeholder="Paste raw notes here..."
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        generate = st.button("Generate Meeting Summary", type="primary")

    with col2:
        clear = st.button("Clear Notes")

    if clear:
        st.rerun()

    if generate:
        if not notes.strip():
            st.warning("Please paste meeting notes first.")
            return

        with st.spinner("Analyzing notes using local Ollama model..."):
            try:
                result = call_ollama_model(notes, model=model)
                markdown_report = generate_markdown_report(result)

                st.success("Meeting summary generated successfully.")

                tab1, tab2, tab3 = st.tabs(["Structured View", "Markdown Report", "Raw JSON"])

                with tab1:
                    st.subheader(result.get("meeting_title", "Meeting Summary"))

                    st.markdown("### Executive Summary")
                    st.write(result.get("executive_summary", "No summary generated."))

                    st.markdown("### Key Discussion Points")
                    for item in result.get("key_discussion_points", []):
                        st.markdown(f"- {item}")

                    st.markdown("### Decisions Made")
                    decisions = result.get("decisions_made", [])
                    if decisions:
                        for item in decisions:
                            st.markdown(f"- {item}")
                    else:
                        st.markdown("- No explicit decisions captured.")

                    st.markdown("### Action Items")
                    actions = result.get("action_items", [])
                    if actions:
                        st.dataframe(actions, use_container_width=True)
                    else:
                        st.markdown("- No action items captured.")

                    st.markdown("### Risks and Open Questions")
                    risks = result.get("risks_and_open_questions", [])
                    if risks:
                        for item in risks:
                            st.markdown(f"- {item}")
                    else:
                        st.markdown("- No risks or open questions captured.")

                    st.markdown("### Follow-Up Email Draft")
                    st.write(result.get("follow_up_email", "No follow-up email generated."))

                with tab2:
                    st.code(markdown_report, language="markdown")
                    st.download_button(
                        label="Download Markdown Report",
                        data=markdown_report,
                        file_name="meeting_summary_report.md",
                        mime="text/markdown"
                    )

                with tab3:
                    st.json(result)

            except Exception as exc:
                st.error("Something went wrong while generating the summary.")
                st.exception(exc)
                st.markdown(
                    """
                    Common fixes:
                    - Make sure Ollama is installed and running.
                    - Pull the selected model first, for example: `ollama pull llama3.2:3b`
                    - Check the model name in the sidebar.
                    """
                )


if __name__ == "__main__":
    main()
