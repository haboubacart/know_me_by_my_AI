from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import HumanMessage
load_dotenv()

model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

model_path = "../sentence-camembert-large"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

EMBEDDING_MODEL = HuggingFaceEmbeddings(
    model_name=model_path,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
LLM_MODEL= ChatOpenAI(api_key= os.getenv("OPENAI_API_KEY"), model="gpt-4o")
RETRIVER = FAISS.load_local("../faiss_index", EMBEDDING_MODEL, allow_dangerous_deserialization=True)


def custom_prompt(retriever, query):
    results = retriever.similarity_search(query, k=4)
    source_knowledge = "\n".join([x.page_content for x in results])
    augment_prompt = f"""Tu es un assistant et tu dois repondre aux questions qui te sont posées par un recruteur sur moi.
Tu dois être consis et convainquant dans tes reponses.
S'il y'a des élement à mettre en valeur dans la reponse, tu peux les mettre dans des balises html comme les paragrahes, le gras, l'italique, les listes. Pas de titre !!!
Si l'utilisateur ne demande pas de détailler, tu dois être synthétique.
Voici le contexte dont tu dois te servir : 
\nContexte :\n{source_knowledge}
\nQuestion : \n{query}"""
    return augment_prompt

def reponse_to_query(llm_model, retriever, query):
    prompt = [
        HumanMessage(content=custom_prompt(retriever, query))]
    response = llm_model.invoke(prompt).content
    return(response)