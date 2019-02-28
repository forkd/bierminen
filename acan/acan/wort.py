#!/usr/local/bin/env python3
# Copyright 2016 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


import math

from acan import sg_to_plato, plato_to_sg, brix_to_sg, sg_to_gu
from acan import litre_to_gallon, gram_to_pound, gram_to_ounce


class Wort():
    """
    Homebrewers must measure the quality of the wort.  After taking samples
    before the fermentation (original gravity) and after the fermentation
    (final gravity), a series of calculations should be made to determine
    the characteristics of that wort, like the percentage of alcohol.

    This class allow homebrewers to measure their worts in all stages of
    brewing --all they have to do is to take 2 samples and name then
    original and final.

    All methods based on [15], except:
    - apparent_attenuation: based on [16] (p.40)
    - real_attenuation: based on [17]
    - mash_efficiency: based on [8] (p.551-556) and [18] --in the scope of
        this project, mash efficiency is equal to brewhouse efficiency.

    All equations consider the wort in ~ 20 degC.

    PARAMETERS
    - original (float): the original gravity (OG) in SG, Brix, or Plato.
    - final (float): the final gravity (FG) in SG, Brix, or Plato.
    - unit (string): the unit of measurements: sg, brix, or plato.
    - grains (list): a list of tuples containing all grain weights in grams
        and their maximum efficiencies in Gravity Units.
        Ex.: [(2948.3, 36), (226.8, 34),(226.8, 34), (226.8, 35), (226.8, 30)]
    - volume (float): total amount of wort after the boil in litres.

    """
    def __init__(self, original, final, unit='sg', grains=None, volume=None):
        if unit == 'sg':
            self.og = original
            self.fg = final
            self.oe = sg_to_plato(self.og)
            self.ae = sg_to_plato(self.fg)
        elif unit == 'plato':
            self.oe = original
            self.ae = final
            self.og = plato_to_sg(self.oe)
            self.fg = plato_to_sg(self.ae)
        elif unit == 'brix':
            self.og = brix_to_sg(original)
            self.fg = brix_to_sg(final)
            self.oe = sg_to_plato(self.og)
            self.ae = sg_to_plato(self.fg)
        else:
            raise ValueError('unit must be sg, plato, or brix')

        if grains:
            if volume:
                self.volume = float(volume)
                total_weight = sum(grain[0] for grain in grains)
                gallons = litre_to_gallon(self.volume)  # speed up calcs
                self.points_pound_gallon = (litre_to_gallon(self.volume) *
                    sg_to_gu(self.og) / gram_to_pound(total_weight))
                self.mash_efficiency = sg_to_gu(self.og) / sum(g[1] *
                    gram_to_pound(g[0]) / gallons for g in grains) * 100
            else:
                raise ValueError('wort\'s volume must be informed')
        else:
            self.points_pound_gallon = self.volume = -1.0
            self.brewhouse_efficiency = self.mash_efficiency = self.volume

        self.real_extract = (0.1808 * self.oe) + (0.8192 * self.ae)
        self.apparent_attenuation = (self.og - self.fg) / (self.og - 1) * 100
        self.real_attenuation = ((self.oe - self.real_extract) / (self.oe -
            1) * 100)
        self.alcohol_by_volume = ((self.og - self.fg) / 0.75) * 100
        self.alcohol_by_weight = (((0.79 * (self.alcohol_by_volume / 100)) /
            self.fg) * 100)
        self.calories = (((6.9 * self.alcohol_by_weight) + (4 *
            (self.real_extract - 0.1))) * self.fg * 3.55)

    def __str__(self):
        return 'Original gravity.....[SG]: {0:7.3f}\n'\
            'Final gravity........[SG]: {1:7.3f}\n'\
            'Original extract..[Plato]: {2:7.3f}\n'\
            'Apparent extract..[Plato]: {3:7.3f}\n'\
            'Real extract......[Plato]: {4:7.3f}\n'\
            'Volume................[L]: {5:7.3f}\n'\
            'Points/Pound/Gallon.[PPG]: {6:7.3f}\n'\
            'Mash efficiency.......[%]: {7:7.3f}\n'\
            'Apparent attenuation..[%]: {8:7.3f}\n'\
            'Real attenuation......[%]: {9:7.3f}\n'\
            'Alcohol by weight.....[%]: {10:7.3f}\n'\
            'Alcohol by volume.....[%]: {11:7.3f}\n'\
            'Calories in 355 mL..[Cal]: {12:7.3f}\n'.format(self.og, self.fg,
            self.oe, self.ae, self.real_extract, self.volume,
            self.points_pound_gallon, self.mash_efficiency,
            self.apparent_attenuation, self.real_attenuation,
            self.alcohol_by_weight, self.alcohol_by_volume, self.calories)


class Hops():
    """
    Equations to estimate hop bitterness and aroma.

    rager, garetz, and tinseth based on [19].  daniels was based on [16],
    p.135-136.  palmer based on [8], p.152-162.

    The default equation used by this class is tinseth, so parameters must
    match those requisites.

    More info on hops can be found at [20].

    """
    def __init__(self, w, a, v, sg, t):
        self.hops_weight = w
        self.hops_alpha = a
        self.wort_volume = v
        self.wort_sg = sg
        self.hops_boil_time = t
        self.wort_bitterness = self.tinseth(self.hops_weight, self.hops_alpha,
            self.wort_volume, self.wort_sg, self.hops_boil_time)

    def rager(self, w, a, v, sg):
        """
        PARAMETERS
        - w (float): hops' weight in grams.
        - a (float): hops' alpha acids in %.
        - v (float): batch volume in litres.
        - sg (float): gravity of batch.

        """
        u = 18.11 + 13.86 * math.tanh((t - 31.32) / 18.27)
        if sg < 1.050: ga = 0
        else: ga = (sg - 1.050) / 0.2
        return (w * u * a * 1000) / (v * (1 + ga))

    def garetz(self, w, a, sg, t, vb, vf, b, h):
        """
        PARAMETERS
        - w (float): hops' weight in grams.
        - a (float): hops' alpha acids in %.
        - sg (float): gravity of batch.
        - t (integer): boiling time in minutes --0 <= t <=90.
        - vb (integer): volume of batch in litres.
        - vf (integer): volume of post boil in litres.
        - b (float): desired bitterness in IBU.
        - h (float): elevation of boiling batch in meters.

        """
        h = h / 3.048 * 10  # meters to feet
        cf = vf + vb
        gf = (((cf * (sg - 1) - 1) - 1.050) / 0.2) + 1
        hf = ((cf * b) / 260) + 1
        tf = ((h / 550) * 0.02) + 1
        ca = gf * hf * tf

        if 0 <= t <= 10: u = 0
        elif 11 <= t <= 15: u = 5
        elif 16 <= t <= 20: u = 5
        elif 21 <= t <= 25: u = 8
        elif 26 <= t <= 30: u = 11
        elif 31 <= t <= 35: u = 14
        elif 36 <= t <= 40: u = 16
        elif 41 <= t <= 45: u = 18
        elif 46 <= t <= 50: u = 19
        elif 51 <= t <= 60: u = 20
        elif 61 <= t <= 70: u = 21
        elif 71 <= t <= 80: u = 22
        elif 81 <= t <= 90: u = 23
        else: raise ValueError('invalid time: {}'.format(t))

        return (u * a * w * 0.1) / (v * ca)

    def tinseth(self, w, a, v, sg, t):
        """
        PARAMETERS
        - w (float): hops' weight in grams.
        - a (float): hops' alpha acids in %.
        - v (float): batch volume in litres.
        - sg (float): gravity of batch.
        - t (integer): boiling time in minutes --0 <= t <=90.

        """
        return ((1.65 * 0.000125 ** (sg - 1)) * ((1 - math.e ** (-0.04 * t)) /
            4.15) * ((a / 100) * w * 1000 / v))

    def daniels(self, w, a, v, sg, t, ht):
        """
        PARAMETERS
        - w (float): hops' weight in grams.
        - a (float): hops' alpha acids in %.
        - v (float): batch volume in litres.
        - sg (float): gravity of batch.
        - t (integer): boiling time in minutes --0 <= t.
        - ht (string): hop type could be 'whole' or 'pellet'.

        """
        if sg < 1.050: c = 1
        else: c = 1 + (sg - 1.050) / 2

        if 0 <= t <= 9: u = (0, 0)
        elif 10 <= t <= 19: u = (5, 6)
        elif 20 <= t <= 29: u = (12, 15)
        elif 30 <= t <= 44: u = (19, 24)
        elif 45 <= t <= 59: u = (22, 27)
        elif 60 <= t <= 74: u = (24, 30)
        elif t > 75: u = (27, 34)
        else: raise ValueError('invalid time: {}'.format(t))

        if ht == 'whole': u = u[0] / 100
        elif ht == 'pellet': u = u[1] / 100
        else: raise ValueError('invalid hop type: {}'.format(ht))

        return (w * u * (a / 100) * 1000) / (v * c)

    def palmer(self, w, a, v, sg, t):
        """
        PARAMETERS
        - w (float): hops' weight in grams.
        - a (float): hops' alpha acids in %.
        - v (float): batch volume in litres.
        - sg (float): gravity of batch.
        - t (integer): boiling time in minutes --0 <= t <=90.

        """
        return (((gram_to_ounce(w) * a) * ((1.65 * 0.000125 ** (sg - 1)) *
            ((1 - math.e ** (-0.04 * t)) / 4.15)) * 75) / litre_to_gallon(v))

    def __str__(self):
        return 'Hops weight.......[g]: {0:6.2f}\n'\
            'Hops alpha acids..[%]: {1:6.2f}\n'\
            'Wort volume.......[L]: {2:6.2f}\n'\
            'Wort SG...........[L]: {3:7.3f}\n'\
            'Hops boil time....[m]: {4:3.0f}\n'\
            'Wort bitterness.[IBU]: {5:7.3f}'.format(self.hops_weight,
            self.hops_alpha, self.wort_volume, self.wort_sg,
            self.hops_boil_time, self.wort_bitterness)
