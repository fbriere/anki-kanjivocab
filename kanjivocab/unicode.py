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


def is_kanji(c):
    """Returns True if a Unicode character is considered a kanji."""

    # Unfortunately, Python does not currently provide a way to obtain the
    # script of a Unicode character (see issue 6331), so we work around this
    # by hard-coding the list of blocks corresponding to the Han script
    # (as of Unicode 6.2).
    #
    # Note that there are also a few characters scattered in "CJK Symbols and
    # Punctuation" that we don't bother to check for.  In fact, U+3005 and
    # U+3007 should *not* be considered kanji, even though they are part of
    # the Han script.

    c = ord(c)

    return (
        (0x2E80 <= c and c <= 0x2EFF) or   # CJK Radicals Supplement
        (0x2F00 <= c and c <= 0x2FDF) or   # Kangxi Radicals
        (0x3400 <= c and c <= 0x4DBF) or   # CJK Unified Ideographs Extension A
        (0x4E00 <= c and c <= 0x9FFF) or   # CJK Unified Ideographs
        (0xF900 <= c and c <= 0xFAFF) or   # CJK Compatibility Ideographs
        (0x20000 <= c and c <= 0x2A6DF) or # CJK Unified Ideographs Extension B
        (0x2A700 <= c and c <= 0x2B73F) or # CJK Unified Ideographs Extension C
        (0x2B740 <= c and c <= 0x2B81F) or # CJK Unified Ideographs Extension D
        (0x2F800 <= c and c <= 0x2FA1F))   # CJK Compatibility Ideographs Supplement

