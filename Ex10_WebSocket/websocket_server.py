"""
Trabalho 2 – Redes de Computadores II
Disciplina: Redes II
Professor: Alessandro Vivas Andrade
Autores: Lavínia Charrua, André Leite, Iasmin Torres
Exercício: 10 – Servidor de Chat (WebSockets)
Descrição: Servidor de chat usando a biblioteca 'websockets'
           que faz broadcast de mensagens para todos 
           os clientes conectados.
Data: 2025-11-13
"""

import asyncio
import websockets
import logging

# Log conexões no terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

CONNECTED_CLIENTS = set()

async def register(websocket):
    CONNECTED_CLIENTS.add(websocket)
    logging.info(f"{websocket.remote_address} conectou. {len(CONNECTED_CLIENTS)} online.")

async def unregister(websocket):
    CONNECTED_CLIENTS.remove(websocket)
    logging.info(f"{websocket.remote_address} desconectou. {len(CONNECTED_CLIENTS)} online.")

async def broadcast(message, sender_websocket):
    if CONNECTED_CLIENTS:
        sender_id = f"[{sender_websocket.remote_address[0]}:{sender_websocket.remote_address[1]}]"
        formatted_message = f"{sender_id}: {message}"
        
        tasks = []
        for client in CONNECTED_CLIENTS:
            tasks.append(client.send(formatted_message))
        
        if tasks:
            await asyncio.gather(*tasks)

async def chat_handler(websocket):
    await register(websocket)
    try:
        async for message in websocket:
            logging.info(f"Mensagem de {websocket.remote_address}: {message}")
            await broadcast(message, websocket)
            
    except websockets.exceptions.ConnectionClosed:
        logging.info("Conexão fechada.")
    finally:
        await unregister(websocket)


async def main():
    HOST = '0.0.0.0'
    PORT = 8765 # Porta padrão
    
    logging.info(f"Servidor WebSocket escutando em ws://{HOST}:{PORT}...")

    async with websockets.serve(chat_handler, HOST, PORT):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor encerrando...")
        logging.info("Servidor desligado.")