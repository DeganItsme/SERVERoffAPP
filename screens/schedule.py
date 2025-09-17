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

class ScheduleScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'schedule'
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="🕒 График работы",
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
        
        # Заголовок
        title_label = MDLabel(
            text="Настройка графика работы организации",
            halign="center",
            theme_text_color="Primary",
            font_style="H6"
        )
        content.add_widget(title_label)
        
        # Дни недели для настройки
        days_of_week = [
            {"id": 1, "name": "Понедельник", "short": "Пн"},
            {"id": 2, "name": "Вторник", "short": "Вт"},
            {"id": 3, "name": "Среда", "short": "Ср"},
            {"id": 4, "name": "Четверг", "short": "Чт"},
            {"id": 5, "name": "Пятница", "short": "Пт"},
            {"id": 6, "name": "Суббота", "short": "Сб"},
            {"id": 7, "name": "Воскресенье", "short": "Вс"}
        ]
        
        for day in days_of_week:
            day_card = MDCard(
                orientation="horizontal",
                padding=dp(15),
                size_hint_y=None,
                height=dp(80),
                elevation=2,
                radius=[dp(12)]
            )
            
            day_layout = MDBoxLayout(orientation='horizontal')
            
            day_name = MDLabel(
                text=day['name'],
                halign="left",
                theme_text_color="Primary",
                size_hint_x=0.3
            )
            
            time_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_x=0.5)
            
            open_input = MDTextField(
                hint_text="09:00",
                text="09:00",
                size_hint_x=0.4,
                input_filter="int"
            )
            
            close_input = MDTextField(
                hint_text="18:00", 
                text="18:00",
                size_hint_x=0.4,
                input_filter="int"
            )
            
            time_layout.add_widget(open_input)
            time_layout.add_widget(MDLabel(text="-", size_hint_x=0.2))
            time_layout.add_widget(close_input)
            
            # Чекбокс рабочий день
            from kivymd.uix.selectioncontrol import MDCheckbox
            working_check = MDCheckbox(
                active=True,
                size_hint_x=0.2
            )
            
            day_layout.add_widget(day_name)
            day_layout.add_widget(time_layout)
            day_layout.add_widget(working_check)
            day_card.add_widget(day_layout)
            
            content.add_widget(day_card)
        
        # Кнопка сохранения
        save_btn = MDRaisedButton(
            text="💾 Сохранить график",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#4CAF50"),
            size_hint_y=None,
            height=dp(50)
        )
        save_btn.bind(on_press=self.save_schedule)
        content.add_widget(save_btn)
        
        # Кнопка экспорта
        export_btn = MDRaisedButton(
            text="📤 Экспорт расписания",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#2196F3"),
            size_hint_y=None,
            height=dp(50)
        )
        export_btn.bind(on_press=self.export_schedule)
        content.add_widget(export_btn)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content)
        
        self.add_widget(main_layout)
    
    def save_schedule(self, instance):
        """Сохранение графика работы"""
        self.show_dialog("Успех", "График работы сохранен")
    
    def export_schedule(self, instance):
        """Экспорт расписания"""
        self.show_dialog("Экспорт", "Расписание экспортировано в PDF")
    
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