#!env/bin/python
#config.py
#
# Configuration file for Ninkasi app.
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

import os

class Production(object):
    DEBUG = False
    JSON_AS_ASCII = False
    DBUSER = 'postgres'
    DBPASS = 'foobar'
    DBHOST = 'localhost'
    DBPORT = '5432'
    DBNAME = 'ninkasi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{0}:{1}@{2}:{3}\
        /{4}'.format(DBUSER, DBPASS, DBHOST, DBPORT, DBNAME)
    SECRET_KEY = '90a81bdaa85b5d9dfc4c0cd89d9edaf93255d5f4160cd67bead46a91'

class Development(Production):
    DEBUG = True

config = {
    'development': 'app.config.Development',
    'production': 'app.config.Production'
}

def configure_app(app):
    app.config.from_object(config[os.getenv('NINKASI_MODE', 'production')])

