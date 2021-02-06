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
            tup = find_in_list_of_list(grid,origin)
            one, two = tup
            grid[one][two] = 'x'
            print(grid)





def set_led(origin,area,shape,color):
    print("lights turned {} in a {} foot {} centered at {}!".format(color,area,shape,origin))

def make_grid(r):
    linea = []
    lineb = []
    linec = []
    lined = []
    for i in range(r):

        linea.append("a{}".format(i))
        lineb.append("b{}".format(i))
        linec.append("c{}".format(i))
        lined.append("d{}".format(i))


    grid = []
    grid.append(list(linea))
    grid.append(list(lineb))
    grid.append(list(linec))
    grid.append(list(lined))

    return grid

def find_in_list_of_list(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return (mylist.index(sub_list), sub_list.index(char))
    raise ValueError("'{char}' is not in list".format(char = char))

grid = make_grid(6)
spell = input('what spell do you want to cast?')
origin = input('where would you like to cast it?')
cast(spell,origin,grid)


