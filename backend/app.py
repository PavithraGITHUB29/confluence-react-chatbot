from flask import Flask, request, jsonify
from flask_cors import CORS
from confluence_fetch import fetch_confluence_pages
from database import store_pages_in_faiss, search_relevant_page
from crew_module import process_page_with_langchain

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests for frontend

index, titles, contents = None, None, None

@app.before_first_request
def initialize():
    global index, titles, contents
    pages = fetch_confluence_pages()
    if not pages:
        print("No pages fetched from Confluence.")
        return
    index, titles, contents = store_pages_in_faiss(pages)
    print("FAISS index initialized.")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided."}), 400

    title, content = search_relevant_page(query, index, titles, contents)

    if not title:
        return jsonify({"answer": "❌ No relevant documentation found."})

    answer = process_page_with_langchain(title, content, query)

    if not answer.strip():
        return jsonify({"answer": "🤷‍♂️ Sorry, no useful answer found in the documentation."})

    return jsonify({
        "title": title,
        "answer": answer
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
