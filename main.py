"""
Mascota Virtual de Informática - Dragón "Antonio"
IPET 249 "Nicolás Copérnico" - Especialidad Informática
 - 6° G - 2026

Controles:  C = Café (energía)   B = Limpiar bugs (salud)
            P = Programar (ánimo)   ESC = Salir
También se puede jugar haciendo clic en los botones.

Escudo: si existe assets/escudo.png se usa esa imagen;
si no, se dibuja un escudo provisorio.
"""
import math
import os
import random
import sys

import pygame

ANCHO, ALTO, FPS = 800, 600, 60

# Paleta institucional
BORDO = (110, 16, 38)
BORDO_OSC = (70, 8, 24)
ROJO = (200, 32, 44)
AMARILLO = (255, 200, 40)
BLANCO = (250, 248, 244)
NEGRO = (30, 26, 30)

# Cuánto baja cada barra por segundo (el "desgaste")
DESGASTE = {"energia": 3.0, "animo": 2.2, "salud": 1.8}
DURACION_CAFE = 1.5  # segundos que dura la animación del café


# ----------------------------------------------------------------- LÓGICA
class Mascota:
    def __init__(self):
        self.energia = 80.0
        self.animo = 80.0
        self.salud = 80.0
        self.t_prog = 0.0  # segundos que le quedan programando
        self.t_cafe = 0.0  # segundos que le quedan tomando café

    def actualizar(self, dt):
        self.energia -= DESGASTE["energia"] * dt
        self.animo -= DESGASTE["animo"] * dt
        self.salud -= DESGASTE["salud"] * dt
        if self.t_cafe > 0:
            self.t_cafe -= dt
        if self.t_prog > 0:
            self.t_prog -= dt
            self.animo += 6 * dt  # programar lo divierte
        self.energia = max(0, min(100, self.energia))
        self.animo = max(0, min(100, self.animo))
        self.salud = max(0, min(100, self.salud))

    @property
    def estado(self):
        if self.t_prog > 0:
            return "programando"
        if self.t_cafe > 0:
            return "feliz"  # mientras toma café se lo ve contento
        if self.energia < 25:
            return "cansado"
        if self.animo < 30 or self.salud < 30:
            return "triste"
        return "feliz"

    def ejecutar(self, accion):
        if accion == "cafe":
            self.energia = min(100, self.energia + 25)
            self.animo = min(100, self.animo + 5)
            self.t_cafe = DURACION_CAFE  # arranca la animación
            return "¡Café de código! +Energía"
        if accion == "bugs":
            self.salud = min(100, self.salud + 25)
            return "¡Bugs eliminados! +Salud"
        if accion == "programar":
            if self.energia < 10:
                return "Sin batería... necesito café primero"
            self.t_prog = 3.0
            self.energia -= 10
            self.salud -= 5
            self.animo = min(100, self.animo + 15)
            return "Programando... -Energía +Ánimo"
        return ""


# ----------------------------------------------------------------- DIBUJO
def estrella(cx, cy, r_ext, rot=-90):
    r_int = r_ext * 0.45
    pts = []
    for i in range(10):
        r = r_ext if i % 2 == 0 else r_int
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def cargar_escudo(size=84):
    ruta = os.path.join("assets", "escudo.png")
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.smoothscale(img, (size, size))
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    pts = [(4, 4), (size - 4, 4), (size - 4, size * 0.55),
           (size / 2, size - 4), (4, size * 0.55)]
    pygame.draw.polygon(s, BLANCO, pts)
    pygame.draw.polygon(s, AMARILLO, pts, 4)
    f = pygame.font.SysFont("arial", 16, bold=True)
    for i, txt in enumerate(("IPET", "249")):
        im = f.render(txt, True, BORDO)
        s.blit(im, im.get_rect(center=(size / 2, size * 0.30 + i * 20)))
    return s


def crear_fondo(escudo):
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill(BORDO_OSC)
    # lluvia de código decorativa
    random.seed(7)
    f = pygame.font.SysFont("consolas,couriernew,monospace", 18)
    for _ in range(80):
        ch = f.render(random.choice("01{}<>/;="), True, (92, 14, 34))
        fondo.blit(ch, (random.randint(0, ANCHO), random.randint(105, 470)))
    # piso
    pygame.draw.rect(fondo, BORDO, (0, 480, ANCHO, ALTO - 480))
    pygame.draw.line(fondo, AMARILLO, (0, 480), (ANCHO, 480), 4)
    # encabezado institucional
    pygame.draw.rect(fondo, BORDO, (0, 0, ANCHO, 100))
    pygame.draw.line(fondo, AMARILLO, (0, 98), (ANCHO, 98), 4)
    fondo.blit(escudo, (14, 8))
    t1 = pygame.font.SysFont("arial", 30, bold=True).render(
        "Mascota Virtual de Informática", True, BLANCO)
    t2 = pygame.font.SysFont("arial", 18).render(
        'IPET 249 "Nicolás Copérnico"  |  ',
        True, AMARILLO)
    fondo.blit(t1, (115, 22))
    fondo.blit(t2, (115, 62))
    return fondo


def dibujar_bug(p, x, y, t):
    x += math.sin(t * 3 + x) * 6
    for i in (-1, 0, 1):
        pygame.draw.line(p, NEGRO, (x + i * 5, y - 6), (x + i * 8, y - 13), 2)
        pygame.draw.line(p, NEGRO, (x + i * 5, y + 6), (x + i * 8, y + 13), 2)
    pygame.draw.ellipse(p, (70, 200, 90), (x - 10, y - 7, 20, 14))
    pygame.draw.circle(p, NEGRO, (int(x + 9), int(y)), 3)


def dibujar_dragon(p, cx, cy, estado, t, fuente_z, cafe=0.0):
    vel = 1.5 if estado == "cansado" else 3
    cy += math.sin(t * vel) * 5
    flap = math.sin(t * vel) * (6 if estado == "cansado" else 14)
    hy = cy - 60  # centro de la cabeza

    # alas
    for lado in (-1, 1):
        pts = [(70, 0), (200, -100 + flap), (170, -30),
               (215, -10 + flap / 2), (150, 30), (80, 50)]
        pts = [(cx + lado * x, cy + y) for x, y in pts]
        pygame.draw.polygon(p, BORDO_OSC, pts)
        pygame.draw.polygon(p, AMARILLO, pts, 3)

    # cola con púas amarillas
    cola = [(60, 60), (150, 80), (215, 50), (245, 10),
            (255, 70), (200, 125), (110, 125), (60, 115)]
    cola = [(cx + x, cy + y) for x, y in cola]
    pygame.draw.polygon(p, BORDO, cola)
    pygame.draw.polygon(p, BORDO_OSC, cola, 3)
    for (a, b, c) in [((100, 78), (112, 58), (126, 82)),
                      ((150, 76), (164, 56), (176, 76)),
                      ((200, 52), (222, 28), (226, 62))]:
        pygame.draw.polygon(p, AMARILLO,
                            [(cx + a[0], cy + a[1]), (cx + b[0], cy + b[1]),
                             (cx + c[0], cy + c[1])])

    # cuerpo y panza
    pygame.draw.ellipse(p, BORDO, (cx - 90, cy - 25, 180, 180))
    pygame.draw.ellipse(p, BORDO_OSC, (cx - 90, cy - 25, 180, 180), 3)
    pygame.draw.ellipse(p, AMARILLO, (cx - 55, cy + 5, 110, 130))
    for i in range(5):
        y = cy + 18 + i * 24
        dx = 55 * math.sqrt(max(0, 1 - ((y - (cy + 70)) / 65) ** 2))
        pygame.draw.line(p, (225, 165, 20), (cx - dx + 4, y), (cx + dx - 4, y), 2)
    # chip / placa de circuito en el pecho
    for i in range(4):
        yy = cy + 58 + i * 9
        pygame.draw.line(p, BORDO_OSC, (cx - 30, yy), (cx - 22, yy), 2)
        pygame.draw.line(p, BORDO_OSC, (cx + 22, yy), (cx + 30, yy), 2)
    pygame.draw.rect(p, BORDO, (cx - 22, cy + 50, 44, 40), border_radius=4)
    pygame.draw.rect(p, ROJO, (cx - 12, cy + 60, 24, 20), border_radius=3)

    # patas y brazos
    for lado in (-1, 1):
        pygame.draw.ellipse(p, BORDO, (cx + lado * 45 - 25, cy + 140, 50, 26))
        pygame.draw.ellipse(p, BORDO_OSC, (cx + lado * 45 - 25, cy + 140, 50, 26), 2)
        for k in (-1, 0, 1):
            pygame.draw.circle(p, AMARILLO, (int(cx + lado * 45 + k * 13), cy + 162), 4)
        pygame.draw.ellipse(p, BORDO, (cx + lado * 95 - 16, cy + 20, 32, 62))
        pygame.draw.ellipse(p, BORDO_OSC, (cx + lado * 95 - 16, cy + 20, 32, 62), 2)

    # cuernos y cabeza
    for lado in (-1, 1):
        pygame.draw.polygon(p, AMARILLO, [(cx + lado * 60, hy - 48),
                                          (cx + lado * 85, hy - 100),
                                          (cx + lado * 35, hy - 62)])
    pygame.draw.ellipse(p, BORDO, (cx - 85, hy - 70, 170, 140))
    pygame.draw.ellipse(p, BORDO_OSC, (cx - 85, hy - 70, 170, 140), 3)

    # hocico y boca
    pygame.draw.ellipse(p, (160, 34, 56), (cx - 38, hy + 15, 76, 48))
    for lado in (-1, 1):
        pygame.draw.circle(p, NEGRO, (cx + lado * 12, hy + 26), 3)
    if estado == "feliz":
        pygame.draw.arc(p, NEGRO, (cx - 16, hy + 30, 32, 22), math.pi * 1.1, math.pi * 1.9, 3)
        for lado in (-1, 1):
            pygame.draw.circle(p, (185, 50, 70), (cx + lado * 62, hy + 28), 8)
        sy = hy - 60 + math.sin(t * 4) * 5
        pygame.draw.polygon(p, AMARILLO, estrella(cx + 135, sy, 11))
        pygame.draw.polygon(p, AMARILLO, estrella(cx - 140, sy + 20, 8))
    elif estado == "triste":
        pygame.draw.arc(p, NEGRO, (cx - 16, hy + 42, 32, 22), math.pi * 0.1, math.pi * 0.9, 3)
    elif estado == "cansado":
        pygame.draw.line(p, NEGRO, (cx - 8, hy + 46), (cx + 8, hy + 46), 3)
    else:  # programando
        pygame.draw.ellipse(p, NEGRO, (cx - 7, hy + 40, 14, 10))

    # lentes de estrella
    gy = hy - 8
    pygame.draw.line(p, AMARILLO, (cx - 8, gy - 11), (cx + 8, gy - 11), 4)
    for lado in (-1, 1):
        gx = cx + lado * 42
        pygame.draw.line(p, AMARILLO, (gx + lado * 34, gy - 11),
                         (cx + lado * 85, gy - 11), 4)
        if estado == "triste":
            pygame.draw.circle(p, (90, 170, 255), (int(gx + lado * 6), int(gy + 30)), 5)
        pygame.draw.polygon(p, (205, 235, 255), estrella(gx, gy, 36))
        pygame.draw.polygon(p, AMARILLO, estrella(gx, gy, 36), 4)
        # ojos
        if estado == "cansado":
            pygame.draw.line(p, NEGRO, (gx - 10, gy + 2), (gx + 10, gy + 2), 3)
        else:
            ox, oy = 0, 0
            if estado == "triste":
                oy = 5
            if estado == "programando":
                ox = math.sin(t * 10) * 5
            pygame.draw.circle(p, NEGRO, (int(gx + ox), int(gy + 2 + oy)), 7)
            pygame.draw.circle(p, BLANCO, (int(gx + ox + 2), int(gy + oy)), 2)

    # auriculares gamer
    pygame.draw.arc(p, NEGRO, (cx - 92, hy - 100, 184, 200), 0, math.pi, 10)
    for lado in (-1, 1):
        px = cx + lado * 92
        pygame.draw.ellipse(p, NEGRO, (px - 18, hy - 30, 36, 60))
        pygame.draw.ellipse(p, ROJO, (px - 12, hy - 22, 24, 44))
        pygame.draw.ellipse(p, AMARILLO, (px - 18, hy - 30, 36, 60), 3)
    pygame.draw.line(p, NEGRO, (cx - 92, hy + 25), (cx - 62, hy + 62), 4)
    pygame.draw.circle(p, ROJO, (cx - 62, hy + 62), 6)

    # extras según estado
    if estado == "cansado":
        for i in range(3):
            z = fuente_z.render("z", True, BLANCO)
            z = pygame.transform.rotozoom(z, 0, 0.8 + i * 0.4)
            p.blit(z, (cx + 100 + i * 24, hy - 70 - i * 24 + math.sin(t * 2 + i) * 4))
    if estado == "programando":
        pygame.draw.rect(p, (40, 40, 52), (cx - 75, cy + 70, 150, 80), border_radius=6)
        pygame.draw.rect(p, (110, 110, 125), (cx - 75, cy + 70, 150, 80), 3, border_radius=6)
        rnd = random.Random(int(t * 6))
        for i in range(5):
            pygame.draw.line(p, (90, 240, 120), (cx - 62, cy + 82 + i * 12),
                             (cx - 62 + rnd.randint(30, 120), cy + 82 + i * 12), 3)
        pygame.draw.rect(p, (110, 110, 125), (cx - 90, cy + 150, 180, 10), border_radius=4)
        for lado in (-1, 1):
            pygame.draw.ellipse(p, BORDO, (cx + lado * 45 - 16, cy + 138, 32, 20))

    if cafe > 0:
        dibujar_taza(p, cx, cy, hy, cafe, t, fuente_z)


def dibujar_taza(p, cx, cy, hy, restante, t, fuente):
    """Taza que sube a la boca, hace sorbos y vuelve a la mano."""
    prog = 1 - restante / DURACION_CAFE  # va de 0 a 1
    if prog < 0.3:
        k = prog / 0.3          # subiendo
    elif prog < 0.7:
        k = 1                   # tomando
    else:
        k = (1 - prog) / 0.3    # bajando
    x0, y0 = cx + 95, cy + 55   # posición de la mano
    x1, y1 = cx + 30, hy + 52   # posición de la boca
    x = x0 + (x1 - x0) * k
    y = y0 + (y1 - y0) * k
    tomando = 0.3 <= prog < 0.7
    if tomando:
        y += math.sin(t * 25) * 2  # temblor de sorbo
    pygame.draw.circle(p, BLANCO, (int(x + 16), int(y)), 8, 3)  # asa
    pygame.draw.rect(p, BLANCO, (x - 14, y - 12, 28, 24), border_radius=5)
    pygame.draw.rect(p, AMARILLO, (x - 14, y - 2, 28, 6))       # franja
    pygame.draw.rect(p, (90, 50, 30), (x - 14, y - 12, 28, 5))  # café
    for i in (-1, 0, 1):  # vapor
        pts = [(x + i * 7 + math.sin(t * 8 + i + j) * 3, y - 16 - j * 6)
               for j in range(4)]
        pygame.draw.lines(p, BLANCO, False, pts, 2)
    if tomando:
        txt = pygame.transform.rotozoom(fuente.render("¡Glup!", True, AMARILLO), 0, 0.6)
        p.blit(txt, (x + 22, y - 45))


class Boton:
    def __init__(self, x, texto, accion):
        self.rect = pygame.Rect(x, 515, 220, 56)
        self.texto, self.accion = texto, accion

    def dibujar(self, p, fuente):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(p, AMARILLO if hover else ROJO, self.rect, border_radius=12)
        pygame.draw.rect(p, BLANCO, self.rect, 3, border_radius=12)
        im = fuente.render(self.texto, True, NEGRO if hover else BLANCO)
        p.blit(im, im.get_rect(center=self.rect.center))


def dibujar_barra(p, fuente, nombre, valor, x, y, ancho=165):
    p.blit(fuente.render(f"{nombre}: {int(valor)}%", True, BLANCO), (x, y))
    pygame.draw.rect(p, NEGRO, (x, y + 24, ancho, 16), border_radius=6)
    color = ROJO if valor < 25 else AMARILLO
    pygame.draw.rect(p, color, (x, y + 24, max(0, ancho * valor / 100), 16), border_radius=6)
    pygame.draw.rect(p, BLANCO, (x, y + 24, ancho, 16), 2, border_radius=6)


# ----------------------------------------------------------------- MAIN
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Mascota Virtual de Informática - IPET 249")
    reloj = pygame.time.Clock()
    f_txt = pygame.font.SysFont("arial", 18, bold=True)
    f_z = pygame.font.SysFont("arial", 30, bold=True)

    fondo = crear_fondo(cargar_escudo())
    mascota = Mascota()
    botones = [Boton(30, "[C] Café de código", "cafe"),
               Boton(290, "[B] Limpiar bugs", "bugs"),
               Boton(550, "[P] Programar", "programar")]
    teclas = {pygame.K_c: "cafe", pygame.K_b: "bugs", pygame.K_p: "programar"}
    posiciones_bugs = [(130, 440), (480, 430), (110, 330), (500, 300), (200, 430)]
    mensaje, t_msg, t = "¡Hola! Soy Antonio, el dragón informatico", 3.0, 0.0

    while True:
        dt = reloj.tick(FPS) / 1000
        t += dt
        for e in pygame.event.get():
            accion = None
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                accion = teclas.get(e.key)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for b in botones:
                    if b.rect.collidepoint(e.pos):
                        accion = b.accion
            if accion:
                mensaje, t_msg = mascota.ejecutar(accion), 2.5

        mascota.actualizar(dt)
        t_msg -= dt

        pantalla.blit(fondo, (0, 0))
        for i in range(int((100 - mascota.salud) // 20)):
            dibujar_bug(pantalla, *posiciones_bugs[i], t)
        dibujar_dragon(pantalla, 300, 330, mascota.estado, t, f_z, mascota.t_cafe)

        # panel de estado
        panel = pygame.Surface((195, 215), pygame.SRCALPHA)
        panel.fill((40, 4, 14, 200))
        pantalla.blit(panel, (590, 125))
        pygame.draw.rect(pantalla, AMARILLO, (590, 125, 195, 215), 3, border_radius=8)
        dibujar_barra(pantalla, f_txt, "Energía", mascota.energia, 605, 138)
        dibujar_barra(pantalla, f_txt, "Ánimo", mascota.animo, 605, 190)
        dibujar_barra(pantalla, f_txt, "Salud", mascota.salud, 605, 242)
        est = f_txt.render("Estado: " + mascota.estado.capitalize(), True, AMARILLO)
        pantalla.blit(est, (605, 300))

        if t_msg > 0:
            im = f_txt.render(mensaje, True, AMARILLO)
            pantalla.blit(im, im.get_rect(center=(ANCHO // 2, 118)))
        for b in botones:
            b.dibujar(pantalla, f_txt)
        pygame.display.flip()


if __name__ == "__main__":
    main()