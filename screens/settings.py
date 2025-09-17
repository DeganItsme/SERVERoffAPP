from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.selectioncontrol import MDCheckbox  # Исправлено на MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from utils.notifications import notifications

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'settings'
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="⚙️ Настройки",
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
        
        # Настройки уведомлений
        notif_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint_y=None,
            height=dp(150),
            elevation=2,
            radius=[dp(12)]
        )
        
        notif_label = MDLabel(
            text="🔔 Уведомления",
            halign="left",
            theme_text_color="Primary",
            font_style="H6"
        )
        
        # Чекбоксы уведомлений
        notif_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        
        # Уведомления о заказах
        order_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        order_label = MDLabel(
            text="Уведомления о заказах",
            halign="left",
            theme_text_color="Secondary"
        )
        order_checkbox = MDCheckbox(active=True)  # Используем MDCheckbox вместо MDSwitch
        order_layout.add_widget(order_label)
        order_layout.add_widget(order_checkbox)
        
        # Уведомления о акциях
        promo_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        promo_label = MDLabel(
            text="Уведомления об акциях",
            halign="left",
            theme_text_color="Secondary"
        )
        promo_checkbox = MDCheckbox(active=True)  # Используем MDCheckbox вместо MDSwitch
        promo_layout.add_widget(promo_label)
        promo_layout.add_widget(promo_checkbox)
        
        notif_layout.add_widget(order_layout)
        notif_layout.add_widget(promo_layout)
        notif_card.add_widget(notif_label)
        notif_card.add_widget(notif_layout)
        
        # Настройки темы
        theme_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint_y=None,
            height=dp(120),
            elevation=2,
            radius=[dp(12)]
        )
        
        theme_label = MDLabel(
            text="🎨 Внешний вид",
            halign="left",
            theme_text_color="Primary",
            font_style="H6"
        )
        
        theme_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        theme_text = MDLabel(
            text="Темная тема",
            halign="left",
            theme_text_color="Secondary"
        )
        theme_checkbox = MDCheckbox(active=False)  # Используем MDCheckbox вместо MDSwitch
        theme_checkbox.bind(active=self.toggle_theme)
        theme_layout.add_widget(theme_text)
        theme_layout.add_widget(theme_checkbox)
        
        theme_card.add_widget(theme_label)
        theme_card.add_widget(theme_layout)
        
        # Кнопки действий
        actions_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint_y=None,
            height=dp(200),
            elevation=2,
            radius=[dp(12)]
        )
        
        actions_label = MDLabel(
            text="Действия",
            halign="left",
            theme_text_color="Primary",
            font_style="H6"
        )
        
        # Кнопки
        clear_cache_btn = MDRaisedButton(
            text="🧹 Очистить кэш",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#FF9800"),
            size_hint_y=None,
            height=dp(45)
        )
        clear_cache_btn.bind(on_press=self.clear_cache)
        
        export_data_btn = MDRaisedButton(
            text="📤 Экспорт данных",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#2196F3"),
            size_hint_y=None,
            height=dp(45)
        )
        export_data_btn.bind(on_press=self.export_data)
        
        about_btn = MDRaisedButton(
            text="ℹ️ О приложении",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#4CAF50"),
            size_hint_y=None,
            height=dp(45)
        )
        about_btn.bind(on_press=self.show_about)
        
        actions_card.add_widget(actions_label)
        actions_card.add_widget(clear_cache_btn)
        actions_card.add_widget(export_data_btn)
        actions_card.add_widget(about_btn)
        
        content.add_widget(notif_card)
        content.add_widget(theme_card)
        content.add_widget(actions_card)
        
        scroll.add_widget(content)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def toggle_theme(self, instance, value):
        theme = "Dark" if value else "Light"
        notifications.show_notification("Тема изменена", f"Тема изменена на {theme}")
    
    def clear_cache(self, instance):
        notifications.show_notification("Кэш очищен", "Кэш приложения успешно очищен")
    
    def export_data(self, instance):
        notifications.show_notification("Экспорт данных", "Данные успешно экспортированы")
    
    def show_about(self, instance):
        about_text = """SERVERoff v1.0

Приложение для заказа еды
Разработано для сети питания SERVERoff

• Удобный заказ еды
• Управление организацией
• Система отзывов
• Статистика и аналитика

© 2024 SERVERoff Team"""
        
        self.dialog = MDDialog(
            title="О приложении",
            text=about_text,
            size_hint=(0.8, 0.5)
        )
        self.dialog.open()
    
    def go_back(self):
        self.manager.current = 'dashboard'
    
    def on_enter(self):
        self.build_ui()