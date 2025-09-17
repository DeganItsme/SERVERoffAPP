from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from utils.database import db
from utils.session import session

class OrgOrdersScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'org_orders'
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="📦 Заказы организации",
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
            spacing=dp(15),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
        
        # Отступ сверху
        top_spacer = MDBoxLayout(size_hint_y=None, height=dp(10))
        content.add_widget(top_spacer)
        
        # Заголовок
        title_label = MDLabel(
            text="Текущие заказы:",
            halign="left",
            theme_text_color="Primary",
            font_style="H5",
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(title_label)
        
        # Пример заказов
        orders = [
            {"id": "#1001", "customer": "Иван Петров", "total": 450, "status": "Готовится", "time": "15:30"},
            {"id": "#1002", "customer": "Мария Сидорова", "total": 320, "status": "Новый", "time": "15:45"},
            {"id": "#1003", "customer": "Алексей Иванов", "total": 550, "status": "В доставке", "time": "16:00"}
        ]
        
        for order in orders:
            order_card = MDCard(
                orientation="vertical",
                padding=dp(15),
                size_hint_y=None,
                height=dp(140),
                elevation=2,
                radius=[dp(12)]
            )
            
            order_info = f"""Заказ: {order['id']}
Клиент: {order['customer']}
Сумма: {order['total']}₽
Статус: {order['status']}
Время: {order['time']}"""
            
            order_label = MDLabel(
                text=order_info,
                halign="left",
                theme_text_color="Primary"
            )
            
            # Кнопки управления
            buttons_layout = MDBoxLayout(
                orientation='horizontal',
                spacing=dp(10),
                size_hint_y=None,
                height=dp(50)
            )
            
            if order['status'] == 'Новый':
                accept_btn = MDRaisedButton(
                    text="Принять",
                    size_hint_x=0.4,
                    md_bg_color=get_color_from_hex("#4CAF50"),
                    size_hint_y=None,
                    height=dp(40)
                )
                accept_btn.bind(on_press=lambda x, o=order: self.update_order_status(o, 'Готовится'))
                
                reject_btn = MDRaisedButton(
                    text="Отклонить",
                    size_hint_x=0.4,
                    md_bg_color=get_color_from_hex("#FF5722"),
                    size_hint_y=None,
                    height=dp(40)
                )
                reject_btn.bind(on_press=lambda x, o=order: self.update_order_status(o, 'Отклонен'))
                
                buttons_layout.add_widget(accept_btn)
                buttons_layout.add_widget(reject_btn)
            
            elif order['status'] == 'Готовится':
                ready_btn = MDRaisedButton(
                    text="Готово",
                    size_hint_x=0.4,
                    md_bg_color=get_color_from_hex("#2196F3"),
                    size_hint_y=None,
                    height=dp(40)
                )
                ready_btn.bind(on_press=lambda x, o=order: self.update_order_status(o, 'Готов'))
                
                buttons_layout.add_widget(ready_btn)
            
            order_card.add_widget(order_label)
            if buttons_layout.children:
                order_card.add_widget(buttons_layout)
            
            content.add_widget(order_card)
        
        scroll.add_widget(content)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def update_order_status(self, order, new_status):
        self.show_dialog("Статус обновлен", f"Заказ {order['id']} теперь: {new_status}")
        # Здесь будет обновление в базе данных
        self.build_ui()
    
    def show_dialog(self, title, text):
        from kivymd.uix.button import MDRaisedButton
        
        dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, 0.3),
            buttons=[
                MDRaisedButton(
                    text="OK",
                    md_bg_color=get_color_from_hex("#FF9800"),
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def go_back(self):
        self.manager.current = 'dashboard'
    
    def on_enter(self):
        self.build_ui()