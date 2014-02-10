""" Tianyu Y.
    May. 4, 2011
    Tetris. Summative for ICS3U
    Controls: ¡û & ¡ú for movement; ¡ü for rotation.
"""
# I - IMPORT AND INITIALIZE 
import pygame, Sprites, random

pygame.init() 
pygame.key.set_repeat(100, 2)
screen = pygame.display.set_mode((480, 480)) 

def main():
    """ This function defines the mainline logic.
    """
    # DISPLAY 
    pygame.display.set_caption("Tetris. L.L") 
    
    pygame.mixer.music.load("./Music/Mint Lemon Tea.wav")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    gameQuit = False
    
    # Intro screen load
    intro()    
    # Call game loop
    while not gameQuit:
        gameQuit = game()
    
def intro():
    """ This function defines an intro loading image/animation.
    """
    intro = []
    for i in range(6):
        intro.append(pygame.image.load("./Pics/intro/start" + str(i) + ".jpg"))
        intro[i].convert()
        
    clock = pygame.time.Clock() 
    for i in range(6):
        clock.tick(15) 
        screen.blit(intro[i], (0, 0))
        pygame.display.flip()              
        if i == 0:
            pygame.time.delay(3000)
      
def game(): 
    """ This function defines the gaming portion.
        When the game ends, the player will be asked whether to continue.
        A boolean value is returned corresponding to the player's choice.
    """
    # ENTITIES 
    background = pygame.image.load("./Pics/background.jpg")
    over = pygame.image.load("./Pics/game over.jpg")
    previewSq = pygame.image.load("./Pics/preview.jpg")
    background = background.convert()
    previewSq = previewSq.convert()
    over = over.convert()
    
    background.blit(previewSq, (338, 20))    
    screen.blit(background, (0, 0))
    
    rotation = pygame.mixer.Sound("./Music/rotation.wav")
    rotation.set_volume(0.3)
    dropped = pygame.mixer.Sound("./Music/dropped.wav")
    dropped.set_volume(0.6)
    
    grid = []
    for i in range(10):
        grid.append([])
        for j in range(16):
            grid[i].append(0)
            
    squares = []
    for i in range(7):
        squares.append(pygame.image.load("./Pics/blocks/block" + str(i+1) + ".jpg"))
        squares[i].convert
    previews = []
    for i in range(7):
        previews.append(pygame.image.load("./Pics/previews/preview" + str(i+1) + ".jpg"))
        previews[i].convert
        
    # Sprites & Groups
    border = []
    for i in range(5):
        border.append(i)
        border[i] = Sprites.Border(screen, i+1)
    block = Sprites.Block(random.randint(1, 7))
    nextBlock = Sprites.Block(random.randint(1, 7))
    score = Sprites.ScoreKeeper()
    level = Sprites.LevelKeeper()
    startPauseButton = Sprites.StartPauseButton()
    resetButton = Sprites.ResetButton()
    muteButton = Sprites.MuteButton()
    
    allSprites = pygame.sprite.Group(border, score, level)
    buttonSprites = pygame.sprite.Group(startPauseButton, resetButton, muteButton)

    # ASSIGN
    clock = pygame.time.Clock() 
    keepGoing = True
    continuing = False
    forcedQuit = False
    
    # LOOP 
    while keepGoing: 
        # TIME 
        clock.tick(60) 
        # EVENT HANDLING
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                keepGoing = False
                forcedQuit = True
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if startPauseButton.rect.collidepoint(pygame.mouse.get_pos()):
                        if not muteButton.getMute():
                            dropped.play()
                        continuing = not continuing
                    elif resetButton.rect.collidepoint(pygame.mouse.get_pos()):
                        if not muteButton.getMute():
                            dropped.play()
                        return False
                    elif muteButton.rect.collidepoint(pygame.mouse.get_pos()):
                        muteButton.muteToggle()
                        if not muteButton.getMute():
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    block.rotate(grid)
                    rotation.play()
                if event.key == pygame.K_LEFT:
                    block.shiftLeft(grid)
                    if not muteButton.getMute():
                        rotation.play()
                if event.key == pygame.K_RIGHT:
                    block.shiftRight(grid)
                    if not muteButton.getMute():
                        rotation.play()
                if event.key == pygame.K_DOWN:
                    if block.drop(grid):
                        if not muteButton.getMute():
                            rotation.play()
                                
        # If tetromino stops falling, record block in grid, reset block at top,
        # add points, play sound.
        if not block.getDescending():
            for pos in block.positions:
                if pos.bottom < 9:
                    break
                grid[pos.left/31][(pos.bottom/31-15)*-1] = block.getType()
            block.reset(nextBlock.getType())
            nextBlock.reset(random.randint(1, 7))
            score.placement(level.getLevel())
            if not muteButton.getMute():
                dropped.play()
            pygame.key.set_repeat()
            pygame.key.set_repeat(100, 2)
            
        # Check for game over, i.e block filling height of window.
        for row in grid:
            if row[15]:
                keepGoing = False
                pygame.time.delay(1500)
                break
        if not keepGoing:
            break     
          
        # Tetris Detection, add points, delete row.
        if tetrisCheck(grid):
            score.tetris(len(tetrisCheck(grid)))
            for tetris in tetrisCheck(grid):
                for i in range(10):
                    del grid[i][tetris]
                    grid[i].append(0)
                
        # Check for level increase.
        if score.getScore() >= (level.getLevel()**1.5) * 1000 and \
           level.getLevel() < 10:
            level.levelUp()

        # REFRESH SCREEN 
        screen.blit(background, (0, 0))
        
        # Draw all existing blocks.
        for i in range(10):
            for j in range(15):
                if grid[i][j]:
                    screen.blit(squares[grid[i][j]-1], (i*31+5, 444-j*31))
                    
        # Draw preview.
        for pos in nextBlock.previews:
            screen.blit(previews[nextBlock.getType()-1], pos)
            
        # Update tetromino, draw.
        block.update(grid, level.getLevel())
        for pos in block.positions:
            screen.blit(squares[block.getType()-1], pos)
        
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)    
        buttonSprites.draw(screen)
        
        pygame.display.flip()
        
        # If game is paused (continuing = False), game will loop until game is
        # unpaused. Buttons and [X] can be clicked; keys will be ignored.
        while not continuing and keepGoing:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    keepGoing = False
                    forcedQuit = True
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if startPauseButton.rect.collidepoint(pygame.mouse.get_pos()):
                        if not muteButton.getMute():
                            dropped.play()
                        continuing = True
                    elif resetButton.rect.collidepoint(pygame.mouse.get_pos()):
                        if not muteButton.getMute():
                            dropped.play()
                        return False
                    elif muteButton.rect.collidepoint(pygame.mouse.get_pos()):
                        muteButton.muteToggle() 
                        buttonSprites.draw(screen)
                        pygame.display.flip()
                        if not muteButton.getMute():
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                            
    # If game was quitted via [x], game will not go through after screen.
    if forcedQuit:
        return True
                            
    # Game Over. Restart?
    # Yes = don't quit game, i.e return False. Vice versa.
    while True:
        clock.tick(60) 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return False
                if event.key == pygame.K_n:
                    pygame.quit()
                    return True
        screen.blit(over, (0, 0))
        pygame.display.flip()
    
def tetrisCheck(grid):
    """ Iterates through the gaming grid and detects a Tetris(full row of blocks).
        Parameter grid, the gaming grid.
        Returns a list of the rows full, that will be eliminated.
    """
    tetris = []
    for j in range(15):
        for i in range(10):
            if not grid[i][j]:
                break
            if i == 9:
                tetris.append(j)
    return tetris
    
# Call the main function 
main()