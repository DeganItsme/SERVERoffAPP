from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

from kivy.core.window import Window
Window.size = (400, 700)

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

# Добавим в импорты
from screens.admin_users import AdminUsersScreen

class SERVERoffApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.material_style = "M3"
        
        # Создаем менеджер экранов
        self.sm = MDScreenManager()
        
        # Импортируем и добавляем экраны
        from screens.login import LoginScreen
        from screens.register import RegisterScreen
        from screens.dashboard import DashboardScreen
        from screens.products import ProductsScreen
        from screens.profile import ProfileScreen
        from screens.menu import MenuScreen
        from screens.cart import CartScreen
        from screens.orders import OrdersScreen
        from screens.reviews import ReviewsScreen
        from screens.org_orders import OrgOrdersScreen
        from screens.org_stats import OrgStatsScreen
        from screens.settings import SettingsScreen
        from screens.social import SocialScreen
        from screens.admin_organizations import AdminOrganizationsScreen
        from screens.directories import DirectoriesScreen
        from screens.news import NewsScreen
        from screens.schedule import ScheduleScreen
        from screens.reports import ReportsScreen

        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(DashboardScreen(name='dashboard'))
        self.sm.add_widget(ProductsScreen(name='products'))
        self.sm.add_widget(ProfileScreen(name='profile'))
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(CartScreen(name='cart'))
        self.sm.add_widget(OrdersScreen(name='orders'))
        self.sm.add_widget(ReviewsScreen(name='reviews'))
        self.sm.add_widget(OrgOrdersScreen(name='org_orders'))
        self.sm.add_widget(OrgStatsScreen(name='org_stats'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(SocialScreen(name='social'))
        self.sm.add_widget(AdminUsersScreen(name='admin_users'))
        self.sm.add_widget(AdminOrganizationsScreen(name='admin_organizations'))
        self.sm.add_widget(DirectoriesScreen(name='directories'))
        self.sm.add_widget(NewsScreen(name='news'))
        self.sm.add_widget(ScheduleScreen(name='schedule'))
        self.sm.add_widget(ReportsScreen(name='reports'))

        return self.sm
    
    def on_start(self):
        from utils.database import db
        from utils.notifications import notifications
    
        print("Инициализация базы данных...")
    
        # ЯВНО вызываем добавление тестовых данных
        db.add_test_data()
    
        # Проверяем всех пользователей в базе
        all_users = db.get_all_users()
        print("Пользователи в базе:")
        for user in all_users:
            print(f"ID: {user[0]}, Email: {user[1]}, Type: {user[2]}, Active: {user[3]}")
    
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"Всего пользователей в базе: {count}")
    
        # Тестовое уведомление при запуске
        notifications.show_notification("Добро пожаловать!", "SERVERoff запущен успешно")

if __name__ == '__main__':
    SERVERoffApp().run()