#!../env/bin/python
#models.py
#
# Ninkasi's models file.
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


from app.database import db


class Type(db.Model):
    __tablename__ = 'Types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    subtypes = db.relationship('Subtype')

    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return '<Type {}>'.format(self.name)

class Subtype(db.Model):
    __tablename__ = 'Subtypes'
    id = db.Column(db.Integer, primary_key=True)
    fk_type = db.Column(None, db.ForeignKey('Types.id'))
    name = db.Column(db.String(30), nullable=False, unique=True)
    styles = db.relationship('Style')

    def __init__(self, fkt, n):
        self.fk_type = Type.query.filter_by(name=fkt).first().id
        self.name = n

    def __repr__(self):
        return '<Subtype {}>'.format(self.name)

class Style(db.Model):
    __tablename__ = 'Styles'
    id = db.Column(db.Integer, primary_key=True)
    fk_subtype = db.Column(None, db.ForeignKey('Subtypes.id'))
    number = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    og_min = db.Column(db.Float, nullable=False)
    og_max = db.Column(db.Float, nullable=False)
    fg_min = db.Column(db.Float, nullable=False)
    fg_max = db.Column(db.Float, nullable=False)
    abv_min = db.Column(db.Float, nullable=False)
    abv_max = db.Column(db.Float, nullable=False)
    ibu_min = db.Column(db.Integer, nullable=False)
    ibu_max = db.Column(db.Integer, nullable=False)
    srm_min = db.Column(db.Integer, nullable=False)
    srm_max = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))

    def __init__(self, fks, num, n, ogi, oga, fgi, fga, abi, aba, 
                 ibi, iba, sri, sra, d):
        self.fk_subtype = Subtype.query.filter_by(name=fks).first().id
        self.number = num
        self.name = n
        self.og_min = ogi
        self.og_max = oga
        self.fg_min = fgi
        self.fg_max = fga
        self.abv_min = abi
        self.abv_max = aba
        self.ibu_min = ibi
        self.ibu_max = iba
        self.srm_min = sri
        self.srm_max = sra
        self.description = d

    def __repr__(self):
        return '<Style {}>'.format(self.name)

