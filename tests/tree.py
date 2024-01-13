import pygame
import math
import random
import re

# Pygame setup
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Growing Tree")

def lRule(c, branch_chance, grow_chance, rot_chance):
    ret = c   

    sign = random.random() > 0.5
    if random.random() < branch_chance:
        ret += '[' + 2*'+-'[sign]
        if c != 'E' and random.random() < 0.1:
            ret += chr(ord(c) + 2)
        else:
            ret += chr(ord(c) + 1)
        ret += ']'

    if random.random() < rot_chance:
        ret += '-+'[sign]

    if random.random() < grow_chance:
        ret += c

    return ret

# L-System rules
rules = {
    'A': lambda d: lRule('A', 0.3, 0.5, 0.001),
    'B': lambda d: lRule('B', 0.3, 0.6, 0.001),
    'C': lambda d: lRule('C', 0.2, 0.8, 0.001),
    'D': lambda d: lRule('D', 0.2, 0.9, 0.001),
    'E': lambda d: lRule('E', 0.2, 0.9, 0.001),
}
axiom = 'A'

# Apply L-System rules
def apply_rules(axiom, rules):
    new_axiom = ""
    for depth, char in enumerate(axiom):
        if char in rules:
            new_axiom += rules[char](depth)
        else:
            new_axiom += char

    return new_axiom

# Draw the tree with branch length and angle adjustments
def draw_tree(screen, axiom, branch_length, angle, time=0):
    x, y = screen_width // 2, screen_height
    stack = []

    for char in axiom:
        if char.isalpha():
            length = branch_length # * random.random() + .5
            new_x = x + length * math.cos(math.radians(angle))
            new_y = y + length * math.sin(math.radians(angle))
            pygame.draw.line(screen, '#855430', (x, y), (new_x, new_y), 2)
            x, y = new_x, new_y
        elif char == '+':
            # angle += random.randint(30, 50)
            angle += 20
        elif char == '-':
            # angle -= random.randint(30, 50)
            angle -= 20
        elif char == '[':
            stack.append((x, y, branch_length, angle))
        elif char == ']':
            # pygame.draw.circle(screen, (0, 255, 0, 0.5), (x, y), branch_length*4)
            x, y, branch_length, angle = stack.pop()

# Main loop for animation
running = True
generation = 0
growth_delay = 0.5
branch_length = 50  # Initial branch length

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    axiom = apply_rules(axiom, rules)
    draw_tree(screen, axiom, branch_length, -90)  # Start with an initial angle of -90 degrees
    pygame.display.update()

    pygame.time.delay(int(growth_delay * 1000))

    generation += 1
    if generation >= 25:
        # print(axiom)
        axiom = apply_rules(axiom, rules)
        screen.fill((0, 0, 0))
        draw_tree(screen, axiom, branch_length, 10)
        running = False

    branch_length *= 0.7

pygame.quit()