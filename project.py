import streamlit as st
import pdfplumber
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# Reads and extracts text content from all pages of a given PDF file.
def readPdfText(pdf):
    full_text = ""
    with pdfplumber.open(pdf) as doc:
        for page in doc.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

# Reads and extracts tables from all pages of a given PDF file.
def readPdfTable(pdf):
  tables = []
  with pdfplumber.open(pdf) as doc:
    for page in doc.pages:
      extracted_table = page.extract_table()
      if extracted_table:
        tables.append(extracted_table)
  return tables

# Extracts specified information from a given text using an AI model.
def extractDataText(text, fields):
    prompt = f"""
    Extract the following information from the given text. Translate it to ENGLISH. 
    Respond ONLY with a JSON object.

    Fields:
    {fields}

    Text:
    {text}
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = completion.choices[0].message.content.strip()
        result = json.loads(content)

    except json.JSONDecodeError:
        print("JSON Parsing Error: Invalid JSON response from OpenAI.")
        result = {}

    return result

# Extracts specific performance scenario data from a given table using an AI model.
def extractDataTable(table):
    prompt = f"""
    Extract all performance scenarios just at maturity (at the end of the Recommended Holding Period) in percentage from the given table.
    Respond ONLY with a JSON object.

    Table:
    {table}
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = completion.choices[0].message.content.strip()
        result = json.loads(content)

    except json.JSONDecodeError:
        print("JSON Parsing Error: Invalid JSON response from OpenAI.")
        result = {}

    return result

# Placeholder function for extracting key details from a given PDF.
def extractDetails(pdf):
    expectedFields = {
        'ISIN': None,
        'SRI': None,
        'RHP': None,
        'PRODUCT NAME': None,
        'ISSUER NAME': None,
        'TARGET MARKET': None
    }
    text = readPdfText(pdf)
    table = readPdfTable(pdf)
    textResult = extractDataText(text=text, fields=expectedFields)
    tableResult = extractDataTable(table)
    result = textResult.copy()
    result['Performance Scenarios at Maturity (%)'] = tableResult
    return result

# Streamlit UI
st.title("PDF Extractor with OpenAI")
st.write("Upload a PDF file to extract structured information.")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    pdf_bytes = BytesIO(uploaded_file.read())  # Convert to BytesIO for pdfplumber
    with st.spinner("Extracting data..."):
        result = extractDetails(pdf_bytes)

    st.subheader("Extracted Information:")
    st.write(f"**ISIN:** {result['ISIN']}")
    st.write(f"**SRI:** {result['SRI']}")
    st.write(f"**RHP:** {result['RHP']}")
    st.write(f"**PRODUCT NAME:** {result['PRODUCT NAME']}")
    st.write(f"**ISSUER NAME:** {result['ISSUER NAME']}")
    st.write(f"**TARGET MARKET:** {result['TARGET MARKET']}")

    # Display performance scenarios
    st.write("**PERFORMANCE SCENARIOS AT RHP:**")
    st.write(f"**Stress:** {result['Performance Scenarios at Maturity (%)']['Stress']}")
    st.write(f"**Unfavorable:** {result['Performance Scenarios at Maturity (%)']['Sfavorevole']}")
    st.write(f"**Moderate:** {result['Performance Scenarios at Maturity (%)']['Moderato']}")
    st.write(f"**Favorable:** {result['Performance Scenarios at Maturity (%)']['Favorevole']}")