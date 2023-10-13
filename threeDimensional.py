import pygame
import math
class ThreeDimensional:
    def __init__(self,shape,screen) -> None:
        self.type="3D"
        self.screen=screen
        self.x=100
        self.y=100
        self.w=360
        self.h=240
        self.scrollOffset=0
        self.rect=pygame.Rect((self.x,self.y,self.w,self.h))
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
        self.shape=shape
        self.angle_x = 0
        self.angle_y = 0
        if self.shape=="cube":
            self.vertices = [
                (-1, -1, -1),
                (1, -1, -1),
                (1, 1, -1),
                (-1, 1, -1),
                (-1, -1, 1),
                (1, -1, 1),
                (1, 1, 1),
                (-1, 1, 1)
            ]
            self.edges = [
                (0, 1), (1, 2), (2, 3), (3, 0),
                (4, 5), (5, 6), (6, 7), (7, 4),
                (0, 4), (1, 5), (2, 6), (3, 7)
            ]
        elif self.shape=="pyramid":
            self.vertices = [
                (0, -1, 0),  # Top vertex
                (-1, 1, -1),  # Bottom-left front vertex
                (1, 1, -1),  # Bottom-right front vertex
                (1, 1, 1),   # Bottom-right back vertex
                (-1, 1, 1)   # Bottom-left back vertex
            ]

            self.edges = [
                (0, 1), (0, 2), (0, 3), (0, 4),  # Edges from the top vertex to the base
                (1, 2), (2, 3), (3, 4), (4, 1),  # Edges on the base
                (1, 2), (2, 3)  # Edges on the front and back faces
            ]
    def pyramid(self,scren):
        self.angle_x += 0.01
        self.angle_y += 0.01
        rotation_x = [
            [1, 0, 0],
            [0, math.cos(self.angle_x), -math.sin(self.angle_x)],
            [0, math.sin(self.angle_x), math.cos(self.angle_x)]
        ]

        rotation_y = [
            [math.cos(self.angle_y), 0, math.sin(self.angle_y)],
            [0, 1, 0],
            [-math.sin(self.angle_y), 0, math.cos(self.angle_y)]
        ]
        rotated_vertices = []
        for vertex in self.vertices:
            rotated = [
                vertex[0],
                vertex[1] * rotation_x[1][1] + vertex[2] * rotation_x[1][2],
                vertex[1] * rotation_x[2][1] + vertex[2] * rotation_x[2][2]
            ]
            rotated = [
                rotated[0] * rotation_y[0][0] + rotated[2] * rotation_y[0][2],
                rotated[1],
                rotated[0] * rotation_y[2][0] + rotated[2] * rotation_y[2][2]
            ]
            rotated_vertices.append(rotated)

        # Project vertices to 2D
        projected_vertices = []
        for vertex in rotated_vertices:
            distance = 5  # distance from camera
            z = 1 / (vertex[2] + distance)
            x = vertex[0] * z
            y = vertex[1] * z
            projected_vertices.append((int(self.x + self.w / 2 + x * (self.w / 3)), int(self.y + self.h / 2 - y * (self.w / 3))))

        # Draw pyramid faces (triangles)
        pyramid_faces = [
            (projected_vertices[0], projected_vertices[1], projected_vertices[4]),
            (projected_vertices[1], projected_vertices[2], projected_vertices[4]),
            (projected_vertices[2], projected_vertices[3], projected_vertices[4]),
            (projected_vertices[3], projected_vertices[0], projected_vertices[4]),
            (projected_vertices[0], projected_vertices[1], projected_vertices[2], projected_vertices[3])
        ]


        # Draw edges
        for edge in self.edges:
            pygame.draw.line(self.screen, (0, 0, 0), projected_vertices[edge[0]], projected_vertices[edge[1]], 2)  # default thickness 2

    def cube(self,screen):
        self.angle_x += 0.01
        self.angle_y += 0.01
        rotation_x = [
            [1, 0, 0],
            [0, math.cos(self.angle_x), -math.sin(self.angle_x)],
            [0, math.sin(self.angle_x), math.cos(self.angle_x)]
        ]

        rotation_y = [
            [math.cos(self.angle_y), 0, math.sin(self.angle_y)],
            [0, 1, 0],
            [-math.sin(self.angle_y), 0, math.cos(self.angle_y)]
        ]
        rotated_vertices = []
        for vertex in self.vertices:
            rotated = [
                vertex[0],
                vertex[1] * rotation_x[1][1] + vertex[2] * rotation_x[1][2],
                vertex[1] * rotation_x[2][1] + vertex[2] * rotation_x[2][2]
            ]
            rotated = [
                rotated[0] * rotation_y[0][0] + rotated[2] * rotation_y[0][2],
                rotated[1],
                rotated[0] * rotation_y[2][0] + rotated[2] * rotation_y[2][2]
            ]
            rotated_vertices.append(rotated)

        # Project vertices to 2D
        projected_vertices = []
        for vertex in rotated_vertices:
            distance = 5  # distance from camera
            z = 1 / (vertex[2] + distance)
            x = vertex[0] * z
            y = vertex[1] * z
            projected_vertices.append((int(self.x + self.w / 2 + x * (self.w / 3)), int(self.y + self.h / 2 - y * (self.w / 3))))


        # Draw edges
        for edge in self.edges:
            pygame.draw.line(screen, (0,0,0), projected_vertices[edge[0]], projected_vertices[edge[1]], 2) #default thickness 2


    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),self.rect)
        pygame.draw.rect(screen,(0,0,0),self.bar)
        pygame.draw.rect(screen,(255,0,0),self.exitRect)
        if self.shape=="cube":
            self.cube(screen)
        elif self.shape=="pyramid":
            self.pyramid(screen)
    def mbHeld(self,mousePos):
        self.x=mousePos[0]
        self.y=mousePos[1]

        if (self.x+self.w)>=self.screen.get_rect().w:
            self.x=self.screen.get_rect().w-self.w
        elif self.x<=0:
            self.x=0
        if (self.y+self.h)>=self.screen.get_rect().h:
            self.y=self.screen.get_rect().h-self.h
        elif self.y<=0:
            self.y=0
            
        self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)

        self.stdout=pygame.Rect(self.x+10,self.y+20,self.w-20,80)
        self.stdin=pygame.Rect(self.x+10,self.y+130,self.w-20,80)