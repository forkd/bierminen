#!env/bin/python
#__init__.py
#
# Initialization routines for Ninkasi.  Remember to create the database
# before running the application.  Details in README.md.
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


from flask import Flask

from app.config import configure_app
from app.views import resp
from app.database import db


app = Flask('ninkasi')
configure_app(app)
app.register_blueprint(resp)
db.init_app(app)

