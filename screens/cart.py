from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

class CartScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'cart'
        self.cart_items = []
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="🛒 Корзина",
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
        
        # Отступ сверху
        top_spacer = MDBoxLayout(size_hint_y=None, height=dp(10))
        content.add_widget(top_spacer)
        
        if not self.cart_items:
            # Пустая корзина
            empty_card = MDCard(
                orientation="vertical",
                padding=dp(30),
                size_hint_y=None,
                height=dp(200),
                elevation=2,
                radius=[dp(15)]
            )
            
            empty_label = MDLabel(
                text="Корзина пуста\n\nДобавьте товары из меню",
                halign="center",
                theme_text_color="Secondary",
                font_style="H6"
            )
            
            empty_card.add_widget(empty_label)
            content.add_widget(empty_card)
        else:
            # Товары в корзине
            cart_label = MDLabel(
                text="Ваш заказ:",
                halign="left",
                theme_text_color="Primary",
                font_style="H6"
            )
            content.add_widget(cart_label)
            
            # Список товаров
            for item in self.cart_items:
                item_card = MDCard(
                    orientation="horizontal",
                    padding=dp(15),
                    size_hint_y=None,
                    height=dp(80),
                    elevation=1,
                    radius=[dp(12)]
                )
                
                item_layout = MDBoxLayout(orientation='horizontal')
                
                item_name = MDLabel(
                    text=item['name'],
                    halign="left",
                    theme_text_color="Primary",
                    size_hint_x=0.6
                )
                
                item_price = MDLabel(
                    text=f"{item['price']}₽",
                    halign="right",
                    theme_text_color="Primary",
                    size_hint_x=0.4
                )
                
                item_layout.add_widget(item_name)
                item_layout.add_widget(item_price)
                item_card.add_widget(item_layout)
                content.add_widget(item_card)
            
            # Итого
            total = sum(item['price'] for item in self.cart_items)
            total_card = MDCard(
                orientation="horizontal",
                padding=dp(15),
                size_hint_y=None,
                height=dp(60),
                elevation=2,
                radius=[dp(12)],
                md_bg_color=get_color_from_hex("#E8F5E8")
            )
            
            total_label = MDLabel(
                text=f"Итого: {total}₽",
                halign="left",
                theme_text_color="Primary",
                font_style="H6"
            )
            
            total_card.add_widget(total_label)
            content.add_widget(total_card)
        
        # Кнопки действий
        buttons_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(120)
        )
        
        if self.cart_items:
            order_btn = MDRaisedButton(
                text="✅ Оформить заказ",
                size_hint_x=0.8,
                pos_hint={'center_x': 0.5},
                md_bg_color=get_color_from_hex("#4CAF50"),
                size_hint_y=None,
                height=dp(50)
            )
            order_btn.bind(on_press=self.create_order)
            
            clear_btn = MDRaisedButton(
                text="🗑️ Очистить корзину",
                size_hint_x=0.8,
                pos_hint={'center_x': 0.5},
                md_bg_color=get_color_from_hex("#FF5722"),
                size_hint_y=None,
                height=dp(50)
            )
            clear_btn.bind(on_press=self.clear_cart)
            
            buttons_layout.add_widget(order_btn)
            buttons_layout.add_widget(clear_btn)
        
        content.add_widget(buttons_layout)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content)
        
        self.add_widget(main_layout)
    
    def add_to_cart(self, product_name, price):
        self.cart_items.append({'name': product_name, 'price': price})
        self.build_ui()
    
    def clear_cart(self, instance):
        self.cart_items = []
        self.build_ui()
        self.show_dialog("Корзина очищена", "Все товары удалены из корзины")
    
    def create_order(self, instance):
        total = sum(item['price'] for item in self.cart_items)
        self.show_dialog("Заказ оформлен", f"Ваш заказ на сумму {total}₽ принят в обработку!")
        self.cart_items = []
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
        self.manager.current = 'menu'
    
    def on_enter(self):
        self.build_ui()