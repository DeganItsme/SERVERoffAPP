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

class AdminOrganizationsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'admin_organizations'
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Верхняя панель
        toolbar = MDTopAppBar(
            title="🏢 Управление организациями",
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
        
        # Кнопка добавления организации
        add_org_btn = MDRaisedButton(
            text="➕ Добавить организацию",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#4CAF50"),
            size_hint_y=None,
            height=dp(50)
        )
        add_org_btn.bind(on_press=self.add_organization)
        content.add_widget(add_org_btn)
        
        # Список организаций
        orgs_label = MDLabel(
            text="Зарегистрированные организации:",
            halign="left",
            theme_text_color="Primary",
            font_style="H6"
        )
        content.add_widget(orgs_label)
        
        # Загрузка организаций из базы данных
        organizations = self.load_organizations()
        
        for org in organizations:
            org_card = MDCard(
                orientation="vertical",
                padding=dp(15),
                size_hint_y=None,
                height=dp(120),
                elevation=2,
                radius=[dp(12)]
            )
            
            org_info = MDBoxLayout(orientation='vertical')
            
            org_name = MDLabel(
                text=f"🏢 {org[1]}",
                halign="left",
                theme_text_color="Primary",
                font_style="H6"
            )
            
            org_details = MDLabel(
                text=f"📞 {org[5]} | 📍 {org[4]}",
                halign="left",
                theme_text_color="Secondary"
            )
            
            org_owner = MDLabel(
                text=f"Владелец: ID {org[2]}",
                halign="left",
                theme_text_color="Secondary"
            )
            
            org_info.add_widget(org_name)
            org_info.add_widget(org_details)
            org_info.add_widget(org_owner)
            
            # Кнопки действий
            actions_layout = MDBoxLayout(
                orientation='horizontal',
                spacing=dp(10),
                size_hint_y=None,
                height=dp(40)
            )
            
            edit_btn = MDRaisedButton(
                text="✏️ Редактировать",
                size_hint_x=0.4,
                md_bg_color=get_color_from_hex("#2196F3"),
                size_hint_y=None,
                height=dp(30)
            )
            edit_btn.bind(on_press=lambda x, o=org: self.edit_organization(o))
            
            manage_btn = MDRaisedButton(
                text="👥 Права доступа",
                size_hint_x=0.4,
                md_bg_color=get_color_from_hex("#FF9800"),
                size_hint_y=None,
                height=dp(30)
            )
            manage_btn.bind(on_press=lambda x, o=org: self.manage_permissions(o))
            
            actions_layout.add_widget(edit_btn)
            actions_layout.add_widget(manage_btn)
            
            org_card.add_widget(org_info)
            org_card.add_widget(actions_layout)
            content.add_widget(org_card)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content)
        
        self.add_widget(main_layout)
    
    def load_organizations(self):
        """Загрузка организаций из базы данных"""
        cursor = db.conn.cursor()
        cursor.execute('''
            SELECT o.*, u.email as owner_email 
            FROM organizations o 
            JOIN users u ON o.owner_id = u.id 
            ORDER BY o.created_at DESC
        ''')
        return cursor.fetchall()
    
    def add_organization(self, instance):
        """Добавление новой организации"""
        self.show_add_dialog()
    
    def edit_organization(self, organization):
        """Редактирование организации"""
        self.show_edit_dialog(organization)
    
    def manage_permissions(self, organization):
        """Управление правами доступа к организации"""
        self.show_permissions_dialog(organization)
    
    def show_add_dialog(self):
        """Диалог добавления организации"""
        dialog_content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, height=dp(300))
        
        name_input = MDTextField(hint_text="Название организации")
        owner_id_input = MDTextField(hint_text="ID владельца")
        desc_input = MDTextField(hint_text="Описание", multiline=True)
        address_input = MDTextField(hint_text="Адрес")
        phone_input = MDTextField(hint_text="Телефон")
        
        dialog_content.add_widget(name_input)
        dialog_content.add_widget(owner_id_input)
        dialog_content.add_widget(desc_input)
        dialog_content.add_widget(address_input)
        dialog_content.add_widget(phone_input)
        
        self.dialog = MDDialog(
            title="Добавить организацию",
            type="custom",
            content_cls=dialog_content,
            buttons=[
                MDRaisedButton(
                    text="Добавить",
                    md_bg_color=get_color_from_hex("#4CAF50"),
                    on_release=lambda x: self.save_new_organization(
                        name_input.text, owner_id_input.text, desc_input.text, 
                        address_input.text, phone_input.text
                    )
                )
            ]
        )
        self.dialog.open()
    
    def save_new_organization(self, name, owner_id, description, address, phone):
        """Сохранение новой организации"""
        try:
            owner_id = int(owner_id)
            org_id = db.add_organization(name, owner_id, description, address, phone)
            if org_id:
                self.show_dialog("Успех", "Организация добавлена")
                self.dialog.dismiss()
                self.build_ui()
            else:
                self.show_dialog("Ошибка", "Не удалось добавить организацию")
        except ValueError:
            self.show_dialog("Ошибка", "ID владельца должен быть числом")
    
    def show_edit_dialog(self, organization):
        """Диалог редактирования организации"""
        dialog_content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, height=dp(300))
        
        name_input = MDTextField(hint_text="Название", text=organization[1])
        desc_input = MDTextField(hint_text="Описание", text=organization[3] or "", multiline=True)
        address_input = MDTextField(hint_text="Адрес", text=organization[4])
        phone_input = MDTextField(hint_text="Телефон", text=organization[5])
        
        dialog_content.add_widget(name_input)
        dialog_content.add_widget(desc_input)
        dialog_content.add_widget(address_input)
        dialog_content.add_widget(phone_input)
        
        self.dialog = MDDialog(
            title="Редактировать организацию",
            type="custom",
            content_cls=dialog_content,
            buttons=[
                MDRaisedButton(
                    text="Сохранить",
                    md_bg_color=get_color_from_hex("#2196F3"),
                    on_release=lambda x: self.save_organization_changes(
                        organization[0], name_input.text, desc_input.text, 
                        address_input.text, phone_input.text
                    )
                )
            ]
        )
        self.dialog.open()
    
    def save_organization_changes(self, org_id, name, description, address, phone):
        """Сохранение изменений организации"""
        # Здесь будет реализация сохранения изменений
        self.show_dialog("Успех", "Изменения сохранены")
        self.dialog.dismiss()
    
    def show_permissions_dialog(self, organization):
        """Диалог управления правами доступа"""
        dialog_content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, height=dp(200))
        
        user_id_input = MDTextField(hint_text="ID пользователя")
        perm_type_input = MDTextField(hint_text="Тип права (admin, manager, etc.)")
        
        dialog_content.add_widget(user_id_input)
        dialog_content.add_widget(perm_type_input)
        
        self.dialog = MDDialog(
            title=f"Права доступа: {organization[1]}",
            type="custom",
            content_cls=dialog_content,
            buttons=[
                MDRaisedButton(
                    text="Выдать право",
                    md_bg_color=get_color_from_hex("#FF9800"),
                    on_release=lambda x: self.grant_permission(
                        organization[0], user_id_input.text, perm_type_input.text
                    )
                )
            ]
        )
        self.dialog.open()
    
    def grant_permission(self, org_id, user_id, permission_type):
        """Выдача права доступа"""
        try:
            user_id = int(user_id)
            if session.is_logged_in():
                success = db.grant_organization_permission(
                    user_id, org_id, permission_type, session.user_data['id']
                )
                if success:
                    self.show_dialog("Успех", "Право доступа выдано")
                    self.dialog.dismiss()
                else:
                    self.show_dialog("Ошибка", "Не удалось выдать право доступа")
        except ValueError:
            self.show_dialog("Ошибка", "ID пользователя должен быть числом")
    
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