'''
programa principal
'''

import meg_pt as meg

# Nome personalizado
meg.meg_talk('Olá. Sou Meg e estou aqui para lhe ajudar. Qual é o seu nome?')
listen_name = meg.meg_listen()
meg.meg_talk('Olá ' + listen_name + ' como eu posso te ajudar?')

while True:
    listen_meg = meg.meg_listen()
    print(listen_meg)
    meg.meg_reply(listen_meg)

    # Encerrar a execução
    if 'parar'in listen_meg or 'sair' in listen_meg or 'pare' in listen_meg or 'encerrar' in listen_meg:
        break
