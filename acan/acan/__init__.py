#!/usr/local/bin/env python3
# Copyright 2016 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


"""
Acan - basic maths around brewing.

Overview
This Python module implements some equations used by homebrewers.  Although
there is no canonical formulas for procedures covered by Acan, I tried to
use those referenced by the most renowned sources.  Therefore, it is highly
probable that if you compare the results given by Acan with other softwares,
you'll find differences.  For the most cases, differences from the second or
third decimal place can be accepted, but bigger differences should be
examined with academical documents, like the NIST's [1].

"""


# Based on [3]
def celsius_to_fahrenheit(c): return (9 / 5) * c + 32
def fahrenheit_to_celsius(f): return (5 / 9) * (f - 32)
def pound_to_gram(p): return p * 4.535924 * 10 ** 2
def gram_to_pound(g): return g / 4.535924 * 10 ** -2
def ounce_to_gram(o): return o * 2.834952 * 10
def gram_to_ounce(g): return g / 2.834952 * 10 ** -1
def gallon_to_litre(g): return g * 3.785412
def litre_to_gallon(l): return l / 3.785412

# Based on [15]
def brix_to_sg(b):
    return 1.000898 + (0.003859118 * b) + (0.00001370735 * b ** 2) + \
        (0.00000003742517 * b ** 3)

def sg_to_brix(s):
    return (204.402187871 * s ** 3) - (846.219914611 * s ** 2) + \
        (1338.585568906 * s) - 696.999179737

def sg_to_plato(s):
    return (135.997 * s ** 3) - (630.272 * s ** 2) + (1111.14 * s) - \
        616.868

def plato_to_sg(p):
    return (0.00000006867329 * p ** 3) + (0.00001256372708 * p ** 2) + \
        (0.00386943912474 * p) + 1.00000786285356

# Derived from previous equations
def brix_to_plato(b): return sg_to_plato(brix_to_sg(b))

# Based on [16] (p.142)
def sg_to_gu(s): return (s - 1) * 1000
def gu_to_sg(g): return g * 0.001 + 1

# Based on [18]
def dbfg_to_gu(d): return d / 100 * 46
def gu_to_dbfg(g): return g / 46 * 100
