import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.ai.ai_model import OpenAIModelPromptTemplate
from src.ai import ai_model
from src.constants import COLLECTION_NAME, RESSOURCES_DIR, TOKEN
from src.helpers import crawl_and_download_pdfs
import src.vector_db.chroma_db_service as chroma_db_service

app = Flask(__name__)
CORS(app)


# create vector db
client = chroma_db_service.Chroma()
ai = OpenAIModelPromptTemplate(client)


@app.route("/import_all_files_to_collection", methods=["GET"])
def create_collection_controller():
        files = os.listdir(RESSOURCES_DIR)
        total_files = [file for file in files]
        # parse and save files
        for file in total_files:
            print(f"file begin {file}")
            client.import_single_file_to_db(filename=file, collection_name=COLLECTION_NAME)

        return "done"


@app.route("/query_result", methods=["POST"])
def query_controller():
    data = request.get_json()
    prompt = data.get("prompt")

    answer = ai.get_answer(prompt=prompt, token=TOKEN, collection_name=COLLECTION_NAME)
    return jsonify({"answer": answer})


@app.route("/crawling", methods=["POST"])
def crawling_controller():
    data = request.get_json()
    url = data.get("url")

    crawl_and_download_pdfs(base_url=url)
    return jsonify({"message": "done"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
