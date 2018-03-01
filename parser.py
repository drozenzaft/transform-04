from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix - 
	    takes 6 arguments (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix - 
	 scale: create a scale matrix, 
	    then multiply the transform matrix by the scale matrix - 
	    takes 3 arguments (sx, sy, sz)
	 move: create a translation matrix, 
	    then multiply the transform matrix by the translation matrix - 
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
	 apply: apply the current transformation matrix to the 
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing

See the file script for an example of the file format
"""
#for converting negative and floating point numbers from strings to numbers
def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def isNegative(s):
    return s[0] == '-' and s[1:].isdigit()
          
def parse_file( fname, points, transform, screen, color ):
    f = open(fname,'r')
    f = f.read()
    g = f.split('\n')
    for c in range(len(g)):
        g[c] = g[c].split(' ')
        for k in range(len(g[c])):
            if g[c][k].isdigit():
                g[c][k] = int(g[c][k])
            elif isFloat(g[c][k]):
                g[c][k] = float(g[c][k])
            elif isNegative(g[c][k]):
                g[c][k] = int(g[c][k])*-1
    i = 0
    print g
    while i < len(g):
        if g[i][0] == 'line':
            i += 1
            add_edge(points,g[i][0],g[i][1],g[i][2],g[i][3],g[i][4],g[i][5])
        elif g[i][0] == 'ident':
            ident(transform)
        elif g[i][0] == 'scale':
            i += 1
            s = make_scale(g[i][0],g[i][1],g[i][2])
            matrix_mult(transform,s)
        elif g[i][0] == 'move':
            i += 1
            s = make_translate(g[i][0],g[i][1],g[i][2])
            matrix_mult(transform,s)
        elif g[i][0] == 'rotate':
            i += 1
            if g[i][0] == 'z':
                s = make_rotZ(g[i][1])
            elif g[i][0] == 'y':
                s = make_rotY(g[i][1])
            elif g[i][0] == 'x':
                s = make_rotX(g[i][1])
            matrix_mult(transform,s)
        elif g[i][0] == 'apply':
            matrix_mult(transform,points)
        elif g[i][0] == 'display':
            draw_lines(points,screen,color)
            display(screen)
        #save doesn't work at all
        elif g[i][0] == 'save':
            draw_lines(points,screen,color)
            i += 1
            h = open(g[i][0],'w')
            a = ''
            for x in screen:
                a += ' '.join(x) + '\n'
                print a
            h.write(a[:len(a)-2])
            h.close()
        i += 1
