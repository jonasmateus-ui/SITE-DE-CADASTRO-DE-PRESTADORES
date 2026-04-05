from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import google.generativeai as genai
import os

app = Flask(__name__)

# --- CONFIGURAÇÃO DA IA (GEMINI) ---
# Substitua pelo sua chave real entre as aspas
CHAVE_IA = "SUA_CHAVE_AQUI" 
genai.configure(api_key=CHAVE_IA)

# Configuração do Banco de Dados
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

# Inicializa o banco sempre que o app carregar
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prestadores ORDER BY id DESC")
    prestadores = cursor.fetchall()
    conn.close()
    return render_template("index.html", prestadores=prestadores)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    servico = request.form.get('servico')
    local = request.form.get('local')
    bio = request.form.get('bio')

    if nome and servico:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO prestadores (nome, servico, local, bio) VALUES (?, ?, ?, ?)', 
                           (nome, servico, local, bio))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao salvar: {e}")
    
    return redirect(url_for('index'))

# --- ROTA DA IA PARA GERAR BIO ---
@app.route('/gerar_bio', methods=['POST'])
def gerar_bio():
    try:
        dados = request.get_json()
        servico = dados.get('servico')
        
        if not servico:
            return jsonify({"erro": "Serviço não informado"}), 400

        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Escreva uma bio profissional curta e vendedora para um {servico}. Seja direto."
        
        response = model.generate_content(prompt)
        return jsonify({"bio_sugerida": response.text})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)