from collections import deque

class BayesianNetwork:
    def __init__(self, newtowrk_dict):
        # Constructor initializat cu dictionarul de noduri din gui
        self.network = newtowrk_dict

    def get_variables(self):
        # Returnarea lisei de variabile din retea
        return list(self.network.keys())

    def get_parents(self, variable):
        # Returneaza lista parintile variabile specificate ca parametru
        return self.network[variable].parents

    def get_children(self, variable):
        # Returneaza lista copiilor unei variabile
        return [v for v in self.network if variable in self.network[v].parents]

    def p(self, variable, value, evidence):
        # Calculeaza probabilitatea variabile egale cu valoarea respectiva
        # conditionata de parintii din evidentele facute
        parents = self.get_parents(variable)
        # parent_values = tuple(evidence[p] for p in parents)
        parent_values = ""
        if len(parents) > 1:

            for p in parents:
                if parent_values == "":
                    parent_values += evidence[p]
                else:
                    parent_values += ", " + evidence[p]
        elif len(parents) == 1:
            parent_values = evidence[parents[0]]

        if parent_values == '':
            parent_values = 'None'
        return self.network[variable].probabilities_dict[parent_values][value]

    def topological_sort(self):
        # Calculul in-degree (numarul de parinti) pentru fiecar variabila
        in_degree = {v: len(self.network[v].parents) for v in self.network}
        # Coada cu variabile fara parinti
        queue = deque([v for v in self.network if in_degree[v] == 0])
        order = []

        while queue:

            v = queue.popleft()
            order.append(v)
            # Se scade in-degree pentru copiii lui v
            for c in self.get_children(v):
                in_degree[c] -= 1
                if in_degree[c] == 0:
                    queue.append(c)
        return order

    def possible_values(self, variable):
        # Returneaza valorile posibile ale unei variabile (deduse din tabele de probabilitati)
        probability_table = self.network[variable].probabilities_dict
        for condition in probability_table:
            return list(probability_table[condition].keys())

class EnumerationInference:

    def __init__(self, bayesian_network):
        self.bayesian_network = bayesian_network

    def enumerate_all(self, variables_list, evidence):
        if not variables_list:
            return 1.0
        Y = variables_list[0]
        rest = variables_list[1:]

        if Y in evidence:
            return self.bayesian_network.p(Y, evidence[Y], evidence) * self.enumerate_all(rest, evidence)
        else:
            total = 0
            for y_value in self.bayesian_network.possible_values(Y):
                new_evidence = evidence.copy()
                new_evidence[Y] = y_value
                total += self.bayesian_network.p(Y, y_value, new_evidence) * self.enumerate_all(rest, new_evidence)
            return total

    def enumeration_ask(self, query_variabile, evidence):
        Q = {}
        variables_order = self.bayesian_network.topological_sort()
        for value in self.bayesian_network.possible_values(query_variabile):
            extended_evidence = evidence.copy()
            extended_evidence[query_variabile] = value
            Q[value] = self.enumerate_all(variables_order, extended_evidence)

        # Normalizare
        normalization_factor = sum(Q.values())
        for val in Q:
            Q[val] /= normalization_factor
        return Q
