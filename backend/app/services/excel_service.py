# services/excel_service.py
import pandas as pd
from typing import Dict, List, Any
import tempfile
import os

class ExcelService:
    @staticmethod
    def parse_excel_file(file_content: bytes) -> pd.DataFrame:
        """Парсинг Excel файла"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_file.write(file_content)
            tmp_file.flush()
            df = pd.read_excel(tmp_file.name)
            os.unlink(tmp_file.name)
        return df
    
    @staticmethod
    def auto_detect_mapping(df: pd.DataFrame, columns: List) -> Dict[str, str]:
        """Автоматическое определение маппинга колонок"""
        mapping = {}
        excel_columns = df.columns.tolist()
        
        for template_col in columns:
            # Простой матчинг по имени
            for excel_col in excel_columns:
                if template_col.name.lower() in excel_col.lower():
                    mapping[template_col.name] = excel_col
                    break
            # Если не нашли, используем первую доступную колонку
            if template_col.name not in mapping and excel_columns:
                mapping[template_col.name] = excel_columns[0]
        
        return mapping
    
    @staticmethod
    def transform_to_records(df: pd.DataFrame, mapping: Dict[str, str]) -> List[Dict[str, Any]]:
        """Трансформация данных Excel в записи"""
        records = []
        
        for _, row in df.iterrows():
            record_data = {}
            
            for template_field, excel_column in mapping.items():
                if excel_column in df.columns:
                    value = row[excel_column]
                    # Обработка NaN значений
                    if pd.isna(value):
                        value = None
                    record_data[template_field] = value
            
            records.append(record_data)
        
        return records