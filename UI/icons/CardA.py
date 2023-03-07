# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the widgets/layouts/flowlayout example from Qt v6.x"""

import sys
from PyQt5.QtCore import Qt, QMargins, QPoint, QRect, QSize
from PyQt5.QtWidgets import QApplication, QLayout, QPushButton, QSizePolicy, QWidget,QFrame


class CardA(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.BtnA = QPushButton("tess")
        self.BtnB = QPushButton("fasdfa")

