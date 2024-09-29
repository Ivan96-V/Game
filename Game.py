import random
import pygame
import math
from pygame import mixer


# Inicializador del juego
pygame.init()


# crear pantalla
pantalla = pygame.display.set_mode((1800,1000))


# Titulo e Icono
pygame.display.set_caption('Invasion Chavista')
icono = pygame.image.load('Maria_Corina.jpg')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Asamblea_nacional_fondo.jpg')

# agregar sonido
mixer.music.load('Sonido_fondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Variable del Jugador
img_jugador = pygame.image.load('Maria_Corina_protagonista_editado.png')
jugador_x = 800
jugador_y = 820
jugador_x_mov = 0
jugador_y_mov = 0

# Variable del Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_mov = []
enemigo_y_mov = []
cantidad_enemigo = 6

for e in range(cantidad_enemigo):
    img_enemigo.append(pygame.image.load('maduro_enemigo_editado.png'))
    enemigo_x.append(random.randint(0, 1616))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_mov.append(0.3)
    enemigo_y_mov.append(60)

# Variable Balas
img_balas = pygame.image.load('actas.png')
balas_x = 0
balas_y = 800
balas_x_mov = 0
balas_y_mov = 3
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# tecxto final de juego
fuente_final = pygame.font.Font('freesansbold.ttf', 100)

def texto_final():
    mi_fuente_final = fuente_final.render(f'HASTA EL FINAL!',True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (500, 500))

# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Chavistas presos: {puntaje}', True, (255,255,255))
    pantalla.blit(texto, (x, y))


# Funcion Jugador
def jugador(x, y):
    pantalla.blit(img_jugador,(jugador_x, jugador_y))


# Funcion Enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene],(x, y))

# Funcion Bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_balas, (x + 110, y + -80))

# Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 52:
        return True
    else:
        return False


# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # imagen fondo
    pantalla.blit(fondo, (0, 0))

    # Salida de pantalla del jugador
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:

            # Movimiento del jugador
            if evento.key == pygame.K_LEFT:
                jugador_x_mov = -2
            if evento.key == pygame.K_RIGHT:
                jugador_x_mov = 2

            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('actas_maria_corina.mp3')
                sonido_bala.play()
                sonido_bala.set_volume(0.05)
                if not bala_visible:
                    balas_x = jugador_x
                    disparar_bala(balas_x, balas_y)

        # Evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_mov = 0
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                jugador_y_mov = 0

    # Modificar ubicacion del jugador
    jugador_x += jugador_x_mov

    # Mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 1616:
        jugador_x = 1616

    # Modificar ubicacion del enemigo
    for e in range(cantidad_enemigo):

        # fin del juego
        if enemigo_y[e] > 650:
            for k in range(cantidad_enemigo):
                enemigo_y[k] = 1200
            texto_final()
            break

        enemigo_x[e] += enemigo_x_mov[e]

    # Mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_mov[e] = 1
            enemigo_y[e] += enemigo_y_mov[e]
        elif enemigo_x[e] >= 1640:
            enemigo_x_mov[e] = -1
            enemigo_y[e] += enemigo_y_mov[e]

        # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], balas_x, balas_y)
        if colision:
            sonido_colision = mixer.Sound('fascistas.mp3')
            sonido_colision.set_volume(0.1)
            sonido_colision.play()
            balas_y = 800
            bala_visible = False
            puntaje += 1
            print(puntaje)
            enemigo_x[e] = random.randint(0, 1616)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    if balas_y <= -40:
        balas_y = 850
        bala_visible = False

    if bala_visible:
        disparar_bala(balas_x, balas_y)
        balas_y -= balas_y_mov

    jugador(jugador_x,jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    # Actualizacion
    pygame.display.update()
