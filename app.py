import os
import streamlit as st
from PyPDF2 import PdfReader
from groq import Groq

# Set up the Streamlit app
st.title("Pakistani Constitution Q&A App")
st.write("Upload the Pakistani Constitution PDF, explore sections, and ask questions.")

# Initialize the Groq API client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Read API key from environment variables

if not GROQ_API_KEY:
    st.error("Groq API key not found. Please set the 'GROQ_API_KEY' environment variable in Hugging Face Spaces settings.")
else:
    client = Groq(api_key=GROQ_API_KEY)

# Upload PDF
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# Predefined sections of the Constitution
sections = {
    "Preamble": (0, 1),
    "Fundamental Rights": (2, 10),
    # Add more sections with their page ranges here
}

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_file, start_page, end_page, max_chars=4000):
    """Extracts text from a specific range of pages in the PDF and limits text length."""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in range(start_page, end_page + 1):
            text += reader.pages[page].extract_text()
        return text[:max_chars].strip()  # Limit text to prevent token overflow
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# Section selection and Q&A functionality
if uploaded_file:
    st.success("PDF uploaded successfully.")
    selected_section = st.selectbox("Select a Section", list(sections.keys()))

    if selected_section:
        start_page, end_page = sections[selected_section]
        section_text = extract_text_from_pdf(uploaded_file, start_page, end_page)

        if section_text:
            st.text_area("Selected Section Text", section_text, height=300)

            # Question input
            question = st.text_input("Ask a question about this section:")

            if question:
                try:
                    st.info("Querying Groq API...")

                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": f"Based on this section of the Pakistani Constitution: {section_text}\n\nQuestion: {question}",
                            }
                        ],
                        model="llama-3.3-70b-versatile",
                        max_tokens=500,  # Limiting output tokens
                        temperature=0.7  # Adjust for more/less randomness
                    )

                    answer = chat_completion.choices[0].message.content
                    st.success(f"Answer: {answer}")
                except Exception as e:
                    st.error(f"Error communicating with Groq API: {e}")
else:
    st.warning("Please upload a PDF file to proceed.")





# import os
# import streamlit as st
# from PyPDF2 import PdfReader
# from groq import Groq

# # Set up the Streamlit app
# st.title("Pakistani Constitution Q&A App")
# st.write("Upload the Pakistani Constitution PDF, explore sections, and ask questions.")

# # Initialize the Groq API client
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Read the API key from environment variables

# if not GROQ_API_KEY:
#     st.error("Groq API key not found. Please set the 'GROQ_API_KEY' environment variable in Hugging Face Spaces settings.")
# else:
#     client = Groq(api_key=GROQ_API_KEY)

# # Upload PDF
# uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# # Predefined sections of the Constitution
# sections = {
#     "Preamble": (0, 1),
#     "Fundamental Rights": (2, 10),
#     # Add more sections with their page ranges here
# }

# # Helper function to extract text from PDF
# def extract_text_from_pdf(pdf_file, start_page, end_page):
#     try:
#         reader = PdfReader(pdf_file)
#         text = ""
#         for page in range(start_page, end_page + 1):
#             text += reader.pages[page].extract_text()
#         return text.strip()
#     except Exception as e:
#         st.error(f"Error extracting text from PDF: {e}")
#         return ""

# # Section selection and Q&A functionality
# if uploaded_file:
#     st.success("PDF uploaded successfully.")
#     selected_section = st.selectbox("Select a Section", list(sections.keys()))

#     if selected_section:
#         start_page, end_page = sections[selected_section]
#         section_text = extract_text_from_pdf(uploaded_file, start_page, end_page)

#         if section_text:
#             st.text_area("Selected Section Text", section_text, height=300)

#             # Question input
#             question = st.text_input("Ask a question about this section:")

#             if question:
#                 # Interact with the Groq API
#                 try:
#                     st.info("Querying Groq API...")
#                     chat_completion = client.chat.completions.create(
#                         messages=[
#                             {
#                                 "role": "user",
#                                 "content": f"Based on this section of the Pakistani Constitution: {section_text}\nQuestion: {question}",
#                             }
#                         ],
#                         model="llama-3.3-70b-versatile",
#                     )

#                     answer = chat_completion.choices[0].message.content
#                     st.success(f"Answer: {answer}")
#                 except Exception as e:
#                     st.error(f"Error communicating with Groq API: {e}")
# else:
#     st.warning("Please upload a PDF file to proceed.")
