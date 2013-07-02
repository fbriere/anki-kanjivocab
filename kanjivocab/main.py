# -*- coding: utf-8 -*-
#
# kanjivocab - Anki plugin to tag vocabulary cards based on kanji
#
# Copyright (c) 2012  Frédéric Brière <fbriere@fbriere.net>
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
import anki.utils

from kanjivocab.unicode import is_kanji


def get_studied_kanji(col, model, field, filter=None):
    """Returns the (frozen) set of all studied kanji."""
    search_str = 'note:"%s"' % model['name']

    if filter:
        search_str += " (" + filter + ")"

    all_flds = col.db.list(
        """select flds from notes join cards on notes.id = cards.nid
            where cards.id in """ +
        anki.utils.ids2str(col.findCards(search_str)))

    idx = col.models.fieldMap(model)[field][0]

    kanji = [anki.utils.splitFields(flds)[idx] for flds in all_flds]

    return frozenset(kanji)

def is_learnable(string, studied_kanji):
    """Returns True if a string is learnable, that is, if it does not contain
    any kanji not yet studied.  Returns None if the string does not contain
    any kanji.
    """
    has_kanji = False

    for c in string:
        if is_kanji(c):
            if c not in studied_kanji:
                return False
            else:
                has_kanji = True

    return True if has_kanji else None

def get_learnable_notes(col, model, field, studied_kanji, require_kanji=True):
    """Returns a pair of lists of notes: those whose field does not contain any
    kanji not yet studied, and those which do.
    """
    notes = [col.getNote(n) for n in col.findNotes('note:"%s"' % model['name'])]

    learnable = []
    not_learnable = []

    for note in notes:
        tmp = is_learnable(note[field], studied_kanji)
        if tmp or (tmp is None and not require_kanji):
            learnable.append(note)
        else:
            not_learnable.append(note)

    return learnable, not_learnable
