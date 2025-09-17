import sqlite3
import hashlib
from datetime import datetime
import logging

class Database:
    def __init__(self, db_name='serveroff.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.setup_logging()
    
    def setup_logging(self):
        """Настройка логирования операций"""
        logging.basicConfig(
            filename='serveroff.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def log_operation(self, user_id, operation, details):
        """Логирование операций в системе"""
        logging.info(f"User {user_id}: {operation} - {details}")
    
    def create_tables(self):
        cursor = self.conn.cursor()
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                user_type TEXT DEFAULT 'client',
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица организаций
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                owner_id INTEGER,
                description TEXT,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users (id)
            )
        ''')
        
        # Таблица продуктов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT,
                organization_id INTEGER,
                is_available INTEGER DEFAULT 1,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (organization_id) REFERENCES organizations (id)
            )
        ''')
        
        # Таблица заказов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                organization_id INTEGER,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                address TEXT,
                phone TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (organization_id) REFERENCES organizations (id)
            )
        ''')
        
        # Таблица элементов заказа
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER DEFAULT 1,
                price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Таблица отзывов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                organization_id INTEGER,
                rating INTEGER DEFAULT 5,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (organization_id) REFERENCES organizations (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                organization_id INTEGER,
                permission_type TEXT,
                granted_by INTEGER,
                granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (organization_id) REFERENCES organizations (id),
                FOREIGN KEY (granted_by) REFERENCES users (id)
            )
        ''')
        
        # Таблица блокировок пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                blocked_by INTEGER,
                reason TEXT,
                blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (blocked_by) REFERENCES users (id)
            )
        ''')
        
        # Таблица справочников системы
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_directories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value TEXT,
                description TEXT,
                category TEXT,
                is_active INTEGER DEFAULT 1,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Таблица новостей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                author_id INTEGER,
                organization_id INTEGER,
                is_published INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users (id),
                FOREIGN KEY (organization_id) REFERENCES organizations (id)
            )
        ''')
        
        # Таблица графиков работы
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER,
                day_of_week INTEGER,
                open_time TEXT,
                close_time TEXT,
                is_working INTEGER DEFAULT 1,
                FOREIGN KEY (organization_id) REFERENCES organizations (id)
            )
        ''')
        
        # Таблица платежей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                organization_id INTEGER,
                amount REAL,
                payment_type TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (organization_id) REFERENCES organizations (id)
            )
        ''')
        
        # Таблица записей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                organization_id INTEGER,
                datetime TEXT,
                service_type TEXT,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (organization_id) REFERENCES organizations (id)
            )
        ''')
        
        # Таблица SMS сообщений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sms_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                message TEXT,
                status TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица форумных сообщений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS forum_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                content TEXT,
                category TEXT,
                is_published INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
    
    def add_test_data(self):
        cursor = self.conn.cursor()
        
        # Проверяем, есть ли уже тестовые пользователи
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = 'test@client.com'")
        if cursor.fetchone()[0] == 0:
            # Тестовый клиент
            client_password = self.hash_password("client123")
            cursor.execute('''
                INSERT INTO users (email, password, first_name, last_name, phone, user_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('test@client.com', client_password, 'Иван', 'Петров', '+79991234567', 'client'))
            
            # Тестовая организация
            org_password = self.hash_password("org123")
            cursor.execute('''
                INSERT INTO users (email, password, first_name, last_name, phone, user_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('test@org.com', org_password, 'Мария', 'Сидорова', '+79997654321', 'organization'))
            
            # Получаем ID организации
            cursor.execute("SELECT id FROM users WHERE email = 'test@org.com'")
            org_user_id = cursor.fetchone()[0]
            
            # Добавляем организацию
            cursor.execute('''
                INSERT INTO organizations (name, owner_id, description, address, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', ('TEST Bakery', org_user_id, 'Лучшая выпечка в городе', 'ул. Тестовая, 123', '+79997654321'))
            
            # Добавляем продукты
            org_id = cursor.lastrowid
            products = [
                ('Самса с мясом', 'Сочная самса с говядиной', 150, 'Выпечка'),
                ('Самса с картошкой', 'Вегетарианский вариант', 120, 'Выпечка'),
                ('Шаурма классическая', 'Курица, овощи, соус', 200, 'Фастфуд'),
                ('Пицца Маргарита', 'Классическая итальянская', 350, 'Фастфуд'),
                ('Чай зеленый', 'Ароматный зеленый чай', 50, 'Напитки')
            ]
            
            for name, desc, price, category in products:
                cursor.execute('''
                    INSERT INTO products (name, description, price, category, organization_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, desc, price, category, org_id))
            
            print("Тестовые данные добавлены")
    
    def hash_password(self, password):
    # Убедимся, что пароль хешируется правильно
        hashed = hashlib.sha256(password.encode()).hexdigest()
        print(f"Хеш пароля '{password}': {hashed}")  # Отладочная информация
        return hashed
    
    def register_user(self, email, password, first_name, last_name, phone, user_type='client'):
        try:
            cursor = self.conn.cursor()
            hashed_password = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (email, password, first_name, last_name, phone, user_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (email, hashed_password, first_name, last_name, phone, user_type))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def login_user(self, email, password):
        cursor = self.conn.cursor()
        hashed_password = self.hash_password(password)
        print(f"Поиск пользователя: {email}, хеш пароля: {hashed_password}")  # Отладочная информация
    
        cursor.execute('''
            SELECT * FROM users WHERE email = ? AND password = ? AND is_active = 1
        ''', (email, hashed_password))

        user = cursor.fetchone()
        print(f"Результат поиска: {user}")  # Отладочная информация
        return user
    
    def get_all_users(self):
        """Метод для отладки - получить всех пользователей"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, email, user_type, is_active FROM users')
        return cursor.fetchall()

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()
    
    def add_organization(self, name, owner_id, description, address, phone):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO organizations (name, owner_id, description, address, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, owner_id, description, address, phone))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            return None
    
    def add_product(self, name, description, price, category, organization_id, image_path=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO products (name, description, price, category, organization_id, image_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, description, price, category, organization_id, image_path))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            return None
    
    def get_products(self, organization_id=None):
        cursor = self.conn.cursor()
        if organization_id:
            cursor.execute('''
                SELECT * FROM products 
                WHERE organization_id = ? AND is_available = 1
                ORDER BY name
            ''', (organization_id,))
        else:
            cursor.execute('''
                SELECT * FROM products 
                WHERE is_available = 1
                ORDER BY name
            ''')
        return cursor.fetchall()
    
    def create_order(self, user_id, organization_id, items, total_amount, address, phone, notes=""):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO orders (user_id, organization_id, total_amount, address, phone, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, organization_id, total_amount, address, phone, notes))
            
            order_id = cursor.lastrowid
            
            for item in items:
                cursor.execute('''
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                ''', (order_id, item['product_id'], item['quantity'], item['price']))
            
            self.conn.commit()
            return order_id
        except sqlite3.Error:
            return None
    
    def get_orders(self, user_id=None, organization_id=None):
        cursor = self.conn.cursor()
        if user_id:
            cursor.execute('''
                SELECT o.*, org.name as org_name 
                FROM orders o 
                JOIN organizations org ON o.organization_id = org.id 
                WHERE o.user_id = ? 
                ORDER BY o.created_at DESC
            ''', (user_id,))
        elif organization_id:
            cursor.execute('''
                SELECT o.*, u.first_name, u.last_name 
                FROM orders o 
                JOIN users u ON o.user_id = u.id 
                WHERE o.organization_id = ? 
                ORDER BY o.created_at DESC
            ''', (organization_id,))
        else:
            cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
        return cursor.fetchall()
    
    def add_review(self, user_id, organization_id, rating, comment):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO reviews (user_id, organization_id, rating, comment)
                VALUES (?, ?, ?, ?)
            ''', (user_id, organization_id, rating, comment))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            return None
    
    def get_reviews(self, organization_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT r.*, u.first_name, u.last_name 
            FROM reviews r 
            JOIN users u ON r.user_id = u.id 
            WHERE r.organization_id = ? 
            ORDER BY r.created_at DESC
        ''', (organization_id,))
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()
    
    # МЕТОДЫ ДЛЯ ОСНОВНЫХ ТРЕБОВАНИЙ:
    
    def update_user_profile(self, user_id, first_name=None, last_name=None, phone=None):
        """Обновление профиля пользователя"""
        try:
            cursor = self.conn.cursor()
            updates = []
            params = []
            
            if first_name:
                updates.append("first_name = ?")
                params.append(first_name)
            if last_name:
                updates.append("last_name = ?")
                params.append(last_name)
            if phone:
                updates.append("phone = ?")
                params.append(phone)
            
            if updates:
                params.append(user_id)
                cursor.execute(f'''
                    UPDATE users SET {', '.join(updates)} WHERE id = ?
                ''', params)
                self.conn.commit()
                self.log_operation(user_id, "UPDATE_PROFILE", f"Updated profile fields: {', '.join(updates)}")
                return True
        except sqlite3.Error as e:
            print(f"Error updating profile: {e}")
            return False
    
    def block_user(self, user_id, blocked_by, reason):
        """Блокировка пользователя"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO user_blocks (user_id, blocked_by, reason)
                VALUES (?, ?, ?)
            ''', (user_id, blocked_by, reason))
            
            # Помечаем пользователя как неактивного
            cursor.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
            
            self.conn.commit()
            self.log_operation(blocked_by, "BLOCK_USER", f"Blocked user {user_id}. Reason: {reason}")
            return True
        except sqlite3.Error:
            return False
    
    def grant_organization_permission(self, user_id, organization_id, permission_type, granted_by):
        """Выдача прав на управление организацией"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO user_permissions (user_id, organization_id, permission_type, granted_by)
                VALUES (?, ?, ?, ?)
            ''', (user_id, organization_id, permission_type, granted_by))
            
            self.conn.commit()
            self.log_operation(granted_by, "GRANT_PERMISSION", 
                f"Granted {permission_type} permission for org {organization_id} to user {user_id}")
            return True
        except sqlite3.Error:
            return False
    
    def add_news(self, title, content, author_id, organization_id=None):
        """Добавление новости"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO news (title, content, author_id, organization_id)
                VALUES (?, ?, ?, ?)
            ''', (title, content, author_id, organization_id))
            
            self.conn.commit()
            self.log_operation(author_id, "ADD_NEWS", f"Added news: {title}")
            return cursor.lastrowid
        except sqlite3.Error:
            return None
    
    def update_work_schedule(self, organization_id, schedules):
        """Обновление графика работы"""
        try:
            cursor = self.conn.cursor()
            
            # Удаляем старый график
            cursor.execute('DELETE FROM work_schedules WHERE organization_id = ?', (organization_id,))
            
            # Добавляем новый график
            for day, schedule in schedules.items():
                cursor.execute('''
                    INSERT INTO work_schedules (organization_id, day_of_week, open_time, close_time, is_working)
                    VALUES (?, ?, ?, ?, ?)
                ''', (organization_id, day, schedule['open'], schedule['close'], schedule['working']))
            
            self.conn.commit()
            self.log_operation(None, "UPDATE_SCHEDULE", f"Updated schedule for org {organization_id}")
            return True
        except sqlite3.Error:
            return False
    
    def create_payment(self, user_id, organization_id, amount, payment_type):
        """Создание платежа"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO payments (user_id, organization_id, amount, payment_type)
                VALUES (?, ?, ?, ?)
            ''', (user_id, organization_id, amount, payment_type))
            
            self.conn.commit()
            self.log_operation(user_id, "CREATE_PAYMENT", f"Payment of {amount} for org {organization_id}")
            return cursor.lastrowid
        except sqlite3.Error:
            return None
    
    def create_appointment(self, user_id, organization_id, datetime, service_type, notes=""):
        """Создание записи"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO appointments (user_id, organization_id, datetime, service_type, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, organization_id, datetime, service_type, notes))
            
            self.conn.commit()
            self.log_operation(user_id, "CREATE_APPOINTMENT", 
                f"Appointment for {service_type} at {datetime} with org {organization_id}")
            return cursor.lastrowid
        except sqlite3.Error:
            return None
    
    def send_sms(self, phone_number, message):
        """Отправка SMS (заглушка)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO sms_messages (phone_number, message, status)
                VALUES (?, ?, ?)
            ''', (phone_number, message, 'sent'))
            
            self.conn.commit()
            self.log_operation(None, "SEND_SMS", f"SMS to {phone_number}: {message[:50]}...")
            return True
        except sqlite3.Error:
            return False
    
    def add_forum_post(self, user_id, title, content, category):
        """Добавление сообщения на форум"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO forum_posts (user_id, title, content, category)
                VALUES (?, ?, ?, ?)
            ''', (user_id, title, content, category))
            
            self.conn.commit()
            self.log_operation(user_id, "ADD_FORUM_POST", f"Forum post: {title} in {category}")
            return cursor.lastrowid
        except sqlite3.Error:
            return None
    
    def add_test_data(self):
        cursor = self.conn.cursor()
    
        # Проверяем, есть ли уже тестовые пользователи
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = 'test@client.com'")
        if cursor.fetchone()[0] == 0:
            print("Добавляем тестовых пользователей...")

            # Тестовый клиент
            client_password = self.hash_password("client123")
            cursor.execute('''
                INSERT INTO users (email, password, first_name, last_name, phone, user_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('test@client.com', client_password, 'Иван', 'Петров', '+79991234567', 'client'))
            print("Добавлен тестовый клиент: test@client.com / client123")
        
            # Тестовая организация
            org_password = self.hash_password("org123")
            cursor.execute('''
                INSERT INTO users (email, password, first_name, last_name, phone, user_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('test@org.com', org_password, 'Мария', 'Сидорова', '+79997654321', 'organization'))
            print("Добавлена тестовая организация: test@org.com / org123")
        
            # Тестовый администратор
            admin_password = self.hash_password("admin123")
            cursor.execute('''
                INSERT INTO users (email, password, first_name, last_name, phone, user_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('admin@serveroff.com', admin_password, 'Администратор', 'Системы', '+79990000000', 'admin'))
            print("Добавлен администратор: admin@serveroff.com / admin123")
        
            # Получаем ID организации
            cursor.execute("SELECT id FROM users WHERE email = 'test@org.com'")
            org_user_id = cursor.fetchone()[0]
        
            # Добавляем организацию
            cursor.execute('''
                INSERT INTO organizations (name, owner_id, description, address, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', ('TEST Bakery', org_user_id, 'Лучшая выпечка в городе', 'ул. Тестовая, 123', '+79997654321'))
        
            # Добавляем продукты
            org_id = cursor.lastrowid
            products = [
                ('Самса с мясом', 'Сочная самса с говядиной', 150, 'Выпечка'),
                ('Самса с картошкой', 'Вегетарианский вариант', 120, 'Выпечка'),
                ('Шаурма классическая', 'Курица, овощи, соус', 200, 'Фастфуд'),
                ('Пицца Маргарита', 'Классическая итальянская', 350, 'Фастфуд'),
                ('Чай зеленый', 'Ароматный зеленый чай', 50, 'Напитки')
            ]
        
            for name, desc, price, category in products:
                cursor.execute('''
                    INSERT INTO products (name, description, price, category, organization_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, desc, price, category, org_id))

            self.conn.commit()
            print("Тестовые данные успешно добавлены")
        else:
            print("Тестовые пользователи уже существуют")

    def update_system_directory(self, directory_id, name, value, description, category, updated_by):
        """Обновление справочника системы"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE system_directories 
                SET name = ?, value = ?, description = ?, category = ?
                WHERE id = ?
            ''', (name, value, description, category, directory_id))
            
            self.conn.commit()
            self.log_operation(updated_by, "UPDATE_DIRECTORY", f"Updated directory {name}")
            return True
        except sqlite3.Error:
            return False

# Глобальный экземпляр базы данных
db = Database()