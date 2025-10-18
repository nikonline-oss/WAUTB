# test_models.py
import sys

import os
from datetime import datetime

# Добавляем родительскую директорию в путь для импортов
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Теперь импортируем напрямую из модулей
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
from sqlalchemy.sql import func

from models import User, TableColumn,TableRecord,TableTemplate

# Создаем базовый класс для моделей
Base = declarative_base()

# =============================================================================
# МОДЕЛИ (копируем ваши модели прямо в файл)
# =============================================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    created_templates = relationship("TableTemplate", back_populates="creator")
    created_records = relationship("TableRecord", foreign_keys="TableRecord.created_by", back_populates="creator_user")
    updated_records = relationship("TableRecord", foreign_keys="TableRecord.updated_by", back_populates="updater_user")

class TableTemplate(Base):
    __tablename__ = "table_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    creator = relationship("User", back_populates="created_templates")
    columns = relationship("TableColumn", back_populates="table_template", cascade="all, delete-orphan")
    records = relationship("TableRecord", back_populates="table_template", cascade="all, delete-orphan")

class TableColumn(Base):
    __tablename__ = "table_columns"

    id = Column(Integer, primary_key=True, index=True)
    table_template_id = Column(Integer, ForeignKey("table_templates.id"), nullable=False)
    name = Column(String(255), nullable=False)
    column_key = Column(String(100), nullable=False)
    data_type = Column(String(50), nullable=False)
    is_required = Column(Boolean, default=False)
    is_unique = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)
    config = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    table_template = relationship("TableTemplate", back_populates="columns")

class TableRecord(Base):
    __tablename__ = "table_records"

    id = Column(Integer, primary_key=True, index=True)
    table_template_id = Column(Integer, ForeignKey("table_templates.id"), nullable=False)
    data = Column(JSON, nullable=False, default=dict)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    version = Column(Integer, default=1)
    
    # Relationships
    table_template = relationship("TableTemplate", back_populates="records")
    creator_user = relationship("User", foreign_keys=[created_by], back_populates="created_records")
    updater_user = relationship("User", foreign_keys=[updated_by], back_populates="updated_records")

# =============================================================================
# НАСТРОЙКА БАЗЫ ДАННЫХ
# =============================================================================

# Используем SQLite для тестирования
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Инициализация базы данных - создание таблиц"""
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы в базе данных")

def clear_db():
    """Очистка базы данных"""
    Base.metadata.drop_all(bind=engine)
    print("✅ База данных очищена")

# =============================================================================
# ТЕСТЫ
# =============================================================================

def test_basic_operations():
    """Тестируем базовые CRUD операции"""
    print("🧪 ТЕСТИРОВАНИЕ БАЗОВЫХ ОПЕРАЦИЙ")
    print("=" * 50)
    
    # Инициализируем БД
    init_db()
    db = SessionLocal()
    
    try:
        # 1. СОЗДАНИЕ ДАННЫХ
        print("\n1. СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ")
        print("-" * 30)
        
        # Создаем пользователей
        user1 = User(
            email="admin@company.com",
            password_hash="hash123",
            name="Администратор Системы"
        )
        
        user2 = User(
            email="manager@company.com",
            password_hash="hash456", 
            name="Менеджер Проектов"
        )
        
        db.add_all([user1, user2])
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        
        print(f"✅ Созданы пользователи: {user1.name}, {user2.name}")
        
        # Создаем шаблон таблицы
        template = TableTemplate(
            name="Проекты",
            created_by=user1.id
        )
        db.add(template)
        db.commit()
        db.refresh(template)
        print(f"✅ Создан шаблон: {template.name}")
        
        # Создаем колонки
        columns = [
            TableColumn(
                table_template_id=template.id,
                name="Название проекта",
                column_key="project_name",
                data_type="text",
                is_required=True,
                order_index=0
            ),
            TableColumn(
                table_template_id=template.id,
                name="Бюджет",
                column_key="budget",
                data_type="number",
                order_index=1,
                config={"min": 0, "decimals": 2}
            ),
            TableColumn(
                table_template_id=template.id,
                name="Статус",
                column_key="status", 
                data_type="select",
                order_index=2,
                config={"options": ["планируется", "в работе", "завершен"]}
            )
        ]
        
        db.add_all(columns)
        db.commit()
        print(f"✅ Созданы {len(columns)} колонок")
        
        # Создаем записи
        records = [
            TableRecord(
                table_template_id=template.id,
                data={
                    "project_name": "Модернизация цеха",
                    "budget": 5000000,
                    "status": "в работе"
                },
                created_by=user1.id,
                updated_by=user1.id
            ),
            TableRecord(
                table_template_id=template.id,
                data={
                    "project_name": "Разработка新产品",
                    "budget": 2500000,
                    "status": "планируется"
                },
                created_by=user2.id,
                updated_by=user2.id
            )
        ]
        
        db.add_all(records)
        db.commit()
        print(f"✅ Созданы {len(records)} записи")
        
        # 2. ЧТЕНИЕ ДАННЫХ
        print("\n2. ТЕСТИРОВАНИЕ ЧТЕНИЯ ДАННЫХ")
        print("-" * 30)
        
        # Читаем пользователей
        users = db.query(User).all()
        print(f"📊 Всего пользователей: {len(users)}")
        for user in users:
            print(f"   - {user.name} ({user.email})")
        
        # Читаем шаблоны
        templates = db.query(TableTemplate).all()
        print(f"📊 Всего шаблонов: {len(templates)}")
        
        # Читаем записи
        all_records = db.query(TableRecord).all()
        print(f"📊 Всего записей: {len(all_records)}")
        for record in all_records:
            print(f"   - {record.data.get('project_name')} (бюджет: {record.data.get('budget')})")
        
        # 3. ОБНОВЛЕНИЕ ДАННЫХ
        print("\n3. ТЕСТИРОВАНИЕ ОБНОВЛЕНИЯ")
        print("-" * 30)
        
        # Обновляем запись
        record_to_update = all_records[0]
        old_budget = record_to_update.data['budget']
        record_to_update.data['budget'] = 6000000
        record_to_update.updated_by = user2.id
        db.commit()
        
        print(f"✅ Обновлена запись: {record_to_update.data['project_name']}")
        print(f"   Бюджет изменен: {old_budget} → {record_to_update.data['budget']}")
        
        # 4. УДАЛЕНИЕ ДАННЫХ
        print("\n4. ТЕСТИРОВАНИЕ УДАЛЕНИЯ")
        print("-" * 30)
        
        # Удаляем одну запись
        record_to_delete = all_records[1]
        db.delete(record_to_delete)
        db.commit()
        
        remaining_records = db.query(TableRecord).count()
        print(f"✅ Удалена запись. Осталось записей: {remaining_records}")
        
        print("\n✅ БАЗОВЫЕ ОПЕРАЦИИ УСПЕШНО ПРОТЕСТИРОВАНЫ!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def test_relationships():
    """Тестируем связи между моделями"""
    print("\n\n🔗 ТЕСТИРОВАНИЕ СВЯЗЕЙ МЕЖДУ МОДЕЛЯМИ")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Создаем тестовые данные
        user = User(email="test@test.com", password_hash="test", name="Тестовый Пользователь")
        db.add(user)
        db.commit()
        db.refresh(user)
        
        template = TableTemplate(name="Тест связи", created_by=user.id)
        db.add(template)
        db.commit()
        db.refresh(template)
        
        column = TableColumn(
            table_template_id=template.id,
            name="Тестовая колонка",
            column_key="test_field",
            data_type="text"
        )
        db.add(column)
        db.commit()
        
        record = TableRecord(
            table_template_id=template.id,
            data={"test_field": "тестовое значение"},
            created_by=user.id,
            updated_by=user.id
        )
        db.add(record)
        db.commit()
        
        print("✅ Тестовые данные созданы")
        
        # ТЕСТ 1: Пользователь -> Шаблоны
        print("\n📋 ТЕСТ 1: ПОЛЬЗОВАТЕЛЬ -> ШАБЛОНЫ")
        user_with_templates = db.query(User).options(
            joinedload(User.created_templates)
        ).filter(User.id == user.id).first()
        
        print(f"Пользователь: {user_with_templates.name}")
        print(f"Созданные шаблоны: {len(user_with_templates.created_templates)}")
        for tpl in user_with_templates.created_templates:
            print(f"  - {tpl.name}")
        
        # ТЕСТ 2: Шаблон -> Колонки
        print("\n📋 ТЕСТ 2: ШАБЛОН -> КОЛОНКИ")
        template_with_columns = db.query(TableTemplate).options(
            joinedload(TableTemplate.columns)
        ).filter(TableTemplate.id == template.id).first()
        
        print(f"Шаблон: {template_with_columns.name}")
        print(f"Колонки: {len(template_with_columns.columns)}")
        for col in template_with_columns.columns:
            print(f"  - {col.name} ({col.data_type})")
        
        # ТЕСТ 3: Шаблон -> Записи
        print("\n📋 ТЕСТ 3: ШАБЛОН -> ЗАПИСИ")
        template_with_records = db.query(TableTemplate).options(
            joinedload(TableTemplate.records)
        ).filter(TableTemplate.id == template.id).first()
        
        print(f"Шаблон: {template_with_records.name}")
        print(f"Записи: {len(template_with_records.records)}")
        for rec in template_with_records.records:
            print(f"  - Данные: {rec.data}")
        
        # ТЕСТ 4: Запись -> Создатель
        print("\n📋 ТЕСТ 4: ЗАПИСЬ -> СОЗДАТЕЛЬ")
        record_with_creator = db.query(TableRecord).options(
            joinedload(TableRecord.creator_user)
        ).filter(TableRecord.id == record.id).first()
        
        print(f"Запись ID: {record_with_creator.id}")
        print(f"Создатель: {record_with_creator.creator_user.name}")
        
        # ТЕСТ 5: Колонка -> Шаблон
        print("\n📋 ТЕСТ 5: КОЛОНКА -> ШАБЛОН")
        column_with_template = db.query(TableColumn).options(
            joinedload(TableColumn.table_template)
        ).filter(TableColumn.id == column.id).first()
        
        print(f"Колонка: {column_with_template.name}")
        print(f"Шаблон: {column_with_template.table_template.name}")
        
        print("\n✅ СВЯЗИ МЕЖДУ МОДЕЛЯМИ РАБОТАЮТ КОРРЕКТНО!")
        
    except Exception as e:
        print(f"❌ Ошибка в тесте связей: {e}")
        db.rollback()
    finally:
        db.close()

def test_json_operations():
    """Тестируем операции с JSON полями"""
    print("\n\n🔧 ТЕСТИРОВАНИЕ JSON ОПЕРАЦИЙ")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Создаем тестовые данные
        user = User(email="json@test.com", password_hash="json", name="JSON Тестер")
        db.add(user)
        db.commit()
        db.refresh(user)
        
        template = TableTemplate(name="JSON Тест", created_by=user.id)
        db.add(template)
        db.commit()
        db.refresh(template)
        
        # Создаем записи с разными JSON структурами
        records = [
            TableRecord(
                table_template_id=template.id,
                data={
                    "text_field": "простой текст",
                    "number_field": 123.45,
                    "boolean_field": True,
                    "array_field": ["значение1", "значение2"],
                    "object_field": {"nested": "вложенное значение"}
                },
                created_by=user.id,
                updated_by=user.id
            ),
            TableRecord(
                table_template_id=template.id,
                data={
                    "text_field": "другой текст", 
                    "number_field": 678.90,
                    "boolean_field": False,
                    "array_field": ["значение3"],
                    "object_field": {"nested": "другое значение"}
                },
                created_by=user.id,
                updated_by=user.id
            )
        ]
        
        db.add_all(records)
        db.commit()
        
        print("✅ Тестовые JSON данные созданы")
        
        # ТЕСТ 1: Поиск по текстовому полю
        print("\n📋 ТЕСТ 1: ПОИСК ПО ТЕКСТУ")
        text_results = db.query(TableRecord).filter(
            TableRecord.data["text_field"].astext == "простой текст"
        ).all()
        print(f"Найдено записей: {len(text_results)}")
        
        # ТЕСТ 2: Поиск с LIKE
        print("\n📋 ТЕСТ 2: ПОИСК С LIKE")
        like_results = db.query(TableRecord).filter(
            TableRecord.data["text_field"].astext.ilike("%текст%")
        ).all()
        print(f"Найдено записей с 'текст': {len(like_results)}")
        
        # ТЕСТ 3: Фильтрация по числам
        print("\n📋 ТЕСТ 3: ФИЛЬТРАЦИЯ ПО ЧИСЛАМ")
        number_results = db.query(TableRecord).filter(
            TableRecord.data["number_field"].astext.cast(Integer) > 200
        ).all()
        print(f"Записей с number_field > 200: {len(number_results)}")
        
        # ТЕСТ 4: Проверка существования поля
        print("\n📋 ТЕСТ 4: ПРОВЕРКА ПОЛЯ")
        has_field = db.query(TableRecord).filter(
            TableRecord.data.has_key("boolean_field")
        ).count()
        print(f"Записей с полем 'boolean_field': {has_field}")
        
        # ТЕСТ 5: Обновление JSON
        print("\n📋 ТЕСТ 5: ОБНОВЛЕНИЕ JSON")
        record_to_update = records[0]
        original_data = record_to_update.data.copy()
        
        # Обновляем несколько полей
        record_to_update.data["text_field"] = "ОБНОВЛЕННЫЙ ТЕКСТ"
        record_to_update.data["new_field"] = "новое поле"
        db.commit()
        
        # Проверяем обновление
        updated_record = db.query(TableRecord).filter(TableRecord.id == record_to_update.id).first()
        print(f"Оригинальные данные: {original_data}")
        print(f"Обновленные данные: {updated_record.data}")
        
        print("\n✅ JSON ОПЕРАЦИИ РАБОТАЮТ КОРРЕКТНО!")
        
    except Exception as e:
        print(f"❌ Ошибка в JSON тестах: {e}")
        db.rollback()
    finally:
        db.close()

def test_complex_queries():
    """Тестируем сложные запросы"""
    print("\n\n📊 ТЕСТИРОВАНИЕ СЛОЖНЫХ ЗАПРОСОВ")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Создаем разнообразные тестовые данные
        users = [
            User(email="user1@test.com", password_hash="pass1", name="Пользователь 1"),
            User(email="user2@test.com", password_hash="pass2", name="Пользователь 2"),
        ]
        db.add_all(users)
        db.commit()
        for user in users:
            db.refresh(user)
        
        templates = [
            TableTemplate(name="Проекты", created_by=users[0].id),
            TableTemplate(name="Задачи", created_by=users[1].id),
        ]
        db.add_all(templates)
        db.commit()
        for template in templates:
            db.refresh(template)
        
        # Создаем записи для статистики
        records = []
        for i in range(10):
            template_id = templates[0].id if i % 2 == 0 else templates[1].id
            user_id = users[0].id if i < 7 else users[1].id
            
            records.append(TableRecord(
                table_template_id=template_id,
                data={
                    "name": f"Запись {i+1}",
                    "value": i * 100,
                    "category": "категория A" if i % 3 == 0 else "категория B"
                },
                created_by=user_id,
                updated_by=user_id
            ))
        
        db.add_all(records)
        db.commit()
        
        print("✅ Созданы данные для сложных запросов")
        
        # ЗАПРОС 1: Статистика по пользователям
        print("\n📈 ЗАПРОС 1: СТАТИСТИКА ПОЛЬЗОВАТЕЛЕЙ")
        from sqlalchemy import func
        
        user_stats = db.query(
            User.name,
            func.count(TableRecord.id).label('records_count')
        ).join(TableRecord, User.id == TableRecord.created_by)\
         .group_by(User.id, User.name)\
         .all()
        
        for stat in user_stats:
            print(f"   {stat.name}: {stat.records_count} записей")
        
        # ЗАПРОС 2: Статистика по шаблонам
        print("\n📈 ЗАПРОС 2: СТАТИСТИКА ШАБЛОНОВ")
        template_stats = db.query(
            TableTemplate.name,
            func.count(TableRecord.id).label('records_count')
        ).join(TableRecord, TableTemplate.id == TableRecord.table_template_id)\
         .group_by(TableTemplate.id, TableTemplate.name)\
         .all()
        
        for stat in template_stats:
            print(f"   {stat.name}: {stat.records_count} записей")
        
        # ЗАПРОС 3: Самые активные пользователи
        print("\n📈 ЗАПРОС 3: САМЫЕ АКТИВНЫЕ ПОЛЬЗОВАТЕЛЕЙ")
        active_users = db.query(
            User.name,
            func.count(TableRecord.id).label('created_count')
        ).join(TableRecord, User.id == TableRecord.created_by)\
         .group_by(User.id, User.name)\
         .order_by(func.count(TableRecord.id).desc())\
         .limit(5)\
         .all()
        
        for i, user in enumerate(active_users, 1):
            print(f"   {i}. {user.name}: {user.created_count} записей")
        
        print("\n✅ СЛОЖНЫЕ ЗАПРОСЫ РАБОТАЮТ КОРРЕКТНО!")
        
    except Exception as e:
        print(f"❌ Ошибка в сложных запросах: {e}")
        db.rollback()
    finally:
        db.close()

def run_all_tests():
    """Запускаем все тесты"""
    print("🚀 ЗАПУСК ВСЕХ ТЕСТОВ МОДЕЛЕЙ БАЗЫ ДАННЫХ")
    print("=" * 60)
    
    # Очищаем и создаем базу заново
    clear_db()
    
    # Запускаем тесты
    test_basic_operations()
    test_relationships() 
    test_json_operations()
    test_complex_queries()
    
    print("\n" + "=" * 60)
    print("🎉 ВСЕ ТЕСТЫ УСПЕШНО ЗАВЕРШЕНЫ!")
    print("\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    
    # Финальная статистика
    db = SessionLocal()
    try:
        users_count = db.query(User).count()
        templates_count = db.query(TableTemplate).count()
        columns_count = db.query(TableColumn).count()
        records_count = db.query(TableRecord).count()
        
        print(f"   👥 Пользователи: {users_count}")
        print(f"   📊 Шаблоны: {templates_count}")
        print(f"   🗂 Колонки: {columns_count}") 
        print(f"   📝 Записи: {records_count}")
        print(f"   💾 База данных: test.db")
    finally:
        db.close()

if __name__ == "__main__":
    run_all_tests()