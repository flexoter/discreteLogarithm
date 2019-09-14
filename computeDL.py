#!/usr/bin/sudo python
# -*- coding: utf-8 -*-
"""
    Module contains functions to compute discrete logarythm

"""

from math import (
    sqrt,
    modf
)
from hashlib import sha256
from sympy import mod_inverse


def find_representation(value):
    """
    Function finds a (2**s_value)*t_value format number representation
    which is required in miller_rabin_test.\n

    :param int value: number represestation of which is required\n

    """

    s_value = int()

    if value % 2 != 0:
        value -= 1

    while value % 2 == 0:
        value /= 2
        s_value += 1

    return s_value, int(value)


def eiler_function(value):
    a, b = find_representation(value)
    return (2 ** a - 2 ** (a - 1)) * (b - 1)


def gelfond_shanks(base, result, field):
    """
    Function finds a logarithm from given result with given base
    using Gelfond-Shanks's algorythm.\n
    Algorythm works on cyclic multiplicative groups with simple fields.\n
    :param int base: base of a logarithm\n
    :param int result: result of a logarithm\n
    :param int field: field of a cyclic multiplicative group\n

    """

    rlt = list()
    dg = int(sqrt(field)) + 1
    gmm = pow(base, dg, field)
    dgr_dict = dict()
    for dgr in range(1, dg + 1):
        hsh = sha256()
        nxt_elem = pow(gmm, dgr, field)
        hsh.update(nxt_elem.to_bytes((nxt_elem.bit_length() + 7) // 8, 'big'))
        dgr_dict[hsh.hexdigest()] = dgr
    for dgr in range(dg + 2):
        hsh = sha256()
        el = (result * pow(base, dgr, field)) % field
        hsh.update(el.to_bytes((el.bit_length() + 7) // 8, 'big'))
        try:
            rslt = dgr_dict[hsh.hexdigest()]
            d = dg*rslt
            if pow(base, d, field) != result:
                if pow(base, d - rslt, field) != result:
                    continue
                else:
                    return d - rslt
            else:
                return d
        except KeyError:
            continue
    return rlt


def pollig_hellman(base, result, field):
    """
    Function finds a logarithm from given result with given base
    using Pollig-Hellman's algorythm.\n
    Algorythm works on cyclic multiplicative groups with simple fields and compound fields.\n
    :param int base: base of a logarithm\n
    :param int result: result of a logarithm\n
    :param int field: field of a cyclic multiplicative group\n

    """

    rng = find_representation(field)[0]
    ftrs = []
    rslt = int()
    if pow(result, (field - 1) // 2, field) == 1:
        ftrs.append(0)
    else:
        ftrs.append(1)
    for dgr in range(1, rng):
        dg = int()
        index = int()
        for ftr in ftrs:        
            dg += ftr * (2 ** index)
            index += 1
        z = (result * pow(mod_inverse(base, field), dg, field)) % field
        m = ((field - 1) // pow(2, dgr + 1, field)) % field
        if pow(z, m, field) == 1:
            ftrs.append(0)
        else:
            ftrs.append(1)
    rslt += ftrs[0]
    for ftr in range(1, len(ftrs)):
        rslt += (ftrs[ftr] * pow(2, ftr, field)) % field
    return rslt


def devide_field(x, a, b, field, base, result):
    """
    Function devides cyclic multiplicative group with fiven field on three subgroups\n
    and finds parameteres for Pollard's-rho algorythm.\n
    :param int base: base of a logarithm\n
    :param int result: result of a logarithm\n
    :param int field: field of a cyclic multiplicative group\n
    :param int x: supposed to be the desired logarythm\n
    :param int a: intermediate value for logarythm conputing\n
    :param int b: intermediate value for logarythm conputing\n

    """

    m = x % 3
    if m == 0:
        x = (x * x) % field
        a = (a * 2) % (field - 1)
        b = (b * 2) % (field - 1)
    elif m == 1:
        x = (x * base) % field
        a = (a + 1) % (field - 1)
    elif m == 2:
        x = (x * result) % field
        b = (b + 1) % (field - 1)
    return x, a, b


def pollard_rho(base, result, field):
    """
    Function finds a logarithm from given result with given base
    using Pollard's-rho algorythm.\n
    Algorythm works on cyclic multiplicative groups with simple fields.\n
    :param int base: base of a logarithm\n
    :param int result: result of a logarithm\n
    :param int field: field of a cyclic multiplicative group\n

    """

    x, a, b = int(1), int(), int()
    dx, da, db = int(x), int(a), int(b)
    for _ in range(field):
        x, a, b = devide_field(x, a, b, field, base, result)
        dx, da, db = devide_field(dx, da, db, field, base, result)
        dx, da, db = devide_field(dx, da, db, field, base, result)
        if x == dx:
            return x

if __name__ == "__main__":
    print(pollard_rho(4096, 230611, 993121))
    print(pollig_hellman(5, 3, 23))
    print(gelfond_shanks(5, 3, 23))