import weaviate
from weaviate.classes.config import Configure
import json
import requests

client = weaviate.connect_to_local()

print(client.is_ready())  # Should print: `True`

client.collections.delete_all()

questions = client.collections.create(
    name="Question",
    vectorizer_config=Configure.Vectorizer.text2vec_ollama(     # Configure the Ollama embedding integration
        api_endpoint="http://host.docker.internal:11434",       # Allow Weaviate from within a Docker container to contact your Ollama instance
        model="nomic-embed-text",                               # The model to use
    ),
    generative_config=Configure.Generative.ollama(              # Configure the Ollama generative integration
        api_endpoint="http://host.docker.internal:11434",       # Allow Weaviate from within a Docker container to contact your Ollama instance
        model="llama3.2",                                       # The model to use
    )
)

resp = requests.get(
    "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
)
data = json.loads(resp.text)

questions = client.collections.get("Question")

with questions.batch.fixed_size(batch_size=200) as batch:
    for d in data:
        batch.add_object(
            {
                "answer": d["Answer"],
                "question": d["Question"],
                "category": d["Category"],
            }
        )
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = questions.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")
client.close()  # Free up resources