#---------------------------[ animate_automata2d_pygame.py ]-----------------------
#
# I intend for this to be used to simulate the various cellular automata covered
# in Wolfram's book "A New Kind of Science".
#
# This script computes evolution steps and animates a 2-d cellular automaton.
# We are using pygame instead of matplotlib to make the graph.
#
#----------------------------------------------------------------------------------



#-----------------------------------[ IMPORTS ]------------------------------------

import sys
import numpy as np
import argparse
import pygame
from pygame import draw
from pygame import Rect as rect
import pygame.freetype

import automata_utils as au
from automata_utils import Automata2D

#----------------------------------[ CONSTANTS ]-----------------------------------

# Pygame settings
SCALE = 5
FRAMERATE = 60
SPEED = 1
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GRAY = 200, 200, 200
DARK_GRAY = 50, 50, 50

#----------------------------------[ FUNCTIONS ]-----------------------------------

# Function defining the arguments for this script
def parse_args():
    parser = argparse.ArgumentParser(description="Runs a 1-D Cellular Automata")
    parser.add_argument( '--width', type=int, dest='width', default=220 )
    parser.add_argument( '--height', type=int, dest='height', default=220 )
    parser.add_argument( '--init_custom', dest='init_custom', default=None )
    parser.add_argument( '--num_neighbors', dest='num_neighbors', default=8, 
            type=int )
    parser.add_argument( '--no-gridlines', dest='gridlines', default=True,
            action="store_false" )
    parser.add_argument( '--rule_num', dest='rule_num', default=746, type=int )
    parser.add_argument( '--num_steps', dest='num_steps', default=300, type=int )
    return parser.parse_args()

# Function for reading a file which describes the initial shape of the automaton
def get_init_shape():
    return 

# Function for initializing the pygame "board"
def init_pygame( width: int, height: int, rule_num: int ):
    
    # Initialize pygame
    pygame.init()

    # Set the caption
    caption = "2D Cellular Automata: Rule %d" % rule_num
    pygame.display.set_caption( caption )
    clock = pygame.time.Clock()

    # Calculate size of window
    window_width = width * SCALE
    window_height = height * SCALE
    screen = pygame.display.set_mode( (window_width, window_height) )

    return screen, clock

#-------------------------------------[ MAIN ]-------------------------------------

# The big cheese
def main():

    # Get those arguments
    args = parse_args()

    # Make the grid for the automaton
    # For simplicity, we'll initialize with a single 1 at the center
    grid = np.zeros( args.height * args.width ).reshape( args.height, args.width )
    grid[ args.height//2, args.width//2 ] = 1.0
    grid[ args.height//2, args.width//2-1 ] = 1.0
    grid[ args.height//2, args.width//2-2 ] = 1.0
    grid[ args.height//2, args.width//2-3 ] = 1.0
    grid[ args.height//2, args.width//2+1 ] = 1.0
    grid[ args.height//2, args.width//2+2 ] = 1.0
    grid[ args.height//2, args.width//2+3 ] = 1.0

    # Make the Automaton
    automaton = Automata2D( grid, args.num_steps )

    # Initialize pygame
    screen, clock = init_pygame( args.width, args.height, args.rule_num )
    frame = 0

    # Main Loop of pygame
    while True:

        # Process events
        for event in pygame.event.get():

            # Process Quit events
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:

                # [ESC]: quit
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

        # Update the frame number
        frame += 1

        # Set screen to white
        screen.fill( WHITE )

        # Draw gridlines, if wanted
        if args.gridlines:
            for i in range( args.width + 1 ):
                draw.line( screen, GRAY, (i * SCALE, 0), (i * SCALE, args.height * SCALE) )
            for i in range( args.height + 1 ):
                draw.line( screen, GRAY, (0, i * SCALE), (args.width * SCALE, i * SCALE ) )

        # Draw squares
        for i in range(args.width):
            for j in range(args.height):
                if automaton.cells[j, i] > 0:
                    draw.rect( screen, BLACK, rect(i * SCALE, j * SCALE, SCALE, SCALE))

        # Iterate the rules for the automaton
        if frame % SPEED == 0:
            automaton.apply_rule_X( args.rule_num, args.num_neighbors )

        # Limit framerate
        clock.tick(FRAMERATE)

        # Render the screen
        pygame.display.flip()

#-------------------------------------[ INIT ]-------------------------------------

if __name__ == "__main__":
    main()

#--------------------------------------[ END ]-------------------------------------
