from flask import Flask, render_template, request, redirect, url_for
import sqlite3

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
    conn.commit()git remote remove origin
    conn.close()

# Rota Principal: Carrega a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota de Cadastro: Recebe os dados do formulário e salva no banco
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    servico = request.form.get('servico')
    local = request.form.get('local')
    bio = request.form.get('bio')

    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO prestadores (nome, servico, local, bio) VALUES (?, ?, ?, ?)', 
                   (nome, servico, local, bio))
    conn.commit()
    conn.close()
    
    # Após cadastrar, redireciona de volta para a página inicial
    return redirect(url_for('index'))

# Rota de Busca: Procura profissionais no banco de dados
@app.route('/buscar')
def buscar():
    profissao = request.args.get('profissao', '')
    
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()
    # Usa o comando SQL LIKE para encontrar serviços semelhantes ao digitado
    cursor.execute("SELECT nome, servico, local, bio FROM prestadores WHERE servico LIKE ?", 
                   ('%' + profissao + '%',))
    resultados = cursor.fetchall()
    conn.close()

    # Organiza os dados para o Flask enviar ao HTML
    lista_profissionais = []
    for r in resultados:
        lista_profissionais.append({
            'nome': r[0],
            'servico': r[1],
            'local': r[2],
            'bio': r[3]
        })

    return render_template('index.html', resultados=lista_profissionais)

if __name__ == '__main__':
    init_db() # Cria o banco de dados assim que o programa inicia
    app.run(debug=True)