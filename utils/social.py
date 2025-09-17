import webbrowser
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.utils import get_color_from_hex

class SocialManager:
    def __init__(self):
        self.social_links = {
            'instagram': 'https://instagram.com/serveroff',
            'facebook': 'https://facebook.com/serveroff',
            'telegram': 'https://t.me/serveroff_channel',
            'whatsapp': 'https://wa.me/79991234567',
            'vkontakte': 'https://vk.com/serveroff'
        }
    
    def open_social(self, platform):
        """Открыть социальную сеть"""
        if platform in self.social_links:
            webbrowser.open(self.social_links[platform])
            return True
        return False
    
    def share_order(self, order_details):
        """Поделиться заказом"""
        share_text = f"Я заказал в SERVERoff: {order_details}"
        # Здесь будет реализация分享 через нативные API
        return True

# Глобальный менеджер социальных сетей
social_manager = SocialManager()