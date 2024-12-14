import json
from collections import deque

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


def variables(retea):
    # Returneaza lista variabilelor din retea
    return list(retea.keys())

def parents(var, retea):
    # Returneaza lista parintilor variabilei var
    return retea[var]['parents']

def children(var, retea):
    # Returneaza lista copiilor unei variabile
    return [v for v in retea if var in retea[v]['parents']]

def possible_values(var, retea):
    # Returneaza valorile posibile ale unei variabile (deduse din tabelele de probabilitate)
    prob_table = retea[var]['prob']
    for cond in prob_table:
        return list(prob_table[cond].keys())

def p(var, value, evidence, retea):
    # Calculeaza P(var=value | parintii(var) din evidence)
    var_parents = parents(var, retea)
    parent_values = tuple(evidence[p] for p in var_parents)
    return retea[var]['prob'][parent_values][value]

def topological_sort(retea):
    
    # Calculam in-degree (numarul de parinti) pentru fiecare variabila
    in_degree = {v: len(retea[v]['parents']) for v in retea}
    # Coada cu variabile fara parinti
    queue = deque([v for v in retea if in_degree[v] == 0])
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        # Scadem in-degree pentru copiii lui v
        for c in children(v, retea):
            in_degree[c] -= 1
            if in_degree[c] == 0:
                queue.append(c)
    return order

def enumeration_ask(query_var, evidence, retea):
    Q = {}
    vars_order = topological_sort(retea)
    for val in possible_values(query_var, retea):
        extended_evidence = evidence.copy()
        extended_evidence[query_var] = val
        Q[val] = enumerate_all(vars_order, extended_evidence, retea)
    # Normalizare
    norm_factor = sum(Q.values())
    for val in Q:
        Q[val] /= norm_factor
    return Q

def enumerate_all(vars_list, evidence, retea):
    if not vars_list:
        return 1.0
    Y = vars_list[0]
    rest = vars_list[1:]
    if Y in evidence:
        return p(Y, evidence[Y], evidence, retea) * enumerate_all(rest, evidence, retea)
    else:
        total = 0
        for y_val in possible_values(Y, retea):
            new_evidence = evidence.copy()
            new_evidence[Y] = y_val
            total += p(Y, y_val, new_evidence, retea)*enumerate_all(rest, new_evidence, retea)
        return total


retea = load_retea_from_json('retea.json')

evidence = {'G': 'Nu', 'A': 'Nu', 'N': 'Nu'}
result = enumeration_ask('O', evidence, retea)
print(result)
