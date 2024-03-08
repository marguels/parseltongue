# Parseltongue 🐍
Parseltongue is a Python application that enables LLM-powered chat with your Obsidian notes. It allows you to create and persist embeddings of your Obsidian notes in a local Qdrant vector database. You can then query these embeddings and use GPT-3.5-turbo to generate a response.

## How it works
1. Embedding Creation: Parseltongue uses a local Qdrant vector database to create embeddings of your Obsidian notes. These embeddings capture the semantic meaning of your notes.
2. Querying: You can query the Qdrant vector database to retrieve relevant embeddings based on a given query. This allows you to find notes that are related to a specific topic or keyword.
3. Response Generation: Once the relevant embeddings are retrieved, Parseltongue utilizes GPT-3.5-turbo, a powerful language model, to generate a response based on the query and the retrieved embeddings. This response can provide insights, suggestions, or answers related to your query.

## Usage
To use Parseltongue, follow these steps:
1. Make sure you have Python 3.12 installed.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate`
4. Install required dependencies by running `pip install -r requirements.txt`.
5. Set up a local Qdrant vector database. You can refer to the [Qdrant quickstart guide](https://qdrant.tech/documentation/quick-start/).
6. Configure the connection details in the application `.env` file. You can refer to `.env.example`, as it contains all configurations needed.
7. Run your Qdrant service:
```shell
docker run -p 6333:6333 -p 6334:6334 \
    -v $/path/to/local/storage:/qdrant/storage:z \
    qdrant/qdrant
```
8. Run the application with `uvicorn app:app --reload`.
9. Start playing!

## Example

Here's an example cURL of how you can use Parseltongue:

```shell
curl --location 'http://localhost:8000/chat' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "user_input": "organising knowledge"
}'
```
