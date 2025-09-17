from kivy.metrics import dp
from kivymd.theming import ThemableBehavior

class RoundedButton(ThemableBehavior):
    """Класс для закругленных кнопок"""
    pass

# Стили для элементов
styles = {
    'button_radius': dp(15),
    'card_radius': dp(10),
    'input_radius': dp(8),
    'primary_color': [1, 0.6, 0, 1],  # Оранжевый
    'secondary_color': [0.2, 0.2, 0.2, 1],
    'background_color': [0.95, 0.95, 0.95, 1]
}