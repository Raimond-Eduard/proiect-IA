from IO.json_parser import Parser

class Helper:
    @staticmethod
    def return_parsed_json(file):
        parsed_file = Parser.load_retea_from_json(file)
        return parsed_file
