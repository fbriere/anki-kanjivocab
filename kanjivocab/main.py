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
import anki.utils

from kanjivocab.find import get_notes_field
from kanjivocab.unicode import is_kanji


def get_studied_kanji(col, field, filter=""):
    """Returns the (frozen) set of all studied kanji."""
    notes = get_notes_field(col, field, filter)
    kanji = [field for id, field in notes]
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

def get_learnable_notes(col, field, studied_kanji, require_kanji=True):
    """Returns a pair of lists of notes IDs: those whose field does not
    contain any kanji not yet studied, and those which do.
    """
    notes = get_notes_field(col, field)

    learnable = []
    not_learnable = []

    for id, field in notes:
        tmp = is_learnable(field, studied_kanji)
        if tmp or (tmp is None and not require_kanji):
            learnable.append(id)
        else:
            not_learnable.append(id)

    return learnable, not_learnable
