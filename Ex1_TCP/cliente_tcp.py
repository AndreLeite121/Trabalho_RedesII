"""
Trabalho 2 – Redes de Computadores II
Disciplina: Redes II
Professor: Alessandro Vivas Andrade
Autores: Lavínia Charrua, André Leite, Iasmin Torres
Exercício: 1 – Cliente TCP
Descrição: Cliente que conecta ao servidor TCP na porta 
           especificada, envia uma mensagem e exibe a 
           resposta de confirmação do servidor.
Data: 2025-11-13
"""

import socket

HOST = '127.0.0.1'  # Endereço do servidor
PORT = 5000         # Porta do servidor

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
            print(f"Conectado ao servidor em {HOST}:{PORT}")
            
            message = input("Digite a mensagem para enviar: ")
            
            if not message:
                print("Mensagem vazia. Encerrando.")
                return

            sock.sendall(message.encode('utf-8'))
            
            data = sock.recv(1024)
            
            print(f"Resposta do servidor: {data.decode('utf-8')}")

        except ConnectionRefusedError:
            print(f"Erro: Conexão recusada. O servidor está on?")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    print("Conexão encerrada.")

if __name__ == "__main__":
    main()