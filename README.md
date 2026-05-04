cat << 'EOF' > README.md
# Comuniq 🚀 | Conectando a Comunidade

![Status](https://img.shields.io/badge/status-Beta-yellow.svg)
![Tecnologia](https://img.shields.io/badge/stack-Vanilla%20JS-orange.svg)
![IA](https://img.shields.io/badge/IA-Gemini%20%26%20Claude-blue.svg)

O **Comuniq** é uma plataforma comunitária voltada para moradores de periferias de São Paulo. O projeto facilita a conexão entre quem precisa de um serviço e prestadores locais, democratizando a divulgação de profissionais autônomos por meio de tecnologia acessível.[cite: 1, 4]

---

## 🔗 Atalhos do Projeto

*   📂 **[Abrir Plataforma (HTML)](./comuniq.html)** - Versão executável do sistema.[cite: 3, 5]
*   📑 **[Memorial de Construção](./Memorial-de%20Construção.pdf)** - Problemas resolvidos e visão do produto.[cite: 1]
*   ⚙️ **[Engenharia de Prompts](./Comuniq_Prompts.pdf)** - Detalhamento técnico das IAs (Tobias).[cite: 2]
*   📘 **[Documentação Completa](./Comuniq_Documentacao_Completa.pdf)** - Guia técnico e funcional.[cite: 3]

---

## 📋 Funcionalidades Principais

*   **Busca Inteligente (Tobias IA):** Interpreta o que você precisa e encontra o profissional certo.[cite: 3]
*   **Contato Direto:** Integração com a API do WhatsApp para negociações.[cite: 3]
*   **Selo Verificado:** Identificação para prestadores com CNPJ.[cite: 1, 3]
*   **Sistema de Alertas:** Notificações de novos serviços no seu bairro.[cite: 1]
*   **Moderação por IA:** Avaliações filtradas para manter um ambiente respeitoso.[cite: 2, 3]

---

## 🤖 Ecossistema de IA (Tobias)

| Funcionalidade | Modelo | Função |
| :--- | :--- | :--- |
| **Chat Tobias** | Gemini Flash | Atendimento geral e acolhedor.[cite: 2] |
| **Busca IA** | Claude Haiku | Classificação de categorias e filtros.[cite: 2] |
| **Moderação** | Gemini Flash | Bloqueio de ofensas em feedbacks.[cite: 2] |
| **Gerador de Perfil** | Gemini Flash | Criação de descrições profissionais.[cite: 2] |

---

## 🛠️ Tecnologias

*   **Linguagens:** HTML5, CSS3 (Mobile-first) e JavaScript Vanilla.[cite: 3, 5]
*   **Armazenamento:** `localStorage` (Persistência local no navegador).[cite: 3]
*   **Modelos:** Google Gemini API e Anthropic Claude API.[cite: 2]

---

## 🎓 Créditos Acadêmicos

Este projeto foi desenvolvido para a disciplina de **Engenharia de Prompt e Aplicações em IA** da **UNICID** (2026).[cite: 1, 2, 3]

---
*Desenvolvido para fortalecer a economia local. 💙*
EOF

echo "✅ README.md com links gerado com sucesso!"
