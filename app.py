from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import os

# ─────────────────────────────────────────────────────────────
#  CONFIGURAÇÃO DO TOBIAS (IA com Gemini)
#
#  Cole sua chave do Google AI Studio abaixo.
#  Acesse: https://aistudio.google.com/app/apikey
#
#  DUAS formas de configurar:
#    1) Variável de ambiente (recomendado para produção):
#       No terminal: export GEMINI_API_KEY="sua_chave_aqui"
#    2) Diretamente no código (somente para testes locais):
#       Substitua "" por "sua_chave_aqui" na linha abaixo.
# ─────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBQbI2tl15wUq7rEALxGe0RXNGCelUeWF8")  # <-- cole sua chave aqui se quiser

# Tenta importar o Gemini. Se a chave não estiver configurada,
# o Tobias funciona em modo offline (sem IA).
GEMINI_OK = False
try:
    import google.generativeai as genai
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_OK = True
except ImportError:
    pass

app = Flask(__name__)
CORS(app)

DB = "dados.db"

# ─── BANCO DE DADOS ───────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prestadores (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT NOT NULL,
            profissao TEXT NOT NULL,
            bairro    TEXT NOT NULL,
            descricao TEXT,
            telefone  TEXT,
            email     TEXT
        )
    """)
    # Dados de exemplo (só insere se a tabela estiver vazia)
    count = conn.execute("SELECT COUNT(*) FROM prestadores").fetchone()[0]
    if count == 0:
        exemplos = [
            ("Carlos Rodrigues", "Eletricista",  "Centro",         "Instalações elétricas residenciais e comerciais. 10 anos de experiência.", "(11) 98765-4321", ""),
            ("Marcia Souza",     "Faxineira",    "Jardim América", "Limpeza residencial e comercial. Diarista ou semanal.", "(11) 91234-5678", "marcia.faxina@gmail.com"),
            ("José Pereira",     "Pedreiro",     "Vila Nova",      "Reformas, construção, reboco, azulejo e contrapiso.", "(11) 97654-3210", ""),
            ("Ana Lima",         "Cozinheira",   "Centro",         "Marmitas fitness e caseiras. Encomendas para festas e eventos.", "(11) 99887-6655", "ana.marmitas@hotmail.com"),
            ("Roberto Nunes",    "Pintor",       "Jardim América", "Pintura interna e externa, textura e verniz.", "(11) 95544-3322", ""),
            ("Paulo Mendes",     "Encanador",    "Centro",         "Conserto de vazamentos, instalação de torneiras e registros.", "(11) 98811-2233", ""),
            ("Fernanda Costa",   "Costureira",   "Bela Vista",     "Consertos, ajustes e confecção sob medida.", "(11) 94433-2211", "fe.costura@gmail.com"),
            ("Tânia Oliveira",   "Diarista",     "Vila Nova",      "Limpeza geral, organização e passa roupa. Segunda a sábado.", "(11) 96677-8899", ""),
        ]
        conn.executemany(
            "INSERT INTO prestadores (nome,profissao,bairro,descricao,telefone,email) VALUES (?,?,?,?,?,?)",
            exemplos
        )
    conn.commit()
    conn.close()

init_db()

# ─── ROTAS ───────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/prestadores")
def listar_prestadores():
    """Retorna todos os prestadores, com filtro opcional por ?q=termo"""
    q = request.args.get("q", "").strip().lower()
    conn = get_conn()
    if q:
        rows = conn.execute(
            """SELECT * FROM prestadores
               WHERE lower(nome) LIKE ?
                  OR lower(profissao) LIKE ?
                  OR lower(bairro) LIKE ?
                  OR lower(descricao) LIKE ?""",
            [f"%{q}%"] * 4
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM prestadores ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/prestadores", methods=["POST"])
def cadastrar_prestador():
    """Cadastra um novo prestador"""
    d = request.json
    campos = ["nome", "profissao", "bairro", "descricao", "telefone"]
    for c in campos:
        if not d.get(c, "").strip():
            return jsonify({"erro": f"Campo '{c}' é obrigatório."}), 400

    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO prestadores (nome,profissao,bairro,descricao,telefone,email) VALUES (?,?,?,?,?,?)",
        (d["nome"], d["profissao"], d["bairro"], d["descricao"], d["telefone"], d.get("email", ""))
    )
    conn.commit()
    novo_id = cur.lastrowid
    row = conn.execute("SELECT * FROM prestadores WHERE id=?", (novo_id,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201

@app.route("/api/tobias", methods=["POST"])
def tobias():
    """Endpoint do assistente Tobias"""
    mensagem = request.json.get("mensagem", "").strip()
    if not mensagem:
        return jsonify({"resposta": "Pode falar, estou aqui! 😊"})

    # Busca prestadores para contexto
    conn = get_conn()
    rows = conn.execute("SELECT * FROM prestadores").fetchall()
    conn.close()
    lista = "\n".join(
        f"- {r['nome']}: {r['profissao']} | Bairro: {r['bairro']} | Tel: {r['telefone']}"
        + (f" | Email: {r['email']}" if r['email'] else "")
        for r in rows
    )

    # Modo com Gemini (IA real)
    if GEMINI_OK:
        prompt = f"""Você é Tobias, assistente simpático do site "Conecta Comunidade".
O site conecta clientes a prestadores de serviço locais.

LISTA DE PRESTADORES DISPONÍVEIS:
{lista}

REGRAS:
- Ajude o usuário a encontrar profissionais na lista acima
- Responda de forma simples e acolhedora (público de periferia)
- Liste nome, profissão, bairro e telefone dos profissionais relevantes
- Se não houver nenhum, diga claramente e sugira buscar em outra categoria
- Nunca invente prestadores que não estão na lista
- Seja breve (máximo 4 linhas)
- Responda sempre em português do Brasil

Pergunta do usuário: {mensagem}"""
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            resposta = model.generate_content(prompt)
            return jsonify({"resposta": resposta.text, "modo": "ia"})
        except Exception as e:
            pass  # cai para o modo offline abaixo

    # Modo offline — lógica baseada em regras
    resposta = tobias_offline(mensagem, rows)
    return jsonify({"resposta": resposta, "modo": "offline"})


def tobias_offline(mensagem, rows):
    """Tobias funcionando sem IA — busca por palavras-chave"""
    msg = mensagem.lower()

    # Saudações
    saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "tudo bem", "tudo bom"]
    if any(s in msg for s in saudacoes):
        return "Olá! 😊 Me diga que tipo de profissional você precisa e em qual bairro que eu te ajudo a encontrar!"

    # Busca no banco por palavras da mensagem
    encontrados = []
    for r in rows:
        campos = f"{r['profissao']} {r['bairro']} {r['nome']} {r['descricao'] or ''}".lower()
        palavras = [p for p in msg.split() if len(p) > 2]
        if any(p in campos for p in palavras):
            encontrados.append(r)

    if not encontrados:
        return (
            "Não encontrei nenhum profissional com esse termo. 🔍\n"
            "Tente falar o tipo de serviço (ex: eletricista, pedreiro, faxina) "
            "ou o nome do bairro!"
        )

    if len(encontrados) == 1:
        r = encontrados[0]
        contato = f"📱 {r['telefone']}" if r['telefone'] else f"✉️ {r['email']}"
        return (
            f"Encontrei 1 profissional para você! ✅\n\n"
            f"👤 {r['nome']} — {r['profissao']}\n"
            f"📍 {r['bairro']}\n"
            f"{contato}"
        )

    linhas = [f"Encontrei {len(encontrados)} profissionais! ✅\n"]
    for r in encontrados[:4]:
        contato = r['telefone'] or r['email'] or "—"
        linhas.append(f"• {r['nome']} ({r['profissao']}, {r['bairro']}) — {contato}")
    if len(encontrados) > 4:
        linhas.append(f"...e mais {len(encontrados)-4}. Use a busca para ver todos!")
    return "\n".join(linhas)


if __name__ == "__main__":
    print("\n✅ Conecta Comunidade rodando em: http://localhost:5000\n")
    if not GEMINI_OK:
        print("⚠️  Tobias em modo OFFLINE (sem chave Gemini). Para ativar a IA,")
        print("   defina GEMINI_API_KEY no topo do app.py ou como variável de ambiente.\n")
    app.run(debug=True)