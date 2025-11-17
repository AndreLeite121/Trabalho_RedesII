"""
Trabalho 2 – Redes de Computadores II
Disciplina: Redes II
Professor: Alessandro Vivas Andrade
Autores: Lavínia Charrua, André Leite, Iasmin Torres
Exercício: 1 – Servidor TCP
Descrição: Servidor que aceita conexões TCP, recebe mensagens 
           do cliente, imprime no console e envia uma 
           confirmação.
Data: 2025-11-13
"""

import socket

HOST = '0.0.0.0'  # Escuta em todas as interfaces
PORT = 5000       # Porta especificada no exercício

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        sock.bind((HOST, PORT))
        
        sock.listen()
        
        print(f"Servidor TCP escutando em {HOST}:{PORT}...")
        
        conn, addr = sock.accept()
        
        with conn:
            print(f"Conectado por {addr}")
            
            while True:
                data = conn.recv(1024) # Recebe até 1024 bytes
                
                if not data:
                    print(f"Cliente {addr} desconectou.")
                    break
                
                msg_recebida = data.decode('utf-8')
                print(f"Recebido de {addr}: {msg_recebida}")
                
                conn.sendall(b"Mensagem recebida")

if __name__ == "__main__":
    main()