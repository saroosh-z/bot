from flask import Flask, render_template
from flask import request, jsonify, abort
import Langchain
from langchain.llms import Cohere

app = Flask(__name__)

db = ""
def answer_from_knowledgebase(message):
    # TODO: Write your code here
    print("::answer_from_knowledgebase started::")
    # qa = Langchain.load_db()
    # res = qa({"query":message})
    res = db({"query":message})
    print(f"::answer_from_knowledgebase ended wth response: {res} ::")

    return res["result"]

def search_knowledgebase(message):
    print("::search_knowledgebase started::")

    res = db({"query":message})
    sources = ""
    # sourc_doc = res['source_documents']
    # print(f"source document converting to string: {sourc_doc}")
    for count,source in enumerate(res['source_documents'],1):
        sources += "Source " + str(count) + "\n"
        sources += source.page_content + "\n"
    print(f"::search_knowledgebase ended wutg sources= {sources}::")
    print(f"finding in source:::::{sources.find(message)}")
    return sources

def answer_as_chatbot(message):
    # TODO: Write your code here
    print("answer_as_chatbot US-01:: started::")
    Langchain.answer_as_bot(message)

    print("answer_as_chatbot US-01:: end::")
    return Langchain.answer_as_bot(message)

@app.route('/kbanswer', methods=['POST'])
def kbanswer():

    message = request.json['message']
    response_message = answer_from_knowledgebase(message)

    # response_message = search_knowledgebase(message)
    return jsonify({'message': response_message}), 200
     

@app.route('/search', methods=['POST'])
def search():    
    message = request.json['message']

    # Search the knowledgebase and generate a response
    # (call search_knowledgebase())
    response_message = search_knowledgebase(message)
    return jsonify({'message': response_message}), 200
     

@app.route('/answer', methods=['POST'])
def answer():
    
    message = request.json['message']
    # Generate a response
    response_message = answer_as_chatbot(message)
    # Return the response as JSON
    return jsonify({'message': response_message}), 200

@app.route("/")
def index():
    return render_template("index.html", title="")

@app.before_request
def load_db():
    global db 
    db= Langchain.load_db()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)