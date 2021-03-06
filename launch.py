# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/
 
# Import a library of functions called 'pygame'
import pygame, pygame.font, pygame.event, pygame.draw, string
from collections import defaultdict
import sys
from pygame.locals import *
import pygbutton
from psWrapper import PyWrapperPointSet
from time import gmtime
import box_disp
 


def main():
    # Initialize the game engine
    pygame.init()

    # Define the colors we will use in RGB format
    black = [  0,  0,  0]
    white = [255,255,255]
    blue =  [  0,  0,255]
    green = [  0,255,  0]
    red =   [255,  0,  0]
    DARKGRAY  = ( 64,  64,  64)
    GRAY      = (128, 128, 128)
    LIGHTGRAY = (212, 208, 200)
    N = 30000
    xpos = 50
    ypos = 550
    whichNonLin1 = 0
    whichNonLin2 = 0
    whichNonLin3 = 0
    whichNonLin4 = 0
    whichNonLin5 = 0
    whichNonLin6 = 0
    whichNonLin7 = 0
    whichNonLin8 = 0
    whichNonLin9 = 0
    whichNonLin10 = 0
    whichNonLin11 = 0
    whichNonLin12 = 0
    numLin = 10

    colorInc = 3

    width = 800
    height = 600

    current_string = [] # input string of number of linear transformations
    save_dir = "" # directory to save images
    # Create a button
    buttonGo = pygbutton.PygButton((width-155, 60, 50, 25), 'Go')
    # Create a button to save image
    buttonSave = pygbutton.PygButton((width-95, 60, 50, 25), 'Save')

    # Create 12 buttons to control the type of non linear transformations to use
    button1 = pygbutton.PygButton((50, 60, 25, 25), '1')
    button2 = pygbutton.PygButton((100, 60, 25, 25), '2')
    button3 = pygbutton.PygButton((150, 60, 25, 25), '3')
    button4 = pygbutton.PygButton((200, 60, 25, 25), '4')
    button5 = pygbutton.PygButton((250, 60, 25, 25), '5')
    button6 = pygbutton.PygButton((300, 60, 25, 25), '6')
    button7 = pygbutton.PygButton((350, 60, 25, 25), '7')
    button8 = pygbutton.PygButton((400, 60, 25, 25), '8')
    button9 = pygbutton.PygButton((450, 60, 25, 25), '9')
    button10 = pygbutton.PygButton((500, 60, 25, 25), '10')
    button11 = pygbutton.PygButton((550, 60, 25, 25), '11')
    button12 = pygbutton.PygButton((600, 60, 25, 25), '12')

    btnumlin = pygbutton.PygButton((50, 550, 20, 20), '')
    btNsim = pygbutton.PygButton((695, 550, 20, 20), '')
    btSaveDir = pygbutton.PygButton((width-80, 30, 20, 20), '')

    # Create a box for number of linear transformations
    

    # Define the colorCon : the function which controls the coloring behavior
    def linearStep(i):
        if i>1:
            y = 0
        elif i<0:
            y = 0
        elif i>=0.6667:
            y = 0   
        elif i<=0.3333:
            y = i*3
        else:
            y = (0.6667-i)*3
        return y

    def colorCon(i, colorCode):
        if colorCode==1:
            return (int)(linearStep(i)*255)
        elif colorCode==2:
            return (int)(linearStep(i-0.1667)*255)
        else:
            return (int)(linearStep(i-0.3333)*255)

    def callWrapper(wrapper, N, whichNonLin1, whichNonLin2,
                    whichNonLin3, whichNonLin4, whichNonLin5,
                    whichNonLin6, whichNonLin7, whichNonLin8,
                    whichNonLin9, whichNonLin10, whichNonLin11,
                    whichNonLin12, numLin):
        prePointsXY = []
        wrapper.go(N, whichNonLin1, whichNonLin2,
                whichNonLin3, whichNonLin4, whichNonLin5,
                whichNonLin6, whichNonLin7, whichNonLin8,
                whichNonLin9, whichNonLin10, whichNonLin11,
                whichNonLin12, numLin)
        pointsX = wrapper.getPointsX()
        pointsY = wrapper.getPointsY()
        calculated = True
        length = len(pointsX)
        # print len(pointsX)
        for i in range(len(pointsX)):
            prePointsXY.append( (pointsX[i]/4+0.5,pointsY[i]/4+0.5) )
        # Count the number of points near a hit point
        hitNumberXY = defaultdict(int)
        pointsXY = defaultdict(int)
        for (a,b) in prePointsXY:
            for j in range(colorInc):
                for k in range(colorInc):
                    hitNumberXY[((int)(a*width)+j,(int)(b*(height-100)+100+k))] +=1
            pointsXY[((int)(a*width),(int)(b*(height-100)+100))] = 1
        # print len(pointsXY.keys())
        color = []
        if len(hitNumberXY.values())!=0:
            maxHit = max(hitNumberXY.values())
            numberHits = range(maxHit)
            for i in numberHits:
                j = (float)(i+1)/(maxHit+1)/1.78+0.22
                # j = (float)(i+1)/(maxHit+1)/2+0.25
                color.append((colorCon(j,1),
                    colorCon(j,2),colorCon(j,3),j))
        # We return a dictionary with point position as keys
        # and color as value
        results = {}
        for (a,b) in pointsXY.keys():
            results[(a,b)] = color[hitNumberXY[(a,b)]-1]
        return results

    def buttonAction(button, state):
        state = 1 - state
        if state==1:
            button.bgcolor = GRAY
        else:
            button.bgcolor = LIGHTGRAY
        return state

    # Set the height and width of the screen
    size=[width,height]
    screen=pygame.display.set_mode(size)
     
    pygame.display.set_caption("Fractal Flame")
     
    #Loop until the user clicks the close button.
    done=False
    clock = pygame.time.Clock()
    calculated = False
    wrapper = PyWrapperPointSet()
    inputMode = False


    while done==False:
     
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick()
         
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
            
            # handle user input
            if event.type == KEYDOWN:
                # if the user presses escape, quit the event loop.
                if event.key == K_ESCAPE:
                    done=True
                elif event.key == K_1:
                    whichNonLin1 = buttonAction(button1,whichNonLin1)
                elif event.key == K_2:
                    whichNonLin2 = buttonAction(button2,whichNonLin2)
                elif event.key == K_3:
                    whichNonLin3 = buttonAction(button3,whichNonLin3)
                elif event.key == K_4:
                    whichNonLin4 = buttonAction(button4,whichNonLin4)
                elif event.key == K_5:
                    whichNonLin5 = buttonAction(button5,whichNonLin5)
                elif event.key == K_6:
                    whichNonLin6 = buttonAction(button6,whichNonLin6)
                elif event.key == K_7:
                    whichNonLin7 = buttonAction(button7,whichNonLin7)
                elif event.key == K_8:
                    whichNonLin8 = buttonAction(button8,whichNonLin8)
                elif event.key == K_9:
                    whichNonLin9 = buttonAction(button9,whichNonLin9)
                elif event.key == K_0:
                    whichNonLin10 = buttonAction(button10,whichNonLin10)
                elif event.key == K_MINUS:
                    whichNonLin11 = buttonAction(button11,whichNonLin11)
                elif event.key == K_EQUALS:
                    whichNonLin12 = buttonAction(button12,whichNonLin12)
                elif event.key == K_RETURN:
                    calculated=True
                    pointToDraw = callWrapper(wrapper, N, whichNonLin1, whichNonLin2,
                        whichNonLin3, whichNonLin4, whichNonLin5,
                        whichNonLin6, whichNonLin7, whichNonLin8,
                        whichNonLin9, whichNonLin10, whichNonLin11,
                        whichNonLin12, numLin)


            if 'click' in buttonGo.handleEvent(event):
                calculated=True
                pointToDraw = callWrapper(wrapper, N, whichNonLin1, whichNonLin2,
                    whichNonLin3, whichNonLin4, whichNonLin5,
                    whichNonLin6, whichNonLin7, whichNonLin8,
                    whichNonLin9, whichNonLin10, whichNonLin11,
                    whichNonLin12, numLin)

                
            if 'click' in buttonSave.handleEvent(event):
                clicktime = (list)(gmtime())
                filename = [save_dir]
                for i in clicktime:
                    filename.append(str(i))
                pygame.image.save(screen, "%s.png" % ''.join(filename))
                

            # Controls the behavior of the 12 buttons on non linear trans
            if 'click' in button1.handleEvent(event):
                whichNonLin1 = buttonAction(button1,whichNonLin1)
            if 'click' in button2.handleEvent(event):
                whichNonLin2 = buttonAction(button2,whichNonLin2)
            if 'click' in button3.handleEvent(event):
                whichNonLin3 = buttonAction(button3,whichNonLin3)
            if 'click' in button4.handleEvent(event):
                whichNonLin4 = buttonAction(button4,whichNonLin4)
            if 'click' in button5.handleEvent(event):
                whichNonLin5 = buttonAction(button5,whichNonLin5)
            if 'click' in button6.handleEvent(event):
                whichNonLin6 = buttonAction(button6,whichNonLin6)
            if 'click' in button7.handleEvent(event):
                whichNonLin7 = buttonAction(button7,whichNonLin7)
            if 'click' in button8.handleEvent(event):
                whichNonLin8 = buttonAction(button8,whichNonLin8)
            if 'click' in button9.handleEvent(event):
                whichNonLin9 = buttonAction(button9,whichNonLin9)
            if 'click' in button10.handleEvent(event):
                whichNonLin10 = buttonAction(button10,whichNonLin10)
            if 'click' in button11.handleEvent(event):
                whichNonLin11 = buttonAction(button11,whichNonLin11)
            if 'click' in button12.handleEvent(event):
                whichNonLin12 = buttonAction(button12,whichNonLin12)
                
            if 'click' in btnumlin.handleEvent(event):
                numLin = (int)(box_disp.test("number of linear"))
            if 'click' in btNsim.handleEvent(event):
                N = (int)(box_disp.test("number of initial points"))
            if 'click' in btSaveDir.handleEvent(event):
                save_dir = box_disp.test("directory to save image")

    

         # Display the box for inputs
 
                    
            
            

        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.
         
        # Clear the screen and set the screen background
        screen.fill(black)
        buttonGo.draw(screen)
        buttonSave.draw(screen)
        button1.draw(screen)
        button2.draw(screen)
        button3.draw(screen)
        button4.draw(screen)
        button5.draw(screen)
        button6.draw(screen)
        button7.draw(screen)
        button8.draw(screen)
        button9.draw(screen)
        button10.draw(screen)
        button11.draw(screen)
        button12.draw(screen)
        btnumlin.draw(screen)
        btNsim.draw(screen)
        btSaveDir.draw(screen)

        # Select the font to use. Default font, 25 pt size.
        font = pygame.font.Font(None, 25)
        screen.blit(font.render(str(numLin), 1, (255,255,255)),
                (75, 553))
        screen.blit(font.render(str(N), 1, (255,255,255)),
                (720, 553))

      
        if calculated:
            # # Draw points
            # drawnPoints = 0
            
            screen.blit(font.render(str(len(pointToDraw.keys())), 1, (255,255,255)),
                (390, 553))
            for (a,b) in pointToDraw.keys():
                # drawnPoints +=1
                pygame.draw.rect(screen,pointToDraw[(a,b)],[a,b,1,1],1)

     
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
     
    # Be IDLE friendly
    pygame.quit ()

main()
