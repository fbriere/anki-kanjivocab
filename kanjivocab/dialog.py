# -*- coding: utf-8 -*-
#
# kanjivocab - Anki add-on to tag vocabulary cards based on kanji
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
from aqt import mw
from aqt.qt import *
import aqt.tagedit

from kanjivocab.ui_dialog import Ui_KanjiVocabDialog
from kanjivocab.help import KanjiVocabHelp


class KanjiVocabDialog(QDialog, Ui_KanjiVocabDialog):
    """Main dialog window."""

    KANJI_DEFAULT_FIELD = "Kanji"
    VOCAB_DEFAULT_FIELD = "Expression"

    def __init__(self):
        QDialog.__init__(self, mw)
        self.setupUi(self)

        # Fill both field combo boxes
        fields = sorted(anki.find.fieldNames(mw.col, downcase=False))
        def fillFieldCombo(combo, default):
            for field in fields:
                combo.addItem(field, field)
                if field == default:
                    combo.setCurrentIndex(combo.count() - 1)

        fillFieldCombo(self.kanjiFieldCombo, self.KANJI_DEFAULT_FIELD)
        fillFieldCombo(self.vocabFieldCombo, self.VOCAB_DEFAULT_FIELD)

        # Cheat and replace tagsLineEdit with a TagEdit
        self.tagsLineEdit.hide()
        self.tagsLineEdit = aqt.tagedit.TagEdit(self)
        self.tagsLineEdit.setCol(mw.col)
        self.tagsLayout.addWidget(self.tagsLineEdit)
        mw.connect(self.tagsLineEdit, SIGNAL("textChanged(const QString &)"),
                   self.on_tagsLineEdit_textChanged)

        self.helpDialog = KanjiVocabHelp()

        self.setOkEnabled(False)

    def setOkEnabled(self, enabled):
        """Enable or disable the OK button."""
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enabled)


    @pyqtSignature("const QString &")
    def on_tagsLineEdit_textChanged(self, text):
        """Callback for when the 'Tags' LineEdit is modified."""
        if text != "":
            self.setOkEnabled(True)
        else:
            self.setOkEnabled(False)

    @pyqtSignature("")
    def on_buttonBox_helpRequested(self):
        """Callback for when the 'Help' button is clicked."""
        self.helpDialog.exec_()


    def _get_field(self, combo):
        """Fetch the field name corresponding to the combo selection."""
        return combo.itemData(combo.currentIndex())

    @property
    def kanji_field(self):
        return self._get_field(self.kanjiFieldCombo)

    @property
    def vocab_field(self):
        return self._get_field(self.vocabFieldCombo)

    @property
    def kanji_filter(self):
        return unicode(self.kanjiFilterLineEdit.text())

    @property
    def require_kanji(self):
        return not self.includeNonKanjiCheckBox.isChecked()

    @property
    def tags(self):
        return unicode(self.tagsLineEdit.text())

    @property
    def delete_tags(self):
        return self.deleteTagsCheckBox.isChecked()

