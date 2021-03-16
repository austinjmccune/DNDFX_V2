#Flask Imports
from flask import Flask, redirect,url_for,render_template,request
from flask_wtf import FlaskForm
from wtforms import SelectField

# XML imports
import xml.etree.ElementTree as ET
#spells xml file parsing
spells_tree = ET.parse('spells.xml')
spells_root = spells_tree.getroot()
#colors xml file parsing
colors_tree = ET.parse('colors.xml')
colors_root = colors_tree.getroot()

#Led contorl imports
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



def cast(spell,origin,grid,direction,dict):
    for x in spells_root.findall('spell'):
        if spell == x.find('name').text:
            name = x.find('name').text
            area = int(x.find('aoe').text)
            shape = x.find('shape').text
            damage_type = x.find('damage_type').text
            for y in colors_root.findall('color'):
                if damage_type == y.find('damage_type').text:
                    rgb = eval(y.find('rgb').text)

            if shape == 'cube' or shape == 'square' or shape == 'None':
                set_led(draw_cube(grid,origin,area),dict,rgb)
            elif shape == 'sphere' or shape == 'cylinder':
                glow_effect(draw_sphere(grid,origin,area),dict,rgb)
            elif shape == 'cone':
                set_led(draw_cone(grid,origin,area,direction),dict,rgb)
            elif shape == 'line':
                set_led(draw_line(grid,origin,area,direction),dict,rgb)

def remove_spell(spell,origin,grid,direction,dict):
    for x in spells_root.findall('spell'):
        if spell == x.find('name').text:
            name = x.find('name').text
            area = int(x.find('aoe').text)
            shape = x.find('shape').text
            damage_type = x.find('damage_type').text
            rgb = (0,0,0)

            if shape == 'cube' or shape == 'square' or shape == 'None':
                set_led(draw_cube(grid,origin,area),dict,rgb)
            elif shape == 'sphere' or shape == 'cylinder':
                set_led(draw_sphere(grid,origin,area),dict,rgb)
            elif shape == 'cone':
                set_led(draw_cone(grid,origin,area,direction),dict,rgb)
            elif shape == 'line':
                set_led(draw_line(grid,origin,area,direction),dict,rgb)

def assign_leds(grid):
    led_dict = {}
    rows = 12
    columns = 19
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
        try:
            pixels[dict[i]] = rgb
            pixels.show()
        except Exception:
            pass

def glow_effect(grid,dict,rgb):
    li = list(rgb)
    x = 0
    t_end = time.time() + 10
    while time.time() < t_end:
        while x < 3:
            for i in range(3):
                if li[i] - 10 > 0:
                    li[i] = round(li[i] - 10)
            rgb = tuple(li)
            for i in grid:
                pixels[dict[i]] = rgb
                pixels.show()
            time.sleep(0.4)
            x = x+1
        while x >= 0:
            for i in range(3):
                if li[i] + 10 <= 255 and li[i] > 0:
                    li[i] = li[i] + 10
            rgb = tuple(li)
            for i in grid:
                pixels[dict[i]] = rgb
                pixels.show()
            time.sleep(0.4)
            x = x-1

def expand_effect(grid,dict,rgb):
    for i in grid:
        pixels[dict[i]] = rgb
        pixels.show()
        time.sleep(.05)
    #glow_effect(grid,dict,rgb)




#functions to create a list for various shapes.

def draw_cube(grid,origin,area):
    tup = find_in_list_of_list(grid,origin)
    r , c = tup
    aoe = []
    if area == 5:
        try:
            aoe.append(grid[r][c])
        except Exception:
            print('out of bounds!')

    #elif area == 20:
        #for i in range(8):
          #  try:
          #      aoe.append(grid[r-4][c+3-i])
          #      aoe.append(grid[r-3][c+3-i])
         #       aoe.append(grid[r-2][c+3-i])
          #      aoe.append(grid[r-1][c+3-i])
          #      aoe.append(grid[r][c+3-i])
          #      aoe.append(grid[r+1][c+3-i])
          #      aoe.append(grid[r+2][c+3-i])
          #      aoe.append(grid[r+3][c+3-i])
          #  except Exception:
            #    print('out of bounds!')
            #    pass

    elif area == 10:
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

    elif area == 20:
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


    else:
        try:
            aoe.append(grid[r][c])
        except Exception:
            print('out of bounds!')

    #make a 100 ft cube (yikes)

    return aoe



def draw_sphere(grid,origin,area):
    tup = find_in_list_of_list(grid,origin)
    r , c = tup
    aoe = []
    if area == 20:
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
    #make a 15 ft sphere
    #make a 30 ft sphere
    #make a 40 ft sphere
    #make a 60 ft sphere
    #elif area == 20:
        #WORK ON THIS WHEN YOU GET A BIGGER BOARD. YOU WILL NEED TO MAKE IF 0 OR 7, ELIF 3 OR 4, ELSE LOGIC TO PRINT THE ROWS CORRECTLY.
       # for i in range(8):
          #  aoe.append(grid[r-4][c+3-i])
          #  aoe.append(grid[r-3][c+3-i])
         #   aoe.append(grid[r-2][c+3-i])
          #  aoe.append(grid[r-1][c+3-i])
          #  aoe.append(grid[r][c+3-i])
          #  aoe.append(grid[r+1][c+3-i])
          #  aoe.append(grid[r+2][c+3-i])
          #  aoe.append(grid[r+3][c+3-i])

    elif area == 10:
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
    else:
        try:
            aoe.append(grid[r][c])
        except Exception:
            print('out of bounds!')

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
        elif direction == 'nw' or direction == 'NW':
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
        elif direction == 'sw' or direction == 'SW':
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
        elif direction == 'se' or direction == 'SE':
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

    #need a bigger board to work on this. adding anyway
    elif area == 30:
        if direction == 'ne' or direction == 'NE':
            for square in (draw_cone(grid,origin,15,'ne')):
                aoe.append(square)
            for square in (draw_cone(grid,grid[r-1][c+1],15,'ne')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r - 3][c], 15, 'ne')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r][c + 3], 15, 'ne')):
                aoe.append(square)


        # North West Cone
        elif direction == 'nw' or direction == 'NW':
            for square in (draw_cone(grid,origin,15,'nw')):
                aoe.append(square)
            for square in (draw_cone(grid,grid[r-1][c-1],15,'nw')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r - 3][c], 15, 'nw')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r][c - 3], 15, 'nw')):
                aoe.append(square)
        # South West Cone
        elif direction == 'sw' or direction == 'SW':
            for square in (draw_cone(grid,origin,15,'sw')):
                aoe.append(square)
            for square in (draw_cone(grid,grid[r+1][c-1],15,'sw')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r + 3][c], 15, 'sw')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r][c - 3], 15, 'sw')):
                aoe.append(square)

        # South East Cone
        elif direction == 'se' or direction == 'SE':
            for square in (draw_cone(grid,origin,15,'se')):
                aoe.append(square)
            for square in (draw_cone(grid,grid[r+1][c+1],15,'se')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r + 3][c], 15, 'se')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r][c + 3], 15, 'se')):
                aoe.append(square)

    elif area == 60:
        if direction == 'ne' or direction == 'NE':
            for square in (draw_cone(grid, origin, 30, 'ne')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r - 6][c + 6], 30, 'sw')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r - 6][c], 30, 'ne')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r][c + 6], 30, 'ne')):
                aoe.append(square)


        # North West Cone
        elif direction == 'nw' or direction == 'NW':
            for square in (draw_cone(grid, origin, 30, 'nw')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r - 6][c - 6], 30, 'se')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r - 6][c], 30, 'nw')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r][c - 6], 30, 'nw')):
                aoe.append(square)
        # South West Cone
        elif direction == 'sw' or direction == 'SW':
            for square in (draw_cone(grid, origin, 30, 'sw')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r + 6][c - 6], 30, 'ne')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r + 6][c], 30, 'sw')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r][c - 6], 30, 'sw')):
                aoe.append(square)

        # South East Cone
        elif direction == 'se' or direction == 'SE':
            for square in (draw_cone(grid, origin, 30, 'se')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r + 6][c + 6], 30, 'nw')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r + 6][c], 30, 'se')):
                aoe.append(square)
            for square in (draw_cone(grid, grid[r][c + 6], 30, 'se')):
                aoe.append(square)


        else:
            try:
                aoe.append(grid[r][c])
            except Exception:
                print('out of bounds!')
        #make 30ft cone
        # make 60ft cone

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
            elif direction == 's' or direction == 'S':
                if r + i >= 0:
                    try:
                        aoe.append(grid[r + i][c])
                    except Exception:
                        print('out of bounds!')
                        pass

            elif direction == 'e' or direction == 'E':
                if c + i >= 0:
                    try:
                        aoe.append(grid[r][c + i])
                    except Exception:
                        print('out of bounds!')
                        pass

            elif direction == 'w' or direction == 'W':
                if c - i >= 0:
                    try:
                        aoe.append(grid[r][c - i])
                    except Exception:
                        print('out of bounds!')
                        pass

            elif direction == 'ne' or direction == 'NE':
                if r - i >= 0 and c + i >= 0:
                    try:
                        aoe.append(grid[r - i][c + i])
                    except Exception:
                        print('out of bounds!')
                        pass

            elif direction == 'nw' or direction == 'NW':
                if r - i >= 0 and c - i >= 0:
                    try:
                        aoe.append(grid[r - i][c - i])
                    except Exception:
                        print('out of bounds!')
                        pass

            elif direction == 'se' or direction == 'SE':
                if r + i >= 0 and c + i >= 0:
                    try:
                        aoe.append(grid[r + i][c + i])
                    except Exception:
                        print('out of bounds!')
                        pass

            elif direction == 'sw' or direction == 'SW':
                if r + i >= 0 and c - i >= 0:
                    try:
                        aoe.append(grid[r + i][c - i])
                    except Exception:
                        print('out of bounds!')
                        pass
            else:
                try:
                    aoe.append(grid[r][c])
                except Exception:
                    print('out of bounds!')


    return aoe

def kill_them_all():
    pixels.fill((0, 0, 0))
    pixels.show()

def make_grid(r):
    linea = []
    lineb = []
    linec = []
    lined = []
    linee = []
    linef = []
    lineg = []
    lineh = []
    linei = []
    linej = []
    linek = []
    linel = []

    #this is plus 2 because I am working with a rectangle at the moment.
    #testing ranges for off the board grid calls.
    for i in range(-7,r+9):

        linea.append("a{}".format(i))
        lineb.append("b{}".format(i))
        linec.append("c{}".format(i))
        lined.append("d{}".format(i))
        linee.append("e{}".format(i))
        linef.append("f{}".format(i))
        lineg.append("g{}".format(i))
        lineh.append("h{}".format(i))
        linei.append("i{}".format(i))
        linej.append("j{}".format(i))
        linek.append("k{}".format(i))
        linel.append("l{}".format(i))

    grid = []
    grid.append(list(linea))
    grid.append(list(lineb))
    grid.append(list(linec))
    grid.append(list(lined))
    grid.append(list(linee))
    grid.append(list(linef))
    grid.append(list(lineg))
    grid.append(list(lineh))
    grid.append(list(linei))
    grid.append(list(linej))
    grid.append(list(linek))
    grid.append(list(linel))

    return grid

def find_in_list_of_list(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return (mylist.index(sub_list), sub_list.index(char))
    raise ValueError("'{char}' is not in list".format(char = char))


grid = make_grid(4)
led_dict = assign_leds(grid)

#Start web functions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

li = []
for x in spells_root.findall('spell'):
    li.append(x.find('name').text)

counter = 0
active_spells = {}
@app.route("/", methods=['GET', 'POST'])
def home():
    form = Form()
    global counter
    global active_spells
    if request.method == 'POST':
        if "cast" in request.form:
            spell = str(form.spell.data)
            origin = str(form.origin.data)
            direction = str(form.direction.data)
            print(spell, origin)
            cast(spell,origin,grid,direction,led_dict)
            active_spells[counter]=[spell,origin,direction]
            counter = counter + 1
        elif "end" in request.form:
            kill_them_all()
            counter = 0
            active_spells.clear()
        for i in range(30):
            if str(i) in request.form:
                print(request.form)
                spell = active_spells[i][0]
                origin = active_spells[i][1]
                direction = active_spells[i][2]
                remove_spell(spell,origin,grid,direction,led_dict)
                del active_spells[i]

    return render_template("index.html", form=form, counter=counter, active_spells=active_spells)

class Form(FlaskForm):
    spell = SelectField('spell', choices= li, default='')
    origin = SelectField('origin', choices= [item for sublist in grid for item in sublist], default='')
    direction = SelectField('direction', choices=['','N','NE','NW','E','W','S','SE','SW'], default='')


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')





