from automataGraphics import *


class Automate:

    def __init__(self):

        self.graph = {}
        self.start = None
        self.exits = []
        self.result = ""
        self.edges = []

    def verify_word(self, word):
        print ("bla bla", word)
        self.edges = []
        node = self.start
        # print (word)

        if word is None:
            if node in self.exits:
                self.result = "Cuvantul este accept de automat. Procesul s-a terminat cu succes."
            else:
                self.result = "Cuvantul nu este acceptat de automat. Executia s-a oprit la caracterul: " + node + "."
        else:
            for i in range(len(word)):

                letter = word[i]
                is_found = False

                for elem in self.graph[node]:
                    if elem[0] == letter:
                        # print ("Am gasit muchia cu valoarea", elem[0], " care se termina in litera", elem[1]);
                        self.edges.append((node, elem[1]))
                        node = elem[1]
                        is_found = True
                        break

                # print (node, self.graph[node], is_found)

                if not is_found:
                    if self.graph.get(letter) is None and not (letter in self.exits):
                        self.result = "Cuvantul nu e acceptat de automat. Caracterul " + letter + " nu exista."
                    else:
                        self.result = "Cuvantul nu este acceptat de automat. Executia s-a oprit la caracterul: " + node + "."
                    break
                else:
                    if i == len(word) - 1:
                        if node in self.exits:
                            self.result = "Cuvantul este acceptat de automat. Procesul s-a terminat cu succes."
                        else:
                            self.result = "Cuvantul nu este acceptat de automat. Executia s-a oprit la caracterul: " + node + ", cautand muchie de valoarea " + letter + "."
                        break

    def print_graph(self):

        print(self.graph)

    def data_to_structure(self, filename):

        with open(filename) as f:

            # prelucrararea nodurilor
            line = f.readline().split()
            while len(line) == 3:

                if line[0] not in self.graph:
                    self.graph[line[0]] = []

                self.graph[line[0]].append((line[2], line[1]))  # tuplul de valoare verificata si elementul adaugat
                line = f.readline().split()

            # adaugarea startului
            self.start = line[0]

            # adaugarea finish-urilor
            line = f.readline().split()
            for i in range(len(line)):
                self.exits.append(line[i])

        # print(self.graph)
        # print(self.word)


auto = Automate()
auto.data_to_structure("input.txt")
# auto.print_graph()
# auto.verify_word(["2", "3", "1", "2"])
# print (auto.result)
#auto.verify_word(["2", "3", "1"])
#print (auto.result)
