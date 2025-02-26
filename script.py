"""
    
    A live cell dies if it has fewer than two live neighbors.
    A live cell with two or three live neighbors lives on to the next generation.
    A live cell with more than three live neighbors dies.
    A dead cell will be brought back to live if it has exactly three live neighbors.

"""

import pygame
import random

pygame.init()

width = 700
height = 400
distance = 5
is_closed = False
probability = 0.5
refresh = 500 # ms

surface = pygame.display.set_mode((width,height))

color_white = (255,255,255)
color_black = (0,0,0)

def initialize(coordinates, nullable = False):
    for x in range(0, width, distance):
        coordinates[x] = {}
        for y in range(0, height, distance):
            if nullable:
                coordinates[x][y] = False
            else:
                coordinates[x][y] = random.random() < probability
    return coordinates

def sample_initialize(coordinates):
    initialize(coordinates, True)
    
    x = int(width / 2)
    y = int(height / 2)
        
    coordinates[x - distance][y] = True
    coordinates[x + 0][y] = True
    coordinates[x + distance][y] = True
    
    return coordinates
      
def evaluate(coordinates):

    new_coordinates = {}
    for x in range(0, width, distance):
        new_coordinates[x] = {}
        for y in range(0, height, distance):
            cell = coordinates[x][y]
                        
            cell_neighborns = []
            
            cell_neighborns.append(coordinates.get(x - distance, {}).get(y - distance, {}))
            cell_neighborns.append(coordinates.get(x, {}).get(y - distance, {}))
            cell_neighborns.append(coordinates.get(x + distance, {}).get(y - distance, {}))
            cell_neighborns.append(coordinates.get(x + distance, {}).get(y, {}))
            cell_neighborns.append(coordinates.get(x + distance, {}).get(y + distance, {}))
            cell_neighborns.append(coordinates.get(x, {}).get(y + distance, {}))
            cell_neighborns.append(coordinates.get(x - distance, {}).get(y + distance, {}))
            cell_neighborns.append(coordinates.get(x - distance, {}).get(y, {}))
                    
            neighborns_alive = list(filter(lambda x: x == True, cell_neighborns))
            neighborns_alive_count = len(neighborns_alive)
            
            new_coordinates[x][y] = False
            
            if (neighborns_alive_count) == 0:
                continue        
            
            if cell and (neighborns_alive_count == 2 or neighborns_alive_count == 3):
                new_coordinates[x][y] = True
            elif cell and neighborns_alive_count < 2:
                new_coordinates[x][y] = False
            elif not cell and neighborns_alive_count == 3:
                new_coordinates[x][y] = True
            elif cell and neighborns_alive_count > 3:
                new_coordinates[x][y] = False
                    
    return new_coordinates


if __name__ == '__main__':
    
    coordinates = {}
    coordinates = initialize(coordinates)
    
    pygame.time.set_timer(pygame.USEREVENT, refresh)

    while not is_closed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_closed = True
            if event.type == pygame.USEREVENT:
                coordinates = evaluate(coordinates)

        for x in range(0, width, distance):
            for y in range(0, height, distance):
                pygame.draw.rect(surface, color_black, pygame.Rect(x, y, distance, distance),  distance)
                if coordinates[x][y]:
                    pygame.draw.rect(surface, color_white, pygame.Rect(x, y, distance, distance),  distance)
        
        pygame.display.flip()
        