#!../env/bin/python
#initdb.py
#
# Database creation routines.
#
# Author: José Lopes de Oliveira Jr. <bierminen.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##


from app.models import db, Type, Subtype, Style


##
# GLOBAL VARIABLES
#
# Note: beers which SRV max is 40+ are indexed as 40.
NA = 0  # Not Applicable -- used in some beer representations
IN = 99  # Infinite -- used in some beer representations
TYPES = (u'Ale', u'Lager', u'Mixed')
SUBTYPES = ((TYPES[0], u'Wheat Beer'),
            (TYPES[0], u'Lambic & Sour Ale'),
            (TYPES[0], u'Belgian Ale'),
            (TYPES[0], u'Pale Ale'),
            (TYPES[0], u'English Bitter'),
            (TYPES[0], u'Scottish Ale'),
            (TYPES[0], u'Brown Ale'),
            (TYPES[0], u'Porter'),
            (TYPES[0], u'Stout'),
            (TYPES[1], u'Pilsner'),
            (TYPES[1], u'American Lager'),
            (TYPES[1], u'European Lager'),
            (TYPES[1], u'Bock'),
            (TYPES[2], u'Alt'),
            (TYPES[2], u'French Ale'),
            (TYPES[2], u'German Amber Ale'),
            (TYPES[2], u'American Special'),
            (TYPES[2], u'Smoked Beer'),
            (TYPES[2], u'Barley Wine'),
            (TYPES[2], u'Strong Ale'))
STYLES = ((SUBTYPES[0][1], 1, u'Berliner Weisse', 1.026, 1.036, 1.006, 1.009, 2.5, 3.6, 3, 12, 2, 4, u'Light body. Refreshing. Slightly fruit. Sour. Low influence of hop. (Schultheiss Berliner Weisse, Berliner Kindl Weisse)'),
          (SUBTYPES[1][1], 2, u'Lambic', 1.044, 1.056, 1.006, 1.012, 4.7, 6.4, 5, 15, 4, 15, u'The most unusual sour-tasting beer with very hop aroma. (Grand Cru Cantillon Bruocsella 1900, Boon, De Neve)'),
          (SUBTYPES[2][1], 3, u'Belgian Gold Ale', 1.065, 1.085, 1.014, 1.020, 7.0, 9.0, 25, 35, 4, 6,u'Fruity. Soft malt aroma. Spice aroma. Low bitterness. (Duvel, Lucifer, La Chouffe, Moinette, Celis Grand Cru)'),
          (SUBTYPES[0][1], 4, u'Belgian White', 1.042, 1.055, 1.008, 1.012, 4.5, 5.5, 15, 28, 2, 4,u'Refreshing. Cloudy. Spiced with coriander and orange peel. Low bitterness. (Celis White, Hoegaarden White, Blanche de Bruges)'),
          (SUBTYPES[1][1], 5, u'Gueuze', 1.044, 1.056, 1.006, 1.012, 4.7, 6.4, 5, 15, 4, 15, u'Blend of young and old Lambic beers. (Lindeman\'s Gueuze Lambic, Belle-Gueuze, Boon, Cantillon, Hanssens)'),
          (SUBTYPES[2][1], 6, u'Tripel', 1.070, 1.100, 1.016, 1.024, 7.0, 10.0, 20, 30, 4, 7, u'Light/pale color, balanced malt and hop aroma. Sweetish. High alcohol content. (Westmalle Tripel, Affligem Tripel, Grimbergen Tripel)'),
          (SUBTYPES[0][1], 7, u'American Wheat', 1.035, 1.055, 1.008, 1.018, 3.5, 5.0, 5, 20, 2, 8, u'Usually clear in contrast to most other wheat beers. Slightly tart. Very refreshing. (Samuel Adams Summer Ale, Catamount American Wheat)'),
          (SUBTYPES[1][1], 8, u'Faro', 1.040, 1.056, 1.006, 1.012, 4.5, 5.5, 5, 15, 4, 15, u'Sweetened version of lambic. (Lindeman\'s)'),
          (SUBTYPES[2][1], 9, u'Saison', 1.052, 1.080, 1.010, 1.015, 4.5, 8.1, 25, 40, 4, 10, u'Fruity. Complex aroma and flavor of high alcohol, herbs, and spices. Moderate hop aroma and flavor. (Saison Dupont, Moinette, Laforet)'),
          (SUBTYPES[3][1], 10, u'Pale Ale', 1.043, 1.056, 1.008, 1.016, 4.5, 5.5, 20, 40, 4, 11, u'Low to medium maltiness. High hop bitterness. Medium hop profile. (Draught Bass, Samuel Smith Old Brewery Pale Ale)'),
          (SUBTYPES[10][1], 11, u'American Lite', 1.024, 1.040, 1.002, 1.008, 2.9, 4.5, 8, 15, 2, 4, u'Little to no malt aroma. Very low in hops. Crisp and dry. Refreshing. (Bud Light, Miller Light)'),
          (SUBTYPES[11][1], 12, u'Munich Helles', 1.044, 1.050, 1.008, 1.012, 4.5, 5.6, 18, 25, 3, 5, u'Mildly hopped and mildly malty. Fuller body than most lagers. (Black Forest Lager, Spaten Premium Lager)'),
          (SUBTYPES[12][1], 13, u'Helles Bock', 1.066, 1.074, 1.011, 1.020, 6.0, 7.5, 20, 35, 4, 10, u'Malty, Mildly hopped. Relatively high alcohol level. (Wuerzbuger Maibock, Spatten Premium Bock, Pschorr Märzenbock)'),
          (SUBTYPES[0][1], 14, u'Weizenbier', 1.040, 1.056, 1.008, 1.016, 4.3, 5.6, 8, 15, 3, 9, u'Notable clove and banana aroma from German wheat yeast. Fruity. Cloudy. Low hop profile. (Erdinger Weissbier, Pyramid wheaten ale, Julius Echter Weizenbier)'),
          (SUBTYPES[1][1], 15, u'Fruit Beer', 1.040, 1.072, 1.008, 1.016, 4.7, 7.0, 15, 21, NA, NA, u'Taste and aroma depend on fruit(s) used. Usually dry and winey. Not all fruit beers are lambic based. (Belle-Vue Kriek, Lindeman\'s Framboise Lambic)'),
          (SUBTYPES[2][1], 16, u'Belgian Pale Ale', 1.040, 1.055, 1.008, 1.013, 3.9, 5.6, 20, 35, 4, 14, u'Low bitterness. Low malt aroma. Slightly fruity and sour. (Celis Pale Bock, DeKoninck Special Palm Ale, Ginder Ale)'),
          (SUBTYPES[3][1], 17, u'American Pale Ale', 1.045, 1.056, 1.010, 1.015, 4.5, 5.7, 20, 40, 4, 11, u'Medium maltiness. High hop bitterness. Medium flavor and aroma from American hop varieties. (Sierra Nevada Pale Ale, Summit Pale Ale, Geary\'s Pale Ale)'),
          (SUBTYPES[4][1], 18, u'Ordinary Bitter', 1.030, 1.038, 1.006, 1.012, 3.0, 3.8, 20, 35, 6, 12, u'Low carbonation. Low to medium maltiness. Mild hop flavor and aroma. (Young\'s Bitter, HSB Premium Bitter)'),
          (SUBTYPES[5][1], 19, u'Scottish Light 60/-', 1.030, 1.035, 1.006, 1.012, 2.8, 4.0, 9, 20, 8, 17, u'Low carbonation. Medium maltiness. Low bitterness. Medium to no hop flavor and aroma. Light smoky/toasty character (Belhaven 60/-, Caledonian 60/-, Maclay 60/- Light, Highland Dark Light)'),
          (SUBTYPES[6][1], 20, u'English Mild', 1.030, 1.038, 1.004, 1.012, 2.5, 4.1, 10, 24, 10, 25, u'Light brown. Mild maltiness. Low alcohol. Low hop bitterness, flavor, and aroma. Light body. (Bank\'s Mild, Fuller\'s Summer Ale)'),
          (SUBTYPES[8][1], 21, u'Dry Stout', 1.035, 1.050, 1.008, 1.014, 3.2, 5.5, 30, 50, 40, IN, u'Roasted barley and malt aromas are prominent. Some sourness. Hop aroma medium to none. (Guinness Draught Stout, Murphy\'s Stout, Beamish Stout)'),
          (SUBTYPES[8][1], 22, u'Foreign Extra Stout', 1.050, 1.075, 1.010, 1.017, 5.0, 7.5, 35, 70, 40, IN, u'Roasted grain aroma and flavor are prominent. Flavor range from sweet to dry. Hop aroma and flavor very low. Fruity. (ABC Stout, Guinness Foreign Extra Stout)'),
          (SUBTYPES[9][1], 23, u'German Pilsner', 1.044, 1.050, 1.006, 1.012, 4.6, 5.4, 25, 45, 2, 4, u'Medium to high hop flavor and aroma. Low maltiness. Crisp, dry, and bitter. Refreshing. (Kulmbacher Moenchshof Pils, Jever Pils, Wickuler Pilsner)'),
          (SUBTYPES[10][1], 24, u'American Standard', 1.040, 1.046, 1.006, 1.010, 4.1, 4.8, 5, 17, 2, 6, u'Similar to American Light, but darker. (Budweiser, Molson Golden, Kirin)'),
          (SUBTYPES[11][1], 25, u'Dortmunder', 1.048, 1.056, 1.010, 1.014, 5.1, 6.1, 23, 29, 4, 6, u'Smooth. Medium malty sweetness. Medium hop aroma and flavor. (Dortmunder Gold, DAB Original, Berghoff Original Lager)'),
          (SUBTYPES[12][1], 26, u'Doppelbock', 1.074, 1.080, 1.020, 1.028, 6.6, 7.9, 20, 30, 12, 30, u'Intense maltiness. Little hop aroma and flavor. Touch of roastiness. A very strong, rich lager. (Paulaner Salvator, Spaten Optimator)'),
          (SUBTYPES[0][1], 27, u'Dunkelweizen', 1.048, 1.056, 1.008, 1.016, 4.5, 6.0, 10, 15, 17, 23, u'Low clove and banana aroma. Malty. Low bitterness. Low hop aroma. (Franziskaner Dunkel-Weizen, Schneider Dunkel Weiss)'),
          (SUBTYPES[1][1], 28, u'Flanders Red', 1.042, 1.060, 1.008, 1.016, 4.0, 5.8, 14, 25, 10, 16, u'Fruity. Malty. Slightly sour. Low hop profile. (Rodenbach, Petrus, Bourgogne des Flanders, Vlaamse Bourgogne)'),
          (SUBTYPES[2][1], 29, u'Belgian Dark Ale', 1.065, 1.098, 1.014, 1.024, 7.0, 12.0, 25, 40, 7, 20, u'Fruity. Malty. Bitter. High alcohol content. (Pawel Kwak, Gourden Carolus, Scaldis, Rocherfort 10, Chimary Grand Reserve)'),
          (SUBTYPES[3][1], 30, u'India Pale Ale', 1.050, 1.075, 1.012, 1.018, 5.1, 7.6, 40, 60, 8, 14, u'Medium maltiness. High hop bitterness. High hop flavor and aroma. (Anchor Liberty Ale, Samuel Smith\'s India Ale, Fuller IPA)'),
          (SUBTYPES[4][1], 31, u'Special Bitter', 1.039, 1.045, 1.006, 1.014, 3.7, 4.8, 25, 40, 12, 14, u'Low carbonation. More malty and higher alcohol than ordinary bitter. Nice bitterness. (Young\'s Ramrod, Fuller\'s London Pride)'),
          (SUBTYPES[5][1], 32, u'Scottish Heavy 70/-',1.035, 1.040, 1.010, 1.014, 3.5, 4.1, 12, 25, 10, 19, u'Low carbonation. Moderate hop profile. Mild smoky character. (Greenmantle Ale, Highland Heavy, Young\'s Scotch Ale)'),
          (SUBTYPES[6][1], 33, u'American Brown', 1.040, 1.055, 1.010, 1.018, 4.2, 6.0, 25, 60, 15, 22, u'Medium maltiness. High hop bitterness, flavor, and aroma. (Pete\'s Wicked Ale, Brooklyn Brown Ale, Shipyard Moos Brown)'),
          (SUBTYPES[7][1], 34, u'Brown Porter',1.040, 1.050, 1.008, 1.014, 3.8, 5.2, 20, 30, 20, 35, u'Moderate roastiness. Moderate bitterness. Hop flavor and aroma low to none. (Samuel Smith Taddy Porter, Fuller\'s London Porter)'),
          (SUBTYPES[8][1], 35, u'Sweet Stout', 1.035, 1.066, 1.010, 1.022, 3.2, 6.4, 20, 40, 40, IN, u'Overall sweet character. Roasted grains dominate the flavor. Some fruitiness. (Mackeson\'s XXX Stout, Samuel Adams Cream Stout)'),
          (SUBTYPES[8][1], 36, u'Imperial Stout', 1.075, 1.090, 1.020, 1.030, 7.8, 9.0, 50, 80, 40, IN, u'Fruity with intense roastiness and maltiness. Evident hop aroma and flavor. High alcohol level. (Samuel Smith Imperial Stout, Courage Imperial Stout)'),
          (SUBTYPES[9][1], 37, u'Bohemian Pilsner', 1.044, 1.056, 1.014, 1.020, 4.1, 5.1, 35, 45, 3, 5, u'Malty, with a distinctive floral and spicy Saaz hop bouquet. Crisp and refreshing. (Pilsner Urquell, Gambrinus Pilsner, Budweiser Budvar)'),
          (SUBTYPES[10][1], 38, u'American Premium', 1.046, 1.050, 1.010, 1.014, 4.6, 5.1, 13, 23, 2, 8, u'Darker version of American Standard (Michelob)'),
          (SUBTYPES[11][1], 39, u'Munich Dunkel', 1.052, 1.056, 1.010, 1.014, 4.8, 5.4, 16, 25, 17, 23, u'Munich malt aroma and flavor. Mild hop flavor. (Ayinger Altbairisch Dunkel, Hacker Pschorr Alt Munich Dark)'),
          (SUBTYPES[12][1], 40, u'Traditional Bock', 1.066, 1.074, 1.018, 1.024, 6.4, 7.6, 20, 30, 15, 30, u'Rich and complex maltiness. No hop aroma and flavor. (Aass Bock, Hacker-Pschorr Dunkel Bock, Dunkel Ritter Bock, Boiler Room Red)'),
          (SUBTYPES[0][1], 41, u'Weizenbock', 1.066, 1.080, 1.016, 1.028, 6.5, 9.6, 12, 25, 10, 30, u'Malty. Low bitterness. Clove and banana aroma from german wheat yeast. (Schneider Aventinus, Pyramid Weizenbock)'),
          (SUBTYPES[1][1], 42, u'Oud Bruin', 1.042, 1.060, 1.008, 1.016, 4.0, 6.5, 14, 30, 12, 20, u'Fruity. Malty. Sherry wine-like. Slightly sour. Very little hop aroma and flavor. (Liefman\'s Goudenband, Felix, Roman)'),
          (SUBTYPES[2][1], 43, u'Dubbel', 1.065, 1.085, 1.012, 1.018, 3.2, 8.0, 20, 25, 10, 20, u'Rich malt aroma. Light to none hop aroma. Full body. Low bitterness. (Westmalle Dubbel, LaTrappe Dubbel, Affligem Dubbel)'),
          (SUBTYPES[3][1], 44, u'American Amber Ale', 1.043, 1.056, 1.008, 1.016, 4.5, 5.7, 20, 40, 11, 18, u'Medium maltiness. Mild to strong flavor and aroma from American hop varieties. Notable caramel flavor. (Big Time Atlas Amber, Bell\'s Amber, North Coast Red Seal Ale)'),
          (SUBTYPES[4][1], 45, u'Extra Special Bitter', 1.046, 1.065, 1.010, 1.018, 3.7, 4.8, 30, 45, 12, 14, u'Low carbonation. Very strong bitterness. Malty. High hop aroma and flavor. (Fuller\'s ESB, Young\'s Special London Ale)'),
          (SUBTYPES[5][1], 46, u'Scottish Export 80/-', 1.040, 1.050, 1.010, 1.018, 4.0, 4.9, 15, 36, 10, 19, u'Low carbonation. Very malty. Medium bitterness. Medium to no hop flavor and aroma. Mild smoky/toasty character. (Highland Severe, Orkney Dark Island, Sherlock\'s Home Piper\'s Pride)'),
          (SUBTYPES[6][1], 47, u'English Brown', 1.040, 1.050, 1.008, 1.014, 3.5, 6.0, 15, 25, 15, 30, u'Sweet and malty. Light caramel flavor. Low hop profile. Some fruitiness. (Newcastle Brown Ale, Samuel Smith Nut Brown)'),
          (SUBTYPES[7][1], 48, u'Robust Porter', 1.050, 1.065, 1.012, 1.016, 4.8, 6.0, 25, 45, 30, 40, u'Roasted malt (coffee-like) aroma and flavor. Hop flavor and aroma moderate to low. (Sierra Nevada Porter, Anchor Porter)'),
          (SUBTYPES[8][1], 49, u'Oatmeal Stout', 1.035, 1.060, 1.008, 1.021, 3.3, 6.1, 20, 50, 40, IN, u'Mild roasted grain aromas. Low hop aroma. Flavor medium sweet with the complexity of roasted grains. Some fruitiness. (Samuel Smith Oatmeal Stout, Young\'s Oatmeal Stout, Brew Moon Eclipse)'),
          (SUBTYPES[8][1], 50, u'Russian Imperial Stout', 1.075, 1.100, 1.018, 1.030, 8.0, 12.0, 50, 90, 40, IN, u'Similar to Imperial Stout, but has higher alcohol level and bitterness. (Harvey & Son\'s Imperial Extra Double Stout)'),
          (SUBTYPES[9][1], 51, u'American Pilsner', 1.045, 1.060, 1.012, 1.018, 5.0, 6.0, 20, 40, 3, 6, u'Medium to high maltiness. Slight sweetness. Medium to high hop aroma and flavor. Refreshing. (Pete\'s Signature Pilsner, Milwaukee Pilsner)'),
          (SUBTYPES[10][1], 52, u'American Dark', 1.040, 1.050, 1.008, 1.012, 4.1, 5.6, 14, 20, 10, 20, u'Malty. Some roasted malt flavor. Low hops. (Michelob Dark, Lowenbrau Dark, Beck\'s Dark, Saint Pauli Girl Dark)'),
          (SUBTYPES[11][1], 53, u'Schwarzbier', 1.044, 1.052, 1.012, 1.016, 3.8, 5.0, 22, 30, 25, 40, u'Malt and roasted malt aroma and flavor. Low hop aroma. Bitterness from roasted malt. (Kulmbacher Mönchschof Kloster Schwartz-Bier)'),
          (SUBTYPES[12][1], 54, u'Eisbock', 1.090, 1.116, 1.023, 1.035, 8.7, 14.4, 25, 50, 18, 40, u'Aroma and flavor dominated by rich malt and concentrated alcohol. No hop aroma and flavor. An extremely strong lager. (Niagara Eisbock)'),
          (SUBTYPES[13][1], 55, u'Kölsch', 1.042, 1.046, 1.006, 1.010, 4.8, 5.2, 20, 30, 4, 5, u'Low maltiness. Light hop aroma and flavor from German noble or Saaz hops. (Malzmuehle, Hellers, Hollywood Blonde)'),
          (SUBTYPES[14][1], 56, u'Biére de Garde', 1.060, 1.080, 1.012, 1.016, 4.5, 8.0, 20, 30, 5, 12, u'Malty and slightly fruity. Low hoppiness. Medium to strong alcohol level. (Jenlain, Castelain, Septante Cinq, Brasseurs Biére de Garde)'),
          (SUBTYPES[15][1], 57, u'Oktoberfest', 1.050, 1.056, 1.012, 1.016, 5.1, 6.5, 18, 30, 7, 12, u'Very flavorful. Distinct German malt aroma and flavor. Moderate hop bitterness and flavor. (Spaten Ur-Märzen, Ayinger Oktoberfest-Märzen, Paulaner Oktoberfest, Wuerzburger Oktoberfest)'),
          (SUBTYPES[16][1], 58, u'Cream Ale', 1.044, 1.055, 1.007, 1.010, 4.5, 6.0, 10, 35, 8, 14, u'Low hop aroma and bittering. Low maltiness. Light and refreshing. (Genesee Cream Ale, Little Kings Cream Ale)'),
          (SUBTYPES[17][1], 59, u'Smoked Beer', 1.050, 1.055, 1.012, 1.016, 5.0, 5.5, 20, 30, 12, 17, u'Sweetish and malty. Similar to Oktoberfest style with evident smoked character. Low hop aroma and flavor. (Schlenkerla Rauchbier)'),
          (SUBTYPES[19][1], 60, u'English Old (strong) ale', 1.060, 1.090, 1.015, 1.022, 6.1, 8.5, 30, 40, 12, 16, u'Well aged. Malty and fruity. High alcohol. Low hop. (Theakston Old Peculier, Young\'s Winter Warmer, Marston Owd Roger)'),
          (SUBTYPES[13][1], 61, u'Altbier', 1.044, 1.048, 1.008, 1.014, 4.6, 5.1, 25, 48, 11, 19, u'Malt dominates all aromas and flavors. High hop bitterness. (DAB Dark, Diebels Alt, Alaskan Amber, Grolsch Autumn Amber)'),
          (SUBTYPES[15][1], 62, u'Vienna', 1.048, 1.056, 1.010, 1.014, 4.6, 5.5, 20, 28, 8, 14, u'Dark German malt aroma. Hop bitterness is moderate. (Negra Modelo, Portland Lager, Leinenkugel Red)'),
          (SUBTYPES[16][1], 63, u'Steam Beer', 1.040, 1.055, 1.012, 1.018, 3.6, 5.0, 35, 45, 8, 17, u'Malty, balanced with hop bitterness. Woody (Northern Brewer) hop flavor. (Anchor Steam, Old Domination Victor Amber)'),
          (SUBTYPES[18][1], 64, u'Barleywine', 1.085, 1.120, 1.024, 1.032, 8.4, 12.2, 50, 100, 14, 22, u'Fruity and malty. High hop aroma and flavor. High alcohol content. (Young\'s Old Nick, Fuller\'s Golden Pride, Sierra Nevada Bigfoot)'),
          (SUBTYPES[19][1], 65, u'Strong "Scotch" Ale', 1.072, 1.085, 1.016, 1.028, 6.0, 9.0, 20, 40, 10, 40, u'Malty with caramel apparent. Hint of roasted malt or smoky flavor. Low hop flavor. (Traquair House, MacAndrew\'s Scotch Ale)'))


def builder():
    db.create_all()

    for t in TYPES:
        db.session.add(Type(t))
    db.session.commit()
    
    for st in SUBTYPES:
        db.session.add(Subtype(st[0], st[1]))
    db.session.commit()

    for s in STYLES:
        db.session.add(Style(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], 
            s[9], s[10], s[11], s[12], s[13]))
    db.session.commit()

