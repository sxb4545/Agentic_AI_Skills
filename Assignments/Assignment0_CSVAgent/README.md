# Hello Agent - CSV FAQ Agent (Week 0 Mini Project)

A small Streamlit web app that answers natural-language questions using **only**
the data inside uploaded CSV files. It uses a LangChain pandas DataFrame agent
backed by an OpenAI chat model (`gpt-4o-mini`).

## What it does

- Upload one or more CSV files (or use the bundled sample data).
- Shows a small preview (first rows) of each loaded file.
- Ask a question in plain English.
- The agent reads the tables and answers from the data only.
- If the answer isn't in the data, it replies:
  *"I could not find this information in the uploaded files."*

## Sample data

The `sample_data/` folder contains the four CSVs from the course
`Week_1_Prerequisites` folder:

- `ecommerce_faqs.csv` — online store FAQs
- `credit_card_terms.csv` — credit card terms and conditions
- `hospital_policy.csv` — hospital visit / records policies
- `saas_docs.csv` — SaaS features, limits, and support details

## Setup

1. (Recommended) Create and activate a virtual environment.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Provide your OpenAI API key. Either:
   - Copy `.env.example` to `.env` and set `OPENAI_API_KEY`, **or**
   - Paste the key directly into the app sidebar at runtime.

## Run

```powershell
streamlit run app.py
```

The app opens in your browser. Enable the sample CSVs (or upload your own),
type a question, and click **Ask**.

## Example questions

- What is the return policy for electronics?
- What does the extended warranty cover?
- What are the visiting hours in the hospital?
- What is the API rate limit for the free plan?

## Notes

- Temperature is set to `0.0` for predictable, non-creative answers.
- `allow_dangerous_code=True` is required by the LangChain pandas agent so it can
  execute pandas expressions against your DataFrames locally. Only run it on data
  you trust.
