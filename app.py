from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = 'ads_unicid_projeto'  # Necessário para usar session (login)

# --- CONFIGURAÇÃO DO TOBIAS (IA) ---
# Se a chave der erro, gere uma nova no Google AI Studio
CHAVE_IA = "AIzaSyBQbI2tl15wUq7rEALxGe0RXNGCelUeWF8" 
genai.configure(api_key=CHAVE_IA)

DB_PATH = "dados.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Tabela de Prestadores (com Raio e Contato)
    cursor.execute('''CREATE TABLE IF NOT EXISTS prestadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT, email TEXT, senha TEXT,
        contato TEXT, profissao TEXT, bairro TEXT, 
        raio INTEGER, bio TEXT)''')
    # Tabela de Clientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT, email TEXT, senha TEXT)''')
    # Tabela de Contratações
    cursor.execute('''CREATE TABLE IF NOT EXISTS contratacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        cliente_id INTEGER, prestador_id INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# --- ROTAS DE NAVEGAÇÃO (ABRIR PÁGINAS) ---

@app.route('/')
def index():
    return render_template("index.html", nome_usuario=session.get('nome'))

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/cadastro_cliente')
def cadastro_cliente():
    return render_template("cadastro_cliente.html")

@app.route('/cadastro_prestador')
def cadastro_prestador():
    return render_template("cadastro_prestador.html")

# --- SISTEMA DE BUSCA (ABRE EM NOVA PÁGINA) ---

@app.route('/pesquisar')
def pesquisar():
    busca = request.args.get('busca', '')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Busca por Nome, Bairro ou Profissão
    query = "SELECT * FROM prestadores WHERE nome LIKE ? OR bairro LIKE ? OR profissao LIKE ?"
    cursor.execute(query, (f'%{busca}%', f'%{busca}%', f'%{busca}%'))
    prestadores = cursor.fetchall()
    conn.close()
    return render_template("resultados.html", prestadores=prestadores, busca=busca)

# --- LÓGICA DE SALVAMENTO E LOGIN ---

@app.route('/salvar_prestador', methods=['POST'])
def salvar_prestador():
    dados = (
        request.form.get('nome'), request.form.get('email'), request.form.get('senha'),
        request.form.get('contato'), request.form.get('profissao'), 
        request.form.get('bairro'), request.form.get('raio'), request.form.get('bio')
    )
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO prestadores (nome, email, senha, contato, profissao, bairro, raio, bio) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', dados)
    conn.commit()
    conn.close()
    return redirect(url_for('login'))

@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
    conn.commit()
    conn.close()
    return redirect(url_for('login'))

@app.route('/login_validar', methods=['POST'])
def login_validar():
    email = request.form.get('email')
    senha = request.form.get('senha')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Tenta Cliente
    cursor.execute('SELECT * FROM clientes WHERE email = ? AND senha = ?', (email, senha))
    user = cursor.fetchone()
    if user:
        session['user_id'], session['nome'] = user['id'], user['nome']
        return redirect(url_for('index'))
    
    # Tenta Prestador
    cursor.execute('SELECT * FROM prestadores WHERE email = ? AND senha = ?', (email, senha))
    user = cursor.fetchone()
    if user:
        session['user_id'], session['nome'] = user['id'], user['nome']
        return redirect(url_for('index'))
    
    return "Erro: Usuário ou senha inválidos."

# --- ASSISTENTE TOBIAS (IA) ---

@app.route('/tobias', methods=['POST'])
def chat_tobias():
    try:
        dados = request.get_json()
        pergunta = dados.get('mensagem')
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Você é o Tobias, assistente do site Conecta. Responda curto: {pergunta}. Se quiserem profissional, peça o bairro."
        response = model.generate_content(prompt)
        return jsonify({"resposta": response.text})
    except Exception as e:
        return jsonify({"resposta": "Tobias está descansando. Tente logo mais!"}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)