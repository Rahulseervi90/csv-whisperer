# 🗂️ CSV Whisperer
 [![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-FF4B4B?style=for-the-badge&logo=streamlit)](https://csv-whisperer.streamlit.app)

> Ask plain-English questions about any CSV file — get instant answers, charts, and the Python code that generated them.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini-1.5--flash-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## What it does

CSV Whisperer lets you talk to your data without writing a single line of code.

- Upload any `.csv` file
- Ask questions like *"What month had the highest sales?"* or *"Show me outliers in column B"*
- Get a plain-English answer + an interactive chart + the generated Python code

---

## Features

| Feature | Details |
|---|---|
| 🤖 AI-powered Q&A | Uses Google Gemini 1.5 Flash to understand your question |
| 📊 Auto-charts | Generates Plotly charts automatically when relevant |
| 🧠 Code transparency | Shows the pandas/plotly code it ran so you can learn |
| ⚡ Quick prompts | One-click example questions to get started fast |
| 🔒 Local execution | Your data never leaves your machine (only the schema is sent to the API) |

---

## Getting started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/csv-whisperer.git
cd csv-whisperer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Gemini API key
Go to [aistudio.google.com](https://aistudio.google.com) and create a free API key.

### 4. Run the app
```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## Project structure

```
csv-whisperer/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Example questions to try

- *"Show a bar chart of the top 10 values in column X"*
- *"What is the average of each numeric column?"*
- *"Which rows have missing data?"*
- *"Is there a correlation between column A and column B?"*
- *"Show the trend of sales over time"*
- *"Find outliers in the price column"*

---

## Tech stack

- **[Streamlit](https://streamlit.io)** — web UI
- **[Google Gemini 1.5 Flash](https://aistudio.google.com)** — LLM for code generation
- **[Pandas](https://pandas.pydata.org)** — data processing
- **[Plotly](https://plotly.com/python/)** — interactive charts

---

## License

MIT — free to use, modify, and distribute.
