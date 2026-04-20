import streamlit as st
import os
import tempfile
import hashlib
import numpy as np
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from langchain_groq import ChatGroq
from typing import List
from langchain_core.embeddings import Embeddings

# ============ CONFIGURATION ============
# Enter your Groq API key here (get it from: https://console.groq.com/keys)
#GROQ_API_KEY = ""  # <<< REPLACE THIS WITH YOUR GROQ API KEY
# To:
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
# =======================================

# Simple hash-based embeddings (no API key, no PyTorch required)
class SimpleHashEmbeddings(Embeddings):
    """
    Simple deterministic embeddings using hashing.
    This is a lightweight fallback that works without any API keys or PyTorch.
    Uses TF-IDF-like approach with character n-grams.
    """
    
    def __init__(self, dim=384):
        self.dim = dim
    
    def _text_to_vector(self, text: str) -> np.ndarray:
        """Convert text to a fixed-size vector using character n-grams and hashing."""
        vector = np.zeros(self.dim, dtype=np.float32)
        
        # Use character 3-grams and 4-grams
        for n in [3, 4]:
            for i in range(len(text) - n + 1):
                ngram = text[i:i+n].lower()
                # Hash the ngram to get an index
                hash_val = int(hashlib.md5(ngram.encode()).hexdigest(), 16)
                idx = hash_val % self.dim
                vector[idx] += 1.0
        
        # Normalize the vector
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector.tolist()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._text_to_vector(text) for text in texts]
    
    def embed_query(self, text: str) -> List[float]:
        return self._text_to_vector(text)



# Page configuration
st.set_page_config(page_title="DocFusion - RAG Chat", page_icon="📄", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .upload-text {
        font-size: 1.2rem;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'vector_db' not in st.session_state:
    st.session_state.vector_db = None
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Title and description
st.title("📄 DocFusion - Document Q&A")
st.markdown("Upload a PDF document and ask questions about its content using AI-powered RAG (Retrieval-Augmented Generation)")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model selection
    model_name = st.selectbox(
        "LLM Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )
    
    # Chunk size configuration
    chunk_size = st.slider("Chunk Size", min_value=200, max_value=1000, value=500, step=50)
    chunk_overlap = st.slider("Chunk Overlap", min_value=0, max_value=200, value=50, step=10)
    
    st.markdown("---")
    st.markdown("**How to use:**")
    st.markdown("1. Upload a PDF document in the right panel")
    st.markdown("2. Wait for processing (embeddings are created locally)")
    st.markdown("3. Ask questions about the document in the left chat panel")
    st.markdown("4. The AI will answer based on your document content")
    
    st.markdown("---")
    st.markdown("**Features:**")
    st.markdown("• 100% free - no paid API keys needed")
    st.markdown("• Local embeddings (no OpenAI/HuggingFace costs)")
    st.markdown("• Fast Groq LLM inference")
    st.markdown("• Supports any PDF document")


# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="upload-text">💬 Ask Questions</p>', unsafe_allow_html=True)
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Query input
    query = st.chat_input("Ask a question about the document...")
    
    if query:
        if not st.session_state.qa_chain:
            st.error("Please set your GROQ_API_KEY in the code (line 16) and upload a document first!")
        else:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": query})
            
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(query)
                
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            response = st.session_state.qa_chain.run(query)
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        except Exception as e:
                            error_msg = f"❌ Error: {str(e)}"
                            st.error(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})

with col2:
    st.markdown('<p class="upload-text">📤 Upload Your Document</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", 
                                      help="Upload a PDF document to query")
    
    if uploaded_file is not None:
        with st.spinner("Processing document..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Load and process the document
                loader = PyPDFLoader(tmp_file_path)
                docs = loader.load()
                
                # Split into chunks
                splitter = CharacterTextSplitter(
                    chunk_size=chunk_size, 
                    chunk_overlap=chunk_overlap
                )
                chunks = splitter.split_documents(docs)
                
                # Create embeddings and vector store
                with st.spinner("Creating embeddings and building vector store..."):
                    # Using simple hash-based embeddings (no API key, no PyTorch)
                    embeddings = SimpleHashEmbeddings(dim=384)
                    vector_db = FAISS.from_documents(chunks, embeddings)
                    
                    st.session_state.vector_db = vector_db
                    
                    # Create QA chain using the API key from configuration
                    if GROQ_API_KEY:
                        retriever = vector_db.as_retriever()
                        qa_chain = RetrievalQA.from_chain_type(
                            llm=ChatGroq(
                                model_name=model_name,
                                groq_api_key=GROQ_API_KEY
                            ),
                            chain_type="stuff",
                            retriever=retriever
                        )
                        st.session_state.qa_chain = qa_chain
                        
                        st.success(f"✅ Document processed successfully! ({len(docs)} pages, {len(chunks)} chunks)")
                    else:
                        st.warning("⚠️ Please set your GROQ_API_KEY in the code (line 16) to enable Q&A")
                        
                    
            except Exception as e:
                st.error(f"❌ Error processing document: {str(e)}")
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit, LangChain, and Groq | Powered by RAG technology")