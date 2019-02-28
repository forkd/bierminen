# Aclla
Database of beer ingredients.  This project intends to be a standard to be used in Bierminen's experiments, as it'll handle all data for many beer ingredients.


## Data: Suppliers
This CSV file contains data of ingredient suppliers.


## Data: Fermentables
Fermentables information:

* `Name` (string): the name of that item.
* `ISO3166-1-Alpha-2` (string): the country of origin in 2 characters.
* `Type` (string): can be `Grain`, `Sugar`, `Extract`, or `Adjunct`.
* `Tags` (string): a kind of subtype; can be `basemalt`, `roastedmalt`, `crystalmalt`, `dryextract`, `liquidextract`, or `glutenfree`.
* `Color` (float): the color associated with the item, in degrees Lovibond.
* `Yield` (integer): amount of fermentable sugar that can be extracted from that item.
* `Source` (string): source of that item.
* `Date` (date): when that item was last modified.

### Sources

* [Brewer's Friend](http://www.brewersfriend.com/fermentables/)
* [BYO](http://byo.com/resources/grains)


## Data: Hops
Hops information:

* `Name` (string): hop name.
* `ISO3166-1-Alpha-2` (string): original country code in 2 chars.
* `Average-Alpha-Acids` (float): percent of alpha acids.
* `Common-Usage` (string): could be `Bittering`, `Aroma`, or `Dual`.
* `Source` (string): source of information.
* `Date` (date): last modification date.

### Sources

* [BYO](https://byo.com/resources/hops)
* [Brewer's Friend](http://www.brewersfriend.com/hops/)
* [Brewtoad](https://www.brewtoad.com/hops)
* How to Brew: PALMER, J. J.  3rd edition.  p.178-197.


## BFParser
Retrieves and parses data from Brewer's Friend site to JSON.  It can be used as a standalone program.

### Fermentable
`Fermentable` class handles the table of fermentable ingredients.

#### Example
```python
>>> from aclla.bfparser import Fermentable
>>> f = Fermentable()
>>> f.parse()
```


## BSParser
This parser is able to retrieve data from BeerSmith's XML files to use with Aclla.  BeerSmith 2 seems to use a dialect derived from BeerXML "standard" [1].

### Grain
The `Grain` class can handle BeerSmith's grain files --usually `Grain.bsmx`.  Just pass the path to that file and the tags you wish to get.  Common tag names are: `_MOD_`, `F_G_NAME`, `F_G_ORIGIN`, `F_G_SUPPLIER`, `F_G_TYPE`, `F_G_IN_RECIPE`, `F_G_INVENTORY`, `F_G_AMOUNT`, `F_G_COLOR`, `F_G_YIELD`, `F_G_LATE_EXTRACT`, `F_G_PERCENT`, `F_G_NOT_FERMENTABLE`, `F_ORDER`, `F_G_COARSE_FINE_DIFF`, `F_G_MOISTURE`, `F_G_DIASTATIC_POWER`, `F_G_PROTEIN`, `F_G_IBU_GAL_PER_LB`, `F_G_ADD_AFTER_BOIL`, `F_G_RECOMMEND_MASH`, `F_G_MAX_IN_BATCH`, `F_G_NOTES`, `F_G_BOIL_TIME`, `F_G_PRICE`, and `F_G_CONVERT_GRAIN`.

### Example
```python
>>> from aclla.bsparser import Grain
>>> g = Grain('/home/forkd/Downloads/Grain.bsmx')
>>> g.parse(['F_G_NAME', 'F_G_YIELD', 'F_G_COLOR', 'F_G_ORIGIN', 'F_G_NOTES'])
```


## References
1. BeerSmith.  Importing and Exporting Files.  Available at: [http://www.beersmith.com/help2/index.html?importing_and_exporting_files.htm](http://www.beersmith.com/help2/index.html?importing_and_exporting_files.htm).
2. BeerXML.  XML Standard for Beer Brewing Data.  Version 1.0.  Available at: [http://www.beerxml.com/beerxml.htm](http://www.beerxml.com/beerxml.htm).


## About
According to [Wikipedia](https://en.wikipedia.org/wiki/Aclla), Aclla in the religion of the Inca Empire were virgins chosen to keep the sacred fires of Inti burning. They were also occasionally sacrificed as well. Their other duties included brewing the beer of the Incas and on occasion serving as companions to the Inca emperor.

This project was conceived by José Lopes as part of his brewing project, [Bierminen](https://bierminen.com).  Join us on [Facebook](https://facebook.com/bierminen).

[Bierminen](https://bierminen.com): Zug von verrükten!

Cheers!

Prost!

Saúde!
