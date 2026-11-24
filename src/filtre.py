def gt(champ, valeur):
    return champ > valeur

def gte(champ, valeur):
    return champ >= valeur

def lt(champ, valeur):
    return champ < valeur

def lte(champ, valeur):
    return champ <= valeur

def e(champ, valeur):
    return champ == valeur

def ne(champ, valeur):
    return champ != valeur

def in_(champ, valeur):
    return champ in valeur

def or_(*conditions):
    return any(conditions)

def and_(*conditions):
    return all(conditions)

def not_(condition):
    return not condition

