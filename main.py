import xml.etree.ElementTree as ET
#spells xml file parsing
spells_tree = ET.parse('spells.xml')
spells_root = spells_tree.getroot()
#colors xml file parsing
colors_tree = ET.parse('colors.xml')
colors_root = colors_tree.getroot()

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
    for x in spells_root.findall('spell'):
        if spell == x.find('name').text:
            name = x.find('name').text
            area = int(x.find('area').text)
            shape = x.find('shape').text
            color = x.find('color').text
            for y in colors_root.findall('color'):
                if color == y.find('name').text:
                    rgb = eval(y.find('rgb').text)

            if shape == 'cube':
                glow_effect(draw_cube(grid,origin,area),dict,rgb)
            elif shape == 'sphere':
                glow_effect(draw_sphere(grid,origin,area),dict,rgb)
            elif shape == 'cone':
                direction = input("what direction?")
                set_led(draw_cone(grid,origin,area,direction),dict,rgb)
            elif shape == 'line':
                direction = input("what direction?")
                set_led(draw_line(grid,origin,area,direction),dict,rgb)


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

def set_led(grid,dict,rgb):
    for i in grid:
        print(dict[i])
        pixels[dict[i]] = rgb
        pixels.show()

def glow_effect(grid,dict,rgb):
    li = list(rgb)
    x = 0
    t_end = time.time() + 60
    while time.time() < t_end:
        while x < 3:
            for i in range(3):
                if li[i] - 10 > 0:
                    li[i] = round(li[i] - 10)
                    print(li[i])
            rgb = tuple(li)
            for i in grid:
                pixels[dict[i]] = rgb
                pixels.show()
            time.sleep(0.3)
            x = x+1
        while x >= 0:
            for i in range(3):
                if li[i] + 10 <= 255 and li[i] > 0:
                    li[i] = li[i] + 10
                    print(li[i])
            rgb = tuple(li)
            for i in grid:
                pixels[dict[i]] = rgb
                pixels.show()
            time.sleep(0.3)
            x = x-1





#functions to create a list for various shapes.

def draw_cube(grid,origin,area):
    tup = find_in_list_of_list(grid,origin)
    r , c = tup
    aoe = []
    if area == 10:
        for i in range(4):
            if (r-2 >= 0) and ((c + 1 - i) >= 0):
                try:
                    aoe.append(grid[r-2][c+1-i])
                except Exception:
                    print('out of bounds!')
                    pass
            if (r+1) and ((c+1 - i) >= 0):
                try:
                    aoe.append(grid[r+1][c+1-i])
                except Exception:
                    print('out of bounds!')
                    pass
            if ((c+1-i) >= 0 ):
                try:
                    aoe.append(grid[r][c+1-i])
                except Exception:
                    print('out of bounds!')
                    pass
            if ((r-1) >= 0 and ((c+1-i) >= 0)):
                try:
                    aoe.append(grid[r-1][c+1-i])
                except Exception:
                    print('out of bounds!')
                    pass
    elif area == 20:
        for i in range(8):
            try:
                aoe.append(grid[r-4][c+3-i])
                aoe.append(grid[r-3][c+3-i])
                aoe.append(grid[r-2][c+3-i])
                aoe.append(grid[r-1][c+3-i])
                aoe.append(grid[r][c+3-i])
                aoe.append(grid[r+1][c+3-i])
                aoe.append(grid[r+2][c+3-i])
                aoe.append(grid[r+3][c+3-i])
            except Exception:
                print('out of bounds!')
                pass

    elif area == 5:
        try:
            aoe.append(grid[r][c])
        except Exception:
            print('out of bounds!')
            pass
        if c-1 >= 0:
            try:
                aoe.append(grid[r][c-1])
            except Exception:
                print('out of bounds!')
                pass
        if r-1 >= 0 and c-1 >= 0:
            try:
                aoe.append(grid[r-1][c-1])
            except Exception:
                print('out of bounds!')
                pass
        if r-1 >= 0:
            try:
                aoe.append(grid[r-1][c])
            except Exception:
                print('out of bounds!')
                pass

    elif area == 0:
        aoe.append(grid[r][c])

    return aoe



def draw_sphere(grid,origin,area):
    tup = find_in_list_of_list(grid,origin)
    r , c = tup
    aoe = []
    if area == 10:
        for i in range(4):
            if (i == 0) or (i == 3):
                if (c + 1 - i) >= 0:
                    try:
                        aoe.append(grid[r][c + 1 - i])
                    except Exception:
                        print('out of bounds!')
                        pass
                if r - 1 and (c + 1 - i) >= 0:
                    try:
                        aoe.append(grid[r - 1][c + 1 - i])
                    except Exception:
                        print('out of bounds!')
                        pass
            else:
                if r - 2 >= 0 and (c + 1 - i) >= 0:
                    try:
                        aoe.append(grid[r-2][c+1-i])
                    except Exception:
                        print('out of bounds!')
                        pass
                if r + 1 >= 0 and (c + 1 - i) >= 0:
                    try:
                        aoe.append(grid[r+1][c+1-i])
                    except Exception:
                        print('out of bounds!')
                        pass
                if (c + 1 - i) >= 0:
                    try:
                        aoe.append(grid[r][c+1-i])
                    except Exception:
                        print('out of bounds!')
                        pass
                if r - 1 >= 0 and (c + 1 - i) >= 0:
                    try:
                        aoe.append(grid[r-1][c+1-i])
                    except Exception:
                        print('out of bounds!')
                        pass
    elif area == 20:
        #WORK ON THIS WHEN YOU GET A BIGGER BOARD. YOU WILL NEED TO MAKE IF 0 OR 7, ELIF 3 OR 4, ELSE LOGIC TO PRINT THE ROWS CORRECTLY.
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
        try:
            aoe.append(grid[r][c])
        except Exception:
            print('out of bounds!')
            pass
        if c-1 >= 0:
            try:
                aoe.append(grid[r][c-1])
            except Exception:
                print('out of bounds!')
                pass
        if r-1 >= 0 and c-1 >= 0:
            try:
                aoe.append(grid[r-1][c-1])
            except Exception:
                print('out of bounds!')
                pass
        if r-1 >= 0:
            try:
                aoe.append(grid[r-1][c])
            except Exception:
                print('out of bounds!')
                pass

    return aoe


def draw_cone(grid,origin,area,direction):
    tup = find_in_list_of_list(grid,origin)
    r , c = tup
    aoe = []
    #North East Cone
    if area == 15:
        if direction == 'ne' or direction == 'NE':
            for i in range(1,4):
                if r - i >= 0:
                    try:
                        aoe.append(grid[r - i ][c])
                    except Exception:
                        print('out of bounds!')
                        pass
                if r - 2 >= 0 and (c + i - 1) >= 0 and i < 3:
                    try:
                        aoe.append(grid[r - 2][c + i - 1])
                    except Exception:
                        print('out of bounds!')
                        pass
                if r - 1 >= 0 and (c + i - 1) >= 0:
                    try:
                        aoe.append(grid[r-1][c + i -1])
                    except Exception:
                        print('out of bounds!')
                        pass
        #North West Cone
        if direction == 'nw' or direction == 'NW':
            for i in range(1,4):
                if r - 1 >= 0 and c - i >=0:
                    try:
                        aoe.append(grid[r - 1 ][c - i])
                    except Exception:
                        print('out of bounds!')
                        pass
                if r - 2 >= 0 and (c - i) >= 0 and i < 3:
                    try:
                        aoe.append(grid[r - 2][c - i])
                    except Exception:
                        print('out of bounds!')
                        pass
                if r - 3 >= 0 and (c - 1) >= 0 and i == 1:
                    try:
                        aoe.append(grid[r-3][c - 1])
                    except Exception:
                        print('out of bounds!')
                        pass
        #South West Cone
        if direction == 'sw' or direction == 'SW':
            for i in range(1,4):
                if c - i >= 0:
                    try:
                        aoe.append(grid[r][c - i])
                    except Exception:
                        print('out of bounds!')
                        pass
                if (r + i -1) >= 0 and (c - 1) >= 0:
                    try:
                        aoe.append(grid[r + i - 1][c - 1])
                    except Exception:
                        print('out of bounds!')
                        pass
                if r + 1 >= 0 and (c - 2) >= 0 and i == 1:
                    try:
                        aoe.append(grid[r + 1][c - 2])
                    except Exception:
                        print('out of bounds!')
                        pass

        # South East Cone
        if direction == 'se' or direction == 'SE':
            for i in range(1,3):
                if i == 1:
                    try:
                        aoe.append(grid[r][c])
                    except Exception:
                        print('out of bounds!')
                        pass
                    if r + i >= 0 and c + i >= 0:
                        try:
                            aoe.append(grid[r + i][c + i])
                        except Exception:
                            print('out of bounds!')
                            pass
                if (c + i) >= 0 and i < 3:
                    try:
                        aoe.append(grid[r][c + i])
                    except Exception:
                        print('out of bounds!')
                        pass
                if r + 1 >= 0:
                    try:
                        aoe.append(grid[r + i][c])
                    except Exception:
                        print('out of bounds!')
                        pass
                if r + i >= 0:
                    try:
                        aoe.append(grid[r + i][c])
                    except Exception:
                        print('out of bounds!')
                        pass

    return aoe

def draw_line(grid,origin,area,direction):
    tup = find_in_list_of_list(grid,origin)
    r , c = tup
    aoe = []
    if area == 30:
        for i in range(1,6):
            if direction == 'n' or direction == 'N':
                if r - i >= 0:
                    try:
                        aoe.append(grid[r - i][c])
                    except Exception:
                        print('out of bounds!')
                        pass
            if direction == 's' or direction == 'S':
                if r + i >= 0:
                    try:
                        aoe.append(grid[r + i][c])
                    except Exception:
                        print('out of bounds!')
                        pass

            if direction == 'e' or direction == 'E':
                if c + i >= 0:
                    try:
                        aoe.append(grid[r][c + i])
                    except Exception:
                        print('out of bounds!')
                        pass

            if direction == 'w' or direction == 'W':
                if c - i >= 0:
                    try:
                        aoe.append(grid[r][c - i])
                    except Exception:
                        print('out of bounds!')
                        pass

            if direction == 'ne' or direction == 'NE':
                if r - i >= 0 and c + i >= 0:
                    try:
                        aoe.append(grid[r - i][c + i])
                    except Exception:
                        print('out of bounds!')
                        pass

            if direction == 'nw' or direction == 'NW':
                if r - i >= 0 and c - i >= 0:
                    try:
                        aoe.append(grid[r - i][c - i])
                    except Exception:
                        print('out of bounds!')
                        pass

            if direction == 'se' or direction == 'SE':
                if r + i >= 0 and c + i >= 0:
                    try:
                        aoe.append(grid[r + i][c + i])
                    except Exception:
                        print('out of bounds!')
                        pass

            if direction == 'sw' or direction == 'SW':
                if r + i >= 0 and c - i >= 0:
                    try:
                        aoe.append(grid[r + i][c - i])
                    except Exception:
                        print('out of bounds!')
                        pass



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
while True:
    spell = input('what spell do you want to cast?')
    origin = input('where would you like to cast it?')
    cast(spell,origin,grid,led_dict)




