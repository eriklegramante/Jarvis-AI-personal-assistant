# 🤖 Atlas - AI Personal Assistant

Projeto de desenvolvimento de um assistente virtual inteligente baseado em **Agentes de IA** e **Workflows Agentic**, focado em automação de tarefas, integração com o sistema operacional e busca de informações em tempo real.

## 📂 Estrutura do Projeto

A arquitetura modular do sistema está organizada da seguinte forma:

* **`agents/`**: Lógica de orquestração de múltiplos agentes.
* **`brain/`**: Gerenciamento de memória de longo prazo e bancos de dados vetoriais (RAG).
* **`config/`**: Configurações globais e definições de parâmetros do sistema.
* **`docs/`**: Documentação técnica, diagramas de fluxo e manuais.
* **`logs/`**: Registros de performance, erros e histórico de requisições.
* **`speech/`**: Módulos de processamento de voz (STT/TTS).
* **`tools/`**: Habilidades do Jarvis (System e Web Tools).
* **`main.py`**: Ponto de entrada e loop principal de execução.
* **`memory_store.db`**: Banco de dados para persistência de informações.

## 🚀 Tecnologias Principais

* **Core:** Gemini 3 Flash Preview (Google Generative AI).
* **Orquestração:** LangChain (LCEL) e AgentExecutor.
* **Linguagem:** Python 3.12+.
* **Ambiente:** Ubuntu/Windows.

## 🛠️ Roadmap de Desenvolvimento

Acompanhamento do progresso das funcionalidades:

- [x] **Fase 1: Core & Setup**
    - [x] Estrutura modular de pastas.
    - [x] Integração com Gemini 3 Flash.
    - [x] Sistema de logs e monitoramento de performance.
- [x] **Fase 2: System Capabilities**
    - [x] Ferramentas de Data/Hora.
    - [x] Verificação de status do sistema e usuários.
- [ ] **Fase 3: Web & Knowledge** (Em progresso)
    - [x] Integração com DuckDuckGo Search.
    - [ ] Ferramenta de leitura de documentação web.
- [ ] **Fase 4: Memory & Persistence**
    - [ ] Implementação de SQLite/ChromaDB na pasta `/brain`.
    - [ ] Memória contextual entre sessões.
- [ ] **Fase 5: Speech Interface**
    - [ ] Integração Whisper (STT).
    - [ ] Integração ElevenLabs ou Edge-TTS (TTS).

---

## ⚙️ Como Executar

1.  **Configurar Ambiente:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz e adicione:
    ```env
    API_KEY_GEMINI=seu_token_aqui
    DEBUG_MODE=False
    ```

3.  **Iniciar o Jarvis:**
    ```bash
    python main.py
    ```

---
Doutrina de Operação: *"Sempre use as ferramentas disponíveis para fornecer informações precisas."*