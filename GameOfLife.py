#REGOLE Conway's Game of Life
#1 Una cellula viva con meno di due vicini vivi MUORE (sottopopolazione).
#2 Una cellula viva con due o tre vicini vivi rimane VIVA (sopravvivenza)
#3 Una cellula viva con più di tre vicini vivi MUORE (sovrappopolazione)
#4 Una cellula morta con esattamente tre vicini vivi diventa VIVA (riproduzione)

import pygame
import random

pygame.init()

nero = (0, 0, 0) #Colori in RGB
bianco = (255, 255, 255) #Colori in RGB

#Costanti per la base 800 x 800 divisibile per ogni casella misura 20
larghezza, altezza = 800, 800
casella_misura = 20
larghezza_griglia = larghezza // casella_misura
altezza_griglia = altezza // casella_misura
FPS = 60

schermo = pygame.display.set_mode((larghezza, altezza))

clock = pygame.time.Clock()

#Funzione per la generazione casuale degli automi
def gen(num):
    return set([(random.randrange(0, altezza_griglia), random.randrange(0, larghezza_griglia)) for _ in range(num)])

#Disegno della griglia (col = colonne generate con l'altezza dello schermo e rig = righe per la larghezza dello schermo)
def disegna_griglia(positions):
    for position in positions:
        col, rig = position
        top_left = (col * casella_misura, rig * casella_misura)
        pygame.draw.rect(schermo, nero, (*top_left, casella_misura, casella_misura))

    for rig in range(altezza_griglia):
        pygame.draw.line(schermo, nero, (0, rig * casella_misura), (larghezza, rig * casella_misura))

    for col in range(larghezza_griglia):
        pygame.draw.line(schermo, nero, (col * casella_misura, 0), (col * casella_misura, altezza))


def regola_griglia(positions):
    all_caselleVicine = set()
    nuove_posizioni = set()

    for position in positions:
        cas_vicine = determina_caselleVicine(position)
        all_caselleVicine.update(cas_vicine)

        cas_vicine = list(filter(lambda x: x in positions, cas_vicine))

        if len(cas_vicine) in [2, 3]:
            nuove_posizioni.add(position)

    for position in all_caselleVicine:
        cas_vicine = determina_caselleVicine(position)
        cas_vicine = list(filter(lambda x: x in positions, cas_vicine))

        if len(cas_vicine) == 3:
            nuove_posizioni.add(position)

    return nuove_posizioni

#Tutte le regole per gli automi vivi o morti sono qua
def determina_caselleVicine(pos):
    x, y = pos
    cas_vicine = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > larghezza_griglia:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > altezza_griglia:
                continue
            if dx == 0 and dy == 0:
                continue

            cas_vicine.append((x + dx, y + dy))

    return cas_vicine

#Richiama tutte le funzioni precedenti e inserisci le funzioni dell'inserimento e cancellazione degli automi
def main():
    running = True
    playing = False
    count = 0
    update_freq = 120

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = regola_griglia(positions)

        pygame.display.set_caption("Attivo" if playing else "Disattivo")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // casella_misura
                rig = y // casella_misura
                pos = (col, rig)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * larghezza_griglia)

        schermo.fill(bianco)
        disegna_griglia(positions)
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()
