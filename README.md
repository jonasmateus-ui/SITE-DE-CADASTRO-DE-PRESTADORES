
# Comuniq 🚀 | Conectando a Comunidade

![Status](https://img.shields.io/badge/status-Beta-yellow.svg)
![Tecnologia](https://img.shields.io/badge/stack-Vanilla%20JS-orange.svg)
![IA](https://img.shields.io/badge/IA-Gemini%20%26%20Claude-blue.svg)

O **Comuniq** é uma plataforma comunitária voltada para moradores de periferias de São Paulo. O projeto visa facilitar a conexão entre quem precisa de um serviço (pedreiros, eletricistas, cabeleireiros, etc.) e prestadores de serviços locais, eliminando a dependência exclusiva do "boca a boca" e democratizando a divulgação de autônomos.

---

## 📋 Funcionalidades Principais

* **Cadastro Simplificado:** Prestadores se cadastram sem necessidade de senhas, gerando um ID único (ex: CQ-00001).
* **Busca Inteligente (Tobias IA):** Sistema que interpreta a necessidade do usuário (ex: "estou com vazamento") para sugerir profissionais compatíveis.
* **Contato Direto:** Integração via API do WhatsApp, garantindo negociação direta entre cliente e prestador.
* **Verificação:** Selo de "Verificado" para profissionais que fornecem CNPJ.
* **Sistema de Alertas:** Notificações via WhatsApp baseadas em categorias e bairros de interesse.
* **Avaliação Segura:** Sistema de estrelas com moderação automática de conteúdo via IA para evitar ofensas.

---

## 🤖 Ecossistema de IA (Tobias)

O Comuniq utiliza uma camada de inteligência artificial otimizada para diferentes tarefas:

| Funcionalidade | Modelo | Função |
| :--- | :--- | :--- |
| **Chat Tobias** | Gemini Flash | Atendimento geral, tom informal e acolhedor. |
| **Busca IA** | Claude Haiku | Traduz linguagem natural para filtros de busca. |
| **Moderação** | Gemini Flash | Filtra avaliações para evitar discursos de ódio. |
| **Descrição** | Gemini Flash | Auxilia prestadores a escreverem seus perfis. |

---

## 🛠️ Tecnologias e Arquitetura

O projeto foi construído com foco em acessibilidade e rapidez:

* **Frontend:** HTML5, CSS3 (Mobile-first) e JavaScript Vanilla.
* **Armazenamento:** `localStorage` (Persistência no navegador do usuário).
* **Integrações:** API do WhatsApp, Anthropic API (Claude), Google Gemini API.

> **Nota sobre Dados:** Por ser uma versão Beta, os dados são armazenados localmente no dispositivo (LocalStorage). Não há banco de dados centralizado nesta versão, portanto, a troca de aparelho resetará as configurações locais.

---

## 🚀 Como Rodar

Este projeto é *client-side only*. Você não precisa de servidores complexos ou banco de dados para testar.

1.  Clone o repositório ou baixe os arquivos.
2.  Abra o arquivo `comuniq.html` em qualquer navegador moderno.
3.  Utilize as ferramentas de busca ou cadastro diretamente na interface.

---

## 📝 Documentação Complementar
Este projeto foi desenvolvido como entrega final para a disciplina de **Engenharia de Prompt e Aplicações em IA** da **UNICID (2026)**. 

Mais detalhes podem ser consultados nos arquivos entregues:
* `Memorial-de Construção.pdf` (Concepção e problemas resolvidos)
* `Comuniq_Prompts.pdf` (Detalhamento técnico da engenharia de prompts)
* `Comuniq_Documentacao_Completa.pdf` (Visão geral do projeto)

---
*Desenvolvido com carinho para a comunidade paulistana. 💙*
EOF

echo "✅ README.md gerado com sucesso!"
