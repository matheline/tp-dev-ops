import copy
import json
from filter import _match_filter
from read import read


def write(table_name, docs):
    with open(f"{table_name}.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=4, ensure_ascii=False)


def set_(doc, champ, valeur):
    doc[champ] = valeur


def unset(doc, champ, _=None):
    doc.pop(champ, None)


def inc(doc, champ, delta):
    doc[champ] = doc.get(champ, 0) + delta


def rename(doc, ancien_nom, nouveau_nom):
    if ancien_nom in doc:
        doc[nouveau_nom] = doc.pop(ancien_nom)


def min_(doc, champ, valeur):
    if champ not in doc or valeur < doc[champ]:
        doc[champ] = valeur


def max_(doc, champ, valeur):
    if champ not in doc or valeur > doc[champ]:
        doc[champ] = valeur


def push(doc, champ, valeur):
    if champ not in doc:
        doc[champ] = []
    doc[champ].append(valeur)


def pull(doc, champ, valeur):
    if champ in doc and isinstance(doc[champ], list):
        doc[champ] = [v for v in doc[champ] if v != valeur]


UPDATE_OPERATORS = {
    "$set": set_,
    "$unset": unset,
    "$inc": inc,
    "$rename": rename,
    "$min": min_,
    "$max": max_,
    "$push": push,
    "$pull": pull,
}


def _apply_update(doc, update_spec):
    """Applique toutes les opérations de mise à jour sur un document."""
    for op, fields in update_spec.items():
        if op not in UPDATE_OPERATORS:
            raise ValueError(f"Opérateur de mise à jour inconnu : {op}")
        func = UPDATE_OPERATORS[op]
        for champ, valeur in fields.items():
            func(doc, champ, valeur)


def _init_doc_from_filter(filter_spec):
    """Initialise un nouveau document à partir des égalités simples du filtre (pour upsert)."""
    new_doc = {}
    if isinstance(filter_spec, dict):
        for k, v in filter_spec.items():
            if not k.startswith("$") and not isinstance(v, dict):
                new_doc[k] = v
    return new_doc


def updateOne(table_name, filter, update, options=None):
    options = options or {}
    docs = read(table_name)
    matched = 0
    modified = 0
    upserted = False

    for doc in docs:
        if _match_filter(doc, filter):
            matched = 1
            avant = copy.deepcopy(doc)
            _apply_update(doc, update)
            if doc != avant:
                modified = 1
            break

    if matched == 0 and options.get("upsert", False):
        new_doc = _init_doc_from_filter(filter)
        _apply_update(new_doc, update)
        docs.append(new_doc)
        upserted = True

    if modified > 0 or upserted:
        write(table_name, docs)

    return {"matchedCount": matched, "modifiedCount": modified, "upserted": upserted}


def updateMany(table_name, filter, update, options=None):
    options = options or {}
    docs = read(table_name)
    matched = 0
    modified = 0
    upserted = False

    for doc in docs:
        if _match_filter(doc, filter):
            matched += 1
            avant = copy.deepcopy(doc)
            _apply_update(doc, update)
            if doc != avant:
                modified += 1

    if matched == 0 and options.get("upsert", False):
        new_doc = _init_doc_from_filter(filter)
        _apply_update(new_doc, update)
        docs.append(new_doc)
        upserted = True

    if modified > 0 or upserted:
        write(table_name, docs)

    return {"matchedCount": matched, "modifiedCount": modified, "upserted": upserted}


def replaceOne(table_name, filter, nouveauDocument, options=None):
    options = options or {}
    docs = read(table_name)
    matched = 0
    modified = 0
    upserted = False

    for i, doc in enumerate(docs):
        if _match_filter(doc, filter):
            matched = 1
            remplacement = copy.deepcopy(nouveauDocument)
            if docs[i] != remplacement:
                docs[i] = remplacement
                modified = 1
            break

    if matched == 0 and options.get("upsert", False):
        docs.append(copy.deepcopy(nouveauDocument))
        upserted = True

    if modified > 0 or upserted:
        write(table_name, docs)

    return {"matchedCount": matched, "modifiedCount": modified, "upserted": upserted}
