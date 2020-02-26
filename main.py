from wordAutomata import *

if __name__ == "__main__":

    auto = Automate()
    auto.data_to_structure("input.txt")

    representation = WindowObject("Automata graphic representation", 1200, 600)
    representation.draw_graph(auto)

    while True:
        word = representation.read_word()
        if word:
            auto.verify_word(word)
            representation.verify_word(auto)
        elif word == False:
            break

    #auto.print_graph()
    #auto.verify_word()