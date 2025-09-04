import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

"""
RAG Template Script
-------------------
This is a plug-and-play Retrieval Augmented Generation (RAG) template.
You can reuse this for any project where you want to:
- Load and index documents
- Store embeddings in a vector database (FAISS)
- Ask questions and get answers based on your docs

Just update file paths, API keys, or model names according to your needs.
"""

# Step 1: Setup your API Key (replace with environment variable for security)
os.environ["OPENAI_API_KEY"] = "your_api_key_here"  # or use Gemini API if preferred

# Step 2: Load your documents (use any loader supported by LangChain)
loader = TextLoader("sample_docs.txt")  # Put your file here
documents = loader.load()

# Step 3: Split documents into smaller chunks (helps better retrieval)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# Step 4: Create embeddings and store in FAISS vector database
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# Step 5: Initialize the LLM (you can swap ChatOpenAI with Gemini, HuggingFace, etc.)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Step 6: Create the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff"
)

# Step 7: Ask questions to your RAG pipeline
print("RAG System Ready! Ask me anything from your docs.\n")
while True:
    query = input("YOU: ")
    if query.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        break
    response = qa_chain.run(query)
    print("RAG:", response)
