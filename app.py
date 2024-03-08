from typing import List
from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from openai import OpenAI
from config.dependencies import get_embeddings_service, get_openai_client

from models.chat_input_model import ChatInput
from models.search_response_model import SearchResponseModel
from prompts.summary_prompts import get_messages


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    app.state.embeddings = await get_embeddings_service()
    print("EmbeddingsService initialized and loaded into app state.")
    yield
    print("shutting down")

app = FastAPI(title="Parseltongue",
              description="API to chat with obsidian vault",
              lifespan=lifespan)


@app.post("/chat", response_model=str)
async def chat(request: ChatInput,
               openai_client: OpenAI = Depends(get_openai_client)):
    documents = app.state.embeddings.search_documents(query=request.user_input)
    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=get_messages(query=request.user_input,
                              documents=documents),
        max_tokens=440
    )
    return completion.choices[0].message.content

@app.post("/search", response_model=List[SearchResponseModel])
async def search(request: ChatInput):
    results = app.state.embeddings.search_documents(query=request.user_input)
    return results