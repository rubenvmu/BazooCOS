# Pantalla
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
FPS = 60

# Jugador
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
PLAYER_JUMP_STRENGTH = 15
GRAVITY = 0.8

# Disparo (bazooka)
ROCKET_SPEED = 12                # Velocidad del proyectil
SHOOT_COOLDOWN = 500             # Tiempo entre disparos (ms)
PROJECTILE_RADIUS = 5

# Escudo
SHIELD_DURATION = 2000           # Duración activa del escudo (ms)
SHIELD_COOLDOWN = 5000           # Tiempo de recarga del escudo (ms)
SHIELD_RADIUS = 50

# Plataformas
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_GAP_Y = 80              # Distancia vertical entre plataformas

# Drones enemigos
DRONE_WIDTH = 40
DRONE_HEIGHT = 40
INITIAL_DRONE_SPAWN_CHANCE = 0.05    # Probabilidad base de aparición de drones
DRONE_SPAWN_INCREMENT = 0.001        # Incremento por cada 100 puntos
DRONE_SPEED_MIN = 1.0
DRONE_SPEED_MAX = 2.5

# Mega Dron
MEGA_DRONE_EVERY_POINTS = 500    # Aparece cada 500 puntos
MEGA_DRONE_HEALTH_MULTIPLIER = 2 # Se multiplica cada vez que aparece

# Power-ups
POWERUP_CHANCE = 0.02            # Probabilidad de aparición aleatoria
POWERUP_DURATION = 7000          # Duración del efecto (ms)

# Colores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (0, 200, 0)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 100)
CYAN = (100, 255, 255)
ORANGE = (255, 150, 50)