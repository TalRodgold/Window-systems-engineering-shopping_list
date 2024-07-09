from PySide6.QtWidgets import QApplication
from model import Food
from view import ShoppingView
from controller import ShoppingController

def main():
    app = QApplication([])
    model = Food()
    view = ShoppingView(model)
    controller = ShoppingController(model, view)
    controller.run()
    app.exec()


if __name__ == "__main__":
    main()
