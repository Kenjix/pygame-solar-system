import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class CorpoCeleste:
    #Construtor
    def __init__(self, name, texture_path, size, distance_from_center=0, 
                 orbit_speed=0, rotation_speed=0, rings=False, rings_texture_path=None):
        self.name = name #Adiciona o nome do corpo celeste
        self.size = size #Adiciona o tamanho do corpo celeste
        self.distance_from_center = distance_from_center #Adiciona a distância do centro
        self.orbit_speed = orbit_speed #Adiciona a velocidade de órbita
        self.rotation_speed = rotation_speed #Adiciona a velocidade de rotação
        self.angle_orbit = 0 #Adiciona o ângulo de órbita
        self.angle_rotation = 0 #Adiciona o ângulo de rotação
        self.texture = self.load_texture(texture_path)
        self.rings = rings  #Adiciona a opção para ter anéis
        self.rings_texture = None #Adiciona a textura dos anéis
        if self.rings and rings_texture_path: #Carrega a textura dos anéis se True
            self.rings_texture = self.load_texture(rings_texture_path)  

    def load_texture(self, texture_path):
        try:
            texture = glGenTextures(1)
            texture_surface = pygame.image.load(texture_path)
            texture_data = pygame.image.tostring(texture_surface, "RGB", True)
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_surface.get_width(),
                         texture_surface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            return texture
        except pygame.error as e:
            print(f"Erro ao carregar a textura {texture_path}: {e}")
            return None

    def draw_rings(self):
        if self.rings and self.rings_texture:
            glPushMatrix()
            glRotatef(360, 1, 0, 0)  #Faz os anéis ficarem planos
            glBindTexture(GL_TEXTURE_2D, self.rings_texture)  #Carrega a textura dos anéis

            #Desenha os anéis com um disco maior para Saturno
            quadric = gluNewQuadric()
            gluQuadricTexture(quadric, GL_TRUE)
            gluDisk(quadric, 1.1 * self.size, 3.0 * self.size, 32, 1)  #Anel de Saturno mais largo

            glPopMatrix()

    def draw(self):
        #Atualiza ângulos de órbita e rotação
        self.angle_orbit += self.orbit_speed
        self.angle_rotation += self.rotation_speed

        #Calcula posição na órbita
        x = self.distance_from_center * math.cos(math.radians(self.angle_orbit))
        z = self.distance_from_center * math.sin(math.radians(self.angle_orbit))

        glPushMatrix()
        glTranslatef(x, 0, z)  #Transformada do corpo celeste na órbita               
        glRotatef(self.angle_rotation, 0, 1, 0)  #Rotação do corpo celeste sobre seu próprio eixo
        glRotatef(160, 0, 1, 1) #Corrige a inclinação dos planetas

        # Define material para reflexão da luz
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1, 1, 1, 1))

        glBindTexture(GL_TEXTURE_2D, self.texture) #Define a textura do corpo celeste
        quadric = gluNewQuadric() #Cria um objeto quadric
        gluQuadricTexture(quadric, GL_TRUE) #Habilita a textura
        gluSphere(quadric, self.size, 32, 32)  #Desenha o corpo celeste
        
        self.draw_rings() #Desenha os anéis (se o planeta tiver)

        glPopMatrix()
