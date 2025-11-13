"""
Trabalho 2 – Redes de Computadores II
Disciplina: Redes II
Professor: Alessandro Vivas Andrade
Autores: Lavínia Charrua, André Leite, Iasmin Torres
Exercício: 3 – Cliente de Chat (TCP)
Descrição: Conecta ao servidor de chat e usa threads separadas
           para enviar (input) e receber (recv) mensagens 
           simultaneamente.
Data: 2025-11-13
"""

import socket
import threading
import sys

# Flag global para sinalizar o encerramento
chat_ativo = True

def receive_messages(sock):
    """
    Thread para receber mensagens do servidor e exibi-las.
    """
    global chat_ativo
    while chat_ativo:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[Servidor encerrou a conexão.]")
                chat_ativo = False
                break
            
            # Limpa a linha atual e imprime a msg recebida
            sys.stdout.write('\r' + ' ' * 20 + '\r') 
            print(f"Outro: {data.decode('utf-8')}")
            sys.stdout.write('Você: ') # Reescreve o prompt
            sys.stdout.flush()
            
        except Exception:
            if chat_ativo:
                print("\n[Erro ao receber. Conexão perdida.]")
            chat_ativo = False
            break

def send_messages(sock):
    """
    Função (na thread principal) para enviar mensagens.
    """
    global chat_ativo
    while chat_ativo:
        try:
            message = input('Você: ')
            
            if not chat_ativo: # Se a thread de recepção caiu
                break
                
            sock.sendall(message.encode('utf-8'))
            
            if message.lower() == 'sair': # Comando de saída
                print("Encerrando...")
                chat_ativo = False
                break
                
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando...")
            chat_ativo = False
            break
        except Exception:
            print("\n[Erro ao enviar. Conexão perdida.]")
            chat_ativo = False
            break
    sock.close()


def main():
    HOST = input("Digite o IP do servidor (ex: 127.0.0.1): ")
    PORT = 5001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
            print("Conectado ao servidor. Digite 'sair' para encerrar.")
        except Exception as e:
            print(f"Não foi possível conectar ao servidor: {e}")
            return

        # Cria e inicia a thread de recebimento
        recv_thread = threading.Thread(target=receive_messages, 
                                       args=(sock,), 
                                       daemon=True)
        recv_thread.start()
        
        # Usa a thread principal para enviar mensagens
        send_messages(sock)
        print("Desconectado.")

if __name__ == "__main__":
    main()