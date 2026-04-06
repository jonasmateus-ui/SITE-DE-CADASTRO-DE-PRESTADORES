from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import google.generativeai as genai
import os

app = Flask(__name__)

# CONFIGURAÇÃO DA IA
CHAVE_IA = "AIzaSyBQbI2tl15wUq7rEALxGe0RXNGCelUeWF8" 
genai.configure(api_key=CHAVE_IA)

DB_PATH = "dados.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prestadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            servico TEXT NOT NULL,
            local TEXT NOT NULL,
            bio TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    sucesso = request.args.get('sucesso', '')
    return render_template("index.html", sucesso=sucesso)

@app.route('/pesquisar')
def pesquisar():
    busca = request.args.get('busca', '')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if busca:
        query = "SELECT * FROM prestadores WHERE nome LIKE ? OR servico LIKE ?"
        cursor.execute(query, (f'%{busca}%', f'%{busca}%'))
    else:
        cursor.execute("SELECT * FROM prestadores")
        
    prestadores = cursor.fetchall()
    conn.close()
    return render_template("resultados.html", prestadores=prestadores, busca=busca)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    servico = request.form.get('servico')
    local = request.form.get('local')
    bio = request.form.get('bio')
    if nome and servico:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO prestadores (nome, servico, local, bio) VALUES (?, ?, ?, ?)', (nome, servico, local, bio))
        conn.commit()
        conn.close()
        return redirect(url_for('index', sucesso='true'))
    return redirect(url_for('index'))

@app.route('/gerar_bio', methods=['POST'])
def gerar_bio():
    try:
        dados = request.get_json()
        servico = dados.get('servico')
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Escreva uma bio profissional curta e vendedora para um {servico} autônomo."
        response = model.generate_content(prompt)
        return jsonify({"bio_sugerida": response.text})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)