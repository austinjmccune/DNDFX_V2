import xml.etree.ElementTree as ET
my_tree = ET.parse('spells.xml')
my_root = my_tree.getroot()

import time
import board
import neopixel

pixel_pin = board.D10

# The number of NeoPixels
num_pixels = 24

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def cast(spell,origin,grid,dict):
    for x in my_root.findall('spell'):
        if spell == x.find('name').text:
            name = x.find('name').text
            area = int(x.find('area').text)
            shape = x.find('shape').text
            color = x.find('color').text
            set_led(draw_cube(grid,origin,area),dict)


def assign_leds(grid):
    led_dict = {}
    rows = 4
    columns = 6
    control_num = 0
    for i in range(rows):
        if i == 0:
            pass
        elif (i%2) == 0:
            control_num = control_num + 1
        else:
            control_num = control_num + 11

        for j in range(columns):
            if (i %2) == 0:
                led_dict[grid[i][j]] = control_num + j
            else:
                led_dict[grid[i][j]] = control_num - j
    return led_dict
def set_led(grid,dict):
    #print(grid)
    #print(dict)
    for i in grid:
        print(dict[i])
        pixels[dict[i]] = (0,255,0)
        pixels.show()
    #pixels[0] = (255,255,0)
    #pixels[1] = (255, 255, 0)
    #pixels[2] = (255, 255, 0)
    #pixels.show()
    #print("lights turned {} in a {} foot {} centered at {}!".format(color,area,shape,origin))



def draw_cube(grid,origin,area):
    tup = find_in_list_of_list(grid,origin)
    r , c = tup
    aoe = []
    if area == 10:
        for i in range(4):
            aoe.append(grid[r-2][c+1-i])
            aoe.append(grid[r+1][c+1-i])
            aoe.append(grid[r][c+1-i])
            aoe.append(grid[r-1][c+1-i])
    elif area == 20:
        for i in range(8):
            aoe.append(grid[r-4][c+3-i])
            aoe.append(grid[r-3][c+3-i])
            aoe.append(grid[r-2][c+3-i])
            aoe.append(grid[r-1][c+3-i])
            aoe.append(grid[r][c+3-i])
            aoe.append(grid[r+1][c+3-i])
            aoe.append(grid[r+2][c+3-i])
            aoe.append(grid[r+3][c+3-i])

    elif area == 5:
        aoe.append(grid[r][c])
        aoe.append(grid[r][c-1])
        aoe.append(grid[r-1][c-1])
        aoe.append(grid[r-1][c])

    return aoe


def make_grid(r):
    linea = []
    lineb = []
    linec = []
    lined = []
    #linee = []
    #linef = []
    #lineg = []
    #lineh = []
    #linei = []
    #linej = []
    #linek = []
    #linel = []

    #this is plus 2 because I am working with a rectangle at the moment.
    for i in range(r+2):

        linea.append("a{}".format(i))
        lineb.append("b{}".format(i))
        linec.append("c{}".format(i))
        lined.append("d{}".format(i))
        #linee.append("e{}".format(i))
       #linef.append("f{}".format(i))
        #lineg.append("g{}".format(i))
        #lineh.append("h{}".format(i))
        #linei.append("i{}".format(i))
        #linej.append("j{}".format(i))
        #linek.append("k{}".format(i))
        #linel.append("l{}".format(i))

    grid = []
    grid.append(list(linea))
    grid.append(list(lineb))
    grid.append(list(linec))
    grid.append(list(lined))
    #grid.append(list(linee))
    #grid.append(list(linef))
    #grid.append(list(lineg))
    #grid.append(list(lineh))
    #grid.append(list(linei))
    #grid.append(list(linej))
    #grid.append(list(linek))
    #grid.append(list(linel))

    return grid

def find_in_list_of_list(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return (mylist.index(sub_list), sub_list.index(char))
    raise ValueError("'{char}' is not in list".format(char = char))

grid = make_grid(4)
led_dict = assign_leds(grid)
spell = input('what spell do you want to cast?')
origin = input('where would you like to cast it?')
cast(spell,origin,grid,led_dict)




