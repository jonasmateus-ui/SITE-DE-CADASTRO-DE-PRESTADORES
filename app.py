from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Configuração e Criação do Banco de Dados SQLite
def init_db():
    conn = sqlite3.connect('dados.db')
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

# CHAMADA CRUCIAL: Inicializa o banco sempre que o app carregar
init_db()

@app.route('/')
def index():
    # Agora a página inicial também precisa buscar os dados para exibir
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome, servico, local, bio FROM prestadores')
    todos = cursor.fetchall()
    conn.close()
    
    # Converte para dicionário para facilitar no HTML
    lista_profissionais = [{'nome': r[0], 'servico': r[1], 'local': r[2], 'bio': r[3]} for r in todos]
    return render_template('index.html', resultados=lista_profissionais)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    servico = request.form.get('servico')
    local = request.form.get('local')
    bio = request.form.get('bio')

    # Validação simples para evitar erro de dados vazios
    if not nome or not servico:
        return redirect(url_for('index'))

    try:
        conn = sqlite3.connect('dados.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO prestadores (nome, servico, local, bio) VALUES (?, ?, ?, ?)', 
                       (nome, servico, local, bio))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro no Banco: {e}")
        return "Erro interno ao salvar", 500
        
    return redirect(url_for('index'))

@app.route('/buscar')
def buscar():
    profissao = request.args.get('profissao', '')
    
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, servico, local, bio FROM prestadores WHERE servico LIKE ?", 
                   ('%' + profissao + '%',))
    resultados = cursor.fetchall()
    conn.close()

    lista_profissionais = [{'nome': r[0], 'servico': r[1], 'local': r[2], 'bio': r[3]} for r in resultados]
    return render_template('index.html', resultados=lista_profissionais)

if __name__ == '__main__':
    app.run(debug=True)