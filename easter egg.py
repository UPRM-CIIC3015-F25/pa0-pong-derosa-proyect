import pygame
from sys import exit
import os
from PIL import Image  # <<-- Pillow para limpiar PNGs

# --- FUNCIÓN: limpiar PNGs problemáticos ---
def limpiar_pngs(carpeta):
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(".png"):
            ruta = os.path.join(carpeta, archivo)
            try:
                img = Image.open(ruta)
                img = img.convert("RGBA")  # asegurar formato válido
                img.save(ruta, "PNG")      # vuelve a guardar limpio
                print(f"[OK] Limpieza: {archivo}")
            except Exception as e:
                print(f"[ERROR] No se pudo limpiar {archivo}: {e}")

# Limpia todas las imágenes en la carpeta fotos antes de iniciar
limpiar_pngs("fotos")

# --- INICIO DEL JUEGO ---
pygame.init()
pantalla = pygame.display.set_mode((1500, 920))
pygame.display.set_caption("Easter Egg")
reloj = pygame.time.Clock()

# Carga imágenes
fondo = pygame.image.load("fotos/game_background_2.png").convert()
piso = pygame.Surface((1500, 200))
piso.fill((139, 69, 19))  # color marrón para el piso

enemigo_img = pygame.image.load('fotos/Wraith_01_Moving Forward_000_fixed.png').convert_alpha()
jefe_img = pygame.transform.scale(
    enemigo_img,
    (enemigo_img.get_width()*2, enemigo_img.get_height()*2)
)

personaje_img = pygame.image.load('fotos/Wraith_02_Moving Forward_000_fixed.png').convert_alpha()

# Variables jugador
jugador_rect = personaje_img.get_rect(midbottom=(100, 820))
vel_y = 0
gravedad = 1
en_suelo = True

# Variables enemigo
enemigos = []
fase = 1
puntaje = 0

# Crear enemigos fase 1
for i in range(5):
    enemigo_rect = enemigo_img.get_rect(midbottom=(800 + i*150, 820))
    enemigos.append({"rect": enemigo_rect, "vel": -5, "es_jefe": False})

def crear_jefe():
    jefe_rect = jefe_img.get_rect(midbottom=(1400, 820))
    enemigos.append({"rect": jefe_rect, "vel": -3, "es_jefe": True})

font = pygame.font.SysFont(None, 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and en_suelo:
                vel_y = -20
                en_suelo = False

    # Aplicar gravedad
    vel_y += gravedad
    jugador_rect.y += vel_y
    if jugador_rect.bottom >= 820:
        jugador_rect.bottom = 820
        vel_y = 0
        en_suelo = True

    # Mover enemigos y detectar colisiones
    for enemigo in enemigos[:]:
        enemigo["rect"].x += enemigo["vel"]

        if enemigo["rect"].right < 0:
            enemigo["rect"].left = 1500

        if jugador_rect.colliderect(enemigo["rect"]):
            if vel_y > 0 and jugador_rect.bottom <= enemigo["rect"].top + 25:
                enemigos.remove(enemigo)
                puntaje += 1
                vel_y = -15  # rebote
           # else:
                #print("¡Perdiste!")
               # pygame.quit()
                #exit()

    if fase == 1 and len(enemigos) == 0:
        fase = 2
        crear_jefe()

    # Dibujar todo
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(piso, (0, 720))

    for enemigo in enemigos:
        if enemigo["es_jefe"]:
            pantalla.blit(jefe_img, enemigo["rect"])
        else:
            pantalla.blit(enemigo_img, enemigo["rect"])

    pantalla.blit(personaje_img, jugador_rect)

    puntaje_surf = font.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    fase_surf = font.render(f"Fase: {fase}", True, (255, 255, 255))
    pantalla.blit(puntaje_surf, (20, 20))
    pantalla.blit(fase_surf, (20, 60))

    pygame.display.update()
    reloj.tick(60)
