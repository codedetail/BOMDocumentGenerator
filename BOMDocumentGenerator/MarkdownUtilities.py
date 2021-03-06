# -*- coding: utf-8; -*-
#
# This file is part of BOM Document Generator Tool.
#
# This tool is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MMC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
#The MIT License (MIT)

#Copyright (c) 2014 firepick

# (c) 2014 firepick-delta, http://delta.firepick.org/
# Author: David Shanklin, http://www.sagesmithing.org

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# These utilities are used to support GitHub Flavored Markdown (GFM for short)

import re

MARKDOWN_HEADER_CHAR = '#'
BLANK_LINE_CHAR = '\n'
BLOCK_QUOTE_CHAR = '>'
STYLING_CHAR = '_'
UNORDERED_LIST_CHAR = '*'

def Paragraphs(text, lines):
    blankLines = BLANK_LINE_CHAR * (lines + 1)
    paragraphString = text + blankLines
    return paragraphString

def Header(text, level):
    levelString = MARKDOWN_HEADER_CHAR * level
    headerString = levelString + ' ' + text
    return headerString

def BlockQuote(text):
    quoteString = BLOCKQUOTE + ' ' + text
    return quoteString

def Bold(text):
    boldString = STYLING_CHAR + text + STYLING_TEXT
    return boldString

def UnorderList(textList):
    listLength = len(textList)
    unorderedListString = ''
    for i in range(1,listLength):
        unorderedListString = unorderedListString + UNORDERED_LIST_CHAR + ' ' + BLANK_LINE_CHAR
    return unordedListString

#def Anchor(text, path):
