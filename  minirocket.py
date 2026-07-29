"""
minirocket.py
A dot, some fuel, and a bit of Newton.
Tsiolkovsky would approve.
"""

import pygame
import sys
import math

pygame.init()
W, H = 600, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("rocket")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 12)

# Physics (SI)
G = 9.81
DRY = 1000.0       # dry mass (kg)
ISP = 310.0        # specific impulse (sec)
THRUST = 35000.0   # Newtons
DV_TARGET = 2500.0 # mission delta‑v (m/s)

# Fuel from Tsiolkovsky: m0 = dry * exp(dv / (isp*g))
ve = ISP * G
m0 = DRY * math.exp(DV_TARGET / ve)
fuel = m0 - DRY    # initial fuel mass (kg)

# State
alt = 0.0          # altitude (m)
v = 0.0            # vertical velocity (m/s)
time = 0.0         # flight time (s)
burn_rate = THRUST / ve   # fuel consumption (kg/s)
dt = 0.02          # fixed timestep

# Screen mapping: 1 pixel = 2 meters
GROUND_Y = 520
X_CENTER = 300

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # Physics (thrust on until fuel empty)
    if fuel > 0:
        mass = DRY + fuel
        acc = THRUST / mass - G   # net upward acceleration
        v += acc * dt
        alt += v * dt
        fuel -= burn_rate * dt
        fuel = max(0.0, fuel)
        time += dt

    # Clamp to ground
    if alt < 0:
        alt = 0.0
        v = 0.0

    # Screen position (Y down)
    y_screen = GROUND_Y - alt / 2.0
    if y_screen < 0:
        y_screen = 0.0

    # Render
    screen.fill((10, 10, 15))

    # Ground
    pygame.draw.rect(screen, (40, 45, 50), (0, GROUND_Y, W, H - GROUND_Y))
    pygame.draw.line(screen, (80, 85, 90), (0, GROUND_Y), (W, GROUND_Y), 2)

    # Rocket dot
    rx = int(X_CENTER)
    ry = int(y_screen)
    pygame.draw.circle(screen, (220, 225, 235), (rx, ry), 6)

    # Flame (if burning)
    if fuel > 0:
        pygame.draw.circle(screen, (255, 150, 30), (rx, ry + 8), 4)

    # Telemetry 
    twr = THRUST / ((DRY + fuel) * G) if fuel > 0 else 0.0
    info = [
        f"alt: {alt:.0f} m",
        f"v: {v:.1f} m/s",
        f"fuel: {fuel:.0f} kg",
        f"twr: {twr:.2f}",
        f"time: {time:.1f} s"
    ]
    for i, txt in enumerate(info):
        surf = font.render(txt, True, (180, 185, 190))
        screen.blit(surf, (10, 10 + i * 18))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()