from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from db_helper import DB, DB_CONFIG
from insert_dialog import InsertDialog
from edit_dialog import EditDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("재고 관리 프로그램(관리자)")
        self.setWindowIcon(QIcon('home.png'))
        self.resize(500, 300)
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
        self.input_name = QLineEdit()
        self.input_price = QLineEdit()
        self.input_stock = QLineEdit()
        
        self.btn_add = QPushButton("추가")
        self.btn_add.clicked.connect(self.open_insert_dialog)
        self.btn1_add = QPushButton("선택항목 삭제")
        self.btn1_add.clicked.connect(self.checked_item_delete)
        
        self.btn_edit = QPushButton("수정하기")
        self.btn_edit.clicked.connect(self.open_edit_dialog)
        
        form_box.addWidget(self.btn_add)
        form_box.addWidget(self.btn1_add)
        form_box.addWidget(self.btn_edit)
        
        
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
            
            check_item = QCheckBox()
            check_item.setCheckState(False)
            check_item.setStyleSheet("""
                QCheckBox   { 
                    width: 30px; 
                    height: 30px; 
                    margin-left: auto;
                    margin-right: auto;
                    margin-top: auto;
                    margin-bottom: auto;
            }
            """)
            self.table.setCellWidget(r, 4, check_item)
            self.table.resizeColumnsToContents()
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
    def checked_item_delete(self):
        item_delete = []
        for r in range(self.table.rowCount()):
            check_item = self.table.cellWidget(r, 4)
            if check_item.checkState() == Qt.Checked:
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
         
            
    def open_insert_dialog(self):
        dialog = InsertDialog()
        if dialog.exec_() == InsertDialog.Accepted:
            self.load_clothes()
            
            
    def open_edit_dialog(self):
        dialog = EditDialog()
        if dialog.exec_() == EditDialog.Accepted:
            self.load_clothes()