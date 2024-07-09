from ui.gui.uis.windows.main_window.ui_main import UI_MainWindow
from PySide6.QtWidgets import QMainWindow

from PySide6.QtWidgets import QMainWindow, QLabel, QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QToolButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from ui.gui.uis.windows.main_window.functions_main_window import *
import sys
import os
from  ui.gui.themes import *

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from ui.qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from ui.gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from ui.gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from ui.gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'


class ShoppingView(QMainWindow):
    def __init__(self, model):
        super(ShoppingView, self).__init__()
        self.model = model
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        self.setWindowTitle("Shopping View")
       
        settings = Settings()
        self.settings = settings.items

        themes = Themes()
        self.themes = themes.items
        
        self.table_widget = None


        self.hide_grips = True 
        SetupMainWindow.setup_gui(self)
        self.show()
        self.initialize_food()
        self.sum_label = QLabel("Total sum: $0.00")
        self.ui.load_pages.row_5_layout.addWidget(self.sum_label)

        self.add_product_button = QPushButton("Add Product")
        self.add_product_button.clicked.connect(self.open_add_product_dialog)
        self.ui.load_pages.row_5_layout.addWidget(self.add_product_button)

        
    def populate_table_with_data(self, data):
        self.table_widget.setRowCount(len(data))
        for row, product in enumerate(data):
            self.table_widget.setItem(row, 2, QTableWidgetItem(product['name']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(f"${product['price']:.2f}"))

    def open_add_product_dialog(self):
        dialog = AddProductDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.name_edit.text()
            price = float(dialog.price_edit.text())
            self.model.post_food(name, price)
            self.ui.load_pages.row_5_layout.removeWidget(self.table_widget)
            self.initialize_food()



    def add_row_to_table(self, product):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(product['name']))
        self.table_widget.setItem(row_position, 1, QTableWidgetItem(f"${product['price']:.2f}"))

    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        
        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # WIDGETS BTN
        if btn.objectName() == "btn_widgets":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_2)



        if btn.objectName() == "push_button_2":
            print("tal button is pressed")
            
        # LOAD USER PAGE
        if btn.objectName() == "btn_add_user":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_3)
        
        # LOAD USER PAGE
        if btn.objectName() == "btn_new_file":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_4)
            
        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_1,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )
        
        

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


    def initialize_food(self):
        self.toggle_button = PyToggle(
            width = 20,
            bg_color ="#1e2229",
            circle_color = "#c3ccdf",
            active_color = "#568af2"
        )
                
        self.table_widget = PyTableWidget(
            radius=8,
            color="#8a95aa",  # text_foreground
            selection_color="#568af2",  # context_color
            bg_color="#343b48",  # bg_two
            header_horizontal_color="#1e2229",  # dark_two
            header_vertical_color="#3c4454",  # bg_three
            bottom_line_color="#3c4454",  # bg_three
            grid_line_color="#2c313c",  # bg_one
            scroll_bar_bg_color="#2c313c",  # bg_one
            scroll_bar_btn_color="#272c36",  # dark_four
            context_color="#568af2"  # context_color
        )

        self.table_widget.setColumnCount(6)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.column_1 = QTableWidgetItem()
        self.column_1.setTextAlignment(Qt.AlignCenter)
        self.column_1.setText("CHECKED")

        self.column_2 = QTableWidgetItem()
        self.column_2.setTextAlignment(Qt.AlignCenter)
        self.column_2.setText("ID")

        self.column_3 = QTableWidgetItem()
        self.column_3.setTextAlignment(Qt.AlignCenter)
        self.column_3.setText("NAME")
        
        self.column_4 = QTableWidgetItem()
        self.column_4.setTextAlignment(Qt.AlignCenter)
        self.column_4.setText("PRICE")

        self.column_5 = QTableWidgetItem()
        self.column_5.setTextAlignment(Qt.AlignCenter)
        self.column_5.setText("")

        self.column_6 = QTableWidgetItem()
        self.column_6.setTextAlignment(Qt.AlignCenter)
        self.column_6.setText("")

        # # Set column
        self.table_widget.setHorizontalHeaderItem(0, self.column_1)
        self.table_widget.setHorizontalHeaderItem(1, self.column_2)
        self.table_widget.setHorizontalHeaderItem(2, self.column_3)
        self.table_widget.setHorizontalHeaderItem(3, self.column_4)
        self.table_widget.setHorizontalHeaderItem(4, self.column_5)
        self.table_widget.setHorizontalHeaderItem(5, self.column_6)

        # Connect toggle button signals to update sum
        self.connect_toggle_buttons()

        # Populate table with data
        df = self.model.get_all_food()
        for row_number, item in enumerate(df):
            self.table_widget.insertRow(row_number)  # Insert row
            
            toggle_button = PyToggle()
            toggle_button.toggled.connect(self.update_total_sum)  # Connect toggle button signal
            self.table_widget.setCellWidget(row_number, 0, toggle_button)
            
            id_item = QTableWidgetItem(str(item['id']))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row_number, 1, id_item)  # Add ID
            
            name_item = QTableWidgetItem(str(item['name']))
            name_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row_number, 2, name_item)  # Add NAME
            
            price_item = QTableWidgetItem(f"${item['price']:.2f}")
            price_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row_number, 3, price_item)  # Add PRICE

            # Set row height
            self.table_widget.setRowHeight(row_number, 35)  # Increase row height to 30 pixels

            # Add delete icon as clickable button
            delete_button = QToolButton()
            delete_button.setIcon(QIcon("icons/delete.svg"))  # Replace with your SVG icon path
            delete_button.setIconSize(QSize(20, 20))
            delete_button.setAutoRaise(True)
            delete_button.clicked.connect(self.delete_row)
            self.table_widget.setCellWidget(row_number, 4, delete_button)
            
            # Add update icon as clickable button
            update_button = QToolButton()
            update_button.setIcon(QIcon("icons/update.svg"))  # Replace with your SVG icon path
            update_button.setIconSize(QSize(20, 20))
            update_button.setAutoRaise(True)
            update_button.clicked.connect(self.update_row)
            self.table_widget.setCellWidget(row_number, 5, update_button)

            
            
            self.table_widget.setRowHeight(row_number,35)
        
        self.ui.load_pages.row_5_layout.insertWidget(0, self.table_widget)

        #self.table_widget.cellClicked.connect(self.open_update_dialog)

    def connect_toggle_buttons(self):
        # Connect all toggle buttons in the table to update sum
        for row in range(self.table_widget.rowCount()):
            toggle_button = self.table_widget.cellWidget(row, 0)
            toggle_button.toggled.connect(self.update_total_sum)

    def update_total_sum(self):
        total_sum = 0.0
        for row in range(self.table_widget.rowCount()):
            toggle_button = self.table_widget.cellWidget(row, 0)
            if toggle_button.isChecked():
                price_item = self.table_widget.item(row, 3)
                total_sum += float(price_item.text().strip('$'))  # Assuming price is stored as a string with '$'

        # Update the sum label
        self.sum_label.setText(f"Total sum: ${total_sum:.2f}")
        



    def delete_row(self):
        button = self.sender()
        if button:
            index = self.table_widget.indexAt(button.pos())
            if index.isValid():
                row = index.row()
                id_item = self.table_widget.item(row, 1)
                product_id = id_item.text()
                print(f"Deleting product with ID: {product_id}")
                self.table_widget.removeRow(index.row())
                self.update_total_sum()
                self.model.delete_from_db(product_id)
                

    def update_row(self):
        button = self.sender()
        if button:
            index = self.table_widget.indexAt(button.pos())
            if index.isValid():
                row = index.row()
                id_item = self.table_widget.item(row, 1)
                name_item = self.table_widget.item(row, 2)
                price_item = self.table_widget.item(row, 3)
                
                dialog = UpdateProductDialog(name_item.text(), float(price_item.text().strip('$')))
                if dialog.exec_() == QDialog.Accepted:
                    new_name = dialog.name_edit.text()
                    new_price = float(dialog.price_edit.text())
                    
                    name_item.setText(new_name)
                    price_item.setText(f"${new_price:.2f}")
                    product_id = id_item.text()
                    self.model.update_db(product_id, new_name, new_price)

class UpdateProductDialog(QDialog):
    def __init__(self, name, price, parent=None):
        super(UpdateProductDialog, self).__init__(parent)
        self.setWindowTitle("Update Product")

        layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit(name)
        self.price_label = QLabel("Price:")
        self.price_edit = QLineEdit(f"{price:.2f}")

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_edit)

        self.button_box = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.button_box.addWidget(self.ok_button)
        self.button_box.addWidget(self.cancel_button)
        layout.addLayout(self.button_box)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)


class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Product")
        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        self.price_edit = QLineEdit()

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_edit)
        form_layout.addWidget(QLabel("Price:"))
        form_layout.addWidget(self.price_edit)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.add_button.clicked.connect(self.add_product)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)

    def add_product(self):
        name = self.name_edit.text()
        price = self.price_edit.text()
        if name and price:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Name and Price must not be empty!")