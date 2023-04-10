from collections import OrderedDict


def ordered_dict_to_dict(org_dict):
    dct = dict(org_dict)
    for k, v in dct.items():
        if isinstance(v, dict):
            dct[k] = ordered_dict_to_dict(v)
    if isinstance(org_dict, OrderedDict):
        dct['__flags'] = 2097152
    return dct
