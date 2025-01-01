from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
from flask_session import Session
from datetime import timedelta
import src.token_manager as token_manager
from src.chatbot import reponse_to_query
import warnings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import FAISS
load_dotenv()
warnings.simplefilter(action='ignore', category=FutureWarning)

load_dotenv()

model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

model_path = "Lajavaness/sentence-camembert-large"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

EMBEDDING_MODEL = HuggingFaceEmbeddings(
    model_name=model_path,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
LLM_MODEL= ChatOpenAI(api_key= os.getenv("OPENAI_API_KEY"), model="gpt-4o")
RETRIVER = FAISS.load_local("./faiss_index", EMBEDDING_MODEL, allow_dangerous_deserialization=True)

def create_app():
    app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    Session(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tokens.db'
    token_manager.db.init_app(app)
    app.secret_key = 'votre_clé_secrète_ici'  
    

    with app.app_context():
        create_tables()
    return app

def create_tables():
    token_manager.db.create_all()

app = create_app()


@app.route('/generate_token', methods=['GET'])
def generate_token():
    tokens = token_manager.create_token()
    return f"Token generated: {tokens}"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        token = request.form['token']
        if token_manager.verify_token(token):
            session['authenticated'] = True
            session['token'] = token
            session.permanent = True
            return redirect(url_for('index'))
        else:
            flash('Token invalide.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    token = session.get('token')
    if token:
        token_manager.invalidate_token(token)
        session.pop('token', None)
    session.pop('authenticated', None)
    flash('Le token a expiré. Veuillez vous reconnecter.', 'success')
    return redirect(url_for('login'))

@app.route('/chat', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        if 'authenticated' in session:
            return render_template('chatbot.html')
        else:
            flash('Vous devez vous connecter pour accéder à cette page.', 'danger')
            return redirect(url_for('login'))
        
    elif request.method == 'POST':     
        data = request.json
        query = data['query']
        reponse = reponse_to_query(LLM_MODEL, RETRIVER, query)
        return jsonify({'query': query, 'answer': reponse})
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=8080) 