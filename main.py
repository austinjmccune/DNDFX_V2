import xml.etree.ElementTree as ET
my_tree = ET.parse('spells.xml')
my_root = my_tree.getroot()
''''
for x in my_root.findall('spell'):
    name = x.find('name').text
    area = int(x.find('area').text)
    shape = x.find('shape').text
    color = x.find('color').text
    print(name)
    print(area)
    print(shape)
    print(color)
    print("the spell name is {}".format(name))
'''

def cast(spell,origin,grid):
    for x in my_root.findall('spell'):
        if spell == x.find('name').text:
            name = x.find('name').text
            area = int(x.find('area').text)
            shape = x.find('shape').text
            color = x.find('color').text
            set_led(origin,area,shape,color)
            draw_cube(grid,origin,area)


def set_led(origin,area,shape,color):
    print("lights turned {} in a {} foot {} centered at {}!".format(color,area,shape,origin))



def draw_cube(grid,origin,area):
    tup = find_in_list_of_list(grid,origin)
    r , c = tup
    if area == 10:
        grid[r][c] = 'x'
        for i in range(2):
            grid[r+i][c] = 'x'
            grid[r][c+i] = 'x'
            grid[r+i][c+i] = 'x'
            grid[r-i][c] = 'x'
            grid[r][c-i] = 'x'
            grid[r-i][c-i] = 'x'
    elif area == 20:
        grid[r][c] = 'x'
        grid[r+1][c] = 'x'
        grid[r][c+1] = 'x'
        grid[r+1][c+1] = 'x'

    elif area == 5:
        a = 2
        grid[r][c] = 'x'
        grid[r][c-1] = 'x'
        grid[r-1][c-1] = 'x'
        grid[r-1][c] = 'x'
           #grid[r-2][c-1+i] = 'x'
           #grid[r+1][c-1+i] = 'x'
           # grid[r-2+i][c-1] = 'x'
           # grid[r-2+i][c+2] = 'x'
           # grid[r-1][c-1+i] = 'x'
           # grid[r-1][c+1+i] = 'x'






    for i in range(12):
        print(grid[i])

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
    for i in range(r):

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

grid = make_grid(12)
spell = input('what spell do you want to cast?')
origin = input('where would you like to cast it?')
cast(spell,origin,grid)


