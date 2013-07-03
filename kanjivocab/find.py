# -*- coding: utf-8 -*-
#
# kanjivocab - Anki plugin to tag vocabulary cards based on kanji
#
# Copyright (c) 2012-2013  Frédéric Brière <fbriere@fbriere.net>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


import anki
import anki.find
from anki.utils import ids2str, splitFields


def field_map(col, field):
    """Returns a dict mapping, for each model containing the specified field,
    that model's ID (as a string) to the field's index."""
    # This was copied from anki.find._findField
    field = field.lower()

    mods = {}
    for m in col.models.all():
        for f in m['flds']:
            if f['name'].lower() == field:
                mods[m['id']] = f['ord']

    return mods

def get_notes_field(col, field, query=""):
    """Returns a list of (note-id, field-contents) tuples for all notes whose
    type contains field, restricted by an optional query."""
    models = field_map(col, field)
    if not models:
        return []

    # The following was mostly copied from anki.find.findNotes
    finder = anki.find.Finder(col)
    tokens = finder._tokenize(query)
    preds, args = finder._where(tokens)
    if preds is None:
        return []

    if preds:
        preds = "(" + preds + ")"
    else:
        preds = "1"

    sql = """select distinct n.id, n.mid, n.flds
        from cards c join notes n on c.nid=n.id
        where n.mid in %s and %s""" % (
            ids2str(models.keys()),
            preds)

    res = col.db.all(sql, *args)

    return [ (id, splitFields(flds)[models[mid]]) for id, mid, flds in res ]
