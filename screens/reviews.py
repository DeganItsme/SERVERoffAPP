from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

class ReviewsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'reviews'
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="⭐ Отзывы и предложения",
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
        
        # Форма отправки отзыва
        review_form = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint_y=None,
            height=dp(300),
            elevation=2,
            radius=[dp(15)]
        )
        
        form_label = MDLabel(
            text="Оставьте ваш отзыв:",
            halign="left",
            theme_text_color="Primary",
            font_style="H6"
        )
        
        self.review_input = MDTextField(
            hint_text="Ваш отзыв или предложение...",
            size_hint_y=None,
            height=dp(100),
            multiline=True
        )
        
        submit_btn = MDRaisedButton(
            text="Отправить отзыв",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#FF9800"),
            size_hint_y=None,
            height=dp(50)
        )
        submit_btn.bind(on_press=self.submit_review)
        
        review_form.add_widget(form_label)
        review_form.add_widget(self.review_input)
        review_form.add_widget(submit_btn)
        
        content.add_widget(review_form)
        
        # Примеры отзывов
        reviews_label = MDLabel(
            text="Последние отзывы:",
            halign="left",
            theme_text_color="Primary",
            font_style="H6"
        )
        content.add_widget(reviews_label)
        
        sample_reviews = [
            "Отличная еда! Быстрая доставка. ★★★★★",
            "Очень вкусная самса, буду заказывать еще! ★★★★☆",
            "Быстро, вкусно, недорого. Рекомендую! ★★★★★"
        ]
        
        for review in sample_reviews:
            review_card = MDCard(
                orientation="vertical",
                padding=dp(15),
                size_hint_y=None,
                height=dp(80),
                elevation=1,
                radius=[dp(12)]
            )
            
            review_label = MDLabel(
                text=review,
                halign="left",
                theme_text_color="Secondary"
            )
            
            review_card.add_widget(review_label)
            content.add_widget(review_card)
        
        scroll.add_widget(content)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def submit_review(self, instance):
        review_text = self.review_input.text.strip()
        if review_text:
            self.show_dialog("Спасибо!", "Ваш отзыв отправлен и будет рассмотрен.")
            self.review_input.text = ""
        else:
            self.show_dialog("Ошибка", "Пожалуйста, напишите ваш отзыв")
    
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
        self.manager.current = 'dashboard'
    
    def on_enter(self):
        self.build_ui()