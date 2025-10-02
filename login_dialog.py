from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from db_helper import DB, DB_CONFIG
from signup_dialog import SignupDialog

class LoginDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("관리자 로그인")
        self.setWindowIcon(QIcon('home.png'))
        
        self.db = DB(**DB_CONFIG)
        
        self.username = self.create_line_edit("아이디")
        self.password = self.create_line_edit("비밀번호")
        self.password.setEchoMode(QLineEdit.Password)
        
        form = QFormLayout()
        form.addRow("아이디", self.username)
        form.addRow("비밀번호", self.password)
        
        self.btn_login = self.create_button("로그인", self.try_login)
        self.btn_signup = self.create_button("회원가입", self.signup)
        
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.btn_login)
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
        
    def try_login(self):
        uid = self.username.text().strip()
        pw = self.password.text().strip()
        if not uid or not pw:
            QMessageBox.warning(self, "오류", "아이디와 비밀번호를 모두 입력하세요")
            return
        
        ok = self.db.login_verify_user(uid, pw)
        if ok:
            self.accept()   # 다이얼로그 통과!
        else:
            QMessageBox.critical(self, "로그인 실패", "아이디 또는 비밀번호가 올바르지 않습니다. ")
            
    def signup(self):
        signup_dialog = SignupDialog()
        if signup_dialog.exec_() == SignupDialog.Accepted:
            self.show()