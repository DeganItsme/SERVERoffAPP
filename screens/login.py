from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from utils.database import db
from utils.session import session

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        self.dialog = None
        
        self.build_ui()
    
    def build_ui(self):
        # Очищаем экран
        self.clear_widgets()
        
        # Основная карточка (уменьшена)
        card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(15),
            size_hint=(0.85, 0.5),  # Уменьшены размеры
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            elevation=2,
            radius=[dp(12)]
        )
        
        # Поля ввода (компактные)
        self.email_input = MDTextField(
            hint_text="Email",
            size_hint_x=0.9,
            size_hint_y=None,
            height=dp(48)
        )
        
        self.password_input = MDTextField(
            hint_text="Пароль",
            password=True,
            size_hint_x=0.9,
            size_hint_y=None,
            height=dp(48)
        )
        
        # Кнопки (компактные)
        login_btn = MDRaisedButton(
            text="Войти",
            size_hint_x=0.9,
            md_bg_color=get_color_from_hex("#FF9800"),
            size_hint_y=None,
            height=dp(45)
        )
        login_btn.bind(on_press=self.login)
        
        register_client_btn = MDFlatButton(
            text="Регистрация (Клиент)",
            size_hint_x=0.9,
            theme_text_color="Custom",
            text_color=get_color_from_hex("#FF9800"),
            size_hint_y=None,
            height=dp(40)
        )
        register_client_btn.bind(on_press=lambda x: self.go_to_register('client'))
        
        register_org_btn = MDFlatButton(
            text="Регистрация (Организация)",
            size_hint_x=0.9,
            theme_text_color="Custom",
            text_color=get_color_from_hex("#FF9800"),
            size_hint_y=None,
            height=dp(40)
        )
        register_org_btn.bind(on_press=lambda x: self.go_to_register('organization'))
        
        card.add_widget(self.email_input)
        card.add_widget(self.password_input)
        card.add_widget(login_btn)
        card.add_widget(register_client_btn)
        card.add_widget(register_org_btn)
        
        self.add_widget(card)
    
    def login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
    
        print(f"Попытка входа: {email}")  # Отладочная информация

        if not email or not password:
            self.show_dialog("Ошибка", "Заполните все поля")
            return

        user = db.login_user(email, password)

        if user:
            print(f"Найден пользователь: {user}")  # Отладочная информация
            session.login(user)
            print(f"Успешный вход: {email}")
            # Обновляем dashboard перед переходом
            dashboard = self.manager.get_screen('dashboard')
            if hasattr(dashboard, 'build_ui'):
                dashboard.build_ui()
            self.manager.current = 'dashboard'
        else:
            print("Пользователь не найден или неверный пароль")  # Отладочная информация
            self.show_dialog("Ошибка", "Неверный email или пароль")
    
    def go_to_register(self, user_type):
        register_screen = self.manager.get_screen('register')
        register_screen.user_type = user_type
        register_screen.build_ui()
        self.manager.current = 'register'
    
    def show_dialog(self, title, text):
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, 0.3)
        )
        self.dialog.open()
    
    def on_enter(self):
        # Очищаем поля при входе на экран
        self.email_input.text = ""
        self.password_input.text = ""