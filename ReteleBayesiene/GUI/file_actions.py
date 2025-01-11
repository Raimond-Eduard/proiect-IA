from tkinter.filedialog import askopenfile


class FileActions:
    @staticmethod
    def create_new_graph(event=None):
        # Functie de sters si de generat o noua zona goala pentru un graf nou
        print("This will later create a new graph entry clearing the previous one")
    @staticmethod
    def save_file(event=None):
        # Salvarea unui graf - daca putem il implementam
        print("This will save the current configuration in either xml or json")
    @staticmethod
    def open_file(event=None):
        # Deschiderea unui graf dintr-un fisier
        # print("This will later open the file selector and try to use a json or xml to parse it's content")
        file = askopenfile()
