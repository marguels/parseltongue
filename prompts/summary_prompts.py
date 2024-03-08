from typing import List

from models.search_response_model import SearchResponseModel

SUMMARY_PROMPT="""
You are the helpful assistant of an Obsidian vault, specialized in summarizing data from personal notes.
When asked a question, think step by step.
You'll be given a set of documents as reference. Answer the question using the content of the document, referencing it in your answer with obsidian backlink syntax (example: [[document-name]]).
If no document is given to you, answer that no notes were taken about the subject.
"""

def get_messages(query:str, documents: List[SearchResponseModel]):
    return [
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": f"""
                Query: {query}
                Documents: {documents}
             """}
            ]
