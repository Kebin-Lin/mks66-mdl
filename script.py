import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    lightConstOps = {'box', 'sphere', 'torus'}

    print symbols
    for command in commands:
        currOp = command['op']
        args = command['args']
        constants = command['constants'] if 'constants' in command and command['constants'] in symbols else None
        areflect = []
        dreflect = []
        sreflect = []

        if currOp in lightConstOps and constants == None:
            constants = '.white'

        if currOp == 'push':
            stack.append( [x[:] for x in stack[-1]] )

        elif currOp == 'pop':
            stack.pop()

        elif currOp == 'move':
            t = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]

        elif currOp == 'rotate':
            theta = args[1] * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]

        elif currOp == 'scale':
            t = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]

        elif currOp == 'sphere':
            add_sphere(tmp, args[0], args[1], args[2], args[3], step_3d)
            matrix_mult(stack[-1], tmp)
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, constants)
            #polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []

        elif currOp == 'box':
            add_box(tmp, args[0], args[1], args[2], args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, constants)
            tmp = []

        elif currOp == 'torus':
            add_torus(tmp, args[0], args[1], args[2], args[3], args[4], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, constants)
            tmp = []

        elif currOp == 'line':
            add_edge( edges, args[0], args[1], args[2], args[3], args[4], args[5] )
            matrix_mult( stack[-1], edges )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []

        elif currOp == 'display' or currOp == 'save':
            if currOp == 'display':
                display(screen)
            else:
                save_extension(screen, args[0] + '.png')

        print command
