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
from anki.cards import Card
from anki.facts import Fact
from anki.models import CardModel

from sqlalchemy.orm import subqueryload, subqueryload_all

from kanjivocab.unicode import is_kanji


def get_studied_kanji(deck, model, field, filter=None, mature=False):
    """Returns the (frozen) set of all studied kanji from a deck."""
    cards = deck.s.query(Card).\
            join(Card.cardModel).\
            options(subqueryload_all(Card.fact, Fact.fields)).\
            filter(CardModel.modelId == model.id).\
            all()

    if filter:
        filtered_ids = frozenset(deck.findCards(filter))
        cards = [c for c in cards if c.id in filtered_ids]

    if mature:
        cards = [c for c in cards if deck.cardIsMature(c)]

    kanji = [c.fact[field.name] for c in cards]

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

def get_learnable_facts(deck, model, field, studied_kanji, require_kanji=True):
    """Returns a pair of lists of facts: those whose field does not contain any
    kanji not yet studied, and those which do.
    """
    facts = deck.s.query(Fact).\
            options(subqueryload(Fact.fields)).\
            filter(Fact.modelId == model.id).\
            all()

    learnable = []
    not_learnable = []

    for fact in facts:
        tmp = is_learnable(fact[field.name], studied_kanji)
        if tmp or (tmp is None and not require_kanji):
            learnable.append(fact)
        else:
            not_learnable.append(fact)

    return learnable, not_learnable
