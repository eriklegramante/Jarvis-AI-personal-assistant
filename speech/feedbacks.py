import asyncio
from edge_tts import Communicate

async def generate_fixed_audio(text, filename):
    voice = "pt-BR-FranciscaNeural" 
    communicate = Communicate(text, voice)
    await communicate.save(filename)
    print(f"Arquivo {filename} gerado com sucesso!")

async def main():
    await generate_fixed_audio("uh, sim?", "speech/sounds/uh_sim?.mp3")
    await generate_fixed_audio("cheguei, o que precisa?", "speech/sounds/cheguei.mp3")
    await generate_fixed_audio("Acordei, o que precisa?", "speech/sounds/acordei.mp3")

if __name__ == "__main__":
    asyncio.run(main())

#Apeans rodar esse modulo para gerar os arquivos de áudio de feedback. Ele usa a voz "AntonioNeural" do Azure TTS, mas você pode escolher outra voz brasileira se preferir. Os arquivos serão salvos na pasta "speech/sounds/" com os nomes especificados.