import pygame
from sys import exit
import random

pygame.init()
pantalla = pygame.display.set_mode((1500, 920))
pygame.display.set_caption("Mario 2D")
reloj = pygame.time.Clock()

# --- Cargar imágenes y reducir tamaño ---
# Reducir jugador a 50% de tamaño original
personaje_img = pygame.image.load('fotos/princi.png').convert_alpha()
ancho_nuevo = personaje_img.get_width() // 2
alto_nuevo = personaje_img.get_height() // 2
personaje_img = pygame.transform.scale(personaje_img, (ancho_nuevo, alto_nuevo))

# Reducir enemigo a 50% de tamaño original
enemigo_img = pygame.image.load('fotos/Wraith_01_Moving Forward_000_fixed.png').convert_alpha()
ancho_nuevo_enemigo = enemigo_img.get_width() // 2
alto_nuevo_enemigo = enemigo_img.get_height() // 2
enemigo_img = pygame.transform.scale(enemigo_img, (ancho_nuevo_enemigo, alto_nuevo_enemigo))

# Piso
piso_altura = 870
piso = pygame.Surface((1500, 200))
piso.fill((139, 69, 19))
fondo=pygame.image.load("fotos/game_background_2.png")
# Meta
meta_rect = pygame.Rect(1400, piso_altura - 400, 50, 100)
meta_img = pygame.Surface((50, 100))
meta_img.fill((255, 255, 0))
meta= pygame.image.load("fotos/gafufo.png")

# Jugador
jugador_rect = personaje_img.get_rect(midbottom=(100, piso_altura))
jugador_hitbox = jugador_rect.inflate(-30, -40)  # hitbox proporcional al sprite reducido

vel_y = 0
gravedad = 1
en_suelo = True
vel_x = 0
speed = 7

# Enemigos
enemigos = []
puntaje = 0

def crear_enemigos():
    enemigos.clear()
    for i in range(3):
        x_pos = 600 + i * random.randint(300, 400)  # dispersión aleatoria
        rect_original = enemigo_img.get_rect(midbottom=(x_pos, piso_altura))
        hitbox = rect_original.inflate(-25, -25)  # hitbox proporcional
        enemigos.append({"rect": rect_original, "hitbox": hitbox, "vel": -2})

font = pygame.font.SysFont(None, 60)
estado_juego = "inicio"

def mostrar_pantalla_inicio():
    pantalla.fill((0, 0, 0))
    texto = font.render("Presiona ENTER para comenzar", True, (255, 255, 255))
    pantalla.blit(texto, (450, 400))
    pygame.display.update()

def mostrar_pantalla_fin(victoria):
    pantalla.fill((0, 0, 0))
    mensaje = "¡Has recuperado a tu gato!" if victoria else "¡Tu gato a sido perdido para siempre!"
    texto = font.render(mensaje, True, (255, 255, 255))
    pantalla.blit(texto, (450, 400))
    texto2 = font.render("Presiona R para reiniciar", True, (255, 255, 255))
    pantalla.blit(texto2, (500, 500))
    pygame.display.update()

# --- Loop principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if estado_juego == "inicio":
        mostrar_pantalla_inicio()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            crear_enemigos()
            tiempo_inicio = pygame.time.get_ticks()
            estado_juego = "jugando"
            jugador_rect.midbottom = (100, piso_altura)
            jugador_hitbox = jugador_rect.inflate(-30, -40)
            puntaje = 0
            vel_y = 0
            vel_x = 0

    elif estado_juego == "fin":
        mostrar_pantalla_fin(victoria)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            estado_juego = "inicio"

    elif estado_juego == "jugando":
        # Controles jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vel_x = -speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vel_x = speed
        else:
            vel_x = 0

        if keys[pygame.K_SPACE] and en_suelo:
            vel_y = -20
            en_suelo = False

        # Movimiento jugador
        vel_y += gravedad
        jugador_rect.y += vel_y
        jugador_rect.x += vel_x

        # Actualizar hitbox jugador
        jugador_hitbox.width = jugador_rect.width - 30
        jugador_hitbox.height = jugador_rect.height - 40
        jugador_hitbox.x = jugador_rect.x + 15
        jugador_hitbox.y = jugador_rect.y + 20

        if jugador_rect.bottom >= piso_altura:
            jugador_rect.bottom = piso_altura
            jugador_hitbox.bottom = piso_altura
            vel_y = 0
            en_suelo = True

        # Limitar dentro de pantalla
        jugador_rect.clamp_ip(pantalla.get_rect())
        jugador_hitbox.clamp_ip(pantalla.get_rect())

        # Inmortal
        tiempo_actual = pygame.time.get_ticks()
        invulnerable = tiempo_actual - tiempo_inicio < 1000

        # Mover enemigos y actualizar hitboxes
        enemigos_actualizados = []
        for enemigo in enemigos:
            enemigo["rect"].x += enemigo["vel"]

            # Hitbox más pequeña y centrada
            enemigo["hitbox"].width = enemigo["rect"].width - 25
            enemigo["hitbox"].height = enemigo["rect"].height - 25
            enemigo["hitbox"].x = enemigo["rect"].x + 12
            enemigo["hitbox"].y = enemigo["rect"].y + 12

            if jugador_hitbox.colliderect(enemigo["hitbox"]):
                pisando = vel_y > 0 and jugador_hitbox.bottom <= enemigo["hitbox"].top + 25
                if pisando:
                    puntaje += 1
                    vel_y = -15
                    # enemigo desaparece con hitbox
                elif not invulnerable:
                    estado_juego = "fin"
                    victoria = False
            else:
                enemigos_actualizados.append(enemigo)

        enemigos = enemigos_actualizados

        # Verificar victoria
        if jugador_hitbox.colliderect(meta_rect):
            estado_juego = "fin"
            victoria = True

        # Dibujar todo
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(piso, (0, piso_altura - 50))
        pantalla.blit(meta, meta_rect)

        for enemigo in enemigos:
            pantalla.blit(enemigo_img, enemigo["rect"])


        pantalla.blit(personaje_img, jugador_rect)


        puntaje_surf = font.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
        pantalla.blit(puntaje_surf, (20, 20))

        pygame.display.update()
        reloj.tick(60)
