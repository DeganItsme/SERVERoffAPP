from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from utils.database import db
from utils.session import session

class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'register'
        self.user_type = 'client'
        self.dialog = None
        self.inputs = {}
    
    def build_ui(self):
        # Очищаем экран
        self.clear_widgets()
        
        # Основной ScrollView
        scroll = MDScrollView(
            do_scroll_x=False,
            bar_width=dp(8),
            bar_color=get_color_from_hex("#FF9800")
        )
        
        # Главный контейнер
        main_container = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Высота контента - УВЕЛИЧИВАЕМ для большего прямоугольника
        if self.user_type == 'client':
            content_height = dp(800)  # Увеличена высота для клиента
        else:
            content_height = dp(1000)  # Увеличена высота для организации
        
        main_container.height = content_height
        
        # Карточка регистрации - УВЕЛИЧИВАЕМ ВЫСОТУ И ДОБАВЛЯЕМ ВЕРХНИЙ ОТСТУП
        card = MDCard(
            orientation="vertical",
            padding=[dp(20), dp(20), dp(20), dp(20)],  # Стандартные отступы
            spacing=dp(15),
            size_hint=(0.95, None),
            height=content_height - dp(50),  # Увеличиваем высоту карточки
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=3,
            radius=[dp(15)]
        )
        
        # ДОБАВЛЯЕМ БОЛЬШОЙ ВЕРХНИЙ ОТСТУП ВНУТРИ КАРТОЧКИ
        top_padding_container = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80)  # БОЛЬШОЙ отступ сверху внутри карточки
        )
        
        # Контейнер для полей
        fields_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            padding=dp(5)
        )
        
        # Базовые поля
        base_fields = [
            ("Имя*", "text"),
            ("Фамилия*", "text"), 
            ("Email*", "email"),
            ("Телефон*", "phone"),
            ("Пароль*", "password"),
            ("Подтверждение пароля*", "password")
        ]
        
        # Дополнительные поля для организаций
        if self.user_type == 'organization':
            base_fields.extend([
                ("Название организации*", "text"),
                ("Адрес*", "text"),
                ("Описание", "text")
            ])
        
        self.inputs = {}
        for hint, input_type in base_fields:
            # Контейнер для каждого поля
            field_container = MDBoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(60),
                padding=dp(2)
            )
            
            field = MDTextField(
                hint_text=hint,
                size_hint_x=1,
                mode="rectangle",
                password=True if "пароль" in hint.lower() else False,
                write_tab=False,
                size_hint_y=None,
                height=dp(50)
            )
            self.inputs[hint] = field
            
            field_container.add_widget(field)
            fields_container.add_widget(field_container)
        
        # Собираем карточку: сначала верхний отступ, потом поля, потом кнопки
        card.add_widget(top_padding_container)  # ДОБАВЛЯЕМ БОЛЬШОЙ ВЕРХНИЙ ОТСТУП
        card.add_widget(fields_container)
        
        # Кнопки
        buttons_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12),
            size_hint_y=None,
            height=dp(120),
            padding=dp(10)
        )
        
        register_btn = MDRaisedButton(
            text="Зарегистрироваться",
            size_hint_x=0.9,
            md_bg_color=get_color_from_hex("#FF9800"),
            size_hint_y=None,
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        register_btn.bind(on_press=self.register)
        
        back_btn = MDRectangleFlatButton(  # Исправлено
            text="Назад к входу",
            size_hint_x=1,
            theme_text_color="Custom",
            text_color=get_color_from_hex("#FF9800"),
            size_hint_y=None,
            height=dp(45),
            pos_hint={'center_x': 0.5}
        )
        back_btn.bind(on_press=self.go_to_login)
        buttons_container.add_widget(register_btn)
        buttons_container.add_widget(back_btn)
        
        card.add_widget(buttons_container)
        
        # Добавляем карточку в основной контейнер
        main_container.add_widget(card)
        
        scroll.add_widget(main_container)
        self.add_widget(scroll)
    
    def register(self, instance):
        # Проверка обязательных полей
        required_fields = ["Имя*", "Фамилия*", "Email*", "Телефон*", "Пароль*", "Подтверждение пароля*"]
        if self.user_type == 'organization':
            required_fields.extend(["Название организации*", "Адрес*"])
        
        for field in required_fields:
            if field not in self.inputs or not self.inputs[field].text.strip():
                self.show_dialog("Ошибка", f"Заполните обязательное поле: {field.replace('*', '')}")
                return
        
        # Проверка email
        email = self.inputs["Email*"].text.strip()
        if "@" not in email or "." not in email:
            self.show_dialog("Ошибка", "Введите корректный email адрес")
            return
        
        # Проверка паролей
        password = self.inputs["Пароль*"].text
        confirm_password = self.inputs["Подтверждение пароля*"].text
        
        if password != confirm_password:
            self.show_dialog("Ошибка", "Пароли не совпадают")
            return
        
        if len(password) < 6:
            self.show_dialog("Ошибка", "Пароль должен содержать минимум 6 символов")
            return
        
        # Проверка телефона
        phone = self.inputs["Телефон*"].text.strip()
        if not phone.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '').isdigit():
            self.show_dialog("Ошибка", "Введите корректный номер телефона")
            return
        
        # Регистрация пользователя
        user_id = db.register_user(
            email=email,
            password=password,
            first_name=self.inputs["Имя*"].text.strip(),
            last_name=self.inputs["Фамилия*"].text.strip(),
            phone=phone,
            user_type=self.user_type
        )
        
        if user_id:
            # Для организаций добавляем информацию об организации
            if self.user_type == 'organization':
                org_id = db.add_organization(
                    name=self.inputs["Название организации*"].text.strip(),
                    owner_id=user_id,
                    description=self.inputs.get("Описание", MDTextField()).text.strip(),
                    address=self.inputs["Адрес*"].text.strip(),
                    phone=phone
                )
                if org_id:
                    print(f"Организация зарегистрирована: {org_id}")
            
            self.show_dialog("Успех", "Регистрация завершена успешно!", success=True)
        else:
            self.show_dialog("Ошибка", "Пользователь с таким email уже существует")
    
    def go_to_login(self, instance):
        self.manager.current = 'login'
    
    def show_dialog(self, title, text, success=False):
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, 0.3),
            buttons=[
                MDRectangleFlatButton(  # Исправлено
                    text="OK",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#FF9800"),
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
        
        if success:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.go_to_login(None), 2)
    
    def on_enter(self):
        # При входе на экран перестраиваем UI
        self.build_ui()