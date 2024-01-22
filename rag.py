from qdrant_client import QdrantClient
from langchain.llms import HuggingFacePipeline
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Qdrant
from langchain.schema.document import Document
from langchain_community.document_loaders.csv_loader import CSVLoader



def load_data(file_path):
    loader = CSVLoader(file_path=file_path, csv_args={
        'delimiter': ',',
        'quotechar': '"',
        'fieldnames': ['Product Name','Price','Description'],
    })

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    all_splits = text_splitter.split_documents(documents)
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {"device": "cuda"}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

    vectordb = Qdrant.from_documents(documents=all_splits, embedding=embeddings, location=":memory:",
        prefer_grpc=True,
        collection_name="my_documents",
    ) # Local mode with in-memory storage only

    retriever = vectordb.as_retriever()
    return retriever

# qa = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",
#     retriever=retriever,
#     verbose=True
# )
def run_my_rag(qa, query):
    print(f"Query: {query}\n")
    result = qa.run(query)
    print("\nResult: ", result)