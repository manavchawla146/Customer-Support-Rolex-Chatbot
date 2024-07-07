import argparse
from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import gradio as gr

import os

# API Key
os.environ["OPENAI_API_KEY"] = ""

# Chroma Path
CHROMA_PATH = "chroma"

# Prompt Template
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def run(query_text):

    # Open AI Embeddings & Chroma DB Initialization
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Similarity Search
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    # Context Construction
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    # Model Invokation
    model = ChatOpenAI()
    response_text = model.invoke(prompt)

    # Source Gathering, standard procedure
    sources = [doc.metadata.get("source", None) for doc, _score in results]

    # Printing formatted response
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    return response_text.content

if __name__ == "__main__":
    demo = gr.Interface(fn=run, inputs="text", outputs="text")
    demo.launch()