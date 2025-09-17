from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from utils.notifications import notifications
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, TwoLineListItem
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'menu'
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="Меню SERVERoff",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=4,
            md_bg_color=get_color_from_hex("#FF9800")
        )
        
        # Основной контейнер
        content = MDBoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(15)
        )
        
        # Категории продуктов
        categories = {
            "🍞 Выпечка": [
                ("Самса с мясом", "150₽ - Сочная самса с говядиной"),
                ("Самса с картошкой", "120₽ - Вегетарианский вариант"),
                ("Лепешки узбекские", "80₽ - Традиционные лепешки")
            ],
            "🍔 Фастфуд": [
                ("Шаурма классическая", "200₽ - Курица, овощи, соус"),
                ("Шаурма острая", "220₽ - С острым соусом"), 
                ("Пицца Маргарита", "350₽ - Классическая итальянская")
            ],
            "🥤 Напитки": [
                ("Чай зеленый", "50₽ - Ароматный зеленый чай"),
                ("Чай черный", "50₽ - Крепкий черный чай"),
                ("Кока-кола", "80₽ - 0.5л")
            ]
        }
        
        for category, products in categories.items():
            # Карточка категории
            category_card = MDCard(
                orientation="vertical",
                padding=dp(15),
                spacing=dp(10),
                size_hint=(1, None),
                height=dp(50 + len(products) * 80),  # Динамическая высота
                elevation=2,
                radius=[dp(12)]
            )
            
            # Заголовок категории
            category_label = MDLabel(
                text=category,
                halign="center",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_y=None,
                height=dp(40)
            )
            
            category_card.add_widget(category_label)
            
            # Контейнер для продуктов
            products_container = MDBoxLayout(
                orientation='vertical',
                spacing=dp(5),
                size_hint_y=None,
                height=dp(len(products) * 80)
            )
            
            for product, description in products:
                # Карточка продукта
                product_card = MDCard(
                    orientation="vertical",
                    padding=dp(10),
                    size_hint_y=None,
                    height=dp(75),
                    elevation=1,
                    radius=[dp(8)],
                    md_bg_color=(0.95, 0.95, 0.95, 1)
                )
                
                # Название продукта
                name_label = MDLabel(
                    text=product,
                    halign="left",
                    theme_text_color="Primary",
                    font_style="Subtitle1",
                    size_hint_y=None,
                    height=dp(25)
                )
                
                # Описание продукта
                desc_label = MDLabel(
                    text=description,
                    halign="left",
                    theme_text_color="Secondary",
                    font_style="Body2",
                    size_hint_y=None,
                    height=dp(20)
                )
                
                product_card.add_widget(name_label)
                product_card.add_widget(desc_label)
                products_container.add_widget(product_card)
            
            category_card.add_widget(products_container)
            content.add_widget(category_card)
        
        # Кнопка заказа
        order_btn = MDRaisedButton(
            text="🛒 Оформить заказ",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#FF9800")
        )
        order_btn.bind(on_press=self.make_order)
        
        content.add_widget(order_btn)
        
        # Добавляем ScrollView
        from kivymd.uix.scrollview import MDScrollView
        scroll = MDScrollView()
        scroll.add_widget(content)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def order_product(self, product):
        notifications.show_notification("Добавлено в корзину", f"{product} добавлен в корзину!")
    # Здесь будет логика добавления в корзину

    def make_order(self, instance):
        self.show_dialog("Заказ", "Функция оформления заказа будет доступна в следующем обновлении")
    
    def show_dialog(self, title, text):
        
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