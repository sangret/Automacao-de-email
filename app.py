import PySimpleGUI as psg

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