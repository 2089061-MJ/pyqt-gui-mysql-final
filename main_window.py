from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from db_helper import DB, DB_CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("재고 관리 프로그램")
        self.db = DB(**DB_CONFIG)
        
        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)
        
        form_box = QHBoxLayout()
        self.input_name = QLineEdit()
        self.input_price = QLineEdit()
        self.input_stock = QLineEdit()
        self.btn_add = QPushButton("추가")
        self.btn_add.clicked.connect(self.add_clothes)
        self.btn1_add = QPushButton("선택항목 삭제")
        self.btn1_add.clicked.connect(self.checked_item_delete)
        
        form_box.addWidget(QLabel("상품명"))
        form_box.addWidget(self.input_name)
        form_box.addWidget(QLabel("가격"))
        form_box.addWidget(self.input_price)
        form_box.addWidget(QLabel("재고량"))
        form_box.addWidget(self.input_stock)
        form_box.addWidget(self.btn_add)
        form_box.addWidget(self.btn1_add)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "상품명", "가격", "재고량", "선택"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        
        
        vbox.addLayout(form_box)
        vbox.addWidget(self.table)
        
        self.load_clothes()
    
    def load_clothes(self):
        rows = self.db.fetch_clothes()
        print(type(rows))
        self.table.setRowCount(len(rows))
        for r, (mid, name, price, stock) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(mid)))
            self.table.setItem(r, 1, QTableWidgetItem(name))
            self.table.setItem(r, 2, QTableWidgetItem(str(price)))
            self.table.setItem(r, 3, QTableWidgetItem(str(stock)))
            
            check_item = QTableWidgetItem()
            check_item.setCheckState(False)
            self.table.setItem(r, 4, check_item)
        self.table.resizeColumnsToContents()
        
    '''def checked_item(self):
        for r in range(self.table.rowCount()):
            check_item = self.table.item(r, 3)
            if check_item.setCheckState == True:
                name = self.table.item(r, 1).text()
                price = self.table.item(r, 2).text()
                stock = self.table.item(r, 3).text()
                print(name, price, stock)
'''

    def checked_item_delete(self):
        item_delete = []
        for r in range(self.table.rowCount()):
            check_item = self.table.item(r, 4)
            if check_item.checkState() == 2:
                mid = self.table.item(r, 0).text()
                item_delete.append(mid)
                
                a = QMessageBox.question(self, "삭제 확인",  f"{len(item_delete)}개의 항목을 삭제하시겠습니까?", 
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if a == QMessageBox.Yes:
                    for mid in item_delete:
                        ok = self.db.delete_item(mid)
                else:
                    QMessageBox.information(self, "취소", "삭제가 취소되었습니다.")
                    
        self.load_clothes()
        
        
    def add_clothes(self):
        name = self.input_name.text().strip()
        price = self.input_price.text().strip()
        stock = self.input_stock.text().strip()
        if not name or not price or not stock:
            QMessageBox.warning(self, "오류", "상품명, 가격, 재고량을 모두 입력하세요")
            return
        ok = self.db.insert_clothes(name, price, stock)
        if ok:
            QMessageBox.information(self, "완료", "추가되었습니다.")
            self.input_name.clear()
            self.input_price.clear()
            self.input_stock.clear()
            self.load_clothes()
        else:
            QMessageBox.critical(self, "실패", "추가 중 오류가 발생했습니다.")