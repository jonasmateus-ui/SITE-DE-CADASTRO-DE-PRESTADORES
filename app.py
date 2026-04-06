from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = 'ads_unicid_projeto'

# CONFIGURAÇÃO DO TOBIAS (IA)
CHAVE_IA = "AIzaSyBQbi2tl15wUq7rEALxGe0RXNGCelUeWF8" # Sua chave atualizada
genai.configure(api_key=CHAVE_IA)

DB_PATH = "dados.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Tabela unificada para manter seu banco organizado
    cursor.execute('''CREATE TABLE IF NOT EXISTS prestadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, senha TEXT,
        contato TEXT, profissao TEXT, bairro TEXT, raio INTEGER, bio TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, senha TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pesquisar')
def pesquisar():
    busca = request.args.get('busca', '')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = "SELECT * FROM prestadores WHERE nome LIKE ? OR bairro LIKE ? OR profissao LIKE ?"
    cursor.execute(query, (f'%{busca}%', f'%{busca}%', f'%{busca}%'))
    prestadores = cursor.fetchall()
    conn.close()
    return render_template("resultados.html", prestadores=prestadores)

@app.route('/salvar_prestador', methods=['POST'])
def salvar_prestador():
    # Coleta os dados do seu formulário original
    dados = (request.form.get('nome'), request.form.get('email'), request.form.get('senha'),
             request.form.get('contato'), request.form.get('profissao'), 
             request.form.get('bairro'), request.form.get('raio'), request.form.get('bio'))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO prestadores (nome,email,senha,contato,profissao,bairro,raio,bio) VALUES (?,?,?,?,?,?,?,?)', dados)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/tobias', methods=['POST'])
def chat_tobias():
    dados = request.get_json()
    pergunta = dados.get('mensagem')
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Você é o Tobias, assistente do site Conecta. Responda curto: {pergunta}"
    response = model.generate_content(prompt)
    return jsonify({"resposta": response.text})

if __name__ == '__main__':
    app.run(debug=True)