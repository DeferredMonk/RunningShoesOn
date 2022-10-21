import pygame
import CustomClasses

def createClouds(N, CustomClass): #Adds clouds to the game
    amountOfClouds = 0
    cloud_group = pygame.sprite.Group()

    while amountOfClouds < 5: 
        amountOfClouds += 1
        cloud = CustomClass("cloud.png")
        cloud_group.add(cloud)
    
    return cloud_group

def addToStackTiles(group, N, X, Y): #Creates a stack of tiles attached to each other

    if N == 1:
        tile = CustomClasses.Tile("stoneHalf.png", X, Y)
        group.add(tile)
	
    else:
        for i in range(N):
            if i == 0:
                tile = CustomClasses.Tile("stoneHalfLeft.png", X, Y)
                X += tile.image.get_width()
            
            elif i == N -1:
                tile = CustomClasses.Tile("stoneHalfRight.png", X, Y)
                X += tile.image.get_width()
            
            else:
                tile = CustomClasses.Tile("stoneHalfMid.png", X, Y)
                X += tile.image.get_width()
            group.add(tile)