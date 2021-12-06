def add_to_dict(dct, key, value):
    if key in dct:
        dct[key] += value
    else:
        dct[key] = value