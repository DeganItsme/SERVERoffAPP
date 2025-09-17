from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from utils.database import db
from utils.session import session

class AdminUsersScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'admin_users'
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="👥 Управление пользователями",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=4,
            md_bg_color=get_color_from_hex("#FF9800")
        )
        
        # Основной контент
        content = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Список пользователей
        users_label = MDLabel(
            text="Все пользователи:",
            halign="left",
            theme_text_color="Primary",
            font_style="H6"
        )
        content.add_widget(users_label)
        
        # Загрузка пользователей из базы данных
        users = self.load_users()
        
        for user in users:
            user_card = MDCard(
                orientation="horizontal",
                padding=dp(15),
                size_hint_y=None,
                height=dp(100),
                elevation=2,
                radius=[dp(12)]
            )
            
            user_info = MDBoxLayout(orientation='vertical')
            
            user_name = MDLabel(
                text=f"{user[3]} {user[4]} ({user[6]})",
                halign="left",
                theme_text_color="Primary"
            )
            
            user_contact = MDLabel(
                text=f"📧 {user[1]} | 📞 {user[5]}",
                halign="left",
                theme_text_color="Secondary"
            )
            
            user_info.add_widget(user_name)
            user_info.add_widget(user_contact)
            
            # Кнопки действий
            actions_layout = MDBoxLayout(
                orientation='vertical',
                spacing=dp(5),
                size_hint_x=0.4
            )
            
            block_btn = MDRaisedButton(
                text="🚫 Заблокировать",
                size_hint_x=1,
                md_bg_color=get_color_from_hex("#FF5722"),
                size_hint_y=None,
                height=dp(30)
            )
            block_btn.bind(on_press=lambda x, u=user: self.block_user(u))
            
            edit_btn = MDRaisedButton(
                text="✏️ Редактировать",
                size_hint_x=1,
                md_bg_color=get_color_from_hex("#2196F3"),
                size_hint_y=None,
                height=dp(30)
            )
            edit_btn.bind(on_press=lambda x, u=user: self.edit_user(u))
            
            actions_layout.add_widget(edit_btn)
            actions_layout.add_widget(block_btn)
            
            user_card.add_widget(user_info)
            user_card.add_widget(actions_layout)
            content.add_widget(user_card)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content)
        
        self.add_widget(main_layout)
    
    def load_users(self):
        """Загрузка пользователей из базы данных"""
        cursor = db.conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        return cursor.fetchall()
    
    def block_user(self, user):
        """Блокировка пользователя"""
        if session.is_logged_in():
            success = db.block_user(user[0], session.user_data['id'], "Административная блокировка")
            if success:
                self.show_dialog("Успех", f"Пользователь {user[3]} заблокирован")
                self.build_ui()
            else:
                self.show_dialog("Ошибка", "Не удалось заблокировать пользователя")
    
    def edit_user(self, user):
        """Редактирование пользователя"""
        self.show_edit_dialog(user)
    
    def show_edit_dialog(self, user):
        """Диалог редактирования пользователя"""
        dialog_content = MDBoxLayout(orientation='vertical', spacing=dp(15))
        
        first_name_input = MDTextField(
            hint_text="Имя",
            text=user[3]
        )
        
        last_name_input = MDTextField(
            hint_text="Фамилия", 
            text=user[4]
        )
        
        phone_input = MDTextField(
            hint_text="Телефон",
            text=user[5]
        )
        
        dialog_content.add_widget(first_name_input)
        dialog_content.add_widget(last_name_input)
        dialog_content.add_widget(phone_input)
        
        self.dialog = MDDialog(
            title=f"Редактирование {user[3]}",
            type="custom",
            content_cls=dialog_content,
            buttons=[
                MDRaisedButton(
                    text="Сохранить",
                    md_bg_color=get_color_from_hex("#FF9800"),
                    on_release=lambda x: self.save_user_changes(
                        user[0], first_name_input.text, last_name_input.text, phone_input.text
                    )
                )
            ]
        )
        self.dialog.open()
    
    def save_user_changes(self, user_id, first_name, last_name, phone):
        """Сохранение изменений пользователя"""
        success = db.update_user_profile(user_id, first_name, last_name, phone)
        if success:
            self.show_dialog("Успех", "Профиль пользователя обновлен")
            self.dialog.dismiss()
            self.build_ui()
        else:
            self.show_dialog("Ошибка", "Не удалось обновить профиль")
    
    def show_dialog(self, title, text):
        """Показать диалоговое окно"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, 0.3)
        )
        self.dialog.open()
    
    def go_back(self):
        self.manager.current = 'dashboard'
    
    def on_enter(self):
        self.build_ui()