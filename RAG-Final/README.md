# RAGv1

0. Collect API key from chatGPT and set the variables OPENAI_API_KEY in both .py scripts as the same.
1. Install all dependencies using the command <code>pip install -r requirements.txt</code>
2. Store the markdown data in the "data" directory
3. Run create_db.py by command <code>python create_db.py</code> to create a vectorstore database using ChromaDB.
4. Finally, to give out prompt use the code template <code>python query_data.py "prompt_data"</code>, replacing the prompt data with your actual prompt.