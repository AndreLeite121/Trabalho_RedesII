"""
Trabalho 2 – Redes de Computadores II
Disciplina: Redes II
Professor: Alessandro Vivas Andrade
Autores: Lavínia Charrua, André Leite, Iasmin Torres
Exercício: 3 – Servidor de Chat (TCP)
Descrição: Aceita conexões de dois clientes e retransmite
           mensagens entre eles em tempo real usando threads.
Data: 2025-11-13
"""

import socket
import threading

HOST = '0.0.0.0'
PORT = 5001
clientes = [] # Lista para manter os sockets dos clientes

def handle_client(conn_origem, addr_origem, conn_destino):
    print(f"[CHAT] Cliente {addr_origem} conectado.")
    try:
        while True:
            data = conn_origem.recv(1024)
            if not data or data.decode('utf-8').lower() == 'sair':
                print(f"[CHAT] Cliente {addr_origem} desconectou.")
                break
            
            if conn_destino:
                try:
                    conn_destino.sendall(data)
                except socket.error:
                    print(f"[CHAT] Erro ao enviar para o outro cliente.")
                    break
            
    except ConnectionResetError:
        print(f"[CHAT] Conexão com {addr_origem} perdida.")
    finally:
        conn_origem.close()
        if conn_destino:
            conn_destino.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(2) # Escuta para até 2 conexões
        
        print(f"Servidor de Chat TCP escutando em {HOST}:{PORT}...")
        
        # Aceita o primeiro cliente
        conn1, addr1 = sock.accept()
        print("Cliente 1 (A) conectado. Aguardando Cliente 2 (B)...")

        # Aceita o segundo cliente
        conn2, addr2 = sock.accept()
        print("Cliente 2 (B) conectado. O chat pode começar.")

        # Inicia a thread A -> B
        thread1 = threading.Thread(target=handle_client, 
                                 args=(conn1, addr1, conn2), 
                                 daemon=True)
        
        # Inicia a thread B -> A
        thread2 = threading.Thread(target=handle_client, 
                                 args=(conn2, addr2, conn1), 
                                 daemon=True)
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        print("Chat encerrado.")
            
if __name__ == "__main__":
    main()