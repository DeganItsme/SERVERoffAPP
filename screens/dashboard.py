from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from utils.session import session

class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="SERVERoff",
            right_action_items=[["logout", lambda x: self.logout()]],
            elevation=10,
            md_bg_color=get_color_from_hex("#FF9800")
        )
        
        # Основной контент
        content = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20)
        )
        
        # Приветствие
        if session.is_logged_in() and 'first_name' in session.user_data:
            welcome_text = f"Добро пожаловать, {session.user_data['first_name']}!"
        else:
            welcome_text = "Добро пожаловать в SERVERoff!"
            
        welcome_label = MDLabel(
            text=welcome_text,
            halign="center",
            theme_text_color="Primary",
            font_style="H5"
        )
        
        # Карточка с информацией
        info_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            size_hint_y=0.3,
            elevation=2,
            radius=[dp(15)]
        )
        
        if session.is_logged_in():
            user_type = "Клиент" if session.user_data.get('user_type') == 'client' else "Организация"
            info_text = f"""
Тип аккаунта: {user_type}
Email: {session.user_data.get('email', 'Не указан')}
Телефон: {session.user_data.get('phone', 'Не указан')}
            """
        else:
            info_text = "Пожалуйста, войдите в систему"
            
        info_label = MDLabel(
            text=info_text,
            halign="left",
            theme_text_color="Secondary"
        )
        
        info_card.add_widget(info_label)
        
        # Кнопки действий
        actions_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=0.6
        )
        
        if session.is_logged_in():
            # ПЕРВОЕ: проверка на администратора - должна быть ВНУТРИ условия is_logged_in
            # В разделе для администраторов добавим новые кнопки:
            if session.user_data.get('user_type') == 'admin':
                admin_btn = MDRaisedButton(
                    text="👥 Управление пользователями",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#FF0000"),
                    size_hint_y=None,
                    height=dp(50)
                    )
                admin_btn.bind(on_press=lambda x: self.go_to_screen('admin_users'))
    
                orgs_btn = MDRaisedButton(
                    text="🏢 Управление организациями",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#2196F3"),
                    size_hint_y=None,
                    height=dp(50)
                    )
                orgs_btn.bind(on_press=lambda x: self.go_to_screen('admin_organizations'))
    
                dirs_btn = MDRaisedButton(
                    text="📚 Справочники системы",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#4CAF50"),
                    size_hint_y=None,
                    height=dp(50)
                    )
                dirs_btn.bind(on_press=lambda x: self.go_to_screen('directories'))
    
                actions_layout.add_widget(admin_btn)
                actions_layout.add_widget(orgs_btn)
                actions_layout.add_widget(dirs_btn)
            # Затем проверяем остальные типы пользователей
            if session.user_data.get('user_type') == 'client':
                menu_btn = MDRaisedButton(
                    text="🍽️ Посмотреть меню",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#FF9800")
                )
                menu_btn.bind(on_press=lambda x: self.go_to_screen('menu'))
                
                cart_btn = MDRaisedButton(
                    text="🛒 Корзина",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#2196F3")
                )
                cart_btn.bind(on_press=lambda x: self.go_to_screen('cart'))
                
                orders_btn = MDRaisedButton(
                    text="📋 Мои заказы",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#4CAF50")
                )
                orders_btn.bind(on_press=lambda x: self.go_to_screen('orders'))
                
                reviews_btn = MDRaisedButton(
                    text="⭐ Отзывы",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#FF9800")
                )
                reviews_btn.bind(on_press=lambda x: self.go_to_screen('reviews'))
                
                social_btn = MDRaisedButton(
                    text="🌐 Соцсети",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#FF9800"),
                    size_hint_y=None,
                    height=dp(50)
                )
                social_btn.bind(on_press=lambda x: self.go_to_screen('social'))
                
                settings_btn = MDRaisedButton(
                    text="⚙️ Настройки",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#9C27B0"),
                    size_hint_y=None,
                    height=dp(50)
                )
                settings_btn.bind(on_press=lambda x: self.go_to_screen('settings'))
                
                profile_btn = MDRaisedButton(
                    text="👤 Мой профиль",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#9C27B0")
                )
                profile_btn.bind(on_press=lambda x: self.go_to_screen('profile'))
                
                actions_layout.add_widget(menu_btn)
                actions_layout.add_widget(cart_btn)
                actions_layout.add_widget(orders_btn)
                actions_layout.add_widget(reviews_btn)
                actions_layout.add_widget(social_btn)
                actions_layout.add_widget(settings_btn)
                actions_layout.add_widget(profile_btn)
            
            # В разделе для организаций добавим новые кнопки:
            elif session.user_data.get('user_type') == 'organization':
                products_btn = MDRaisedButton(
                    text="📦 Управление продуктами",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#FF9800")
                    )
                products_btn.bind(on_press=lambda x: self.go_to_screen('products'))
    
                orders_btn = MDRaisedButton(
                    text="📋 Управление заказами",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#2196F3")
                    )
                orders_btn.bind(on_press=lambda x: self.go_to_screen('org_orders'))
    
                stats_btn = MDRaisedButton(
                    text="📊 Статистика",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#4CAF50")
                    )
                stats_btn.bind(on_press=lambda x: self.go_to_screen('org_stats'))
    
                news_btn = MDRaisedButton(
                    text="📰 Новости",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#9C27B0"),
                    size_hint_y=None,
                    height=dp(50)
                        )
                news_btn.bind(on_press=lambda x: self.go_to_screen('news'))
    
                schedule_btn = MDRaisedButton(
                    text="🕒 График работы",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#FF9800"),
                    size_hint_y=None,
                    height=dp(50)
                    )
                schedule_btn.bind(on_press=lambda x: self.go_to_screen('schedule'))
    
                reports_btn = MDRaisedButton(
                    text="📊 Отчеты",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#2196F3"),
                    size_hint_y=None,
                    height=dp(50)
                    )
                reports_btn.bind(on_press=lambda x: self.go_to_screen('reports'))
    
                settings_btn = MDRaisedButton(
                    text="⚙️ Настройки",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#9C27B0"),
                    size_hint_y=None,
                    height=dp(50)
                    )
                settings_btn.bind(on_press=lambda x: self.go_to_screen('settings'))
    
                profile_btn = MDRaisedButton(
                    text="👤 Мой профиль",
                    size_hint_x=0.8,
                    pos_hint={'center_x': 0.5},
                    md_bg_color=get_color_from_hex("#9C27B0")
                    )
                profile_btn.bind(on_press=lambda x: self.go_to_screen('profile'))
    
                actions_layout.add_widget(products_btn)
                actions_layout.add_widget(orders_btn)
                actions_layout.add_widget(stats_btn)
                actions_layout.add_widget(news_btn)
                actions_layout.add_widget(schedule_btn)
                actions_layout.add_widget(reports_btn)
                actions_layout.add_widget(settings_btn)
                actions_layout.add_widget(profile_btn)
        
        content.add_widget(welcome_label)
        content.add_widget(info_card)
        content.add_widget(actions_layout)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content)
        
        self.add_widget(main_layout)
    
    def go_to_screen(self, screen_name):
        """Переход на указанный экран"""
        self.manager.current = screen_name
    
    def logout(self):
        from utils.session import session
        session.logout()
        print("Выход из системы")
        self.manager.current = 'login'
    
    def on_enter(self):
        self.build_ui()