import math
import pygame

def distance(p1, p2):
    """Devuelve la distancia entre dos puntos."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def point_inside_circle(point, center, radius):
    """Comprueba si un punto está dentro de un círculo."""
    return distance(point, center) <= radius

def load_and_scale(path, size):
    """Carga una imagen y la escala al tamaño deseado."""
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except pygame.error as e:
        print(f"[ERROR] No se pudo cargar: {path} → {e}")
        return pygame.Surface(size)

def clamp(value, min_value, max_value):
    """Restringe un valor dentro de un rango."""
    return max(min_value, min(value, max_value))

def rect_center(rect):
    """Devuelve el centro de un rect como tupla (x, y)."""
    return (rect.x + rect.width // 2, rect.y + rect.height // 2)