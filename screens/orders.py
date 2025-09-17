from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

class OrdersScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'orders'
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="📋 История заказов",
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
        
        # Пример истории заказов
        orders = [
            {"id": "#001", "date": "25.08.2024", "total": 450, "status": "Доставлен"},
            {"id": "#002", "date": "24.08.2024", "total": 320, "status": "Доставлен"},
            {"id": "#003", "date": "23.08.2024", "total": 550, "status": "В процессе"}
        ]
        
        if not orders:
            empty_card = MDCard(
                orientation="vertical",
                padding=dp(30),
                size_hint_y=None,
                height=dp(200),
                elevation=2,
                radius=[dp(15)]
            )
            
            empty_label = MDLabel(
                text="История заказов пуста\n\nСделайте свой первый заказ!",
                halign="center",
                theme_text_color="Secondary",
                font_style="H6"
            )
            
            empty_card.add_widget(empty_label)
            content.add_widget(empty_card)
        else:
            for order in orders:
                order_card = MDCard(
                    orientation="vertical",
                    padding=dp(15),
                    size_hint_y=None,
                    height=dp(120),
                    elevation=2,
                    radius=[dp(12)]
                )
                
                order_info = f"Заказ {order['id']}\nДата: {order['date']}\nСумма: {order['total']}₽\nСтатус: {order['status']}"
                
                order_label = MDLabel(
                    text=order_info,
                    halign="left",
                    theme_text_color="Primary"
                )
                
                order_card.add_widget(order_label)
                content.add_widget(order_card)
        
        scroll.add_widget(content)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def go_back(self):
        self.manager.current = 'dashboard'
    
    def on_enter(self):
        self.build_ui()