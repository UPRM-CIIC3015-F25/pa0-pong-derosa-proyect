import pygame, sys, random, subprocess
import cv2
import time

# Ruta del video
video_path = 'fotos/papotico.mp4'

# Crear objeto de captura
cap = cv2.VideoCapture(video_path)
delay= int(1000/30/0.85)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Video', frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# --- Inicialización ---
pygame.init()
screen_width = 700
screen_height = 500
pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

# --- Colores y fuente ---
bg_color = pygame.Color('grey12')
light_grey = pygame.Color('grey83')
font = pygame.font.SysFont(None, 60)
basic_font = pygame.font.Font('freesansbold.ttf', 32)

#



# --- Variables de juego ---
ball_size = 30
player_width = 250
player_height = 20
ball = pygame.Rect(screen_width / 2 - ball_size/2, screen_height / 2 - ball_size/2, ball_size, ball_size)
player = pygame.Rect(screen_width/2 - player_width/2, screen_height - 30, player_width, player_height)

ball_speed_x = 0
ball_speed_y = 0
player_speed = 0

score = 0
velocidad_aumento = 1.1

start = False
menu_inicio = True

# --- Funciones ---
def mostrar_pantalla_inicio():
    pantalla.fill((0, 0, 0))
    texto = font.render("Presiona ENTER para comenzar", True, (255, 255, 255))
    pantalla.blit(texto, (screen_width/2 - texto.get_width()/2, screen_height/2 - 30))
    pygame.display.update()

def ejecutar_otro_codigo():
    """
    Ejecuta el otro archivo Python cuando se alcance el puntaje deseado.
    """
    pygame.quit()  # cerrar ventana de Pygame
    subprocess.run(["python", "easter egg.py"])  # ejecutar otro código
    sys.exit()  # salir del código actual

def ball_movement():
    global ball_speed_x, ball_speed_y, score, start

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if start and ball_speed_x == 0 and ball_speed_y == 0:
        speed = 7
        ball_speed_x = speed * random.choice((1, -1))
        ball_speed_y = speed * random.choice((1, -1))

    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:
            score += 1
            ball_speed_y *= -velocidad_aumento
            ball_speed_x *= velocidad_aumento
            try:
                Ball_touch_paddle_sfx = pygame.mixer.Sound("Bop_sound.wav")
                Ball_touch_paddle_sfx.play()
            except:
                pass
            limit_speed()

            # ✅ Verificar si se alcanza el puntaje para cambiar de juego
            if score >= 15 :
                ejecutar_otro_codigo()

    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1
    if ball.bottom > screen_height:
        pygame.mixer.music.stop()
        restart()

def player_movement():
    player.x += player_speed
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    global ball_speed_x, ball_speed_y, score
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x, ball_speed_y = 0, 0
    score = 0

def limit_speed():
    global ball_speed_x, ball_speed_y
    max_speed = 25
    if abs(ball_speed_x) > max_speed:
        ball_speed_x = max_speed * (1 if ball_speed_x > 0 else -1)
    if abs(ball_speed_y) > max_speed:
        ball_speed_y = max_speed * (1 if ball_speed_y > 0 else -1)

# --- Loop principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if menu_inicio:
                if event.key == pygame.K_RETURN:
                    menu_inicio = False
                    start = True
            else:
                if event.key == pygame.K_LEFT:
                    player_speed -= 10
                if event.key == pygame.K_RIGHT:
                    player_speed += 10
                if event.key == pygame.K_SPACE:
                    start = True
        if event.type == pygame.KEYUP and not menu_inicio:
            if event.key == pygame.K_LEFT:
                player_speed += 10
            if event.key == pygame.K_RIGHT:
                player_speed -= 10

    if menu_inicio:
        mostrar_pantalla_inicio()
        continue

    if start and not pygame.mixer_music.get_busy():
        try:
            pygame.mixer.music.load("Megalovania.wav")
            pygame.mixer.music.play()
        except:
            pass

    ball_movement()
    player_movement()

    colores = ["Red", "Blue", "Yellow", "Green"]
    ball_color = pygame.Color(random.choice(colores))

    pantalla.fill(bg_color)
    pygame.draw.rect(pantalla, light_grey, player)
    pygame.draw.ellipse(pantalla, ball_color, ball)
    player_text = basic_font.render(f'{score}', False, light_grey)
    pantalla.blit(player_text, (screen_width/2 - 15, 10))

    pygame.display.flip()
    clock.tick(60)
