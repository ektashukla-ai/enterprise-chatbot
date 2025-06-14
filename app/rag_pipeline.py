from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from app.embeddings import load_vectorstore
from app.config import LLM_MODEL, TOP_K, OPENAI_API_KEY

retriever = load_vectorstore().as_retriever(search_kwargs={"k": TOP_K})
llm = ChatOpenAI(model_name=LLM_MODEL,
                 openai_api_key=OPENAI_API_KEY)

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

def answer_query(query):
    result = rag_chain(query)
    return result