class SessionManager:
    def __init__(self):
        self.current_user = None
        self.user_data = {}
    
    def login(self, user_data):
        self.current_user = user_data
        # Преобразуем tuple в словарь с понятными ключами
        self.user_data = {
            'id': user_data[0],
            'email': user_data[1],
            'password': user_data[2],
            'first_name': user_data[3],
            'last_name': user_data[4],
            'phone': user_data[5],
            'user_type': user_data[6],
            'is_active': user_data[7],
            'created_at': user_data[8]
        }
        print(f"Успешный вход: {self.user_data['email']} (тип: {self.user_data['user_type']})")
    
    def logout(self):
        if self.current_user:
            print(f"Выход из системы: {self.user_data.get('email', 'Unknown')}")
        self.current_user = None
        self.user_data = {}
    
    def is_logged_in(self):
        return self.current_user is not None
    
    def is_admin(self):
        return self.user_data.get('user_type') == 'admin'
    
    def is_organization(self):
        return self.user_data.get('user_type') == 'organization'

# Глобальный менеджер сессий
session = SessionManager()