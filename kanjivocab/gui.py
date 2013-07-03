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


from aqt import mw
from aqt.qt import *
import aqt.utils

from kanjivocab.main import get_studied_kanji, get_learnable_notes
from kanjivocab.dialog import KanjiVocabDialog


def onMenuEntry():
    """Callback for our menu entry."""
    dialog = KanjiVocabDialog()
    if dialog.exec_():
        mw.progress.start(immediate=True)
        mw.progress.update(_("Reading list of studied kanji"))

        studied_kanji = get_studied_kanji(col=mw.col,
                                          field=dialog.kanji_field,
                                          filter=dialog.kanji_filter)

        mw.progress.update(_("Tagging vocabulary cards"))

        mw.checkpoint(_("Tag vocabulary cards based on kanji"))

        learnable, not_learnable = get_learnable_notes(col=mw.col,
                                                       field=dialog.vocab_field,
                                                       studied_kanji=studied_kanji,
                                                       require_kanji=dialog.require_kanji)

        mw.col.tags.bulkAdd(learnable, dialog.tags)
        if dialog.delete_tags:
            mw.col.tags.bulkRem(not_learnable, dialog.tags)

        mw.progress.finish()

        # FIXME: Do we need to do something?
        #mw.deck.refreshSession()

        aqt.utils.showInfo("Applied tags on %u out of %u notes (based on %u kanji)." % (
            len(learnable),
            len(learnable) + len(not_learnable),
            len(studied_kanji)))

def init():
    """Hook this plugin into Anki."""
    action = QAction(_("Tag vocabulary cards based on kanji"), mw)

    mw.connect(action, SIGNAL("triggered()"), onMenuEntry)
    mw.form.menuTools.addAction(action)

