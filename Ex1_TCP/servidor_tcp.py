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
    """
    Função principal para configurar e rodar o servidor TCP.
    """
    # Cria o socket TCP/IP (AF_INET para IPv4, SOCK_STREAM para TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Permite reutilizar o endereço local rapidamente
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Vincula o socket ao endereço e porta
        sock.bind((HOST, PORT))
        
        # Começa a escutar por conexões
        sock.listen()
        
        print(f"Servidor TCP escutando em {HOST}:{PORT}...")
        
        # Aceita a conexão do cliente
        conn, addr = sock.accept()
        
        with conn:
            print(f"Conectado por {addr}")
            
            while True:
                data = conn.recv(1024) # Recebe até 1024 bytes
                
                # Validação de mensagem vazia (cliente desconectou)
                if not data:
                    print(f"Cliente {addr} desconectou.")
                    break
                
                msg_recebida = data.decode('utf-8')
                print(f"Recebido de {addr}: {msg_recebida}")
                
                # Responde com a confirmação
                conn.sendall(b"Mensagem recebida")

if __name__ == "__main__":
    main()