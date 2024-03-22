# https://medium.com/@uppadhyayraj/using-retrieval-augmented-generation-rag-to-enhance-local-large-language-models-e81b156f1457
# Using Retrieval Augmented Generation (RAG) to Enhance Local Large Language Models
# by, Raj Uppadhyay

#importing the main libraries for setting up code to interact with LLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp


# Defining a Promt Template to interact with LLM
template = """Question: {question}
Answer: Let's work this out in a step by step way to be sure we have the right answer."""

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
n_gpu_layers = 1 # Change this value based on your model and your GPU VRAM pool.
n_batch = 512 # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

# Make sure the model path is correct for your system!
llm = LlamaCpp(
model_path="D:/00_LLM_Models/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf",
n_gpu_layers=n_gpu_layers, n_batch=n_batch,
n_ctx = 3000,
temperature=0.0,
max_tokens=2000,
top_p=1,
callback_manager=callback_manager,
verbose=True, # Verbose is required to pass to the callback manager
)
#Question for LLM
question = "Which are the top 5 companies in world with their revenue in table format?"

#providing the results
#-- print("<====================================== Outcome from model =======================================>")
#-- llm.invoke(question)

# Starting the RAG inclusion from here

# Defining a Promt Template to interact with LLM
template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate(template=template, input_variables=["question"])

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

#include some libraries to read and load data from web
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://www.investopedia.com/biggest-companies-in-the-world-by-market-cap-5212784")
data = loader.load()

#split the data into small chunks 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

#Performing Embedding
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma

#storing the data in Vector Store
vectorstore = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())

question = "Which are the top 5 companies in world with their revenue in table format?"
docs = vectorstore.similarity_search(question)
len(docs)

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# Prompt
prompt = PromptTemplate.from_template(
    "Summarize the main themes in these retrieved docs: {docs}"
)


# Chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

from langchain import hub
from langchain_core.runnables import RunnablePassthrough, RunnablePick 

# Prompt
rag_prompt_llama = hub.pull("rlm/rag-prompt-llama")
rag_prompt_llama.messages

# retrieving the data from vector store
retriever = vectorstore.as_retriever()
qa_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt_llama
    | llm
    | StrOutputParser()
)

#finally getting the outcome
print("<====================================== Outcome from model with RAG =============================>")
qa_chain.invoke(question)

