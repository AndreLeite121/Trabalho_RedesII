"""
Trabalho 2 – Redes de Computadores II
Disciplina: Redes II
Professor: Alessandro Vivas Andrade
Autores: Lavínia Charrua, André Leite, Iasmin Torres
Exercício: 4 – Servidor de Hora (TCP com Threads)
Descrição: Servidor multithread que atende múltiplos clientes, 
           envia a hora atual (HH:MM:SS) e registra 
           logs em 'servidor_hora.log'.
Data: 2025-11-13
"""

import socket
import threading
import logging
from datetime import datetime

HOST = '0.0.0.0'
PORT = 7000       # Porta especificada no exercício

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("servidor_hora.log"), # Log em arquivo
        logging.StreamHandler()                    # Log no console
    ]
)

def handle_client(conn, addr):

    try:
        logging.info(f"Solicitação recebida de {addr}")
        
        # Obtém a hora atual no formato HH:MM:SS
        current_time = datetime.now().strftime("%H:%M:%S")
        
        conn.sendall(current_time.encode('utf-8'))
        
        logging.info(f"Hora enviada ({current_time}) para {addr}")
        
    except Exception as e:
        # Garante que o servidor continue se um cliente falhar
        logging.error(f"Erro ao atender {addr}: {e}")
        
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen()
        
        logging.info(f"Servidor de Hora escutando em {HOST}:{PORT}...")
        
        while True:
            try:
                conn, addr = sock.accept()
                
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr),
                    daemon=True 
                )
                client_thread.start()
                
            except KeyboardInterrupt:
                print("\nServidor encerrando...")
                break
            except Exception as e:
                logging.error(f"Erro ao aceitar conexão: {e}")

if __name__ == "__main__":
    main()