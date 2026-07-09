import os
import time
from dotenv import load_dotenv


load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_groq import ChatGroq  
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.graphs import Neo4jGraph
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  


PDF_PATH = "C:/Users/vishn/rag-graph/MAININPUTDOCUMENT.pdf" 

if not NEO4J_PASSWORD:
    print(".env file not found")
    exit()


print("Neo4j connecting")
graph = Neo4jGraph(
    url=NEO4J_URI, 
    username=NEO4J_USERNAME, 
    password=NEO4J_PASSWORD
)


graph.query("MATCH (n) DETACH DELETE n")
graph.query("DROP INDEX vector_index IF EXISTS")
print("Existing database emptied")


print(f"Loading source pdf")
try:
    loader = PyPDFLoader(PDF_PATH)
    raw_docs = loader.load()
except Exception as e:
    print(f"{os.path.abspath(PDF_PATH)} not found")
    print(f"{e}")
    exit()


raw_docs = raw_docs[0:40] 

print("start chunking doc")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = text_splitter.split_documents(raw_docs)
print(f"{len(documents)} text chunks made")


print("Initialise Groq and embeddings")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY, 
    model_name="llama-3.3-70b-versatile", 
    temperature=0
)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


llm_transformer = LLMGraphTransformer(llm=llm)

print("Extract graph nodes and relationships")

#batching Loop

batch_size = 5

for i in range(0, len(documents), batch_size):
    batch = documents[i : i + batch_size]
    print(f" - Processing batch {i} to {i + len(batch)} / {len(documents)}...")
    
    try:
        #extrract from this small batch
        graph_documents = llm_transformer.convert_to_graph_documents(batch)
        
        #upload to Neo4j
        graph.add_graph_documents(
            graph_documents, 
            baseEntityLabel=True, 
            include_source=True 
        )
        print(f"   Saved batch to Neo4j")
        
    except Exception as e:
        print(f"   Error on batch {i} ---> {e}")
        time.sleep(5) #pause on error

print("graph structure uploaded")


print("try creating vector index")

graph.query("""
CREATE VECTOR INDEX vector_index IF NOT EXISTS
FOR (d:Document)
ON (d.embedding)
OPTIONS {indexConfig: {
 `vector.dimensions`: 384,
 `vector.similarity_function`: 'cosine'
}}
""")

print("calculat and store embeddings")
for i, doc in enumerate(documents):
    try:
        #calculate embedding
        embedding = embeddings.embed_query(doc.page_content)
        
        #update neo4j
        graph.query("""
        MATCH (d:Document {text: $text})
        SET d.embedding = $embedding
        """, {"text": doc.page_content, "embedding": embedding})
        
        if i % 10 == 0:
            print(f"embedded {i}/{len(documents)} chunks")
            
    except Exception as e:
        print(f"Error embedding chunk {i} --> {e}")

print("Graph built and Vector Index ready!!!!!!!!!!")