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

class DirectoriesScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'directories'
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="📚 Справочники системы",
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
        
        # Категории справочников
        categories = [
            {"name": "Категории продуктов", "icon": "🍕", "category": "product_categories"},
            {"name": "Типы организаций", "icon": "🏢", "category": "org_types"},
            {"name": "Статусы заказов", "icon": "📦", "category": "order_statuses"},
            {"name": "Способы оплаты", "icon": "💳", "category": "payment_methods"},
            {"name": "Типы услуг", "icon": "🔧", "category": "service_types"}
        ]
        
        for category in categories:
            cat_card = MDCard(
                orientation="horizontal",
                padding=dp(20),
                size_hint_y=None,
                height=dp(80),
                elevation=2,
                radius=[dp(12)]
            )
            
            cat_layout = MDBoxLayout(orientation='horizontal')
            
            icon_label = MDLabel(
                text=category['icon'],
                halign="left",
                theme_text_color="Primary",
                font_style="H4",
                size_hint_x=0.2
            )
            
            name_label = MDLabel(
                text=category['name'],
                halign="left",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_x=0.6
            )
            
            manage_btn = MDRaisedButton(
                text="Управлять",
                size_hint_x=0.2,
                md_bg_color=get_color_from_hex("#2196F3"),
                size_hint_y=None,
                height=dp(40)
            )
            manage_btn.bind(on_press=lambda x, c=category: self.manage_directory(c))
            
            cat_layout.add_widget(icon_label)
            cat_layout.add_widget(name_label)
            cat_layout.add_widget(manage_btn)
            cat_card.add_widget(cat_layout)
            
            content.add_widget(cat_card)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content)
        
        self.add_widget(main_layout)
    
    def manage_directory(self, category):
        """Управление справочником"""
        self.show_directory_dialog(category)
    
    def show_directory_dialog(self, category):
        """Диалог управления справочником"""
        # Пример данных справочника
        sample_data = {
            "product_categories": ["Выпечка", "Фастфуд", "Напитки", "Десерты"],
            "org_types": ["Ресторан", "Кафе", "Бар", "Столовая"],
            "order_statuses": ["Новый", "Готовится", "Готов", "Доставляется", "Завершен"],
            "payment_methods": ["Наличные", "Карта", "Онлайн", "Криптовалюта"],
            "service_types": ["Доставка", "Самовывоз", "Бронирование", "Кейтеринг"]
        }
        
        dialog_content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, height=dp(300))
        
        title_label = MDLabel(
            text=f"Управление: {category['name']}",
            halign="center",
            theme_text_color="Primary",
            font_style="H6"
        )
        dialog_content.add_widget(title_label)
        
        # Поле для добавления нового значения
        new_value_input = MDTextField(hint_text="Новое значение")
        dialog_content.add_widget(new_value_input)
        
        # Список текущих значений
        values_label = MDLabel(
            text="Текущие значения:",
            halign="left",
            theme_text_color="Secondary"
        )
        dialog_content.add_widget(values_label)
        
        values_text = MDLabel(
            text="\n".join(sample_data.get(category['category'], [])),
            halign="left",
            theme_text_color="Secondary"
        )
        dialog_content.add_widget(values_text)
        
        self.dialog = MDDialog(
            title=category['name'],
            type="custom",
            content_cls=dialog_content,
            buttons=[
                MDRaisedButton(
                    text="Добавить",
                    md_bg_color=get_color_from_hex("#4CAF50"),
                    on_release=lambda x: self.add_directory_value(category, new_value_input.text)
                )
            ]
        )
        self.dialog.open()
    
    def add_directory_value(self, category, value):
        """Добавление значения в справочник"""
        if value.strip():
            self.show_dialog("Успех", f"Значение '{value}' добавлено в {category['name']}")
            self.dialog.dismiss()
        else:
            self.show_dialog("Ошибка", "Введите значение")
    
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