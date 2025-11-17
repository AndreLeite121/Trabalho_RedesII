"""
Trabalho 2 – Redes de Computadores II
Disciplina: Redes II
Professor: Alessandro Vivas Andrade
Autores: Lavínia Charrua, André Leite, Iasmin Torres
Exercício: 4 – Cliente de Hora (TCP)
Descrição: Cliente simples que conecta ao servidor de hora,
           solicita (implicitamente, ao conectar) 
           e exibe a hora recebida no console.
Data: 2025-11-13
"""

import socket

HOST = '127.0.0.1'  # Endereço do servidor
PORT = 7000         # Porta do servidor

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            
            data = sock.recv(1024)
            
            if data:
                print(f"Hora atual (Servidor): {data.decode('utf-8')}")
            else:
                print("Servidor não enviou dados.")
                
    except ConnectionRefusedError:
        print(f"Erro: Conexão recusada em {HOST}:{PORT}. Servidor offline?")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()