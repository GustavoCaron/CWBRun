import pygame
from pygame.locals import *
from sys import exit
from random import randrange, choice
from button import Button
from pygame import mixer

pygame.init()
pygame.mixer.init()
LARGURA = 1280
ALTURA = 920
tela = pygame.display.set_mode((LARGURA, ALTURA))
BRANCO = (255, 255, 255)
pygame.display.set_caption('data/CWB RUN')
BG = pygame.image.load('data/BG.png').convert_alpha()
CWB = pygame.image.load('data/cwb.jpg').convert_alpha()
FUNDOMORTE = pygame.image.load('data/fundofernando.png').convert_alpha()
GROUND = pygame.image.load('data/ground.png')

def get_font(size):
    return pygame.font.Font('data/font.ttf', size)

def play():

    tela.fill(BRANCO)
    nuvem_sprite_sheet = pygame.image.load('data/nuvemSpriteSheet.png')
    capivara_sprite_sheet = pygame.image.load('data/capivaraSpritesheet.png')
    player_sprite_sheet = pygame.image.load('data/playerSpritesheet.png').convert_alpha()
    vendedor_sprite_sheet = pygame.image.load('data/vendedorSpritesheet.png')
    som_colisao = pygame.mixer.Sound('data/death_sound.wav')
    som_colisao.set_volume(1)
    som_pontuacao = pygame.mixer.Sound('data//score_sound.wav')
    som_pontuacao.set_volume(1)
    som_fundo = pygame.mixer.Sound('data/fundo_sound.WAV')
    som_fundo.play(-1)
    som_fundo.set_volume(10)
    colidiu = False
    escolha_obstaculo = choice([0, 1])
    pontos = 0
    velocidade_jogo = 10

    #DEFININDO MENU CASO JOGADOR MORRA
    def restart():
        while True:
            tela.blit(FUNDOMORTE, (275, 175))
            RESTART_MOUSE_POS = pygame.mouse.get_pos()

            RESTART_BUTTON = Button(image=pygame.image.load("data/Restart Rect.png"), pos=(650, 480),
                                 text_input="RESTART", font=get_font(45), base_color="#ffffff", hovering_color="Green")

            QUIT_BUTTON = Button(image=pygame.image.load("data/Quit Rect 2.png"), pos=(650, 590),
                                 text_input="SAIR", font=get_font(45), base_color="#ffffff", hovering_color="Red")

            for button in [RESTART_BUTTON, QUIT_BUTTON]:
                button.changeColor(RESTART_MOUSE_POS)
                button.update(tela)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESTART_BUTTON.checkForInput(RESTART_MOUSE_POS):
                        play()
                    if QUIT_BUTTON.checkForInput(RESTART_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            som_fundo.stop()

    def exibe_mensagem(pontos,tamanho, cor):
        fonte = pygame.font.SysFont('font.ttf', 70, True, False)
        mensagem = f'{pontos}'
        texto_formatado = fonte.render(mensagem, True, (BRANCO))
        return texto_formatado

    class player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.som_pulo = pygame.mixer.Sound('data/jump_sound.wav')
            self.som_pulo.set_volume(1)
            self.imagens_player = []
            for i in range(4):
                img = player_sprite_sheet.subsurface((i * 32, 0), (32, 32))
                img = pygame.transform.scale(img, (32 * 3, 32 * 3))
                self.imagens_player.append(img)

            self.index_lista = 0
            self.image = self.imagens_player[self.index_lista]
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.pos_y_inicial = ALTURA - 64 - 96 // 2
            self.rect.topleft = (100, self.pos_y_inicial)  # 368   416(centro y)
            self.pulo = False

        def pular(self):
            self.pulo = True
            self.som_pulo.play()
            img = player_sprite_sheet.subsurface((4 * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_player.append(img)


        def update(self):
            if self.pulo == True:
                if self.rect.y <= self.pos_y_inicial - 150:
                    self.pulo = False
                self.rect.y -= 15

            else:
                if self.rect.y >= self.pos_y_inicial:
                    self.rect.y = self.pos_y_inicial
                else:
                    self.rect.y += 15

            if self.index_lista > 3 and self.pulo == False:
                self.index_lista = 0
            elif self.pulo == True:
                self.index_lista = 4
            self.index_lista += 0.25
            self.image = self.imagens_player[int(self.index_lista)]


    class Nuvens(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = nuvem_sprite_sheet.subsurface((0 * 32, 0), (32, 32))
            self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
            self.rect = self.image.get_rect()
            self.rect.y = randrange(150, 200, 50)
            self.rect.x = LARGURA - randrange(30, 300, 90)

        def update(self):
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
                self.rect.y = randrange(50, 200, 50)
            self.rect.x -= velocidade_jogo

    class Chao(pygame.sprite.Sprite):
        def __init__(self, pos_x):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(GROUND, (32 * 2, 32 * 2))
            self.rect = self.image.get_rect()
            self.rect.y = ALTURA - 64
            self.rect.x = pos_x * 64

        def update(self):
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

    class Capivara(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.imagens_capivara = []
            for i in range(4):
                img = capivara_sprite_sheet.subsurface((i * 32, 0), (32, 32))
                img = pygame.transform.scale(img, (32 * 3, 32 * 3))
                self.imagens_capivara.append(img)

            self.index_lista = 0
            self.image = self.imagens_capivara[self.index_lista]
            self.mask = pygame.mask.from_surface(self.image)
            self.escolha = escolha_obstaculo
            self.rect = self.image.get_rect()
            self.rect.center = (LARGURA, ALTURA - 64)
            self.rect.x = LARGURA

        def update(self):
            if self.escolha == 1:
                if self.rect.topright[0] < 0:
                    self.rect.x = LARGURA
                self.rect.x -= velocidade_jogo

                if self.index_lista > 3:
                    self.index_lista = 0
                self.index_lista += 0.25
                self.image = self.imagens_capivara[int(self.index_lista)]

    class VendedorAlfajor(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.imagens_vendedor = []
            for i in range(3):
                imgvendedor = vendedor_sprite_sheet.subsurface((i * 32, 0), (32, 32))
                imgvendedor = pygame.transform.scale(imgvendedor, (32 * 3, 32 * 3))
                self.imagens_vendedor.append(imgvendedor)

            self.index_lista = 1
            self.image = self.imagens_vendedor[self.index_lista]
            self.mask = pygame.mask.from_surface(self.image)
            self.escolha = escolha_obstaculo
            self.rect = self.image.get_rect()
            self.rect.center = (LARGURA, ALTURA - 64)
            self.rect.x = LARGURA

        def update(self):
            if self.escolha == 0:
                if self.rect.topright[0] < 0:
                    self.rect.x = LARGURA
                self.rect.x -= velocidade_jogo

                if self.index_lista > 2:
                    self.index_lista = 0
                self.index_lista += 0.25
                self.image = self.imagens_vendedor[int(self.index_lista)]


    todas_as_sprites = pygame.sprite.Group()
    player = player()
    todas_as_sprites.add(player)

    for i in range(4):
        nuvem = Nuvens()
        todas_as_sprites.add(nuvem)

    for i in range(LARGURA * 2):
        chao = Chao(i)
        todas_as_sprites.add(chao)

    capivara = Capivara()
    todas_as_sprites.add(capivara)

    vendedoralfajor = VendedorAlfajor()
    todas_as_sprites.add(vendedoralfajor)

    grupo_obstaculos = pygame.sprite.Group()
    grupo_obstaculos.add(capivara)
    grupo_obstaculos.add(vendedoralfajor)
    relogio = pygame.time.Clock()

    while True:
        relogio.tick(30)
        tela.blit(CWB, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE and colidiu == False:
                    if player.rect.y != player.pos_y_inicial:
                        pass
                    else:
                        player.pular()

        colisoes = pygame.sprite.spritecollide(player, grupo_obstaculos, False, pygame.sprite.collide_mask)
        todas_as_sprites.draw(tela)
        pygame.display.update()

        if capivara.rect.topright[0] <= 0 or vendedoralfajor.rect.topright[0] <= 0:
            escolha_obstaculo = choice([0, 1])
            capivara.rect.x = LARGURA
            vendedoralfajor.rect.x = LARGURA
            capivara.escolha = escolha_obstaculo
            vendedoralfajor.escolha = escolha_obstaculo

        if colisoes and colidiu == False:
            som_colisao.play()
            colidiu = True

        if colidiu == True:
            if pontos % 100 == 0:
                pontos += 1
            restart()

        else:
            pontos += 1
            todas_as_sprites.update()
            texto_pontos = exibe_mensagem(pontos, 100, (0, 0, 0))

        if pontos % 100 == 0:
            som_pontuacao.play()
            if velocidade_jogo >= 23:
                velocidade_jogo += 0
            else:
                velocidade_jogo += 1

        tela.blit(texto_pontos, (1020, 30))
        pygame.display.flip()

def main_menu():
    while True:
        tela.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("data/Play Rect.png"), pos=(950, 550),
                             text_input="JOGAR", font=get_font(50), base_color="#ffffff", hovering_color="Green")

        QUIT_BUTTON = Button(image=pygame.image.load("data/Quit Rect.png"), pos=(950, 700),
                             text_input="SAIR", font=get_font(50), base_color="#ffffff", hovering_color="Red")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(tela)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
main_menu()