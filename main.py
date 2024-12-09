import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from celestial_body import CelestialBody

#Função para configurar o OpenGL
def setup_opengl():
    glEnable(GL_DEPTH_TEST) #Habilita o teste de profundidade
    glEnable(GL_TEXTURE_2D) #Habilita o uso de texturas
    glClearColor(0, 0, 0, 1) #Define a cor de fundo
    glEnable(GL_LIGHTING) #Habilita a iluminação
    glEnable(GL_LIGHT0) #Habilita a luz 0

    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1)) #Define a posição da luz
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1)) #Define a cor da luz
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1)) #Define a cor ambiente da luz
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1)) #Define a cor especular da luz

def main():
    pygame.init()

    #Capura a resolução da tela
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | DOUBLEBUF | OPENGL)
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h

    #Pega a resolução da tela e ajusta a perspectiva
    gluPerspective(45, (screen_width / screen_height), 0.1, 1000)
    
    #Posiciona a câmera em visão lateral
    gluLookAt(70, 0, 0, 0, 0, 0, 0, 1, 0)

    #Inicializa as configurações do OpenGL
    setup_opengl()

    #Instancia o objeto de fundo com tamanho 200
    background = CelestialBody("Fundo", "assets/textures/milky_way.jpg", 200)

    #Instancia o objeto do Sol com tamanho 5
    sun = CelestialBody("Sol", "assets/textures/sun.jpg", 5)

    #Instancia os planetas com seus respectivos atributos no array
    planets = [
        CelestialBody("Mercúrio", "assets/textures/mercury.jpg", 0.5, 6, 1, 0.5),
        CelestialBody("Vênus", "assets/textures/venus.jpg", 1, 9, 0.8, 0.4),
        CelestialBody("Terra", "assets/textures/earth.jpg", 1.2, 12, 0.6, 0.3),
        CelestialBody("Marte", "assets/textures/mars.jpg", 0.9, 15, 0.5, 0.25),
        CelestialBody("Júpiter", "assets/textures/jupiter.jpg", 3, 20, 0.3, 0.2),
        CelestialBody("Saturno", "assets/textures/saturn.jpg", 2.5, 25, 0.2, 0.15, rings=True, rings_texture_path="assets/textures/saturn_ring.png"),
        CelestialBody("Urano", "assets/textures/uranus.jpg", 2, 30, 0.15, 0.1),
        CelestialBody("Netuno", "assets/textures/neptune.jpg", 2, 35, 0.1, 0.05),
    ]
    
    #Loop principal
    clock = pygame.time.Clock()
    running = True

    while running:
        #Captura eventos do teclado para fechar a janela
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #Limpa o buffer de cor e de profundidade

        background.draw() #Desenha o fundo
        sun.draw() #Desenha o Sol

        #Desenha os planetas
        for planet in planets:
            planet.draw()

        pygame.display.flip() #Atualiza a tela
        clock.tick(60) #Limita a taxa de quadros por segundo

    pygame.quit()


if __name__ == "__main__":
    main()