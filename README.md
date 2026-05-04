
# Comuniq 🚀 | Conectando a Comunidade

![Status](https://img.shields.io/badge/status-Beta-yellow.svg)
![Tecnologia](https://img.shields.io/badge/stack-Vanilla%20JS-orange.svg)
![IA](https://img.shields.io/badge/IA-Gemini%20%26%20Claude-blue.svg)

O **Comuniq** é uma plataforma comunitária desenhada para moradores de periferias de São Paulo. O projeto facilita a ligação entre quem precisa de um serviço e prestadores locais, democratizando a divulgação de profissionais autônomos através de tecnologia acessível e inteligência artificial.

---

## 🔗 Acesso aos Ficheiros e Documentação

Navega pelos documentos oficiais do projeto localizados na pasta `/documentacao`:

* 🌐 **[Executar Plataforma (HTML)](./comuniq.html)** - Ficheiro principal da aplicação.
* 📑 **[Memorial de Construção](./documentacao/Memorial-de%20Construção.pdf)** - Conceito, problema e visão do produto.
* ⚙️ **[Engenharia de Prompts](./documentacao/Comuniq_Prompts.pdf)** - Detalhamento técnico das IAs (Tobias).
* 📘 **[Documentação Completa](./documentacao/Comuniq_Documentacao_Completa.pdf)** - Guia técnico, funcional e evidências.
* 🖼️ **[Diagrama do Ecossistema](./documentacao/diagrama-ecossistema.jpeg)** - Estrutura visual do sistema.

---

## 📋 Funcionalidades Principais

* **Busca Inteligente (Tobias IA):** Interpreta necessidades em linguagem natural (ex: "tenho um cano partido") e encontra o profissional certo.
* **Contacto Direto:** Integração nativa com a API do WhatsApp para negociações sem intermediários.
* **Selo Verificado:** Identificação visual para prestadores que inserem CNPJ, aumentando a confiança.
* **Sistema de Alertas:** Notificações baseadas em categorias e bairros de interesse.
* **Moderação por IA:** Avaliações filtradas automaticamente para manter o respeito na comunidade.

---

## 🤖 Ecossistema de IA (Tobias)

O sistema utiliza múltiplos modelos para garantir eficiência e baixo custo:

| Funcionalidade | Modelo | Papel no Sistema |
| :--- | :--- | :--- |
| **Chat Tobias** | Gemini Flash | Atendimento geral, dúvidas e suporte. |
| **Busca IA** | Claude Haiku | Classificação de categorias e mapeamento de intenção. |
| **Moderação** | Gemini Flash | Filtro de linguagem ofensiva em feedbacks. |
| **Gerador de Perfil** | Gemini Flash | Escrita automática de descrições profissionais. |

---

## 🛠️ Detalhes Técnicos

* **Arquitetura:**
