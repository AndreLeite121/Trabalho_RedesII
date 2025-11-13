"""
Trabalho 2 – Redes de Computadores II
Disciplina: Redes II
Professor: Alessandro Vivas Andrade
Autores: Lavínia Charrua, André Leite, Iasmin Torres
Exercício: 2 – Servidor Echo (UDP)
Descrição: Servidor que utiliza UDP para receber mensagens 
           (de até 64KB) de clientes e enviá-las 
           de volta (eco).
Data: 2025-11-13
"""

import socket

HOST = '0.0.0.0'  # Escuta em todas as interfaces
PORT = 6000       # Porta especificada no exercício
BUFFER_SIZE = 65535 # Tamanho máximo de um datagrama UDP (aprox. 64KB)

def main():
    """
    Função principal para configurar e rodar o servidor Echo UDP.
    """
    # Cria o socket UDP (AF_INET para IPv4, SOCK_DGRAM para UDP)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f"Servidor UDP Echo escutando em {HOST}:{PORT}...")
        
        while True:
            try:
                # Recebe dados E o endereço do remetente
                data, addr = sock.recvfrom(BUFFER_SIZE)
                
                msg_recebida = data.decode('utf-8')
                print(f"Mensagem recebida de {addr}: {msg_recebida}")
                
                # Envia a mesma mensagem de volta (eco)
                sock.sendto(data, addr)
                print(f"Eco enviado para {addr}")

            except Exception as e:
                print(f"Erro ao processar datagrama: {e}")

if __name__ == "__main__":
    main()