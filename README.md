# PDF Extractor with OpenAI

A Streamlit application that extracts structured financial data from PDF documents using OpenAI's GPT-4 and pdfplumber.

## Features
- Extracts text and tables from PDFs using `pdfplumber`.
- Uses GPT-4 to extract key financial details such as ISIN, SRI, RHP, product name, issuer name, and performance scenarios.
- Provides a simple and interactive Streamlit-based user interface for uploading and processing PDFs.

## Installation

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/your-username/pdf-extractor-openai.git
   cd pdf-extractor-openai

2. **Set up OpenAI API Key:**
  Create a .env file in the project root and add the following line:
  ```bash
  OPENAI_API_KEY=your_openai_api_key_here
  ```

3. **Run the Streamlit app:**
  ```bash
  streamlit run app.py
  ```
