import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
import os, re, traceback

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CSV Whisperer",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* App background */
.stApp { background: #F7F8FA; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Hero strip */
.hero {
    background: #1A1D27;
    border-radius: 14px;
    padding: 2.2rem 2.4rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.4rem;
}
.hero-icon {
    font-size: 2.6rem;
    line-height: 1;
}
.hero-title {
    font-size: 1.7rem;
    font-weight: 600;
    color: #FFFFFF;
    margin: 0 0 2px;
    letter-spacing: -0.4px;
}
.hero-sub {
    font-size: 0.85rem;
    color: #8B90A0;
    margin: 0;
}

/* Stat cards */
.stat-row { display: flex; gap: 12px; margin-bottom: 1.2rem; flex-wrap: wrap; }
.stat-card {
    background: #FFFFFF;
    border: 1px solid #E8EAF0;
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    flex: 1;
    min-width: 120px;
}
.stat-label { font-size: 11px; color: #8B90A0; text-transform: uppercase; letter-spacing: 0.6px; margin: 0 0 3px; }
.stat-value { font-size: 1.25rem; font-weight: 600; color: #1A1D27; margin: 0; }

/* Query box wrapper */
.query-wrap {
    background: #FFFFFF;
    border: 1px solid #E8EAF0;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}

/* Answer card */
.answer-card {
    background: #FFFFFF;
    border: 1px solid #E8EAF0;
    border-left: 3px solid #5B6CFF;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-top: 0.8rem;
    font-size: 0.9rem;
    color: #2D3142;
    line-height: 1.7;
}

/* Code block */
.code-block {
    background: #1A1D27;
    color: #A8D8A8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    overflow-x: auto;
    margin-top: 0.5rem;
    line-height: 1.6;
}

/* Example pill buttons */
.pill-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 0.6rem; }
.pill {
    background: #F0F1FF;
    color: #5B6CFF;
    border: 1px solid #D0D3FF;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    cursor: pointer;
    white-space: nowrap;
}

/* Section header */
.section-label {
    font-size: 11px;
    font-weight: 600;
    color: #8B90A0;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin: 0 0 0.6rem;
}

/* Streamlit button override */
.stButton > button {
    background: #5B6CFF !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 0.45rem 1.2rem !important;
    font-size: 0.88rem !important;
}
.stButton > button:hover { background: #4455EE !important; }

/* Upload area */
[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 1.5px dashed #D0D3FF;
    border-radius: 12px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-icon">🗂️</div>
    <div>
        <p class="hero-title">CSV Whisperer</p>
        <p class="hero-sub">Ask plain English questions about any CSV — get instant answers, charts, and code.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── API Key ───────────────────────────────────────────────────────────────────
api_key = os.getenv("GOOGLE_API_KEY", "")
if not api_key:
    with st.expander("🔑 Enter your Google Gemini API key", expanded=True):
        api_key = st.text_input("API Key", type="password", placeholder="AIza...")
        st.caption("Get a free key at [aistudio.google.com](https://aistudio.google.com). Key is only used in this session.")

if api_key:
    genai.configure(api_key=api_key)

# ── File Upload ───────────────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload your CSV file", type=["csv"], label_visibility="collapsed")

if uploaded:
    df = pd.read_csv(uploaded)
    st.session_state["df"] = df

    # Stat cards
    nulls = int(df.isnull().sum().sum())
    num_cols = len(df.select_dtypes(include="number").columns)
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card"><p class="stat-label">Rows</p><p class="stat-value">{len(df):,}</p></div>
        <div class="stat-card"><p class="stat-label">Columns</p><p class="stat-value">{len(df.columns)}</p></div>
        <div class="stat-card"><p class="stat-label">Numeric cols</p><p class="stat-value">{num_cols}</p></div>
        <div class="stat-card"><p class="stat-label">Missing values</p><p class="stat-value">{nulls:,}</p></div>
        <div class="stat-card"><p class="stat-label">File</p><p class="stat-value" style="font-size:0.85rem">{uploaded.name}</p></div>
    </div>
    """, unsafe_allow_html=True)

    # Data preview
    with st.expander("Preview data", expanded=False):
        st.dataframe(df.head(20), use_container_width=True)

    # ── Query Section ─────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Ask a question</p>', unsafe_allow_html=True)

    examples = [
        "Show a bar chart of the top 5 values",
        "What are the outliers?",
        "Summarize each column",
        "Show the trend over time",
        "What is the correlation between columns?",
        "Which rows have missing data?",
    ]

    # Example pills via buttons
    cols = st.columns(len(examples))
    for i, ex in enumerate(examples):
        if cols[i].button(ex, key=f"ex_{i}", use_container_width=True):
            st.session_state["query_input"] = ex

    query = st.text_input(
        "Your question",
        value=st.session_state.get("query_input", ""),
        placeholder="e.g. Which month had the highest sales?",
        label_visibility="collapsed",
        key="query_input",
    )

    if st.button("Ask →", use_container_width=False) and query and api_key:
        col_info = "\n".join([f"- {c} ({df[c].dtype}): sample {df[c].dropna().head(3).tolist()}" for c in df.columns])
        schema = f"DataFrame shape: {df.shape}\nColumns:\n{col_info}\n\nFirst 5 rows:\n{df.head(5).to_string()}"

        prompt = f"""You are a Python data analyst. A user uploaded a CSV with this structure:

{schema}

User question: "{query}"

Respond with:
1. A brief plain-English answer (2-3 sentences).
2. Python code using pandas and plotly that answers the question. The dataframe is already loaded as `df`. Use plotly.express (px) or plotly.graph_objects (go) for charts. Assign the final result to a variable called `result` (a DataFrame, string, or number) and the chart (if any) to `fig`.

Format exactly:
ANSWER: <your plain english answer>
CODE:
```python
<code here>
```
"""
        with st.spinner("Thinking..."):
            try:
                model = genai.GenerativeModel("gemini-flash-latest")
                response = model.generate_content(prompt)
                raw = response.text

                # Parse answer and code
                answer = ""
                code = ""
                if "ANSWER:" in raw:
                    answer = raw.split("ANSWER:")[1].split("CODE:")[0].strip()
                if "```python" in raw:
                    code = raw.split("```python")[1].split("```")[0].strip()

                if answer:
                    st.markdown(f'<div class="answer-card">💬 {answer}</div>', unsafe_allow_html=True)

                if code:
                    with st.expander("Generated code", expanded=False):
                        st.markdown(f'<div class="code-block">{code}</div>', unsafe_allow_html=True)

                    # Execute code safely
                    local_vars = {"df": df.copy(), "pd": pd, "px": px, "go": go}
                    exec(code, {}, local_vars)

                    if "fig" in local_vars and local_vars["fig"] is not None:
                        fig = local_vars["fig"]
                        fig.update_layout(
                            paper_bgcolor="white",
                            plot_bgcolor="#F7F8FA",
                            font_family="Inter",
                            margin=dict(l=20, r=20, t=40, b=20),
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    if "result" in local_vars:
                        res = local_vars["result"]
                        if isinstance(res, pd.DataFrame):
                            st.dataframe(res, use_container_width=True)
                        elif res is not None:
                            st.info(str(res))

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.code(traceback.format_exc())

    elif st.button("Ask →") and not api_key:
        st.warning("Please enter your Gemini API key above.")

else:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem; color: #8B90A0;">
        <div style="font-size:3rem; margin-bottom:1rem;">📂</div>
        <p style="font-size:1rem; font-weight:500; color:#2D3142;">Upload a CSV to get started</p>
        <p style="font-size:0.85rem;">Ask questions in plain English — no SQL or pandas required.</p>
    </div>
    """, unsafe_allow_html=True)
