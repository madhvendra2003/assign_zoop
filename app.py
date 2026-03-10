import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
def load_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        extract = page.extract_text()
        if extract:
            text += extract + "\n"
    return text        



st.title("Resume chatbot")

up_file = st.file_uploader("Upload resume Pdf" , type = "pdf")

if up_file is not None :

    if "pdf_text " not in st.session_state:
        st.session_state.pdf_text = load_pdf(up_file)
        print(st.session_state.pdf_text)
        st.success("pdf is loaded")

    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview",temperature=0)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []   

    for q,a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            st.markdown(a)


    question = st.chat_input("Ask Question")
    
    if question :
        with st.chat_message("user"):
            st.markdown(question)

        messages = [
            SystemMessage(
                content=f"You are an expert Assitant . Answer the user's question based only on the following document :\n{st.session_state.pdf_text}"
            )
        ]    
            
        for q, a in st.session_state.chat_history:
            messages.append(HumanMessage(content=q))
            messages.append(AIMessage(content=a))

        messages.append(HumanMessage(content=question))

        with st.chat_message("assistant"):  
            response = llm.invoke(messages)
            if isinstance(response.content, list):
                    final_answer = response.content[0].get("text", "")
            else:
                    final_answer = response.content
            st.markdown(final_answer)
        
        st.session_state.chat_history.append((question, final_answer))
        







