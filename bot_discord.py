import discord
import os
from dotenv import load_dotenv

load_dotenv()

# Intents para permitir acceso a contenido de mensajes
intents = discord.Intents.default()
intents.message_content = True

# Instancia del cliente
client = discord.Client(intents=intents)

api_key = os.getenv('DISCORD_KEY')

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

    # Reemplaza con el ID de tu canal
    canal_id = 1135148074919022763
    canal = client.get_channel(canal_id)

    print(f'Extrayendo mensajes del canal: {canal.name}')

    mensajes = []
    async for mensaje in canal.history(limit=1000):
        mensajes.append({
            "autor": str(mensaje.author),
            "contenido": mensaje.content,
            "fecha": mensaje.created_at.isoformat()
        })

    # Guardar los datos en archivo
    import json
    with open("mensajes_discord.json", "w", encoding="utf-8") as f:
        json.dump(mensajes, f, indent=4)

    await client.close()

# Token de tu bot
client.run(api_key)
