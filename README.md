# PDFJSONExtraction
Extracting JSON-based docs from pdfs. Converting unstructured to structured data, leveraging OPENAI. 

Specific Use Case:
Extracting business-oriented data from pitch decks. 

Tech Used:
Langchain (for LLM alterations), OpenAI (for modelling), Streamlit (for data visualisations), Pydantic (for data model instanstiations and parsing output), PyPDFLoader (for loading PDFs).

User Flow:
1. Streamlit GUI initialises
2. User prompted to enter pitch deck
3. OpenAI LLM chunks text, retrieves relevant info based from Pydantic models
4. JSON file is returned, available for download


Instructions for use:

1. pip install -r requirements.txt (in terminal)
2. Amend API keys as necessary
3. streamlit run app.py (in terminal)
4. Enter pdf and enjoy
