from graphics import *
from random import randint
from math import sqrt, atan, sin, cos, pi

white = color_rgb(255, 255, 255)
red = color_rgb(255, 0, 0)
green = color_rgb(124,252,0)

class Node:

    def __init__(self, text, rad, x=0, y=0):

        self.center = Point(x, y)
        self.radius = rad
        self.circle = Circle(self.center, self.radius)

        self.text = Text(self.center, text)

        self.color = None

    def print_node(self, window):
        self.circle.draw(window)
        self.text.draw(window)

    def get_center(self):
        return self.center

    def get_text(self):
        return self.text.getText()

    def set_color(self, r, g, b):
        self.color = color_rgb(r, g, b)
        self.circle.setFill(self.color)

class Arrow:

    def __init__(self, start, finish, value, direction, angle):

        self.line = Line(start, finish)
        self.line.setArrow(direction)
        self.arrow_color = white
        self.line.setFill(self.arrow_color)

        self.center = self.line.getCenter()
        self.angle = angle
        text_pos = Point(self.center.getX() - cos(self.angle + pi / 2) * 20, self.center.getY() - sin(self.angle + pi / 2) * 20)

        self.text = Text(text_pos, value)
        self.text.setFill(self.arrow_color)

        self.nodes = ("", "")

    def set_nodes(self, start, finish):
        self.nodes = (start, finish)

    def print_arrow(self, window):
        self.line.draw(window)
        self.text.draw(window)

    def unprint_arrow(self):
        self.line.undraw()
        self.text.undraw()

    def set_color(self, value):
        self.arrow_color = value
        self.line.setFill(self.arrow_color)

class Reader:
    def __init__(self, point, length):
        self.entry = Entry(point, length)

    def get_input(self):
        return  self.entry.getText()

    def set_text(self, text):
        return self.entry.setText(text)

    def print_reader(self, win):
        return self.entry.draw(win)

class WindowObject:
    def __init__(self, name, width, height):

        value = randint(30, 70)
        self.background_color = color_rgb(value, value, value)

        self.width = width
        self.height = height
        self.win = GraphWin(name, width, height)
        self.win.setBackground(self.background_color)

        self.nodeList = []
        self.arrowList = []

        self.infoText = Text(Point(self.width / 2, self.height - 30), "")
        self.infoText.setTextColor(white)
        self.infoText.setSize(15)

        self.entry = Reader(Point(self.width / 2, 30), 20)
        self.entry.print_reader(self.win)

    """"
    def get_random_coord(self, rad):
        const = 3
        x = randint(const * rad, self.width - const * rad)
        y = randint(const * rad, self.height - (const + 5) * rad)
        return x, y
    """""

    def print_info_message(self, node):
        self.infoText.setText("Click pentru a afisa nodul " + node)
        self.infoText.draw(self.win)

    def print_result_message(self, obj):
        self.infoText.undraw()
        self.infoText.setText(obj.result)
        self.infoText.setSize(15)
        self.infoText.draw(self.win)

    def mouse_click(self):
        click = self.win.getMouse()
        return click.getX(), click.getY()


    def draw_graph(self, obj):

        graph = obj.graph
        print (obj.edges)

        for elem in graph:

            indexStart = self.search_node(elem, obj)

            for connection in graph[elem]:

                indexFinish = self.search_node(connection[1], obj)

                start = self.nodeList[indexStart]
                finish = self.nodeList[indexFinish]

                # coordonatele centrelor
                c1x = start.center.getX()
                c1y = start.center.getY()
                r1 = start.radius

                c2x = finish.center.getX()
                c2y = finish.center.getY()
                r2 = finish.radius

                if c1x != c2x:
                    a = atan((c1y - c2y) / (c1x - c2x)) #unghiul liniei fata de ox

                    if c1x > c2x:
                        startPoint = Point(c1x - r1 * cos(a), c1y - r1 * sin(a))
                        finishPoint = Point(c2x + r2 * cos(a), c2y + r2 * sin(a))
                    else:
                        startPoint = Point(c1x + r1 * cos(a), c1y + r1 * sin(a))
                        finishPoint = Point(c2x - r2 * cos(a), c2y - r2 * sin(a))
                else:
                    a = pi / 2
                    ct = 1.5

                    if c1y < c2y:
                        startPoint = Point(c1x + ct * r1, c1y + ct * r1)
                        finishPoint = Point(c2x + r2, c2y + r2)
                    else:
                        startPoint = Point(c1x - ct * r1, c1y - ct * r1)
                        finishPoint = Point(c2x - r2, c2y - r2)

                arrow = self.create_arrow(startPoint, finishPoint, connection[0], "last", a)
                arrow.set_nodes(elem, connection[1])
                arrow.set_color(white)
                arrow.print_arrow(self.win)

    def verify_word(self, obj):
        for arrow in self.arrowList:

            arrow.unprint_arrow()
            arrow.set_color(white)
            arrow.print_arrow(self.win)

            for edge in obj.edges:
                if arrow.nodes[0] == edge[0] and arrow.nodes[1] == edge[1]:
                        arrow.unprint_arrow()
                        arrow.set_color(green)
                        arrow.print_arrow(self.win)
                        break
        self.print_result_message(obj)

    def read_word(self):

        # citirea cuvantului
        #print (line)
        if self.win.getMouse():
            #print (self.win.checkKey())
            line = self.entry.get_input()
            self.entry.set_text("")
            if line == "*":
                self.win.close()
                return False
            if line == "":
                word = None
            elif line == line.split()[0]:
                # daca "cuvantul"(din limbajul automatului) e dat caracter cu caracter (sau daca e dat cuvant cu cuvant)
                word = list(line)
            else:
                word = line.split()
            return word

    def search_node(self, elem, obj):

        for i in range(len(self.nodeList)):
            if self.nodeList[i].get_text() == elem:
                return i
        return self.create_node(elem, obj)

    def create_arrow(self, start, finish, value, direction, angle):
        arrow = Arrow(start, finish, value, direction, angle)
        self.arrowList.append(arrow)
        return arrow

    def create_node(self, text, obj):

        const = randint(30, 50)
        if self.width > self.height:
            radius = const / (self.width / self.height)
        else:
            radius = const / (self.height / self.width)

        self.print_info_message(text)
        coord = self.mouse_click()
        node = Node(text, radius, coord[0], coord[1])

        if node.get_text() in obj.exits:
            node.set_color(173, 255, 47)
        elif node.get_text() == obj.start:
            node.set_color(210, 210, 0)
        else:
            node.set_color(160, 0, 0)

        node.print_node(self.win)
        self.nodeList.append(node)

        self.infoText.undraw()

        return len(self.nodeList) - 1
