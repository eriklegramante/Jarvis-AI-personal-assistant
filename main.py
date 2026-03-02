import os
import time
import threading
import asyncio
from dotenv import load_dotenv
import re
import pygame
import random

#langchain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

#modules imports
from tools import get_all_jarvis_tools
from speech.speaker import JarvisSpeaker
from logs.logger import setup_logger
from ui.avatar import JarvisAvatar
from speech.listener import JarvisListener


load_dotenv()
logger = setup_logger()

pygame.init()
pygame.mixer.init()

avatar = JarvisAvatar("ui/assets")

listener = JarvisListener(model_size="tiny")
tools_do_jarvis = get_all_jarvis_tools(username="Root")

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.3,
    google_api_key=os.getenv("API_KEY_GEMINI")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é o Jarvis, um assistente de IA britânico e sofisticado. "
               "Sempre use as ferramentas para validar dados de sistema ou buscar na web."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

try:
    agent = create_tool_calling_agent(llm, tools_do_jarvis, prompt)
    debug_status = os.getenv("DEBUG_MODE", "False") == "True"
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools_do_jarvis, 
        verbose=debug_status, 
        handle_parsing_errors=True
    )
    logger.info(">>> Sistemas inicializados com sucesso, senhor.")
except Exception as e:
    logger.error(f"Erro crítico na inicialização: {e}")

def clean_text_for_speech(text):
    """Garante que o texto seja uma string e remove Markdown."""
    text = str(text) 
    text = text.replace("*", "").replace("#", "").replace("`", "")
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def play_voice_background(text):
    """Controla a animação de fala simultânea ao áudio."""
    try:
        avatar.set_talking(True)
        speaker = JarvisSpeaker()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(speaker.speak(text))
        loop.close()
    except Exception as e:
        logger.error(f"Erro no áudio/avatar: {e}")
    finally:
        avatar.set_talking(False)

def play_random_feedback():
    sounds = ["acordei.mp3", "aoba.mp3", "cheguei.mp3","diga.mp3", "pode_falar.mp3"]
    chosen = random.choice(sounds)
    sound = pygame.mixer.Sound(f"speech/sounds/{chosen}")
    ch = sound.play()
    return ch

async def main_loop():
    historico = []
    gatilhos = ["jarvis", "ok jarvis", "olá jarvis", "hey jarvis"]
    print("\n>>> Jarvis Online. Aguardando comandos, senhor.")

    while True:
        try:
            while avatar.is_talking:
                await asyncio.sleep(0.05)

            entrada_bruta = await asyncio.to_thread(listener.listen)

            if not entrada_bruta or len(entrada_bruta.strip()) < 2:
                continue

            entrada_lower = entrada_bruta.lower()

            if any(g in entrada_lower for g in gatilhos):
                avatar.current_state = "listening"

                duration = play_random_feedback()
                await asyncio.sleep(duration)

                await asyncio.sleep(duration + 0.1)
                await asyncio.to_thread(listener.reset_noise, 0.3)

                pergunta = await asyncio.to_thread(listener.listen)
                print(">>> TRANSCRICAO PERGUNTA:", repr(pergunta))
                if not pergunta.strip():
                    continue

                pergunta = await asyncio.to_thread(listener.listen)
                if not pergunta or len(pergunta.strip()) < 2:
                    print("[Standby] Nenhuma pergunta detectada após o wake word.")
                    continue

                comando_limpo = pergunta.strip()
                print(f"PROCESSANDO: {comando_limpo}")

                resultado = agent_executor.invoke({
                    "input": comando_limpo,
                    "chat_history": historico
                })

                resposta = resultado.get("output", "")
                if isinstance(resposta, list) and resposta:
                    resposta = resposta[0].get("text", str(resposta))

                print(f"\nJARVIS: {resposta}")

                texto_limpo = clean_text_for_speech(resposta)
                threading.Thread(target=play_voice_background, args=(texto_limpo,), daemon=True).start()

                historico.append(("human", comando_limpo))
                historico.append(("ai", resposta))

            else:
                print(f"[Standby] Ouvi: {entrada_bruta}")

        except Exception as e:
            logger.error(f"Falha no ciclo: {e}")
            await asyncio.sleep(1)

def chat_thread():
    asyncio.run(main_loop()) 

if __name__ == "__main__":
    thread_jarvis = threading.Thread(target=chat_thread, daemon=True)
    thread_jarvis.start()

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        try:
            avatar.draw()
        except Exception as e:
            pass
            
        clock.tick(30) 

    pygame.quit()