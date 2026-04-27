# Conecta Comunidade 🤝

## Como rodar

### 1. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 2. (Opcional) Ativar o Tobias com IA real
Abra o `app.py` e cole sua chave do Gemini na linha indicada:
```python
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "SUA_CHAVE_AQUI")
```
Ou defina como variável de ambiente no terminal:
```bash
# Windows
set GEMINI_API_KEY=sua_chave_aqui

# Mac/Linux
export GEMINI_API_KEY=sua_chave_aqui
```
Pegue sua chave gratuita em: https://aistudio.google.com/app/apikey

> Sem a chave, o Tobias funciona em modo offline com respostas automáticas.

### 3. Iniciar o servidor
```bash
python app.py
```

### 4. Acessar no navegador
Abra: http://localhost:5000

---

## Estrutura de arquivos
```
conecta/
├── app.py              ← servidor Flask (backend)
├── requirements.txt    ← dependências Python
├── dados.db            ← banco SQLite (criado automaticamente)
└── templates/
    └── index.html      ← interface do site
```

## API (rotas do servidor)
| Método | Rota               | Descrição                     |
|--------|--------------------|-------------------------------|
| GET    | /                  | Abre o site                   |
| GET    | /api/prestadores   | Lista todos os prestadores    |
| GET    | /api/prestadores?q=| Busca por termo               |
| POST   | /api/prestadores   | Cadastra novo prestador       |
| POST   | /api/tobias        | Envia mensagem pro Tobias     |

## ⚠️ Segurança
- **NÃO compartilhe** o arquivo `credenciais.json` — ele contém chaves privadas do Firebase.
- **NÃO suba** o `dados.db` para repositórios públicos.
- Para produção, use variáveis de ambiente para todas as chaves.
