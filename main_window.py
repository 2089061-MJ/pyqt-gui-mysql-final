from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox, QMenuBar, QAction, QScrollArea
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import Qt
from db_helper import DB, DB_CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("재고 관리 프로그램(관리자)")
        self.setWindowIcon(QIcon('home.png'))
        # 윈도우 스타일 설정
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f4f4;
            }
            QPushButton {
                border-radius: 5px;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 14px;
            }
            QTableWidget {
                background-color: white;
                border-radius: 5px;
                font-size: 14px;
                padding: 10px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QLabel {
                font-size: 14px;
            }
        """)
        
        self.db = DB(**DB_CONFIG)
        
        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)
        
        form_box = QHBoxLayout()
        self.input_name = self.create_line_edit("상품명")
        self.input_price = self.create_line_edit("가격")
        self.input_stock = self.create_line_edit("재고량")
        self.btn_add = self.create_button("추가", self.add_clothes)
        self.btn1_add = self.create_button("선택항목 삭제", self.checked_item_delete)
        self.btn1_add.clicked.connect(self.checked_item_delete)
        
        form_box1 = QHBoxLayout()
        self.edit_name = self.create_line_edit("수정할 상품명")
        self.edit_price = self.create_line_edit("수정할 가격")
        self.edit_stock = self.create_line_edit("수정할 재고량")
        self.btn_edit_load = self.create_button("선택항목 불러오기", self.edit_load)
        self.btn_edit = self.create_button("선택항목 수정", self.checked_item_edit)
        
        form_box.addWidget(QLabel("상품명"))
        form_box.addWidget(self.input_name)
        form_box.addWidget(QLabel("가격"))
        form_box.addWidget(self.input_price)
        form_box.addWidget(QLabel("재고량"))
        form_box.addWidget(self.input_stock)
        form_box.addWidget(self.btn_add)
        form_box.addWidget(self.btn1_add)
        
        form_box1.addWidget(QLabel("수정할 상품명"))
        form_box1.addWidget(self.edit_name)
        form_box1.addWidget(QLabel("수정할 가격"))
        form_box1.addWidget(self.edit_price)
        form_box1.addWidget(QLabel("수정할 재고량"))
        form_box1.addWidget(self.edit_stock)
        form_box1.addWidget(self.btn_edit_load)
        form_box1.addWidget(self.btn_edit)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "상품명", "가격", "재고량", "선택"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        
        vbox.addLayout(form_box)
        vbox.addLayout(form_box1)
        vbox.addWidget(self.table)
        
        self.load_clothes()
        
        self.setMinimumSize(400, 400)
        
    def create_line_edit(self, placeholder_text):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding : 5px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }                    
        """)
        return line_edit
    
    def create_button(self, text, action):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                border: none;
                min-width: 120px;
                margin: 5px
            }              
            QPushButton:hover {
                background-color: #45a049;
            }       
            QPushButton:disabled {
                background-color: #ddd;
            }
        """)
        button.clicked.connect(action)
        return button
   
   
   
   
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
            
        self.table.resizeRowsToContents()    
        self.table.resizeColumnsToContents()
        
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 350)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 172)
        
    def checked_item_edit(self):
        edit_name = self.edit_name.text().strip()
        edit_price = self.edit_price.text().strip()
        edit_stock = self.edit_stock.text().strip()
        
        ok = self.db.edit_item(edit_name, edit_price, edit_stock)
        
        if not edit_name or not edit_price or not edit_stock:
            QMessageBox.critical(self, "주의", "수정할 값을 입력하세요.")
        
        elif ok:
            QMessageBox.information(self, "완료", "수정완료 되었습니다.")
            self.edit_name.clear()
            self.edit_price.clear()
            self.edit_stock.clear()
            self.load_clothes()
        else:
            QMessageBox.critical(self, "실패", "수정 작업중에 오류가 발생하였습니다.")
    def edit_load(self):
        mid = None
        for r in range(self.table.rowCount()):
            check_item = self.table.item(r, 4)
            if check_item.checkState() == 2:
                mid = self.table.item(r, 0).text()
                break
        if mid is None:
            QMessageBox.warning(self, "경고", "수정할 항목을 선택하세요")
            return
        
        result = self.db.load_edit(mid)
        
        if result:
            self.edit_name.setText(result[1])
            self.edit_price.setText(str(result[2]))
            self.edit_stock.setText(str(result[3]))
            
        else:
            QMessageBox.warning(self, "오류", "선택한 항목을 불러오지 못했습니다.")
            
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