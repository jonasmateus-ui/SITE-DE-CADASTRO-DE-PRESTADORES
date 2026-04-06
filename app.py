from flask import Flask, render_template, request, redirect, jsonify, session
import sqlite3
import os
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "conecta-segredo-2025")

genai.configure(api_key=os.getenv("API_KEY"))

DB = "dados.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS prestadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        profissao TEXT NOT NULL,
        bairro TEXT NOT NULL,
        contato TEXT,
        bio TEXT,
        email TEXT,
        senha TEXT,
        raio INTEGER DEFAULT 10
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS contratacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        prestador TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ─── PÁGINAS ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html', user=session.get('user'))

@app.route('/login')
def login():
    if 'user' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/cadastro_cliente')
def cadastro_cliente():
    return render_template('cadastro_cliente.html')

@app.route('/cadastro_prestador')
def cadastro_prestador():
    return render_template('cadastro_prestador.html')

# ─── AUTENTICAÇÃO ─────────────────────────────────────────────────────────────

@app.route('/login_validar', methods=['POST'])
def login_validar():
    email = request.form.get('email', '').strip()
    senha = request.form.get('senha', '')

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM clientes WHERE email=? AND senha=?", (email, senha)
    ).fetchone()
    conn.close()

    if user:
        session['user'] = email
        session['nome'] = user['nome']
        return redirect('/')

    return render_template('login.html', erro="E-mail ou senha incorretos.")

@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():
    nome  = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    senha = request.form.get('senha', '')

    if not (nome and email and senha):
        return render_template('cadastro_cliente.html', erro="Preencha todos os campos.")

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO clientes (nome,email,senha) VALUES (?,?,?)",
            (nome, email, senha)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return render_template('cadastro_cliente.html', erro="E-mail já cadastrado.")
    conn.close()
    return redirect('/login')

@app.route('/salvar_prestador', methods=['POST'])
def salvar_prestador():
    campos = ['nome', 'profissao', 'bairro', 'contato', 'email', 'senha', 'bio', 'raio']
    dados = {c: request.form.get(c, '').strip() for c in campos}

    conn = get_db()
    conn.execute(
        """INSERT INTO prestadores (nome,profissao,bairro,contato,email,senha,bio,raio)
           VALUES (:nome,:profissao,:bairro,:contato,:email,:senha,:bio,:raio)""",
        dados
    )
    conn.commit()
    conn.close()
    return redirect('/')

# ─── BUSCA ────────────────────────────────────────────────────────────────────

@app.route('/pesquisar')
def pesquisar():
    busca = request.args.get('busca', '').strip()
    if not busca:
        return redirect('/')

    conn = get_db()
    prestadores = conn.execute(
        """SELECT * FROM prestadores
           WHERE nome LIKE ? OR profissao LIKE ? OR bairro LIKE ?""",
        (f'%{busca}%',) * 3
    ).fetchall()
    conn.close()

    return render_template('resultados.html', prestadores=prestadores, busca=busca)

# ─── CONTRATAÇÃO ──────────────────────────────────────────────────────────────

@app.route('/contratar/<int:prestador_id>')
def contratar(prestador_id):
    if 'user' not in session:
        return redirect('/login')

    conn = get_db()
    prestador = conn.execute(
        "SELECT nome FROM prestadores WHERE id=?", (prestador_id,)
    ).fetchone()

    if prestador:
        conn.execute(
            "INSERT INTO contratacoes (cliente,prestador) VALUES (?,?)",
            (session['user'], prestador['nome'])
        )
        conn.commit()

    conn.close()
    return jsonify({"ok": True, "mensagem": f"Contratação de {prestador['nome']} realizada!"})

# ─── TOBIAS (IA) ──────────────────────────────────────────────────────────────

@app.route('/tobias', methods=['POST'])
def tobias():
    data = request.get_json()
    msg  = data.get('mensagem', '').strip()

    if not msg:
        return jsonify({"resposta": "Pode falar! Como posso ajudar?"})

    conn = get_db()
    todos = conn.execute("SELECT nome, profissao, bairro, contato FROM prestadores").fetchall()
    conn.close()

    if todos:
        lista_txt = "\n".join(
            f"- {r['nome']} | {r['profissao']} | Bairro: {r['bairro']} | Contato: {r['contato']}"
            for r in todos
        )
    else:
        lista_txt = "(nenhum prestador cadastrado ainda)"

    system_prompt = f"""Você é o Tobias, assistente virtual simpático da plataforma Conecta Comunidade.
Seu trabalho é ajudar usuários a encontrar prestadores de serviço locais.

PRESTADORES CADASTRADOS NA PLATAFORMA:
{lista_txt}

REGRAS:
- Se o usuário perguntar sobre algum serviço ou profissão, filtre a lista acima e apresente os profissionais relevantes de forma amigável.
- Se nenhum prestador for encontrado para o serviço pedido, diga isso e sugira outras formas de ajudar.
- Se a pergunta for geral (saudação, dúvida sobre a plataforma), responda de forma útil e simpática.
- Sempre responda em português brasileiro, de forma breve e objetiva.
- Não invente prestadores que não estão na lista acima.
"""

    try:
        model = genai.GenerativeModel('gemini-pro')
        r = model.generate_content(
            [{"role": "user", "parts": [system_prompt + "\n\nUsuário: " + msg]}]
        )
        resposta = r.text
    except Exception as e:
        resposta = f"Ops, tive um problema técnico. Tente buscar diretamente na barra de pesquisa! (erro: {e})"

    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)