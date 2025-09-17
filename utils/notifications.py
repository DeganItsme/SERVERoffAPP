from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

class NotificationManager:
    def __init__(self):
        self.dialog = None
        self.notification_queue = []
        self.is_showing = False
    
    def show_notification(self, title, message, duration=3):
        """Показать уведомление"""
        self.notification_queue.append((title, message, duration))
        self.process_queue()
    
    def process_queue(self):
        """Обработать очередь уведомлений"""
        if not self.is_showing and self.notification_queue:
            title, message, duration = self.notification_queue.pop(0)
            self.is_showing = True
            
            if self.dialog:
                self.dialog.dismiss()
            
            self.dialog = MDDialog(
                title=title,
                text=message,
                size_hint=(0.8, 0.3),
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        md_bg_color=get_color_from_hex("#FF9800"),
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()
            
            # Автоматическое закрытие через duration секунд
            Clock.schedule_once(lambda dt: self.close_notification(), duration)
    
    def close_notification(self):
        """Закрыть текущее уведомление"""
        if self.dialog:
            self.dialog.dismiss()
        self.is_showing = False
        self.process_queue()

# Глобальный менеджер уведомлений
notifications = NotificationManager()