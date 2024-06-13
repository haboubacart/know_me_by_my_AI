from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
from flask_session import Session
from datetime import timedelta, datetime
import token_manager
from dotenv import load_dotenv
from chatbot import reponse_to_query, LLM_MODEL, RETRIVER
load_dotenv()
    
def create_app():
    app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=10)
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
    return f"Tokens generated: {tokens}"

@app.route('/login', methods=['GET', 'POST'])
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
    flash('Votre temps est écoulé. Veuillez vous reconnecter.', 'success')
    return redirect(url_for('login'))

@app.route('/', methods=['GET','POST'])
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
    
    if 'authenticated' in session:
        return render_template('app.html')
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=8080) 