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

from kanjivocab.ui_help import Ui_KanjiVocabHelp


class KanjiVocabHelp(QDialog, Ui_KanjiVocabHelp):
    """Help window"""

    def __init__(self):
        QDialog.__init__(self, mw)
        self.setupUi(self)

