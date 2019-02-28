# Acan
Maths around brewing.  Acan implements some known equations used by homebrewers.  All of them are well documented, so anyone could check where they came from and why.

Acan only needs Python 3 to run.  Having it, just install Acan and import it in your programs:

```
$ pip3 install acan
$ python3
>>> import acan
```


## Classes
Acan is a object-oriented calculator, so classes were implemented to do all the job.


### Hydrometer
Hydrometer class has all the methods needed to support hydrometer usage.  The basic usage of this class is to instantiate it with the value read on hydrometer --in SG.  Alternatively you can set up the temperatures to calibrate your results.

More info on its docstring.

#### Examples
In the first example, we only instantiate an Hydrometer object with the value read on hydrometer --e.g., 1.010.

In the second example, we calibrate the hydrometer using the temperatures.  The first parameter is the value, the second is the current temperature of the sample, and the last value is the temperature in which the hydrometer was calibrated.

```python
>>> from acan.tools import Hydrometer
>>> # First example
...
>>> h = Hydrometer(1.010)
>>> print(h)
SG...:  1.010
Plato:  2.56
Brix.:  2.34
>>> # Second example
...
>>> h1 = Hydrometer(1.010, 37, 20)
>>> print(h1)
SG...:  1.015
Plato:  3.78
Brix.:  3.56
```

### Refractometer
Refractometer class implements methods specific to refractometers.  The most common way to use it is to inform the value --in Plato (ideally) or Brix-- and it'll correct this value automatically with the default correction factor.  Read the class' docstring for more information.

#### Calibration
If you wish to set the calibration of your refractometer, you can use the `calibration` parameter, which accepts an iterable object with a tuple of refractometer value and the corresponding hydrometer value.  Let's go to examples to understand how it works.

#### Examples
```python
>>> from acan.tools import Refractometer
>>> # First example
...
>>> r = Refractometer(23.75)
r.calibration
1.04
>>> print(r)
SG...:  1.097
Plato: 23.029
Brix.: 22.837
>>> # Second example
...
>>> r1 = Refractometer(23.75, calibration=[(12.6, 1.050), (11.5, 1.045), (13.7, 1.055)])
>>> r1.calibration
1.0395278561663661
>>> print(r1)
SG...:  1.097
Plato: 23.040
Brix.: 22.847
```


### Palette
This class has methods relative to color calculations.  The easiest way to use it is to instantiate an object with the corresponding color value in SRM, EBC or Lovibond.

#### Examples
```python
>>> from acan.tools import Palette
>>> # First example
...
>>> p = Palette(15)
>>> print(p)
SRM: 15.00
EBC: 29.55
L..: 11.63
Hex: #964726
>>> # Second example
...
>>> p1 = Palette(20, 'ebc')
>>> print(p1)
SRM: 10.16
EBC: 20.00
L..:  8.06
Hex: #a45a2d
```


### Wort
Wort class aggregates all methods used to measure the wort quality.  To use it, just take original and final gravities, and pass them as parameter to this class --for final gravity, you can assume the last sample taken from the wort.

#### Examples
```python
>>> from acan.wort import Wort
>>> w = Wort(1.051, 1.013)
>>> print(w)
Original gravity....[SG]:   1.051
Final gravity.......[SG]:   1.013
Volume...............[L]:   0.000
Efficiency...........[%]:   0.000
Original extract.[Plato]:  12.625
Actual extract...[Plato]:   3.321
Real extract.....[Plato]:   5.003
Apparent attenuation.[%]:  73.692
Real attenuation.....[%]:  60.368
Alcohol by weight....[%]:   3.951
Alcohol by volume....[%]:   5.067
Calories in 355 mL.[Cal]: 168.579
```

To calculate the efficiency, use the parameters `grains` and `volume`.  Consider the example below:

* 2948.3 grams of 36 maximum efficiency --in PPG-- malt;
* 226.8 grams of 34 m.e. malt (x2);
* 226.8 grams of 35 m.e. malt;
* 226.8 grams of 30 m.e. malt;
* 22.71 litres of wort; and
* OG == 1.038.

The efficiency could be calculated like this:

```python
>>> from acan.wort import Wort
>>> print(Wort(1.038, 1.013, grains=[(2948.3, 36), (226.8, 34),(226.8, 34), (226.8, 35), (226.8, 30)], volume=22.71))
Original gravity.....[SG]:   1.038
Final gravity........[SG]:   1.013
Original extract..[Plato]:   9.510
Apparent extract..[Plato]:   3.321
Real extract......[Plato]:   4.440
Volume................[L]:  22.710
Points/Pound/Gallon.[PPG]:  26.821
Mash efficiency.......[%]:  75.866
Apparent attenuation..[%]:  65.789
Real attenuation......[%]:  59.573
Alcohol by weight.....[%]:   2.600
Alcohol by volume.....[%]:   3.333
Calories in 355 mL..[Cal]: 126.936
```

For more information, read the class' docstring.  It's important to note that in this work, brewhose and mash efficiencies are the same.


### Hops
This class have common equations to calculate hop bitterness.  Methods like Tinseth, Rager, and Garetz are covered here as well as those used by John Palmer and Ray Daniels.

#### Examples
```python
>>> from acan.wort import Hops
>>> h = Hops(56.69904, 7, 18.92706, 1.020, 12)
>>> print(h)
Hops weight.......[g]:  56.70
Hops alpha acids..[%]:   7.00
Wort volume.......[L]:  18.93
Wort SG...........[L]:   1.020
Hops boil time....[m]:  12
Wort bitterness.[IBU]:  26.554
>>> h.daniels(28.34952, 12.5, 22.712471, 1.048, 60, 'whole')
37.44575392083054
```


## PyPI

Acan is now [published at Python Package Index (PyPI)](https://pypi.python.org/pypi/acan).  A `Makefile` was created to automate all the job of packaging, but some things must to be set first.

The steps below were based on:

* [Packaging and Distributing Projects](https://packaging.python.org/distributing/)
* [How to submit a package to PyPI](http://peterdowns.com/posts/first-time-with-pypi.html)

### Configuration

The very first thing to be set up is the `setup.py`.  This file must updated with the new version at least.  The versioning adopted by Acan is: `<major version>`.`<minor version>`.`<bug fixes>`.  By `<major version>`, we can understand very big changes in the code.  `<minor version>` means new features in the current version, like new classes.  Finally, `<bug fixes>` are, of course, bug fixes, or little changes in the code, like typo fixes.

In order to upload this new version to PyPI, a `~/.pypirc` file must be created with a content like this --considering you already have a PyPI account:

```bash
[distutils]
index-servers =
    pypi

[pypi]
repository=https://www.python.org/pypi
username=USERNAME
password=PASSWORD
```

Note that I had problems using some special characters in `PASSWORD`.

After all of this, just run `$ make pypi` to create the package and upload it to PyPI.

This way, the process I follow is:

1. Clone, create virtualenv, and modify the project.
2. Update the version in `setup.py`.
3. Commit to GitHub.
4. Run `make pypi`.


## References
1. NIST.  Polarimetry, Saccharimetry and the Sugars.  1942.  Available at: <http://www.boulder.nist.gov/div838/SelectedPubs/Circular%20440%20Table%20114.pdf>.
2. Brew Your Own.  Calculating Alcohol Content, Attenuation, Extract and Calories: Advanced Homebrewing.  2005.  Available at: <http://byo.com/hops/item/408-calculating-alcohol-content-attenuation-extract-and-calories-advanced-homebrewing>.
3. HAYNES, W.N.  CRC Handbook of Chemistry and Physics Internet Version. 2015.  96th edition.
4. Brewtoad.  Alcohol Calculator.  Available at: <https://www.brewtoad.com/tools/alcohol-calculator>.
5. Onebeer.  Refractometer Calculator.  Available at: <http://onebeer.net/refractometer.shtml>.
6. DEVRIES, J.  Specific Gravity and Brix/Plato Conversion.  Available at: <http://jayson.devri.es/2010/08/specific-gravity-and-brixplato.html>.
7. Brewtarget.  HydrometerTool.cpp.  Available at: <https://github.com/Brewtarget/brewtarget/blob/develop/src/HydrometerTool.cpp#L134>
8. PALMER, J.J.  How to Brew. 2006.  3rd edition.
9. Brewer's Friend.  Using your Refractometer Correctly for Maximum Accuracy in Home Brewing.  Available at: <http://www.brewersfriend.com/2013/04/24/using-your-refractometer-correctly-for-maximum-accuracy-in-home-brewing/>.
10. Brew Your Own.  Refractometers.  Available at: < http://byo.com/stories/item/1313-refractometers>.
11. Zymurgy.  Using a Refractometer.  2013.  Vol 36, no. 4.  p.48-53.
12. BeerSmith.  Beer Color: Understanding SRM, Lovibond and EBC.  Available at: <http://beersmith.com/blog/2008/04/29/beer-color-understanding-srm-lovibond-and-ebc/>.
13. Brewtoad.  Color Converter.  Available at: <https://www.brewtoad.com/tools/color-converter>.
14. Beer Judge Certification Program (BJCP).  2015 Style Guidelines - Beer Style Guidelines.  Available at: <http://www.bjcp.org/docs/2015_Guidelines_Beer.pdf>.
15. Home Brew Digest.  Brewing Calculator 2.41.  Available at: <http://hbd.org/deb/downloads.html>.
16. DANIELS, R.  Designing Great Beers.  2000.
17. BeerSmith.  Apparent and Real Attenuation for Beer Brewers - Part 2. Available at: <http://beersmith.com/blog/2010/09/14/apparent-and-real-attenuation-for-beer-brewers-part-2/>.
18. Kegerator.  How to Calculate Brewhouse Efficiency.  Available at: <http://learn.kegerator.com/brewhouse-efficiency/>.
19. PYLE, N.  Norm Pyle's Hops FAQ.  Available at: <http://www.realbeer.com/hops/FAQ.html>.
20. Real Beer.  The Hop Page.  Available at: <http://www.realbeer.com/hops>.


## About
According to [Wikipedia](https://en.wikipedia.org/wiki/Acan), Acan is the Maya god of wine and intoxication, and his name means 'belch'.  He is identified with the local brew, [balché](https://en.wikipedia.org/wiki/Balch%C3%A9), made from fermented honey to which the bark of the balché tree has been added.

This project was conceived by José Lopes as part of his brewing project, [Bierminen](https://bierminen.com).  Join us on [Facebook](https://facebook.com/bierminen).

[Bierminen](https://bierminen.com): Zug von verrükten!

Cheers!

Prost!

Saúde!
