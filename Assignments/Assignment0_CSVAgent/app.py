"""
Hello Agent - CSV FAQ Agent
============================
Week 0 Mini Project (Applied Agentic AI for SWEs)

A small Streamlit web app that lets support agents upload one or more CSV files
and ask natural-language questions. A LangChain pandas DataFrame agent (backed by
an OpenAI chat model) reads the tabular data and answers using ONLY the CSV
content. If the answer is not in the data, it says so clearly.
"""

import os
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
load_dotenv()  # Load OPENAI_API_KEY from a local .env file if present.

SAMPLE_DATA_DIR = Path(__file__).parent / "sample_data"

SYSTEM_PROMPT = """
You are "Hello Agent", a careful support assistant that answers questions using
ONLY the data contained in the uploaded CSV files (provided to you as pandas
DataFrames).

Rules you must always follow:
- Answer strictly from the data in the DataFrames. Do NOT use general world
  knowledge and do NOT guess.
- When several tables are available, first decide which DataFrame is most
  relevant to the question, then read the value(s) from it.
- For text questions, return the key piece of text (for example from an
  'Answer', 'Policy Text', 'Detail Text' or 'Description' column).
- For numeric questions, compute totals or averages from the data when needed.
- Reply in clear, plain English that a support agent could copy-paste into an
  email or chat.
- If the answer cannot be found in the data, reply exactly with:
  "I could not find this information in the uploaded files."
""".strip()


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def build_agent(dataframes, api_key):
    """Create a LangChain pandas DataFrame agent over the given DataFrames."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, api_key=api_key)
    agent = create_pandas_dataframe_agent(
        llm,
        dataframes,
        verbose=False,
        agent_type="openai-functions",
        allow_dangerous_code=True,
    )
    return agent


def load_uploaded_files(uploaded_files):
    """Read uploaded CSVs into a dict of {filename: DataFrame}."""
    data = {}
    for uploaded in uploaded_files:
        try:
            data[uploaded.name] = pd.read_csv(uploaded)
        except Exception as exc:  # noqa: BLE001 - surface parse errors to the UI
            st.warning(f"Could not read '{uploaded.name}': {exc}")
    return data


def load_sample_files():
    """Read the bundled sample CSVs into a dict of {filename: DataFrame}."""
    data = {}
    if not SAMPLE_DATA_DIR.exists():
        return data
    for csv_path in sorted(SAMPLE_DATA_DIR.glob("*.csv")):
        try:
            data[csv_path.name] = pd.read_csv(csv_path)
        except Exception as exc:  # noqa: BLE001
            st.warning(f"Could not read '{csv_path.name}': {exc}")
    return data


# --------------------------------------------------------------------------- #
# Page setup
# --------------------------------------------------------------------------- #
st.set_page_config(page_title="Hello Agent - CSV FAQ Agent", page_icon="🗂️")
st.title("🗂️ Hello Agent - CSV FAQ Agent")
st.caption(
    "Upload your CSV files, ask a question in plain English, and get an answer "
    "drawn only from the data."
)

# --------------------------------------------------------------------------- #
# Sidebar: API key + data source
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.header("⚙️ Settings")

    api_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input(
        "OpenAI API key",
        value=api_key,
        type="password",
        help="Your key is only used for this session and is never stored.",
    )

    st.divider()
    st.subheader("📁 Data source")
    use_sample = st.checkbox(
        "Use bundled sample CSVs",
        value=True,
        help="E-commerce FAQs, credit card terms, hospital policy and SaaS docs.",
    )
    uploaded_files = st.file_uploader(
        "Or upload your own CSV files",
        type="csv",
        accept_multiple_files=True,
    )

# --------------------------------------------------------------------------- #
# Load data
# --------------------------------------------------------------------------- #
dataframes_by_name = {}
if uploaded_files:
    dataframes_by_name.update(load_uploaded_files(uploaded_files))
if use_sample:
    # Do not overwrite uploaded files that share a name.
    for name, df in load_sample_files().items():
        dataframes_by_name.setdefault(name, df)

# --------------------------------------------------------------------------- #
# Preview loaded data
# --------------------------------------------------------------------------- #
if dataframes_by_name:
    st.subheader("📊 Loaded files")
    for name, df in dataframes_by_name.items():
        with st.expander(f"{name}  ({len(df)} rows × {len(df.columns)} cols)"):
            st.dataframe(df.head(), use_container_width=True)
else:
    st.info(
        "No data loaded yet. Enable the sample CSVs or upload your own files "
        "from the sidebar to get started."
    )

# --------------------------------------------------------------------------- #
# Question + answer
# --------------------------------------------------------------------------- #
st.subheader("💬 Ask a question")
with st.form("question_form"):
    question = st.text_input(
        "Your question",
        placeholder="e.g. What is the return policy for electronics?",
    )
    submitted = st.form_submit_button("Ask")

if submitted:
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not dataframes_by_name:
        st.error("Please load at least one CSV file first.")
    elif not question.strip():
        st.error("Please type a question.")
    else:
        with st.spinner("Reading the data and thinking..."):
            try:
                agent = build_agent(list(dataframes_by_name.values()), api_key)
                final_query = f"{SYSTEM_PROMPT}\n\nQuestion: {question.strip()}"
                result = agent.invoke(final_query)
                answer = result["output"] if isinstance(result, dict) else str(result)
                st.markdown("### ✅ Answer")
                st.write(answer)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Something went wrong: {exc}")

st.divider()
st.caption(
    "Data-only rule: answers come strictly from the uploaded CSVs. If the "
    "information is not present, the agent will say so."
)
