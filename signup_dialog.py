from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG

class SignupDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("재고관리 프로그램 회원가입")
        self.db = DB(**DB_CONFIG)
        
        self.signup_username = QLineEdit()
        self.signup_password = QLineEdit()
        self.signup_password.setEchoMode(QLineEdit.Password)
        
        form = QFormLayout()
        form.addRow("아이디", self.signup_username)
        form.addRow("비밀번호", self.signup_password)
        
        self.btn_signup = QPushButton("회원가입하기")
        self.btn_signup.clicked.connect(self.signup_try)
        
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.btn_signup)
        self.setLayout(layout)
        
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
            
        