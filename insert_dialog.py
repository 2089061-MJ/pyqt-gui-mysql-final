from PyQt5.QtWidgets import *
from db_helper import DB, DB_CONFIG
from PyQt5.QtGui import *

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("재고 관리 상품 추가")
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
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 15px;
            }
            QSpinBox {
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 15px;
            }
        """)
        self.db = DB(**DB_CONFIG)

        self.input_name = QLineEdit()
        self.input_price = QLineEdit()
        self.input_stock = QSpinBox()

        form = QFormLayout()
        form.addRow("상품명", self.input_name)
        form.addRow("가격", self.input_price)
        form.addRow("재고", self.input_stock)

        
        buttonBox = QHBoxLayout()

        self.btn_submit = QPushButton("추가")
        self.btn_submit.clicked.connect(self.add_clothes)
        self.btn_cancel = QPushButton("취소")
        self.btn_cancel.clicked.connect(self.reject)

        buttonBox.addWidget(self.btn_submit)
        buttonBox.addWidget(self.btn_cancel)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(buttonBox)
        # layout.addWidget(buttonBox)
        self.setLayout(layout)

    
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
            
        else:
            QMessageBox.critical(self, "실패", "추가 중 오류가 발생했습니다.")
        self.accept()