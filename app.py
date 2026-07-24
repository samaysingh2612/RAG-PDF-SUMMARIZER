import os
import streamlit as st

from rag import upload_pdf, ask_question


st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="📄",
)

st.title("📄 PDF Question Answering")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file is not None:

    os.makedirs("temp", exist_ok=True)

    pdf_path = os.path.join(
        "temp",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Upload to Pinecone"):

        with st.spinner("Uploading..."):

            upload_pdf(pdf_path)

        st.success("PDF Uploaded Successfully ✅")


st.divider()

query = st.text_input(
    "Ask a Question"
)

if st.button("Ask"):

    if query.strip() == "":
        st.warning("Enter a question.")
    else:

        with st.spinner("Thinking..."):

            answer = ask_question(query)

        st.subheader("Answer")

        st.write(answer)