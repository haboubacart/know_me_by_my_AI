from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from chatbot import reponse_to_query, LLM_MODEL, RETRIVER
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
       return render_template('chatbot.html')
    elif request.method == 'POST':     
        data = request.json
        query = data['query']
        reponse = reponse_to_query(LLM_MODEL, RETRIVER, query)
        return jsonify({'query': query, 'answer': reponse})

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=8080) 