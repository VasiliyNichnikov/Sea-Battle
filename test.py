import pygame


pygame.init()
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Sea Battle')
runner = True

surface.fill(WHITE)
draw_map(first_draw=True)
pygame.display.flip()

# запуск игры
while runner:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                check_input_mouse(event.pos)
                draw_map()

    # surface.fill(WHITE)
    pygame.display.flip()

pygame.quit()
