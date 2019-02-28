#!env/bin/python
#queries.py
#
# Implements methods to answer users queries.
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


from flask import jsonify, make_response


from app.models import Style, Subtype, Type


def error_response(status):
    if status == 404:
        return make_response(jsonify({'status':'not found'}), status)
    else:
        return make_response(jsonify({'status':'server error ({})'.format(
            status)}), status)

def style_response(status, num=-1, n='', st='', t='', ogi=-1, oga=-1,
        fgi=-1, fga=-1, abi=-1, aba=-1, ibi=-1, iba=-1, sri=-1, sra=-1, d=''):
    if status == 200:
        return {'number':num, 'name':n, 'subtype':st, 'type':t, 
            'og_min':ogi, 'og_max':oga, 'fg_min':fgi, 'fg_max':fga, 
            'abv_min':abi, 'abv_max':aba, 'ibu_min':ibi, 'ibu_max':iba, 
            'srm_min':sri, 'srm_max':sra, 'description':d}
    else:
        return error_response(status)

def get_styles(n):
    styles_list = []

    if n: styles = Style.query.filter_by(number=n)
    else: styles = Style.query.all()

    for s in styles:
        st = Subtype.query.filter_by(id=s.fk_subtype).first()
        t = Type.query.filter_by(id=st.fk_type).first()

        styles_list.append(style_response(200, s.number, s.name, st.name,
            t.name, s.og_min, s.og_max, s.fg_min, s.fg_max,
            s.abv_min, s.abv_max, s.ibu_min, s.ibu_max, s.srm_min, s.srm_max,
            s.description))

    if len(styles_list):
        return jsonify({'status':'OK', 'styles':styles_list})
    else:
        return style_response(404)

