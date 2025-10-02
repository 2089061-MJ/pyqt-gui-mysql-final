from PyQt5.QtWidgets import *
from db_helper import DB, DB_CONFIG
from PyQt5.QtGui import *

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("재고 관리 수정하기")
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

        self.edit_name = QLineEdit()
        self.edit_price = QLineEdit()
        self.edit_stock = QSpinBox()

        form = QFormLayout()
        form.addRow("수정할 상품명", self.edit_name)
        form.addRow("수정할 가격", self.edit_price)
        form.addRow("수정할 재고", self.edit_stock)

        
        buttonBox = QHBoxLayout()

        self.btn_submit = QPushButton("수정하기")
        self.btn_submit.clicked.connect(self.item_edit)
        self.btn_cancel = QPushButton("취소")
        self.btn_cancel.clicked.connect(self.reject)

        buttonBox.addWidget(self.btn_submit)
        buttonBox.addWidget(self.btn_cancel)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(buttonBox)
        # layout.addWidget(buttonBox)
        self.setLayout(layout)
        
        
        
        
    def item_edit(self):
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
            
        else:
            QMessageBox.critical(self, "실패", "수정 작업중에 오류가 발생하였습니다.")
        self.accept()