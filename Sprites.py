""" Tianyu Y.
    May. 4, 2011
    Tetris module. Summative for ICS3U
"""

import pygame

class Border(pygame.sprite.Sprite): 
    """ Border Sprite. Does not update.
    """
    def __init__(self, screen, type): 
        """ Borderlining for game grid and game window. 
            Parameter screen, type an integer, specifying which border it is.
            Type 1 = Top horizontal, 2 = Bottom horizontal, 3 = Left vertical,
            4 = Middle vertical, 5 = Right vertical. 
        """
        # Call the parent __init__() method 
        pygame.sprite.Sprite.__init__(self) 
          
        # Depending on type, create corresponding rectangle.
        # Set rect attr.
        if type == 1:
            self.image = pygame.Surface((screen.get_width(), 5)) 
            self.rect = self.image.get_rect() 
            self.rect.left = 0
            self.rect.top = 0
        elif type == 2:
            self.image = pygame.Surface((screen.get_width(), 5)) 
            self.rect = self.image.get_rect() 
            self.rect.left = 0
            self.rect.bottom = screen.get_height()
        elif type == 3:
            self.image = pygame.Surface((5, screen.get_width())) 
            self.rect = self.image.get_rect() 
            self.rect.left = 0
            self.rect.top = 0
        elif type == 4:
            self.image = pygame.Surface((5, screen.get_width())) 
            self.rect = self.image.get_rect() 
            self.rect.right = 319
            self.rect.top = 0
        elif type == 5:
            self.image = pygame.Surface((5, screen.get_width())) 
            self.rect = self.image.get_rect() 
            self.rect.right = screen.get_width()
            self.rect.top = 0
            
        self.image = self.image.convert() 
        self.image.fill((255, 255, 255))
        
class ScoreKeeper(pygame.sprite.Sprite): 
    """ Score Keeping Label Sprite.
    """
    def __init__(self): 
        """ Creates label, displaying score.
            No parameters.
        """
        # Call the parent __init__() method 
        pygame.sprite.Sprite.__init__(self) 
  
        # Load our custom font, and initialize the starting score. 
        self.__font = pygame.font.Font("Cicle Fina.ttf", 18)  
        self.__score = 0
        
    def placement(self, level):
        """ Adds to the opints total when a block is placed, according to the 
            current level.
            Parameter level integer, representing the level.
        """
        self.__score += (20 + 10 * level)
          
    def tetris(self, tetris): 
        """ Adds to the points total according to the no. of tetris achieved at once,
            Parameter tetris integer, representing such no.
        """
        for i in range(tetris):
            self.__score += (i + 1) / 2.0 * 1000
            
    def getScore(self):
        """ Returns the current score.
        """
        return self.__score
  
    def update(self): 
        """ Automatically display current score in right of the screen.
        """
        message = "Score: %d" %(self.__score)
        self.image = self.__font.render(message, 1, (255, 0, 255)) 
        self.rect = self.image.get_rect() 
        self.rect.left = 365
        self.rect.top = 160
        
class LevelKeeper(pygame.sprite.Sprite):
    """ Level Keeping Label Sprite.
    """
    def __init__(self):
        """ Creates label, displaying label.
        """
        # Call the parent __init__() method 
        pygame.sprite.Sprite.__init__(self) 
  
        # Load our custom font, and initialize the starting score. 
        self.__font = pygame.font.Font("Cicle Fina.ttf", 18)  
        self.__level = 1
        
    def levelUp(self):
        """ Increases the level by 1.
        """
        self.__level += 1
        
    def getLevel(self):
        """ Returns the level.
        """
        return self.__level
        
    def update(self): 
        """ Automatically display current level in right of the screen.
        """
        message = "Level: %d" %(self.__level)
        self.image = self.__font.render(message, 2, (255, 0, 255)) 
        self.rect = self.image.get_rect() 
        self.rect.left = 365
        self.rect.top = 185
        
# The three button sprites will be used for collision detection only.
class StartPauseButton(pygame.sprite.Sprite):
    """ Start/Pause Button Sprite.
    """
    def __init__(self):
        """ Creates Button.
        """
        # Call the parent __init__() method 
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.image.load("./Pics/buttons/startpause.jpg")
        self.rect = self.image.get_rect()
        self.rect.left = 349
        self.rect.top = 225
        
class ResetButton(pygame.sprite.Sprite):
    """ Reset Button Sprite.
    """
    def __init__(self):
        """ Creates Button.
        """
        # Call the parent __init__() method 
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.image.load("./Pics/buttons/reset.jpg")
        self.rect = self.image.get_rect()
        self.rect.left = 349
        self.rect.top = 260
        
class MuteButton(pygame.sprite.Sprite):
    """ Mute Button Sprite.
    """
    def __init__(self):
        """ Creates Button.
        """
        # Call the parent __init__() method 
        pygame.sprite.Sprite.__init__(self) 
        
        self.__pics = [pygame.image.load("./Pics/mute.gif"),\
                       pygame.image.load("./Pics/unmute.gif")]
        self.image = self.__pics[1]
        self.rect = self.image.get_rect()
        self.rect.left = 440
        self.rect.top = 450
        self.__mute = False
        
    def muteToggle(self):
        """ Toggles the mute image.
        """
        self.__mute = not self.__mute
        if self.__mute:
            self.image = self.__pics[0]
        else:
            self.image = self.__pics[1]
        
    def getMute(self):
        """ Returns the mute attribute.
        """
        return self.__mute

class Block(pygame.sprite.Sprite): 
    """ Block Sprite.
    """
    def __init__(self, type):
        """ Creates a tetromino, composed of four square blocks.
            Parameter type indicates 1 of 7 type of tetrominoes.
            Seven tetromino types: Type representation(# of rotation statuses) 
            O(1), I(2), Z(2), S(2), L(4), J(4), T(4)
            type: 1 = O; 2 = I; 3 = Z; 4 = S; 5 = L; 6 = J; 7 = T
            
            470*310 game grid, 10*15 blocks. Blocks 31*31
        """
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        self.__descending = True
        self.__status = 1 
        self.__timer = 0
        self.__speed = 30
        self.__level = 1
        
        self.reset(type)
            
    def shiftLeft(self, grid):
        """ Attempts to shift the tetromino to its left.
        """
        # No shift conditions. 
        # Determines whether it is at the left edge of screen.
        for pos in self.positions:
            if pos.left <= 5:
                return
            if pos.bottom <= 9:
                return
            # Determines whether an existing block is to its immediate left.
            if grid[pos.left/31-1][(pos.bottom/31-15)*-1]:
                return
        # Shift
        for pos in self.positions:
            pos.left -= 31
        
    def shiftRight(self, grid):
        """ Attempts to shift the tetromino to its right.
        """
        # No shift conditions. 
        # Determines whether it is at the left edge of screen.
        for pos in self.positions:
            if pos.right >= 314:
                return
            if pos.bottom <= 9:
                return
            # Determines whether an existing block is to its immediate right.
            if grid[pos.left/31+1][(pos.bottom/31-15)*-1]:
                return
        # Shift
        for pos in self.positions:
            pos.left += 31
            
    def drop(self, grid):
        """ Moves the block down. Uses same check mechanism as update.
        """
        # Check that all blocks are in appropriate positionings.
        for pos in self.positions:
            if pos.bottom >= 473:
                self.__descending = False
                return
            if pos.bottom < 9:
                break
            if grid[pos.left/31][((pos.bottom/31-15)*-1)-1]:
                self.__descending = False
                return
        # Drop
        for pos in self.positions:
            pos.top += 31
            
        return True

    def getDescending(self):
        """ Returns the descending attribute.
        """
        return self.__descending
    
    def getType(self):
        """ Returns the type attribute.
        """
        return self.__type
        
    def update(self, grid, level):
        """ Determines whether the tetromino should stop dropping, drop, or 
            wait until an appropriate time to drop.
            Parameter grid game grid, level current level, which will change the 
            speed of block drops.
        """ 
        for pos in self.positions:
            # Determines whether the tetromino reaches the bottom.
            if pos.bottom >= 474:
                self.__descending = False
                return
            # Determines whether the tetromino stacks on another block.
            if pos.bottom < 9:
                break
            if grid[pos.left/31][((pos.bottom/31-15)*-1)-1]:
                self.__descending = False
                return
        
        # Check for level up, speed increase.
        if level > self.__level:
            self.__level += 1
            self.__speed -= 1
            
        # Keeps track of time for drop and drops when appropriate.
        self.__timer += 1
        if self.__timer == self.__speed:
            for pos in self.positions:
                pos.top += 31
            self.__timer = 0
            
    def rotate(self, grid):
        """ Rotates the tetromino, according to the type and status. The status
            will increase by 1, until it reaches the max. possible status, by which
            it'll return to 1.
            *O Shape has no other states. All rotations are clockwise.
            
            Seven tetromino types: Type representation(# of rotation statuses)
            O(1), I(2), Z(2), S(2), L(4), J(4), T(4)
            type: 1 = O; 2 = I; 3 = Z; 4 = S; 5 = L; 6 = J; 7 = T
        """ 
        
        if self.__type == 1:
            return
        elif self.__type == 2:
            if self.__status == 1:
                if self.positions[1].right > 253 or self.positions[1].left < 35:
                    return
                self.positions[0] = self.positions[0].move(62, -31)
                self.positions[2] = self.positions[2].move(31, 31)
                self.positions[3] = self.positions[3].move(-31, 62)
                self.__status = 2
            else:
                if self.positions[1].bottom > 443:
                    return
                self.positions[0] = self.positions[0].move(-62, 31)
                self.positions[2] = self.positions[2].move(-31, -31)
                self.positions[3] = self.positions[3].move(31, -62)
                self.__status = 1
        elif self.__type == 3:
            if self.__status == 1:
                self.positions[0] = self.positions[0].move(62, -31)
                self.positions[3] = self.positions[3].move(0, -31)
                self.__status = 2
            else:
                if self.positions[2].left < 34:
                    return
                self.positions[0] = self.positions[0].move(-62, 31)
                self.positions[3] = self.positions[3].move(0, 31)
                self.__status = 1
        elif self.__type == 4:
            if self.__status == 1:
                self.positions[0] = self.positions[0].move(31, -62)
                self.positions[1] = self.positions[1].move(31, 0)
                self.__status = 2
            else:
                if self.positions[2].left < 34:
                    return
                self.positions[0] = self.positions[0].move(-31, 62)
                self.positions[1] = self.positions[1].move(-31, 0)
                self.__status = 1
        elif self.__type == 5:
            if self.__status == 1:
                if self.positions[3].right > 285:
                    return
                self.positions[0] = self.positions[0].move(31, -62)
                self.positions[3] = self.positions[3].move(31, -62)
                self.__status = 2
            elif self.__status == 2:
                self.positions[1] = self.positions[1].move(62, 31)
                self.positions[2] = self.positions[2].move(62, 31)
                self.__status = 3
            elif self.__status == 3:
                if self.positions[0].left < 31:
                    return
                self.positions[0] = self.positions[0].move(-31, 62)
                self.positions[3] = self.positions[3].move(-31, 62)
                self.__status = 4
            elif self.__status == 4:
                self.positions[1] = self.positions[1].move(-62, -31)
                self.positions[2] = self.positions[2].move(-62, -31)
                self.__status = 1
        elif self.__type == 6:
            if self.__status == 1:
                if self.positions[0].left < 31:
                    return
                self.positions[2] = self.positions[2].move(-62, 31)
                self.positions[3] = self.positions[3].move(-62, 31)
                self.__status = 2
            elif self.__status == 2:
                self.positions[0] = self.positions[0].move(-31, -62)
                self.positions[1] = self.positions[1].move(-31, -62)
                self.__status = 3
            elif self.__status == 3:
                if self.positions[1].right > 310:
                    return
                self.positions[2] = self.positions[2].move(62, -31)
                self.positions[3] = self.positions[3].move(62, -31)
                self.__status = 4
            elif self.__status == 4:
                self.positions[0] = self.positions[0].move(31, 62)
                self.positions[1] = self.positions[1].move(31, 62)
                self.__status = 1
        elif self.__type == 7:
            if self.__status == 1:
                self.positions[1] = self.positions[1].move(-31, -31)
                self.positions[3] = self.positions[3].move(-62, -62)
                self.__status = 2
            elif self.__status == 2:
                if self.positions[2].right > 285:
                    return
                self.positions[0] = self.positions[0].move(62, -62)
                self.positions[1] = self.positions[1].move(31, -31)
                self.__status = 3
            elif self.__status == 3:
                self.positions[1] = self.positions[1].move(31, 31)
                self.positions[3] = self.positions[3].move(62, 62)
                self.__status = 4
            elif self.__status == 4:
                if self.positions[2].left < 35:
                    return
                self.positions[0] = self.positions[0].move(-62, 62)
                self.positions[1] = self.positions[1].move(-31, 31)
                self.__status = 1
            
    def reset(self, type):
        """ Resets the tetromino at the top of the screen, with a new type.
        """ 
        self.__type = type
        self.__status = 1 
        self.__descending = True
        
        if self.__type == 1:
            self.positions = [pygame.Rect(129, -21, 31, 31), pygame.Rect(129, -52, 31, 31),\
                              pygame.Rect(160, -21, 31, 31), pygame.Rect(160, -52, 31, 31)]
            self.previews = [pygame.Rect(374, 110, 25, 25), pygame.Rect(374, 85, 25, 25),\
                             pygame.Rect(399, 110, 25, 25), pygame.Rect(399, 85, 25, 25)]
        elif self.__type == 2:
            self.positions = [pygame.Rect(129, -21, 31, 31), pygame.Rect(129, -52, 31, 31),\
                              pygame.Rect(129, -83, 31, 31), pygame.Rect(129, -114, 31, 31)]
            self.previews = [pygame.Rect(386, 110, 25, 25), pygame.Rect(386, 85, 25, 25),\
                             pygame.Rect(386, 60, 25, 25), pygame.Rect(386, 35, 25, 25)]
        elif self.__type == 3:
            self.positions = [pygame.Rect(98, -52, 31, 31), pygame.Rect(129, -21, 31, 31),\
                              pygame.Rect(129, -52, 31, 31), pygame.Rect(160, -21, 31, 31)]
            self.previews = [pygame.Rect(361, 85, 25, 25), pygame.Rect(386, 110, 25, 25),\
                             pygame.Rect(386, 85, 25, 25), pygame.Rect(411, 110, 25, 25)]
        elif self.__type == 4:
            self.positions = [pygame.Rect(98, -21, 31, 31), pygame.Rect(129, -21, 31, 31),\
                              pygame.Rect(129, -52, 31, 31), pygame.Rect(160, -52, 31, 31)]
            self.previews = [pygame.Rect(361, 110, 25, 25), pygame.Rect(386, 110, 25, 25),\
                             pygame.Rect(386, 85, 25, 25), pygame.Rect(411, 85, 25, 25)]
        elif self.__type == 5:
            self.positions = [pygame.Rect(129, -21, 31, 31), pygame.Rect(129, -52, 31, 31),\
                              pygame.Rect(129, -83, 31, 31), pygame.Rect(160, -21, 31, 31),]
            self.previews = [pygame.Rect(374, 110, 25, 25), pygame.Rect(374, 85, 25, 25),\
                             pygame.Rect(374, 60, 25, 25), pygame.Rect(399, 110, 25, 25)]
        elif self.__type == 6:
            self.positions = [pygame.Rect(129, -21, 31, 31), pygame.Rect(160, -21, 31, 31),\
                              pygame.Rect(160, -52, 31, 31), pygame.Rect(160, -83, 31, 31),]
            self.previews = [pygame.Rect(374, 110, 25, 25), pygame.Rect(399, 110, 25, 25),\
                             pygame.Rect(399, 85, 25, 25), pygame.Rect(399, 60, 25, 25)]
        elif self.__type == 7:
            self.positions = [pygame.Rect(98, -21, 31, 31), pygame.Rect(129, -21, 31, 31),\
                              pygame.Rect(129, -52, 31, 31), pygame.Rect(160, -21, 31, 31)]
            self.previews = [pygame.Rect(361, 110, 25, 25), pygame.Rect(386, 110, 25, 25),\
                             pygame.Rect(386, 85, 25, 25), pygame.Rect(411, 110, 25, 25)]
       