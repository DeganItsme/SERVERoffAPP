from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton, MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from utils.notifications import notifications
from kivymd.uix.list import MDList, OneLineListItem
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from utils.database import db
from utils.session import session

class ProductsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'products'
        self.dialog = None
        self.build_ui()
    def build_ui(self):
        self.clear_widgets()
    
        main_layout = MDBoxLayout(orientation='vertical')
    
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="Управление продуктами",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=4,
            md_bg_color=get_color_from_hex("#FF9800")
        )
    
        # Основной контент С ОТСТУПОМ
        content = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20)
        )
    
        # ДОБАВЛЯЕМ ОТСТУП СВЕРХУ
        top_spacer = MDBoxLayout(size_hint_y=None, height=dp(10))
        content.add_widget(top_spacer)

        # Список продуктов
        products_label = MDLabel(
            text="Мои продукты:",
            halign="left",
            theme_text_color="Primary",
            font_style="H6"
        )
        
        # Контейнер для списка
        products_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=0.7
        )
        
        # Загружаем продукты из базы данных
        self.load_products(products_container)
        
        # Кнопка добавления продукта
        add_btn = MDFloatingActionButton(
            icon="plus",
            md_bg_color=get_color_from_hex("#FF9800"),
            pos_hint={'center_x': 0.9, 'center_y': 0.1},
            size_hint=(None, None),
            size=(dp(56), dp(56))
        )
        add_btn.bind(on_press=self.add_product)
        
        content.add_widget(products_label)
        content.add_widget(products_container)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content)
        self.add_widget(main_layout)
        self.add_widget(add_btn)
    
    def load_products(self, container):
        container.clear_widgets()
    
        products = [
            "Самса с мясом - 150₽",
            "Самса с картошкой - 120₽", 
            "Шаурма классическая - 200₽",
            "Пицца Маргарита - 350₽",
            "Лагман - 250₽"
        ]   
    
        if not products:
            empty_label = MDLabel(
                text="Нет продуктов",
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(50)
            )
            container.add_widget(empty_label)
            return
    
        # Создаем карточки для продуктов вместо списка
        for product in products:
            product_card = MDCard(
                orientation="horizontal",
                padding=dp(15),
                size_hint_y=None,
                height=dp(60),
                elevation=1,
                radius=[dp(8)],
                md_bg_color=(0.95, 0.95, 0.95, 1)
            )
        
            product_label = MDLabel(
                text=product,
                halign="left",
                theme_text_color="Primary",
                size_hint_x=0.8
            )
        
            product_card.add_widget(product_label)
            container.add_widget(product_card)
    
    def add_product(self, instance):
        self.show_dialog("Добавление продукта", "Форма добавления нового продукта")
    
    def edit_product(self, product):
        self.show_dialog("Редактирование", f"Редактирование: {product}")
    
    def go_back(self):
        self.manager.current = 'dashboard'
    
    def show_dialog(self, title, text):
        notifications.show_notification(title, text)

        if self.dialog:
            self.dialog.dismiss()
    
        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, 0.4),
            buttons=[
                MDRectangleFlatButton(
                    text="Отмена",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#FF9800"),
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(  # Изменили на MDRaisedButton для consistency
                    text="Сохранить",
                    md_bg_color=get_color_from_hex("#FF9800"),
                    on_release=lambda x: self.save_product()
                )
            ]
        )
        self.dialog.open()
    
    def save_product(self):
        print("Продукт сохранен")
        self.dialog.dismiss()