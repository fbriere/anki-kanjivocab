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
from anki.utils import splitFields


def field_idx(col, model, field):
    return col.models.fieldMap(model)[field][0]

def get_notes_field(col, model, field, query=""):
    """Returns a list of (note-id, field-contents) tuples for all notes whose
    type matches model, restricted by an optional query."""
    idx = field_idx(col, model, field)

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
        where n.mid = %s and %s""" % (
            model['id'],
            preds)

    res = col.db.all(sql, *args)

    return [ (id, splitFields(flds)[idx]) for id, mid, flds in res ]
