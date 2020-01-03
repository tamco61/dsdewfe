from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QTableWidget, QPushButton
from PyQt5 import uic
import sys, sqlite3


class Maim(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()
        self.pushButton.clicked.connect(self.run)

    def initUI(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"])
        self.data = sqlite3.connect('coffee.sqlite')
        cur = self.data.cursor()
        lst = cur.execute("""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(len(lst))
        for i in range(len(lst)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(lst[i][0])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(lst[i][1]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(lst[i][2]))
            if lst[i][3] is not None:
                self.tableWidget.setItem(i, 3, QTableWidgetItem(cur.execute(f"""SELECT title FROM type WHERE id = {lst[i][3]}""").fetchone()[0]))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(lst[i][4]))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(lst[i][5]))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(lst[i][6]))

    def run(self):
        self.addd = AddWindow(self)
        self.addd.show()

    def add(self):
        self.tableWidget.setRowCount(0)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM coffee WHERE id>0").fetchall()
        print('3')
        for row, cof in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for col, d in enumerate(cof):
                if col == 3:
                    if str(d) == '1':
                        d = 'молотый'
                    elif str(d) == '2':
                        d = 'в зернах'
                if d is not None:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(d)))
                else:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(''))
        print('2')
        self.tableWidget.resizeColumnsToContents()


class AddWindow(QWidget):
    def __init__(self, mainW):
        self.MainW = mainW
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI()

    def initUI(self):
        self.save_btn.clicked.connect(self.save)
        self.add_btn.clicked.connect(self.add)
        self.table_init()
        self.addAlltotable()

    def addAlltotable(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM coffee WHERE id>0").fetchall()
        for row, cof in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for col, d in enumerate(cof[1:]):
                if col == 2:
                    if str(d) == '1':
                        d = 'молотый'
                    elif str(d) == '2':
                        d = 'в зернах'
                if d is not None:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(d)))
                else:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(''))

        self.tableWidget.resizeColumnsToContents()

    def table_init(self):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ['название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])

        self.tableWidget.resizeColumnsToContents()

    def save(self):
        #   self.tableWidget = QTableWidget(self)
        titles = ['name', 'degree', 'type', 'taste', 'price', 'volume']
        self.cleanDB()

        for row in range(self.tableWidget.rowCount() + 1):
            data = {}
            for col in range(self.tableWidget.columnCount() + 1):
                item = self.tableWidget.item(row, col)
                if item is not None and item.text() != '':
                    data[titles[col]] = item.text()

            keys, vals = list(data.keys()), list(data.values())
            for i in range(len(keys)):
                if keys[i] in ('name', 'taste', 'degree', 'volume'):
                    vals[i] = "'" + vals[i] + "'"
                if keys[i] == 'type':
                    if vals[i] == 'молотый':
                        vals[i] = '1'
                    elif vals[i] == 'в зернах':
                        vals[i] = '2'

            if keys != []:
                s = f"INSERT INTO coffee({', '.join(keys)}) VALUES ({', '.join(vals)})"
                self.toDB(s)
        print('1')

        self.MainW.add()
        print('1')
        self.close()

    def cleanDB(self):
        con = sqlite3.connect("coffee.sqlite")
        with con:
            cur = con.cursor()
            cur.execute("DELETE from coffee WHERE id>0")

    def toDB(self, sql_string):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        with con:
            cur.execute(sql_string)

    def add(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Maim()
    form.show()
    sys.exit(app.exec_())
