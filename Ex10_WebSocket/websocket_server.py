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

# Log para vermos conexões no terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Conjunto (set) para armazenar todos os clientes conectados
CONNECTED_CLIENTS = set()

async def register(websocket):
    """ Adiciona cliente ao conjunto de conexões ativas. """
    CONNECTED_CLIENTS.add(websocket)
    logging.info(f"{websocket.remote_address} conectou. {len(CONNECTED_CLIENTS)} online.")

async def unregister(websocket):
    """ Remove cliente do conjunto. """
    CONNECTED_CLIENTS.remove(websocket)
    logging.info(f"{websocket.remote_address} desconectou. {len(CONNECTED_CLIENTS)} online.")

async def broadcast(message, sender_websocket):
    """ Envia uma mensagem para todos os clientes, exceto o remetente. """
    if CONNECTED_CLIENTS:
        # Prepara a mensagem formatada
        # Usamos o IP:PORTA como identificador
        sender_id = f"[{sender_websocket.remote_address[0]}:{sender_websocket.remote_address[1]}]"
        formatted_message = f"{sender_id}: {message}"
        
        # Cria tarefas de envio para todos os clientes
        tasks = []
        for client in CONNECTED_CLIENTS:
            tasks.append(client.send(formatted_message))
        
        if tasks:
            await asyncio.wait(tasks)

async def chat_handler(websocket, path):
    """
    Gerencia a conexão de cada cliente.
    """
    await register(websocket)
    try:
        # Loop para escutar mensagens deste cliente
        async for message in websocket:
            logging.info(f"Mensagem de {websocket.remote_address}: {message}")
            # Faz o broadcast da mensagem para todos
            await broadcast(message, websocket)
            
    except websockets.exceptions.ConnectionClosed:
        logging.info("Conexão fechada.")
    finally:
        await unregister(websocket)

def main():
    """
    Inicia o servidor WebSocket.
    """
    HOST = '0.0.0.0'
    PORT = 8765 # Porta padrão
    
    start_server = websockets.serve(chat_handler, HOST, PORT)
    
    logging.info(f"Servidor WebSocket escutando em ws://{HOST}:{PORT}...")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrando...")
    finally:
        loop.close()
        logging.info("Servidor desligado.")

if __name__ == "__main__":
    main()