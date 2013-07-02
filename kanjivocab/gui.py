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


from ankiqt import mw, ui

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from kanjivocab.main import get_studied_kanji, get_learnable_facts
from kanjivocab.dialog import KanjiVocabDialog


def onMenuEntry():
    """Callback for our menu entry."""
    dialog = KanjiVocabDialog()
    if dialog.exec_():
        mw.deck.startProgress()
        mw.deck.updateProgress(_("Reading list of studied kanji"))

        studied_kanji = get_studied_kanji(deck=mw.deck,
                                          model=dialog.kanji_model,
                                          field=dialog.kanji_field,
                                          filter=dialog.kanji_filter,
                                          mature=dialog.kanji_mature)

        mw.deck.updateProgress(_("Tagging vocabulary cards"))

        undo = _("Tag vocabulary cards based on kanji")
        mw.deck.setUndoStart(undo)

        learnable, not_learnable = get_learnable_facts(deck=mw.deck,
                                                       model=dialog.vocab_model,
                                                       field=dialog.vocab_field,
                                                       studied_kanji=studied_kanji,
                                                       require_kanji=dialog.require_kanji)

        mw.deck.addTags([f.id for f in learnable], dialog.tags)
        if dialog.delete_tags:
            mw.deck.deleteTags([f.id for f in not_learnable], dialog.tags)

        mw.deck.setUndoEnd(undo)
        mw.deck.finishProgress()

        # FIXME: Is this all we need to do?
        mw.deck.refreshSession()

        ui.utils.showInfo("Applied tags on %u out of %u facts (based on %u kanji)." % (
            len(learnable),
            len(learnable) + len(not_learnable),
            len(studied_kanji)))

def init():
    """Hook this plugin into Anki."""
    action = QAction(_("Tag vocabulary cards based on kanji"), mw)

    mw.connect(action, SIGNAL("triggered()"), onMenuEntry)
    mw.mainWin.menuTools.addAction(action)

