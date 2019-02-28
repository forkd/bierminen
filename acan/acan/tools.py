#!/usr/local/bin/env python3
# Copyright 2016 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


from acan import celsius_to_fahrenheit
from acan import sg_to_plato, plato_to_sg, sg_to_brix, brix_to_sg, brix_to_plato


class Hydrometer():
    """
    Hydrometers usually output values in SG, but the temperature
    affects the results.

    This class corrects the result using a formula according to [6] and [7].
    It also tries to be compliant to [8] (p.739-740), but it could not be
    achieved at all.

    Hydrometers usually read values between 1.000 and 1.200, where 1.150 is
    the last common value.

    PARAMETERS
    - value (float): value read on hydrometer in Specific Gravity.
    - temperature (float): sample temperature in degrees Celsius.
    - calibration (float): calibration temperature in degrees Celsius.

    """
    def __init__(self, value, temperature=15, calibration=15):
        tf = celsius_to_fahrenheit(temperature)
        cf = celsius_to_fahrenheit(calibration)

        # temperature correction factor
        factor = (1.00130346 - 0.000134722124 * tf + 0.00000204052596 * \
            tf ** 2 - 0.00000000232820948 * tf ** 3) / (1.00130346 - \
            0.000134722124 * cf + 0.00000204052596 * cf ** 2 - \
            0.00000000232820948 * cf ** 3)

        self.sg = value * factor
        self.plato = sg_to_plato(self.sg)
        self.brix = sg_to_brix(self.sg)

    def __str__(self):
        return 'SG...: {0:6.3f}\nPlato: {1:5.2f}\nBrix.: {2:5.2f}\
                    '.format(self.sg, self.plato, self.brix)


class Refractometer():
    """
    [8] (p.741-742) points out that "the scale in the viewing window of a
    refractometer is scaled in degrees Brix", but he also points that
    "the wort is not made of sucrose; it is made up of several different
    refraction index than a pure sucrose solution."  This way, industry
    standard equations were created to allow conversions between the
    various scales with a reasonable degree of accuracy.  In other words,
    you should convert the number read on refractometer.

    Refractometers usually read values between 0 and 32 (%) Brix, but we'll
    prefer those whose outputs in Plato.  Anyway, Acan can convert between
    these two units using the Specific Gravity conversion equations.
    According to [9], many refractometers have built in Auto Temperature
    Compensation (ATC).  In this case, any measurements under 37 degC, will
    be OK.

    An additional step must be taken if the wort is fermenting, but all the
    user must do is to change the fermenting parameter to that value read
    after the boil --OG.  Note that the unit used with this parameter --brix
    or plato-- must match the refractometer's unit.  For instance, if the
    refractometer reads values in Plato, fermenting should inform the OG
    in Plato.

    If you want to know more on refractometers, read [11].

    In a matter of comparison, BeerSmith 2 has 3 modes of operation for
    refractometers: unfermented, fermenting, and finished beer.  The first
    one is used at the end of boiling.  The second is used during the
    fermentation process, with the OG --just like the fermenting parameter
    works.  The third mode is used for finished beer, i.e., after the
    fermentation, before the primming.  In this last mode, one sample must
    be taken for refractometer and another for hydrometer, then the calibration
    is applyed using the values read in these two devices --here, the
    calibration parameter do this job.

    REFERENCES
    - fermenting_correction based on [5].
    - new_calibration based on [10] --example usage in README.md.

    PARAMETERS
    - value (float): value read on refractometer in degrees Brix.
    - unit (string): the unit of value in degrees brix or plato.
    - calibration (list): a list of tuples with calibration values, like this:
        [(refractometer, hydrometer), (...), ...]
    - fermenting (float): if the sample was taken from a fermenting wort,
        the OG must be informed in this parameter in degrees Brix.

    """
    def __init__(self, value, unit='brix', calibration=None, fermenting=None):
        self.value = value

        if calibration:
            self.calibration = self.new_calibration(calibration)
        else:
            self.calibration = 1.04

        if fermenting:  # FG/AE must be corrected during the fermentation
            if unit == 'brix':
                self.value = self.fermenting_correction(fermenting, self.value)
            elif unit == 'plato':
                self.value = brix_to_plato(
                    self.fermenting_correction(fermenting, self.value))

        if unit == 'brix':
            self.brix = self.value / self.calibration
            self.sg = brix_to_sg(self.brix)
            self.plato = sg_to_plato(self.sg)
        elif unit == 'plato':
            self.plato = self.value / self.calibration
            self.sg = plato_to_sg(self.plato)
            self.brix = plato_to_sg(self.plato)
        else:
            raise ValueError('unit must be brix or plato')

    def new_calibration(self, calibration):
        """
        First calibrate refractometer with distilled water (20 degC)
        to 0 Brix/Plato.

        PARAMETERS
        - calibration (list): list of tuples according to calibration
            parameter.

        TODO: this formula seems to lose accuracy on 4th decimal and
            should be fixed.

        """
        total = 0
        for r,h in calibration:
            total += r / sg_to_brix(h)
        return (total / len(calibration))

    def fermenting_correction(self, oe, ae):
        """
        Uses OE and AE to correct the sample value read during fermentation.
        - OE: Original Extract (OG)
        - AE: Apparent Extract (FG)

        RETURNS
        - (float): AE in degrees Brix.

        """
        return sg_to_brix(1.001843 - 0.002318474 * oe - 0.000007775 *
            oe ** 2 - 0.000000034 * oe ** 3 + 0.00574 * ae + 0.00003344 *
            ae ** 2 + 0.000000086 * ae ** 3)

    def __str__(self):
        return 'SG...: {0:6.3f}\nPlato: {1:6.3f}\nBrix.: {2:6.3f}\
                    '.format(self.sg, self.plato, self.brix)


class Palette():
    """
    Methods based on [12] and [13].  The three scales used here are:
    - Standard Reference Method (SRM)
    - European Brewing Convention (EBC)
    - Lovibond (L) --in honor of its creator, J. W. Lovibond (1833-1918)

    color_reference is based on [14].  Those hex values were found on the
    internet so they're not accurate.

    PARAMETERS
    - value (float): the color value in SRM, EBC, or Lovibond.
    - unit (string): scale used: srm, ebc, or l.

    """
    def __init__(self, value, unit='srm'):
        if unit == 'srm':
            self.srm = value
            self.ebc = self.srm_to_ebc(self.srm)
            self.l = self.srm_to_l(self.srm)

        elif unit == 'ebc':
            self.ebc = value
            self.srm = self.ebc_to_srm(self.ebc)
            self.l = self.srm_to_l(self.srm)

        elif unit == 'l':
            self.l = value
            self.srm = self.l_to_srm(self.l)
            self.ebc = self.srm_to_ebc(self.srm)

        else:
            raise ValueError('unit must be srm, ebc or l')

        self.hex = self.color_reference(self.srm)

    def ebc_to_srm(self, ebc):
        return ebc * 0.508

    def srm_to_ebc(self, srm):
        return srm * 1.97

    def l_to_srm(self, l):
        return (1.3546 * l) - 0.76

    def srm_to_l(self, srm):
        return (srm + 0.76) / 1.3546

    def color_reference(self, srm):
        color_map = {'straw': '#f0ecbc',
            'yellow': '#e5d67b',
            'gold': '#d1a133',
            'amber': '#bc742c',
            'deep-amber': '#a45a2d',
            'light-copper': '#a45a2d',
            'copper': '#964726',
            'deep-copper': '#7d3123',
            'light-brown': '#7d3123',
            'brown': '#65221a',
            'dark-brown': '#4f1313',
            'very-dark-brown': '#311315',
            'black': '#270a0f',
            'black-opaque': '#000000'}

        if 2 <= srm <= 3: return color_map['straw']
        elif 3 < srm <= 4: return color_map['yellow']
        elif 5 < srm <= 6: return color_map['gold']
        elif 6 < srm <= 9: return color_map['amber']
        elif 10 < srm <= 14: return color_map['deep-amber']
        elif 14 < srm <= 17: return color_map['copper']
        elif 17 < srm <= 18: return color_map['deep-copper']
        elif 19 < srm <= 22: return color_map['brown']
        elif 22 < srm <= 30: return color_map['dark-brown']
        elif 30 < srm <= 35: return color_map['very-dark-brown']
        elif 35 < srm <= 40: return color_map['black']
        elif 40 < srm: return color_map['black-opaque']
        else: return None

    def __str__(self):
        return 'SRM: {0:5.2f}\nEBC: {1:5.2f}\nL..: {2:5.2f}\nHex: {3}\
                    '.format(self.srm, self.ebc, self.l, self.hex)
