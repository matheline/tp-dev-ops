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

COMPARISON_OPS = {
    "$gt": gt,
    "$gte": gte,
    "$lt": lt,
    "$lte": lte,
    "$eq": e,
    "$ne": ne,
    "$in": in_,
}

def _match_filter(doc, filter_spec):
    if callable(filter_spec):
        return filter_spec(doc)

    for key, condition in filter_spec.items():
        if key == "$and":
            if not and_(*(_match_filter(doc, sub) for sub in condition)):
                return False
        elif key == "$or":
            if not or_(*(_match_filter(doc, sub) for sub in condition)):
                return False
        elif key == "$not":
            if not not_(_match_filter(doc, condition)):
                return False

        elif isinstance(condition, dict):
            valeur_doc = doc.get(key)
            for op, valeur_cible in condition.items():
                if op == "$not":
                    if not not_(_match_filter(doc, {key: valeur_cible})):
                        return False
                elif op in COMPARISON_OPS:
                    if valeur_doc is None and op in ("$gt", "$gte", "$lt", "$lte"):
                        return False
                    if not COMPARISON_OPS[op](valeur_doc, valeur_cible):
                        return False
                else:
                    raise ValueError(f"Opérateur de filtre inconnu : {op}")

        else:
            if not e(doc.get(key), condition):
                return False

    return True
