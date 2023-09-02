'''
  1- Crie uma versão do jogo da velha 4x4. As regras são as mesmas da versão 3x3.

  A estratégia para esse exercício foi utilizar um loop while na função principal iniciar_jogo()
  que só vai ser interrompido quando for levantada uma exception de fim de jogo durante 
  as verificações de vitória e velha. 
  Na jogada, o usuário insere uma coordenada em forma de tupla para jogar. 
'''

class FimDeJogoException(BaseException):
  pass

jogadores = ['X', 'O']
tabuleiro = [[' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ']]
ultima_jogada = (-1, -1)

def iniciar_jogo():
  '''Função principal do jogo que contém o laço de repetição de turnos, e chama cada uma das etapas do turno'''
  print(colorido("*JOGO DA VELHA*", cores['HEADER']))

  printar_tabuleiro()
  while True:
    try:
      pedir_jogada()
      verificar_fim_de_jogo()
      passar_vez()
    except FimDeJogoException:
      break


def printar_tabuleiro():
  '''Imprime o tabuleiro atual formatado'''
  for i, linha in enumerate(tabuleiro):
    for j, el in enumerate(linha):
      print(f" {colorido(el, cores[el])} ", end="")
      if (not e_ultimo_elemento(j, linha)):
        print(f"|", end="")
    if (not e_ultimo_elemento(i, tabuleiro)):
      printar_divisoria()
  print("\n")

def e_ultimo_elemento(index, lista):
  '''Verifica se o elemento é o último da lista'''
  return index == (len(lista) - 1)

def printar_divisoria():
  '''Imprime a divisória com o tamanho adequado para o tabuleiro'''
  divisoria = '-' * (4 * len(tabuleiro))
  print(f"\n{divisoria[:-1]}")


def pedir_jogada(): 
  '''Etapa 1: Inicia uma jogada do usuário'''
  print(f"Vez do {colorido(jogadores[0], cores[jogadores[0]])}!")
  receber_coordenada()

def receber_coordenada():
  '''Recebe input de coordenada do usuário até que receba uma válida no formato x,y, e insere a jogada no tabuleiro.
  
  É tida como válida quando está no formato correto, somente números, que esteja dentro do range do tabuleiro e não esteja preenchida. 
  '''
  while True:
    try:
      coordenada = tuple(map((lambda pos : int(pos)), input("Insira a casa para jogar. ex. x,y ").split(',')))
      if (len(coordenada) != 2):
        raise ValueError
      
      if ((coordenada[0] or coordenada[1]) > (len(tabuleiro) - 1)):
        print(f"Essa casa não existe. Escolha uma entre 0 e {len(tabuleiro) - 1}")
        continue
      
      if (tabuleiro[coordenada[0]][coordenada[1]] != ' '):
        print("Essa casa está ocupada... Escolha outra.")
        continue
      
      global ultima_jogada
      ultima_jogada = coordenada
      tabuleiro[coordenada[0]][coordenada[1]] = jogadores[0]
      printar_tabuleiro()
      break
    except ValueError as e:
      print("Insira uma casa válida com somente números no formato x,y")  


def verificar_fim_de_jogo():
  '''Etapa 2: Executa verificações de fim de jogo (vitória ou velha)
  
  Verifica somente as seções pertinentes à jogada do usuário
  '''
  verificar_linha(ultima_jogada[0])
  verificar_coluna(ultima_jogada[1])
  if (coordenada_esta_em_diagonal_principal(ultima_jogada)):
    verificar_diagonal_principal()

  if (coordenada_esta_em_diagonal_secundaria(ultima_jogada)):
    verificar_diagonal_secundaria()

  verificar_velha()

def verificar_linha(i_linha):
  '''Verifica se o jogador completou a linha em sua jogada'''
  if (verificar_se_completou_secao(tabuleiro[i_linha])):
    jogador_ganhou()

def verificar_coluna(i_col):
  '''Verifica se o jogador completou a coluna em sua jogada'''
  if (verificar_se_completou_secao([ linha[i_col] for linha in tabuleiro ])):
    jogador_ganhou()

def coordenada_esta_em_diagonal_principal(coordenada):
  '''Verifica se a jogada foi na diagonal principal'''
  return coordenada[0] == coordenada[1]

def verificar_diagonal_principal():
  '''Verifica se o jogador completou a diagonal principal em sua jogada'''
  if (verificar_se_completou_secao([ tabuleiro[i][i] for i in range(0, len(tabuleiro)) ])):
    jogador_ganhou()

def coordenada_esta_em_diagonal_secundaria(coordenada):
  '''Verifica se a jogada foi na diagonal secundária'''
  return coordenada[0] + coordenada[1] == len(tabuleiro) - 1

def verificar_diagonal_secundaria():
  '''Verifica se o jogador completou a diagonal secundária em sua jogada'''
  if (verificar_se_completou_secao([ tabuleiro[i][len(tabuleiro) - i - 1] for i in range(len(tabuleiro)) ])):
    jogador_ganhou()

def verificar_velha():
  '''Verifica se o tabuleiro foi completado, e, portanto, deu velha'''
  if(all([casa in jogadores for linha in tabuleiro for casa in linha])):
    print("Deu velha :(")
    raise FimDeJogoException

def verificar_se_completou_secao(secao):
  '''Função auxiliar para verificar se o jogador completou determinada seção.
  
  Tome como "seção" qualquer sentido que se possa ganhar o jogo (linha, coluna ou diagonais principal e secundária).
  '''
  return all([ casa == jogadores[0] for casa in secao ])

def jogador_ganhou():
  '''Função auxiliar para determinar vitória do jogador e encerrar o jogo.'''
  print(colorido(f'{jogadores[0]} ganhou!!', cores[jogadores[0]]) + " Parabéns!!!")
  raise FimDeJogoException


def passar_vez():
  '''Etapa 3: Passa a vez para o próximo jogador.'''
  jogadores.append(jogadores.pop(0))


cores = {
  'HEADER': '\033[45m',
  'O': '\033[94m',
  'X': '\033[91m',
  ' ': '',
  'RESET': '\033[0m'
}

def colorido(texto, cor):
  '''Retorna um texto colorido com a cor escolhida.'''
  return f"{cor}{texto}{cores['RESET']}"

iniciar_jogo()