# services/excel_service.py
import pandas as pd
from typing import Dict, List, Any, Tuple
import io  # Добавляем импорт io
from datetime import datetime
import json

class ExcelService:
    @staticmethod
    def parse_excel_file(file_content: bytes) -> pd.DataFrame:
        """Парсинг Excel файла из памяти (без временных файлов)"""
        try:
            # Используем BytesIO для чтения из памяти
            with io.BytesIO(file_content) as buffer:
                df = pd.read_excel(buffer)
            return df
        except Exception as e:
            raise ValueError(f"Ошибка при чтении Excel файла: {str(e)}")
    
    @staticmethod
    def _convert_value(value: Any, data_type: str) -> Any:
        """Конвертирует значение в нужный тип данных"""
        if pd.isna(value) or value is None:
            return None
            
        try:
            if data_type == 'text':
                return str(value)
            elif data_type == 'number':
                if isinstance(value, (int, float)):
                    return float(value)
                elif isinstance(value, str):
                    cleaned = value.replace(' ', '').replace(',', '.')
                    return float(cleaned)
                else:
                    return float(value)
            elif data_type == 'boolean':
                if isinstance(value, bool):
                    return value
                elif isinstance(value, (int, float)):
                    return bool(value)
                elif isinstance(value, str):
                    return value.lower() in ['true', '1', 'yes', 'да', 'истина']
                else:
                    return bool(value)
            elif data_type == 'date':
                if isinstance(value, datetime):
                    return value.strftime('%Y-%m-%d')
                elif isinstance(value, str):
                    for fmt in ['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%Y.%m.%d']:
                        try:
                            dt = datetime.strptime(value, fmt)
                            return dt.strftime('%Y-%m-%d')
                        except ValueError:
                            continue
                return str(value)
            elif data_type == 'datetime':
                if isinstance(value, datetime):
                    return value.isoformat()
                elif isinstance(value, str):
                    for fmt in ['%Y-%m-%d %H:%M:%S', '%d.%m.%Y %H:%M', '%Y-%m-%dT%H:%M:%S']:
                        try:
                            dt = datetime.strptime(value, fmt)
                            return dt.isoformat()
                        except ValueError:
                            continue
                return str(value)
            elif data_type == 'select':
                return str(value)
            else:
                return str(value)
        except (ValueError, TypeError) as e:
            print(f"Ошибка конвертации значения {value} в тип {data_type}: {e}")
            return str(value)

    @staticmethod
    def auto_detect_mapping(df: pd.DataFrame, table_columns: List) -> Dict[str, str]:
        """Автоматическое определение маппинга колонок по имени"""
        mapping = {}
        excel_columns = df.columns.tolist()
        used_excel_columns = set()
        
        # Сначала пытаемся найти точное совпадение по имени
        for col in table_columns:
            col_name_lower = col.name.lower()
            
            for excel_col in excel_columns:
                excel_col_lower = str(excel_col).lower()
                if col_name_lower == excel_col_lower and excel_col not in used_excel_columns:
                    mapping[col.name] = excel_col
                    used_excel_columns.add(excel_col)
                    break
        
        # Затем частичные совпадения
        for col in table_columns:
            if col.name in mapping:
                continue
                
            col_name_lower = col.name.lower()
            best_match = None
            best_score = 0
            
            for excel_col in excel_columns:
                if excel_col in used_excel_columns:
                    continue
                    
                excel_col_lower = str(excel_col).lower()
                
                if col_name_lower in excel_col_lower or excel_col_lower in col_name_lower:
                    score = len(set(col_name_lower) & set(excel_col_lower))
                    if score > best_score:
                        best_score = score
                        best_match = excel_col
            
            if best_match:
                mapping[col.name] = best_match
                used_excel_columns.add(best_match)
        
        # Заполняем оставшиеся колонки по порядку
        for col in table_columns:
            if col.name not in mapping:
                for excel_col in excel_columns:
                    if excel_col not in used_excel_columns:
                        mapping[col.name] = excel_col
                        used_excel_columns.add(excel_col)
                        break
        
        return mapping
    
    @staticmethod
    def get_preview_data(df: pd.DataFrame, rows: int = 10) -> List[Dict]:
        """Возвращает превью данных для отображения пользователю"""
        preview_df = df.head(rows)
        preview_data = []
        
        for _, row in preview_df.iterrows():
            record = {}
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    record[col] = None
                else:
                    # Для превью оставляем строковое представление
                    record[col] = str(value) if not isinstance(value, (int, float, bool)) else value
            preview_data.append(record)
        
        return preview_data
    
    @staticmethod
    def validate_data_with_schema(df: pd.DataFrame, mapping: Dict[str, str], table_columns: List) -> Tuple[bool, List[Dict]]:
        """Упрощенная валидация данных по схеме таблицы (без обязательных полей)"""
        errors = []
        
        # Проверяем только типы данных в первых 10 строках для примера
        sample_size = min(10, len(df))
        for i in range(sample_size):
            for col in table_columns:
                if col.name in mapping:
                    excel_col = mapping[col.name]
                    if excel_col in df.columns:
                        value = df.iloc[i][excel_col]
                        
                        # Пропускаем пустые значения
                        if pd.isna(value):
                            continue
                            
                        try:
                            ExcelService._convert_value(value, col.data_type)
                        except Exception as e:
                            errors.append({
                                'type': 'type_conversion_error',
                                'message': f'Строка {i+1}: неверный тип данных в поле "{col.name}" - {str(e)}',
                                'row': i + 1,
                                'column': col.name,
                                'value': str(value)
                            })
        
        return len(errors) == 0, errors

    @staticmethod
    def transform_to_records(df: pd.DataFrame, mapping: Dict[str, str], table_columns: List) -> List[Dict[str, Any]]:
        """Трансформация данных Excel в записи с учетом типов данных"""
        records = []
        
        # Создаем словарь колонок для быстрого доступа
        column_dict = {col.name: col for col in table_columns}
        print(f"column_dict {df}")
        for index, row in df.iterrows():
            record_data = {}
            print(record_data)
            for column_name, excel_column in mapping.items():
                print(f"column_name {column_name}, column {excel_column}")
                if excel_column in df.columns:
                    value = row[excel_column]
                    print(f"value {value}, column {excel_column}")
                    # Получаем информацию о типе данных колонки
                    col_info = column_dict.get(column_name)
                    data_type = col_info.data_type if col_info else 'text'
                    
                    # Конвертируем значение
                    converted_value = ExcelService._convert_value(value, data_type)
                    record_data[column_name] = converted_value
            
            # Добавляем только если есть хотя бы одно непустое поле
            if any(v is not None for v in record_data.values()):
                records.append({'data': record_data})
        
        return records
    
    @staticmethod
    def create_table_from_excel(df: pd.DataFrame, table_name: str) -> Tuple[Dict, List[Dict]]:
        """Создает структуру таблицы и данные из Excel файла"""
        columns = []
        for col_name in df.columns:
            col_data = df[col_name]
            
            # Определяем тип данных на основе первых непустых значений
            data_type = 'text'  # по умолчанию
            
            numeric_values = pd.to_numeric(col_data, errors='coerce')
            if numeric_values.notna().sum() > len(col_data) * 0.8:
                data_type = 'number'
            elif pd.to_datetime(col_data, errors='coerce').notna().sum() > len(col_data) * 0.8:
                data_type = 'datetime'
            elif col_data.dropna().apply(lambda x: str(x).lower() in ['true', 'false', '0', '1', 'да', 'нет']).all():
                data_type = 'boolean'
            
            columns.append({
                'name': str(col_name),
                'data_type': data_type,
                'order_index': len(columns),
                'config': {}
            })
        
        # Трансформируем данные
        records_data = []
        for _, row in df.iterrows():
            record = {}
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    record[str(col)] = None
                else:
                    # Для создания таблицы сохраняем оригинальные типы
                    record[str(col)] = value
            records_data.append({'data': record})
        
        table_template = {
            'name': table_name,
            'columns': columns
        }
        
        return table_template, records_data

    @staticmethod
    def process_excel_import(
        file_content: bytes,
        mapping: Dict[str, str],
        table_columns: List,
        skip_first_rows: int = 0
    ) -> Tuple[int, List[Dict[str, Any]]]:
        """Основной метод для импорта данных из Excel"""
        try:
            # Парсим Excel
            df = ExcelService.parse_excel_file(file_content)
            
            # Пропускаем указанное количество строк
            if skip_first_rows > 0:
                df = df.iloc[skip_first_rows:].reset_index(drop=True)
            
            # Валидируем данные
            is_valid, errors = ExcelService.validate_data_with_schema(df, mapping, table_columns)
            if not is_valid:
                return 0, errors
            
            # Трансформируем в записи
            print(f"df in {df}, {mapping}, {table_columns}")
            records = ExcelService.transform_to_records(df, mapping, table_columns)
            
            return len(records), []
            
        except Exception as e:
            print(e)
            return 0, [{'type': 'processing_error', 'message': str(e)}]

    @staticmethod
    def get_excel_preview(
        file_content: bytes, 
        table_columns: List,
        skip_first_rows: int = 0
    ) -> Dict[str, Any]:
        """Получение превью Excel файла и предложенного маппинга"""
        try:
            df = ExcelService.parse_excel_file(file_content)
            
            # Пропускаем строки если нужно
            if skip_first_rows > 0:
                df = df.iloc[skip_first_rows:].reset_index(drop=True)
            
            # Автоматический маппинг
            suggested_mapping = ExcelService.auto_detect_mapping(df, table_columns)
            
            # Превью данных
            preview_data = ExcelService.get_preview_data(df)
            
            return {
                'columns': df.columns.tolist(),
                'preview_data': preview_data,
                'suggested_mapping': suggested_mapping,
                'table_columns': [{'name': col.name, 'data_type': col.data_type} for col in table_columns]
            }
            
        except Exception as e:
            raise ValueError(f"Ошибка при обработке Excel файла: {str(e)}")