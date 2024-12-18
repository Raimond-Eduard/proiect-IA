from IO.json_parser import Parser
from collections import deque

class BayesianNetwork:
    def __init__(self, filename):
        self.retea = Parser.load_retea_from_json(filename)

    def get_node_positions(self):
        # Returneaza lista (sau dictionar) cu positiile fiecarei variable
        res = {}
        for i in self.retea.keys():
            res[i] = self.retea[i]['position']
        return res

    def variables(self):
        # Returneaza lista variabilelor din retea
        return list(self.retea.keys())

    def parents(self, var):
        # Returneaza lista parintilor variabilei var
        return self.retea[var]['parents']

    def children(self, var):
        # Returneaza lista copiilor unei variabile
        return [v for v in self.retea if var in self.retea[v]['parents']]

    def possible_values(self, var):
        # Returneaza valorile posibile ale unei variabile (deduse din tabelele de probabilitate)
        prob_table = self.retea[var]['prob']
        for cond in prob_table:
            return list(prob_table[cond].keys())

    def p(self, var, value, evidence):
        # Calculeaza P(var=value | parintii(var) din evidence)
        var_parents = self.parents(var)
        parent_values = tuple(evidence[p] for p in var_parents)
        return self.retea[var]['prob'][parent_values][value]

    def topological_sort(self):
        # Calculam in-degree (numarul de parinti) pentru fiecare variabila
        in_degree = {v: len(self.retea[v]['parents']) for v in self.retea}
        # Coada cu variabile fara parinti
        queue = deque([v for v in self.retea if in_degree[v] == 0])
        order = []
        while queue:
            v = queue.popleft()
            order.append(v)
            # Scadem in-degree pentru copiii lui v
            for c in self.children(v):
                in_degree[c] -= 1
                if in_degree[c] == 0:
                    queue.append(c)
        return order


class EnumerationInference:
    def __init__(self, bayesian_network):
        self.bn = bayesian_network

    def enumeration_ask(self, query_var, evidence):
        Q = {}
        vars_order = self.bn.topological_sort()
        for val in self.bn.possible_values(query_var):
            extended_evidence = evidence.copy()
            extended_evidence[query_var] = val
            Q[val] = self.enumerate_all(vars_order, extended_evidence)
        # Normalizare
        norm_factor = sum(Q.values())
        for val in Q:
            Q[val] /= norm_factor
        return Q

    def enumerate_all(self, vars_list, evidence):
        if not vars_list:
            return 1.0
        Y = vars_list[0]
        rest = vars_list[1:]
        if Y in evidence:
            return self.bn.p(Y, evidence[Y], evidence) * self.enumerate_all(rest, evidence)
        else:
            total = 0
            for y_val in self.bn.possible_values(Y):
                new_evidence = evidence.copy()
                new_evidence[Y] = y_val
                total += self.bn.p(Y, y_val, new_evidence)*self.enumerate_all(rest, new_evidence)
            return total

if __name__ == "__main__":
    retea = BayesianNetwork('../defaults/Problema_Febrei.json')
    engine = EnumerationInference(retea)

    evidence = {'Gripa': 'Nu', 'Abces': 'Nu', 'Anorexie': 'Nu'}
    result = engine.enumeration_ask('Oboseala', evidence)
    print(result)
    print("This is just for testing purpose, to run hit on main.py")
