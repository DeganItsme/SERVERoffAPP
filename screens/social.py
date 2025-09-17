from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from utils.social import social_manager
from utils.notifications import notifications

class SocialScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'social'
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="🌐 Социальные сети",
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
        
        # Социальные сети
        social_platforms = [
            {"name": "Instagram", "icon": "📷", "color": "#E1306C", "platform": "instagram"},
            {"name": "Facebook", "icon": "📘", "color": "#1877F2", "platform": "facebook"},
            {"name": "Telegram", "icon": "📨", "color": "#0088CC", "platform": "telegram"},
            {"name": "WhatsApp", "icon": "💚", "color": "#25D366", "platform": "whatsapp"},
            {"name": "VKontakte", "icon": "🔵", "color": "#0077FF", "platform": "vkontakte"}
        ]
        
        for platform in social_platforms:
            social_card = MDCard(
                orientation="horizontal",
                padding=dp(20),
                size_hint_y=None,
                height=dp(70),
                elevation=2,
                radius=[dp(12)],
                md_bg_color=get_color_from_hex(platform['color'] + "20")  # 20% прозрачности
            )
            
            # Иконка и название
            icon_label = MDLabel(
                text=platform['icon'],
                halign="left",
                theme_text_color="Custom",
                text_color=get_color_from_hex(platform['color']),
                font_style="H5",
                size_hint_x=0.2
            )
            
            name_label = MDLabel(
                text=platform['name'],
                halign="left",
                theme_text_color="Custom",
                text_color=get_color_from_hex(platform['color']),
                font_style="H6",
                size_hint_x=0.5
            )
            
            # Кнопка перехода
            follow_btn = MDRaisedButton(
                text="Перейти",
                size_hint_x=0.3,
                md_bg_color=get_color_from_hex(platform['color']),
                size_hint_y=None,
                height=dp(40)
            )
            follow_btn.bind(on_press=lambda x, p=platform['platform']: self.open_social(p))
            
            social_card.add_widget(icon_label)
            social_card.add_widget(name_label)
            social_card.add_widget(follow_btn)
            
            content.add_widget(social_card)
        
        # Раздел "Поделиться приложением"
        share_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint_y=None,
            height=dp(150),
            elevation=2,
            radius=[dp(12)]
        )
        
        share_label = MDLabel(
            text="📤 Поделиться приложением",
            halign="center",
            theme_text_color="Primary",
            font_style="H6"
        )
        
        share_btn = MDRaisedButton(
            text="Поделиться SERVERoff",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#FF9800"),
            size_hint_y=None,
            height=dp(50)
        )
        share_btn.bind(on_press=self.share_app)
        
        share_card.add_widget(share_label)
        share_card.add_widget(share_btn)
        
        content.add_widget(share_card)
        
        scroll.add_widget(content)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def open_social(self, platform):
        success = social_manager.open_social(platform)
        if success:
            notifications.show_notification("Открывается...", f"Переход в {platform.capitalize()}")
        else:
            notifications.show_notification("Ошибка", "Не удалось открыть социальную сеть")
    
    def share_app(self, instance):
        share_text = "Попробуй SERVERoff - лучшее приложение для заказа еды! 🍔🥤"
        # В реальном приложении здесь будет нативный sharing
        notifications.show_notification("Поделиться", "Функция поделиться будет доступна в следующем обновлении")
    
    def go_back(self):
        self.manager.current = 'dashboard'
    
    def on_enter(self):
        self.build_ui()