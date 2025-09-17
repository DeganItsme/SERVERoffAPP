from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from utils.database import db
from utils.session import session

class NewsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'news'
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="📰 Управление новостями",
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
        
        # Кнопка добавления новости
        add_news_btn = MDRaisedButton(
            text="➕ Добавить новость",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#4CAF50"),
            size_hint_y=None,
            height=dp(50)
        )
        add_news_btn.bind(on_press=self.add_news)
        content.add_widget(add_news_btn)
        
        # Список новостей
        news_label = MDLabel(
            text="Последние новости:",
            halign="left",
            theme_text_color="Primary",
            font_style="H6"
        )
        content.add_widget(news_label)
        
        # Загрузка новостей из базы данных
        news_items = self.load_news()
        
        if not news_items:
            empty_label = MDLabel(
                text="Новостей пока нет",
                halign="center",
                theme_text_color="Secondary"
            )
            content.add_widget(empty_label)
        else:
            for news in news_items:
                news_card = MDCard(
                    orientation="vertical",
                    padding=dp(15),
                    size_hint_y=None,
                    height=dp(150),
                    elevation=2,
                    radius=[dp(12)]
                )
                
                news_title = MDLabel(
                    text=news[1],
                    halign="left",
                    theme_text_color="Primary",
                    font_style="H6"
                )
                
                news_content = MDLabel(
                    text=f"{news[2][:100]}..." if news[2] and len(news[2]) > 100 else news[2],
                    halign="left",
                    theme_text_color="Secondary"
                )
                
                news_info = MDLabel(
                    text=f"Автор: ID {news[3]} | Дата: {news[6]}",
                    halign="left",
                    theme_text_color="Secondary",
                    font_style="Caption"
                )
                
                # Кнопки действий
                actions_layout = MDBoxLayout(
                    orientation='horizontal',
                    spacing=dp(10),
                    size_hint_y=None,
                    height=dp(40)
                )
                
                publish_btn = MDRaisedButton(
                    text="📢 Опубликовать" if not news[5] else "👁️ Снять с публикации",
                    size_hint_x=0.4,
                    md_bg_color=get_color_from_hex("#2196F3") if not news[5] else get_color_from_hex("#FF9800"),
                    size_hint_y=None,
                    height=dp(30)
                )
                publish_btn.bind(on_press=lambda x, n=news: self.toggle_publish(n))
                
                edit_btn = MDRaisedButton(
                    text="✏️ Редактировать",
                    size_hint_x=0.3,
                    md_bg_color=get_color_from_hex("#4CAF50"),
                    size_hint_y=None,
                    height=dp(30)
                )
                edit_btn.bind(on_press=lambda x, n=news: self.edit_news(n))
                
                delete_btn = MDRaisedButton(
                    text="🗑️ Удалить",
                    size_hint_x=0.3,
                    md_bg_color=get_color_from_hex("#FF5722"),
                    size_hint_y=None,
                    height=dp(30)
                )
                delete_btn.bind(on_press=lambda x, n=news: self.delete_news(n))
                
                actions_layout.add_widget(publish_btn)
                actions_layout.add_widget(edit_btn)
                actions_layout.add_widget(delete_btn)
                
                news_card.add_widget(news_title)
                news_card.add_widget(news_content)
                news_card.add_widget(news_info)
                news_card.add_widget(actions_layout)
                
                content.add_widget(news_card)
        
        scroll.add_widget(content)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def load_news(self):
        """Загрузка новостей из базы данных"""
        cursor = db.conn.cursor()
        cursor.execute('SELECT * FROM news ORDER BY created_at DESC')
        return cursor.fetchall()
    
    def add_news(self, instance):
        """Добавление новости"""
        self.show_add_dialog()
    
    def edit_news(self, news):
        """Редактирование новости"""
        self.show_edit_dialog(news)
    
    def toggle_publish(self, news):
        """Публикация/снятие с публикации"""
        new_status = 0 if news[5] else 1
        cursor = db.conn.cursor()
        cursor.execute('UPDATE news SET is_published = ? WHERE id = ?', (new_status, news[0]))
        db.conn.commit()
        
        action = "опубликована" if new_status else "снята с публикации"
        self.show_dialog("Успех", f"Новость {action}")
        self.build_ui()
    
    def delete_news(self, news):
        """Удаление новости"""
        cursor = db.conn.cursor()
        cursor.execute('DELETE FROM news WHERE id = ?', (news[0],))
        db.conn.commit()
        
        self.show_dialog("Успех", "Новость удалена")
        self.build_ui()
    
    def show_add_dialog(self):
        """Диалог добавления новости"""
        dialog_content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, height=dp(350))
        
        title_input = MDTextField(hint_text="Заголовок новости")
        content_input = MDTextField(hint_text="Содержание новости", multiline=True, size_hint_y=None, height=dp(150))
        
        dialog_content.add_widget(title_input)
        dialog_content.add_widget(content_input)
        
        self.dialog = MDDialog(
            title="Добавить новость",
            type="custom",
            content_cls=dialog_content,
            buttons=[
                MDRaisedButton(
                    text="Добавить",
                    md_bg_color=get_color_from_hex("#4CAF50"),
                    on_release=lambda x: self.save_new_news(title_input.text, content_input.text)
                )
            ]
        )
        self.dialog.open()
    
    def save_new_news(self, title, content):
        """Сохранение новой новости"""
        if title.strip() and content.strip():
            if session.is_logged_in():
                news_id = db.add_news(title, content, session.user_data['id'])
                if news_id:
                    self.show_dialog("Успех", "Новость добавлена")
                    self.dialog.dismiss()
                    self.build_ui()
                else:
                    self.show_dialog("Ошибка", "Не удалось добавить новость")
        else:
            self.show_dialog("Ошибка", "Заполните все поля")
    
    def show_edit_dialog(self, news):
        """Диалог редактирования новости"""
        dialog_content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, height=dp(350))
        
        title_input = MDTextField(hint_text="Заголовок", text=news[1])
        content_input = MDTextField(hint_text="Содержание", text=news[2], multiline=True, size_hint_y=None, height=dp(150))
        
        dialog_content.add_widget(title_input)
        dialog_content.add_widget(content_input)
        
        self.dialog = MDDialog(
            title="Редактировать новость",
            type="custom",
            content_cls=dialog_content,
            buttons=[
                MDRaisedButton(
                    text="Сохранить",
                    md_bg_color=get_color_from_hex("#2196F3"),
                    on_release=lambda x: self.save_news_changes(news[0], title_input.text, content_input.text)
                )
            ]
        )
        self.dialog.open()
    
    def save_news_changes(self, news_id, title, content):
        """Сохранение изменений новости"""
        if title.strip() and content.strip():
            cursor = db.conn.cursor()
            cursor.execute('UPDATE news SET title = ?, content = ? WHERE id = ?', (title, content, news_id))
            db.conn.commit()
            
            self.show_dialog("Успех", "Новость обновлена")
            self.dialog.dismiss()
            self.build_ui()
        else:
            self.show_dialog("Ошибка", "Заполните все поля")
    
    def show_dialog(self, title, text):
        """Показать диалоговое окно"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, 0.3)
        )
        self.dialog.open()
    
    def go_back(self):
        self.manager.current = 'dashboard'
    
    def on_enter(self):
        self.build_ui()