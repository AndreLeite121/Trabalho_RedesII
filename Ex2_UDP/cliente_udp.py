"""
Trabalho 2 – Redes de Computadores II
Disciplina: Redes II
Professor: Alessandro Vivas Andrade
Autores: Lavínia Charrua, André Leite, Iasmin Torres
Exercício: 2 – Cliente Echo (UDP)
Descrição: Cliente UDP que envia mensagens ao servidor e exibe a 
           resposta (eco) recebida. Permite envio contínuo 
           até que 'sair' seja digitado.
Data: 2025-11-13
"""

import socket

HOST = '127.0.0.1'  # Endereço do servidor (localhost)
PORT = 6000         # Porta do servidor
BUFFER_SIZE = 65535 # Tamanho máximo

def main():
    """
    Função principal para conectar e interagir com o servidor UDP.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        print("Cliente UDP pronto. Digite 'sair' para encerrar.")
        
        while True:
            message = input("Mensagem > ")
            
            # Comando de saída manual
            if message.lower() == 'sair':
                break
            
            # Validação de tamanho antes de enviar
            if len(message.encode('utf-8')) > BUFFER_SIZE:
                print(f"Erro: Mensagem excede o limite de {BUFFER_SIZE} bytes.")
                continue

            sock.sendto(message.encode('utf-8'), (HOST, PORT))
            
            # Define um timeout para tratar perda de pacotes
            sock.settimeout(5.0) # Espera 5 segundos
            
            try:
                data, _ = sock.recvfrom(BUFFER_SIZE)
                print(f"Eco recebido: {data.decode('utf-8')}")
                
            except socket.timeout:
                print("Erro: Tempo limite de resposta (servidor offline ou pacote perdido).")
            
    print("Cliente encerrado.")

if __name__ == "__main__":
    main()