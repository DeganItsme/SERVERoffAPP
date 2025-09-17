from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

class OrgStatsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'org_stats'
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="📊 Статистика",
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
        
        # Статистика
        stats = [
            {"title": "Общая выручка", "value": "25,430₽", "icon": "💰"},
            {"title": "Заказов сегодня", "value": "12", "icon": "📦"},
            {"title": "Средний чек", "value": "345₽", "icon": "🧾"},
            {"title": "Новых клиентов", "value": "8", "icon": "👥"},
            {"title": "Рейтинг", "value": "4.8★", "icon": "⭐"}
        ]
        
        for stat in stats:
            stat_card = MDCard(
                orientation="horizontal",
                padding=dp(20),
                size_hint_y=None,
                height=dp(80),
                elevation=2,
                radius=[dp(12)]
            )
            
            stat_layout = MDBoxLayout(orientation='horizontal')
            
            icon_label = MDLabel(
                text=stat['icon'],
                halign="left",
                theme_text_color="Primary",
                font_style="H4",
                size_hint_x=0.2
            )
            
            text_layout = MDBoxLayout(orientation='vertical')
            
            title_label = MDLabel(
                text=stat['title'],
                halign="left",
                theme_text_color="Secondary",
                font_style="Body2"
            )
            
            value_label = MDLabel(
                text=stat['value'],
                halign="left",
                theme_text_color="Primary",
                font_style="H6"
            )
            
            text_layout.add_widget(title_label)
            text_layout.add_widget(value_label)
            
            stat_layout.add_widget(icon_label)
            stat_layout.add_widget(text_layout)
            stat_card.add_widget(stat_layout)
            
            content.add_widget(stat_card)
        
        # График продаж (заглушка)
        chart_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint_y=None,
            height=dp(200),
            elevation=2,
            radius=[dp(12)]
        )
        
        chart_label = MDLabel(
            text="📈 График продаж за неделю",
            halign="center",
            theme_text_color="Primary",
            font_style="H6"
        )
        
        chart_desc = MDLabel(
            text="Пн: 12 заказов\nВт: 15 заказов\nСр: 18 заказов\nЧт: 14 заказов\nПт: 20 заказов\nСб: 25 заказов\nВс: 22 заказа",
            halign="center",
            theme_text_color="Secondary"
        )
        
        chart_card.add_widget(chart_label)
        chart_card.add_widget(chart_desc)
        content.add_widget(chart_card)
        
        scroll.add_widget(content)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def go_back(self):
        self.manager.current = 'dashboard'
    
    def on_enter(self):
        self.build_ui()