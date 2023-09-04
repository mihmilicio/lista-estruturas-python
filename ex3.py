'''
3- Desenvolver o jogo https://term.ooo/ a partir do arquivo lista_palavras.txt. O jogo deve ser
jogado por meio do terminal, mantendo a lógica do jogo original. Devem aparecer as letras que
já foram descobertas, as letras já tentadas no teclado e assim por diante. Atente-se à
formatação.



'''
import string
import random
from unidecode import unidecode

arquivo = "lista_palavras.txt"

lista_palavras = []
palavra = ''
tentativas = []
max_tentativas = 6

# Utilizando sets para evitar elementos repetidos desnecessariamente
letras_nao_existentes = set()
letras_posicao_errada = set()
letras_acertadas = set()

teclado = 'Q W E R T Y U I O P\n' + ' A S D F G H J K L \n' + '  Z X C V B N M  '

class VitoriaException(BaseException):
  pass

def iniciar_jogo():
  print(colorido("*TERMOOO*", cores['HEADER']))

  sortear_palavra()
  while len(tentativas) < max_tentativas:
    try:
      printar_tentativas()
      printar_teclado()
      palpite = pedir_palpite()
      verificar_palpite(palpite)
    except VitoriaException:
      printar_tentativas()
      print(colorido("Parabéns! Você venceu!!", cores['CERTA']))
      return

  printar_tentativas()
  print(colorido(f"Que pena :( não foi dessa vez... A palavra era {palavra}", cores['ERRADA']))

def ler_arquivo(arq):
    """ Lê arquivo especificado e retorna uma lista com todas as linhas """    
    with open(arq, encoding="UTF-8") as f:
        return [linha.strip() for linha in f] # método strip remove o '\n' do final da linha

def sortear_palavra():
  global lista_palavras
  lista_palavras = [ unidecode(palavra) for palavra in ler_arquivo(arquivo) ]
  print(lista_palavras)
  
  global palavra
  palavra = random.choice(lista_palavras).upper()
  print(palavra)


def printar_tentativas():
  print("\n")
  for i in range(max_tentativas):
    if (len(tentativas) > i):
      printar_letras_coloridas_palpite(tentativas[i])
    else:
      print("  " + ("_ " * len(palavra)))


def printar_letras_coloridas_palpite(palpite: str):
  palavra_processada = palavra
  output = ['-'] * len(palavra)

  # primeiro marca todas as verdes
  for i, (letra_palpite, letra_palavra) in enumerate(zip(palpite, palavra)):
    if letra_palpite == letra_palavra:
      output[i] = colorido(letra_palpite, cores['CERTA'])
      palavra_processada = palavra_processada.replace(letra_palpite, "-", 1)

  # marca os amarelos, de forma compatível com letras duplicadas
  for i, (letra_palpite, letra_palavra) in enumerate(zip(palpite, palavra)):
    if letra_palpite in palavra_processada and output[i] == '-':
      output[i] = colorido(letra_palpite, cores['POSICAO'])
      palavra_processada = palavra_processada.replace(letra_palpite, "-", 1)
  
  for i, slot in enumerate(output):
    if slot == '-':
      output[i] = colorido(palpite[i], cores['ERRADA'])

  print("  " + ' '.join(output))


def printar_teclado():
  print("")
  for char in teclado:
    if char in letras_acertadas:
      print(colorido(char, cores['CERTA']), end='')
    elif char in letras_posicao_errada:
      print(colorido(char, cores['POSICAO']), end='')
    elif char in letras_nao_existentes:
      print(colorido(char, cores['ERRADA']), end='')
    else:
      print(char, end='')
  print("\n")


def pedir_palpite():
  while True:
    palpite = input("Digite seu palpite: ").upper()
    
    if (len(palpite) != len(palavra)):
      print(f"Tente uma palavra de {len(palavra)} letras.")
      continue

    if (any([ c not in string.ascii_uppercase for c in palpite ])):
      print("Insira somente letras simples")
      continue

    if (palpite.lower() not in lista_palavras):
      print("Essa palavra não existe por aqui... Tente novamente")
      continue

    return palpite

def verificar_palpite(palpite: str):
  tentativas.append(palpite)
  if (palpite == palavra):
    raise VitoriaException

  # status das letras para o teclado

  letras_contidas = [ letra for letra in palpite if letra in palavra ]

  # zip() une as duas listas como uma lista de tuplas. x é a letra no palpite e y é a letra na palavra
  letras_acertadas.update([x for x, y in zip(palpite, palavra) if x==y])

  letras_posicao_errada.update([ letra for letra in letras_contidas if letra not in letras_acertadas ])

  letras_nao_existentes.update([ letra for letra in palpite if letra not in letras_contidas  ])


cores = {
  'HEADER': '\033[45m',
  'CERTA': '\033[92m',
  'POSICAO': '\033[33m',
  'ERRADA': '\033[91m',
  ' ': '',
  'RESET': '\033[0m'
}

def colorido(texto, cor):
  '''Retorna um texto colorido com a cor escolhida.'''
  return f"{cor}{texto}{cores['RESET']}"

iniciar_jogo()