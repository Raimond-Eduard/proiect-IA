class Helper:
    @staticmethod
    def get_selected_value(list_selection):
        for i in list_selection.curselection():
            print(list_selection.get(i))