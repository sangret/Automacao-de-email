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

def download_emails(email_usuário, senha_usuario, pasta_anexos):
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(email_usuário, senha_usuario)
        imap.select("inbox")
        status, mensagens = imap.search(None, "UNSEEN")
        ids_email = mensagens[0].split()
        for id_email in ids_email:
            resultado, dados_email = imap.fetch(id_email, "(RFC822)")
            for resposta in dados_email:
                if isinstance(resposta, tuple):
                    mensagem = email.message_from_bytes(resposta[1])
                    assunto, codificacao = decode_header(mensagem["Subject"])[0]
                    if isinstance(assunto, bytes):
                        assunto = assunto.decode(codificacao or 'utf-8')
                    print(f"Baixando o e-mail: {assunto}")
                    baixar_anexos(imap, id_email, pasta_anexos)
        imap.logout()
        print("Download concluido")
    except Exception as e:
        print(f"Erro: {e}")

def criar_interface():
    psg.theme('reddit')

    layout = [
        [psg.Text('E-mail'), psg.Input(key='email')],
        [psg.Text('Senha do app'), psg.Input(key='senha', password_char='*')],
        [psg.Text('Pasta para salvar anexos'), psg.FolderBrowse(target='input_anexos'), psg.Input(key='input_anexos')],
        [psg.Button('Iniciar Download')]
    ]

    janela = psg.Window('Automação de Download de E-mails', layout)

    while True:
        event, values = janela.read()

        if event == psg.WIN_CLOSED:
            break
        if event == 'Iniciar Download':
            email_usuario = values['email']
            senha_usuario = values['senha']
            pasta_anexos = values['input_anexos']
            if email_usuario and senha_usuario and pasta_anexos:
                download_emails(email_usuario, senha_usuario, pasta_anexos)
            else:
                psg.popup("Preencha todos os campos!")

    janela.close()

# Iniciar a interface gráfica
criar_interface()