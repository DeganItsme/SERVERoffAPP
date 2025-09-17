from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from utils.session import session

class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'profile'
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
    
        main_layout = MDBoxLayout(orientation='vertical')
    
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="Мой профиль",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=4,
            md_bg_color=get_color_from_hex("#FF9800")
        )
    
        # Основной контент с прокруткой
        from kivymd.uix.scrollview import MDScrollView
        scroll = MDScrollView()
    
        content = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
    
        # ДОБАВЛЯЕМ ОТСТУП СВЕРХУ
        top_spacer = MDBoxLayout(size_hint_y=None, height=dp(10))
        content.add_widget(top_spacer)
        
        if session.is_logged_in():
            # Карточка с информацией о пользователе
            info_card = MDCard(
                orientation="vertical",
                padding=dp(20),
                spacing=dp(15),
                size_hint_y=None,
                height=dp(250),
                elevation=2,
                radius=[dp(15)]
            )
            
            user_info = f"""Имя: {session.user_data.get('first_name', 'Не указано')}
Фамилия: {session.user_data.get('last_name', 'Не указано')}
Email: {session.user_data.get('email', 'Не указано')}
Телефон: {session.user_data.get('phone', 'Не указано')}
Тип аккаунта: {'Клиент' if session.user_data.get('user_type') == 'client' else 'Организация'}"""
            
            info_label = MDLabel(
                text=user_info,
                halign="left",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(180)
            )
            
            info_card.add_widget(info_label)
            
            # Кнопки действий
            actions_card = MDCard(
                orientation="vertical",
                padding=dp(20),
                spacing=dp(15),
                size_hint_y=None,
                height=dp(200),
                elevation=2,
                radius=[dp(15)]
            )
            
            actions_layout = MDBoxLayout(
                orientation='vertical',
                spacing=dp(15),
                size_hint_y=None,
                height=dp(150)
            )
            
            edit_btn = MDRaisedButton(
                text="Редактировать профиль",
                size_hint_x=0.8,
                pos_hint={'center_x': 0.5},
                md_bg_color=get_color_from_hex("#FF9800"),
                size_hint_y=None,
                height=dp(50)
            )
            edit_btn.bind(on_press=self.edit_profile)
            
            change_password_btn = MDRaisedButton(
                text="Сменить пароль",
                size_hint_x=0.8,
                pos_hint={'center_x': 0.5},
                md_bg_color=get_color_from_hex("#2196F3"),
                size_hint_y=None,
                height=dp(50)
            )
            change_password_btn.bind(on_press=self.change_password)
            
            actions_layout.add_widget(edit_btn)
            actions_layout.add_widget(change_password_btn)
            actions_card.add_widget(actions_layout)
            
            content.add_widget(info_card)
            content.add_widget(actions_card)
        else:
            # Если пользователь не авторизован
            error_card = MDCard(
                orientation="vertical",
                padding=dp(20),
                spacing=dp(15),
                size_hint_y=None,
                height=dp(150),
                elevation=2,
                radius=[dp(15)]
            )
            
            error_label = MDLabel(
                text="Пожалуйста, войдите в систему",
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(100)
            )
            
            error_card.add_widget(error_label)
            content.add_widget(error_card)
        
        scroll.add_widget(content)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
    
    def edit_profile(self, instance):
        self.show_dialog("Редактирование профиля", "Функция редактирования профиля будет доступна в следующем обновлении")
    
    def change_password(self, instance):
        self.show_dialog("Смена пароля", "Функция смены пароля будет доступна в следующем обновлении")
    
    def go_back(self):
        self.manager.current = 'dashboard'
    
    def show_dialog(self, title, text):
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, 0.3),
            buttons=[
                MDRaisedButton(
                    text="OK",
                    md_bg_color=get_color_from_hex("#FF9800"),
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def on_enter(self):
        self.build_ui()