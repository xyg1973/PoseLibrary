import sys
from PySide2.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QWidget
from PySide2.QtCore import Qt

# Create the application object
app = QApplication(sys.argv)

# Create the tree widget
tree = QTreeWidget()
tree.setColumnCount(2)
tree.setHeaderLabels(["Name", "Type"])

# Create some top-level items
cities = QTreeWidgetItem(tree)
cities.setText(0, "Cities")
osloItem = QTreeWidgetItem(cities)
osloItem.setText(0, "Oslo")
osloItem.setText(1, "Yes")
berlinItem = QTreeWidgetItem(cities)
berlinItem.setText(0, "Berlin")
berlinItem.setText(1, "Yes")

# Create a button and a slot function
button = QPushButton("Add child")
def add_child():
    # Get the current selected item
    current = tree.currentItem()
    if current:
        # Get the number of children
        count = current.childCount()
        # Create a new child item
        child = QTreeWidgetItem()
        child.setText(0, f"Child {count + 1}")
        child.setText(1, "No")
        # Set the child item to be editable
        child.setFlags(child.flags() | Qt.ItemIsEditable)
        # Add the child item to the current item
        current.addChild(child)

# Connect the button to the slot function
button.clicked.connect(add_child)

# Create a widget and a layout to hold the tree and the button
widget = QWidget()
layout = QVBoxLayout()
layout.addWidget(tree)
layout.addWidget(button)
widget.setLayout(layout)

# Show the widget and execute the application
widget.show()
sys.exit(app.exec_())