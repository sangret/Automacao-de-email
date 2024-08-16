import imaplib #Biblioteca para acessar e-mails via IMAP
import email #Biblioteca para manipulação de e-mails
from email.header import decode_header  #Função para decodificar cabeçalhos em formatos distintos
import os #Biblioteca de interação com Sistema operacional, para manipular arquivos e diretórios
import PySimpleGUI as psg #Biblioteca GUI para criar uma interface amigável para usuários

def baixar_anexos(imap, id_email, pasta_anexos):
    resultado, dados_email = imap.fetch(id_email, "(RFC822)")
    for parte_resposta in dados_email:
        if isinstance(parte_resposta, tuple):
            mensagem = email.message_from_bytes(parte_resposta[1])
            if mensagem.is_multipart():
                for parte in mensagem.walk():
                    if parte.get_content_maintype() == "multipart":
                        continue
                    if parte.get("Content-Disposition") is None:
                        continue
                    nome_arquivo = parte.get_filename()
                    if nome_arquivo:
                        caminho_arquivo = os.path.join(pasta_anexos, nome_arquivo)
                        with open(caminho_arquivo, "wb") as f:
                            f.write(parte.get_payload(decode=True))
                            print(f"Anexo {nome_arquivo} salvo em {caminho_arquivo}")












psg.theme('reddit')

janela_principal = [
    [psg.Text('E-mail'), psg.Input(key = 'email')],
    [psg.Text('Senha'), psg.Input(key = 'senha', password_char = '*')],
    [psg.FolderBrowse('Escolher pasta anexos',target = 'input_anexos'), psg.Input(key = 'input_anexos')],
    [psg.FolderBrowse('Escolher pasta planilha',target = 'input_planilha'), psg.Input(key = 'input_planilha')],
    [psg.Button('Salvar')]
]

janela = psg.Window('Principal', layout = janela_principal)

while True:
    event, values = janela.read()
    if event == psg.WIN_CLOSED:
        break
    elif event == 'Salvar':
         email = values['email']
         senha = values['senha']
         caminho_anexos = values['input_anexos']
         caminho_planilha = values['input_planilha']