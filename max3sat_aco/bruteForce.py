import itertools
# Função para verificar se uma atribuição de valores satisfaz todas as cláusulas
def is_satisfiable(variables, clauses, assignment):
    print('run')
    # Atribuindo os valores das variáveis de acordo com a combinação
    var_map = dict(zip(variables, assignment))
    
    # Verificando se todas as cláusulas são satisfeitas
    for clause in clauses:
        clause_satisfied = False
        for var, sign in clause.items():
            if (sign == 1 and var_map[var] == 1) or (sign == -1 and var_map[var] == 0):
                clause_satisfied = True
                break
        if not clause_satisfied:
            return False
    return True

# Função brute-force para testar todas as combinações
def brute_force_3sat(variables, clauses):
    
    # Gerando todas as combinações possíveis de 0 (False) e 1 (True) para as variáveis
    num_vars = len(variables)
    for assignment in itertools.product([0, 1], repeat=num_vars):
        # Verificando se a combinação atual satisfaz a fórmula
        if is_satisfiable(variables, clauses, assignment):
            return True, dict(zip(variables, assignment))
    return False, None

# Exemplo de uso
variables = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49']
clauses = [
    {'x0': 1, 'x1': -1, 'x2': -1},
    {'x1': 1, 'x3': -1, 'x4': 1},
    {'x2': 1, 'x5': 1, 'x6': -1},
    {'x3': 1, 'x7': -1, 'x8': 1},
    {'x4': 1, 'x9': -1, 'x10': 1},
    {'x5': -1, 'x11': 1, 'x12': -1},
    {'x6': 1, 'x13': -1, 'x14': 1},
    {'x7': -1, 'x15': 1, 'x16': -1},
    {'x8': 1, 'x17': -1, 'x18': 1},
    {'x9': -1, 'x19': 1, 'x20': -1},
    {'x10': 1, 'x21': -1, 'x22': 1},
    {'x11': -1, 'x23': 1, 'x24': -1},
    {'x12': 1, 'x25': -1, 'x26': 1},
    {'x13': -1, 'x27': 1, 'x28': -1},
    {'x14': 1, 'x29': -1, 'x30': 1},
    {'x15': -1, 'x31': -1, 'x32': -1},
    {'x16': 1, 'x33': -1, 'x34': 1},
    {'x17': -1, 'x35': 1, 'x36': -1},
    {'x18': 1, 'x37': -1, 'x38': 1},
    {'x19': -1, 'x39': -1, 'x40': -1},
    {'x20': 1, 'x41': -1, 'x42': 1},
    {'x21': -1, 'x43': 1, 'x44': -1},
    {'x22': 1, 'x45': -1, 'x46': 1},
    {'x23': -1, 'x47': 1, 'x48': -1},
    {'x24': -1, 'x49': -1, 'x0': 1},
    {'x25': -1, 'x1': 1, 'x2': -1},
    {'x26': 1, 'x3': -1, 'x4': -1},
    {'x27': -1, 'x5': 1, 'x6': 1},
    {'x28': 1, 'x7': -1, 'x8': 1},
    {'x29': -1, 'x9': 1, 'x10': -1},
    {'x30': 1, 'x11': -1, 'x12': 1},
    {'x31': -1, 'x13': 1, 'x14': -1},
    {'x32': 1, 'x15': -1, 'x16': 1},
    {'x33': -1, 'x17': 1, 'x18': -1},
    {'x34': 1, 'x19': -1, 'x21': 1},
    {'x35': -1, 'x21': 1, 'x22': -1},
    {'x36': 1, 'x23': -1, 'x24': 1},
    {'x37': -1, 'x25': 1, 'x26': -1},
    {'x38': 1, 'x27': -1, 'x28': 1},
    {'x39': -1, 'x29': 1, 'x30': -1},
    {'x40': 1, 'x31': -1, 'x32': 1},
    {'x41': -1, 'x33': 1, 'x34': -1},
    {'x42': 1, 'x35': -1, 'x36': 1},
    {'x43': -1, 'x37': 1, 'x38': -1},
    {'x44': 1, 'x39': -1, 'x40': 1},
    {'x45': -1, 'x41': 1, 'x42': -1},
    {'x46': 1, 'x43': -1, 'x44': 1},
    {'x47': -1, 'x45': 1, 'x46': -1},
    {'x48': 1, 'x47': -1, 'x49': 1},
    {'x49': -1, 'x0': 1, 'x1': -1},
    {'x0': 1, 'x2': 1, 'x3': -1},
    {'x1': -1, 'x0': 1, 'x5': -1},
    {'x2': 1, 'x6': -1, 'x7': 1},
    {'x3': -1, 'x8': 1, 'x9': -1},
    {'x0': 1, 'x0': -1, 'x11': 1},
    {'x5': -1, 'x12': 1, 'x13': -1},
    {'x6': 1, 'x14': -1, 'x14': 1},
    {'x7': -1, 'x16': 1, 'x17': -1},
    {'x8': 1, 'x18': -1, 'x19': 1},
    {'x9': -1, 'x20': 1, 'x21': -1},
    {'x10': 1, 'x22': -1, 'x23': 1},
    {'x11': -1, 'x24': 1, 'x25': -1},
    {'x12': 1, 'x26': -1, 'x27': 1},
    {'x13': -1, 'x28': 1, 'x29': -1},
    {'x14': 1, 'x30': -1, 'x31': 1},
    {'x15': -1, 'x32': 1, 'x33': -1},
    {'x16': 1, 'x34': -1, 'x35': 1},
    {'x17': -1, 'x36': 1, 'x37': -1},
    {'x18': 1, 'x38': -1, 'x39': 1},
    {'x19': -1, 'x40': 1, 'x41': -1},
    {'x20': 1, 'x42': -1, 'x43': 1},
    {'x21': -1, 'x44': 1, 'x45': -1},
    {'x22': 1, 'x46': -1, 'x47': 1},
    {'x23': -1, 'x48': 1, 'x49': -1},
    {'x24': 1, 'x0': -1, 'x1': 1},
    {'x25': -1, 'x2': -1, 'x3': 1},
    {'x26': 1, 'x4': 1, 'x5': -1},
    {'x27': -1, 'x6': 1, 'x7': -1},
    {'x28': 1, 'x8': -1, 'x9': 1},
    {'x29': -1, 'x10': 1, 'x11': -1},
    {'x30': 1, 'x12': -1, 'x13': 1},
    {'x31': -1, 'x14': 1, 'x15': -1},
    {'x32': 1, 'x16': -1, 'x17': 1},
    {'x33': -1, 'x18': 1, 'x19': -1},
    {'x34': 1, 'x20': -1, 'x21': 1},
    {'x35': -1, 'x22': 1, 'x23': -1},
    {'x36': 1, 'x24': -1, 'x25': 1},
    {'x37': -1, 'x26': 1, 'x27': -1},
    {'x38': 1, 'x28': -1, 'x29': 1},
    {'x39': -1, 'x30': 1, 'x31': -1},
    {'x40': 1, 'x32': -1, 'x33': 1},
    {'x41': -1, 'x34': 1, 'x35': -1},
    {'x42': 1, 'x36': -1, 'x37': 1},
    {'x43': -1, 'x38': 1, 'x39': -1},
    {'x44': 1, 'x40': -1, 'x41': 1},
    {'x45': -1, 'x42': 1, 'x43': -1},
    {'x46': 1, 'x44': -1, 'x45': 1},
    {'x47': -1, 'x46': 1, 'x47': -1},
    {'x48': 1, 'x49': -1, 'x0': 1}
]

# Testando a fórmula
satisfiable, assignment = brute_force_3sat(variables, clauses)
if satisfiable:
    print("A fórmula é satisfazível! Atribuição das variáveis:", assignment)
else:
    print("A fórmula não é satisfazível.")
