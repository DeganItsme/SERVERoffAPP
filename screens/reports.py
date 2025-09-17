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

class ReportsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'reports'
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="📊 Отчеты",
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
        
        # Типы отчетов
        report_types = [
            {
                "title": "📈 Отчет по продажам",
                "description": "Анализ продаж за выбранный период",
                "color": "#4CAF50"
            },
            {
                "title": "👥 Отчет по клиентам", 
                "description": "Статистика клиентской базы и активность",
                "color": "#2196F3"
            },
            {
                "title": "🍕 Отчет по продуктам",
                "description": "Популярность продуктов и выручка",
                "color": "#FF9800"
            },
            {
                "title": "🕒 Отчет по времени",
                "description": "Анализ заказов по времени суток",
                "color": "#9C27B0"
            },
            {
                "title": "📋 Финансовый отчет",
                "description": "Полная финансовая отчетность",
                "color": "#F44336"
            }
        ]
        
        for report in report_types:
            report_card = MDCard(
                orientation="vertical",
                padding=dp(20),
                size_hint_y=None,
                height=dp(120),
                elevation=2,
                radius=[dp(12)]
            )
            
            report_title = MDLabel(
                text=report['title'],
                halign="left",
                theme_text_color="Primary",
                font_style="H6"
            )
            
            report_desc = MDLabel(
                text=report['description'],
                halign="left",
                theme_text_color="Secondary"
            )
            
            generate_btn = MDRaisedButton(
                text="Сформировать отчет",
                size_hint_x=0.6,
                pos_hint={'center_x': 0.5},
                md_bg_color=get_color_from_hex(report['color']),
                size_hint_y=None,
                height=dp(40)
            )
            generate_btn.bind(on_press=lambda x, r=report: self.generate_report(r))
            
            report_card.add_widget(report_title)
            report_card.add_widget(report_desc)
            report_card.add_widget(generate_btn)
            
            content.add_widget(report_card)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content)
        
        self.add_widget(main_layout)
    
    def generate_report(self, report):
        """Генерация отчета"""
        self.show_dialog("Отчет", f"Отчет '{report['title']}' сформирован и готов к скачиванию")
    
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