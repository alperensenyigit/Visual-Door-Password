import videogui #gui class implementation
from PyQt5.QtWidgets import QApplication #python
import sys #sys module implementation

# main class
class Main:

    #main method for run program
    def main(self):
        app = QApplication(sys.argv)
        a = videogui.App()
        a.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    Run = Main().main()
    