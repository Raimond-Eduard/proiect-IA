import json

class Parser:
    @staticmethod
    def load_retea_from_json(filename):
        with open(filename, 'r') as f:
            data = json.load(f)

        new_data = {}
        for var, info in data.items():
            new_info = info.copy()
            new_prob = {}
            for cond_str, val in info['prob'].items():
                cond_tuple = eval(cond_str)
                new_prob[cond_tuple] = val
            new_info['prob'] = new_prob
            new_data[var] = new_info
        return new_data