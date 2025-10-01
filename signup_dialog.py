from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG

class SignupDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("관리자 회원가입")
        self.db = DB(**DB_CONFIG)
        
        self.signup_username = self.create_line_edit("아이디")
        self.signup_password = self.create_line_edit("비밀번호")
        self.signup_password.setEchoMode(QLineEdit.Password)
        
        form = QFormLayout()
        form.addRow("아이디", self.signup_username)
        form.addRow("비밀번호", self.signup_password)
        
        self.btn_signup = self.create_button("회원가입하기", self.signup_try)
    
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.btn_signup)
        self.setLayout(layout)
        
        
        
        
        
    def create_line_edit(self, placeholder_text):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }                      
            QLineEdit:focus {
                border-color: #4CAF50;
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
                border-radius: 5px;
                border: none;
                min-width: 120px;
                margin: 10px 0;
            }               
            QPushButton:hover {
                background-color: #45a049;
            }
            QPuchButton:disabled {
                background-color: #ddd;
            }
        """)
        button.clicked.connect(action)
        return button    
        
        
    def signup_try(self):
        uid = self.signup_username.text().strip()
        pw = self.signup_password.text().strip()
        if not uid or not pw:
            QMessageBox.warning(self, "오류", "아이디와 비밀번호를 모두 입력하세요.")
            return
        
        ok = self.db.signup_verify_user(uid)
        if ok:
            QMessageBox.critical(self, "경고", "아이디가 이미 존재합니다. 다른 아이디를 입력하세요.")
            return
        
        ok1 = self.db.signup_user(uid, pw)
        if ok1:
            QMessageBox.information(self, "회원가입 성공", "가입되셨습니다!")
            self.accept()
        else:
            QMessageBox.critical(self, "오류", "회원가입에 실패하셨습니다.")
            
        