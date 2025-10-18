# services/excel_import_service.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from ..database import get_db

from .excel_service import ExcelService
from ..crud.table import table_template_repository, table_column_repository, table_record_repository
from ..schemas.table import TableRecordCreate
from ..schemas.excel import ExcelImportResponse
from fastapi import Depends, HTTPException, status, UploadFile

logger = logging.getLogger(__name__)

class ExcelImportService:
    def __init__(self, db: Session):
        self.db = db
    
    async def preview_excel_import(
        self, 
        file: UploadFile, 
        table_template_id: int,
        skip_first_rows: int = 0
    ) -> Dict[str, Any]:
        """Превью импорта из Excel"""
        try:
            # Читаем файл
            file_content = await file.read()
            
            # Получаем колонки таблицы
            table_columns = table_column_repository.get_by_template_id(self.db, table_template_id)
            if not table_columns:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Шаблон таблицы не найден или не имеет колонок"
                )
            
            # Получаем превью
            preview_data = ExcelService.get_excel_preview(file_content, table_columns, skip_first_rows)
            
            return preview_data
            
        except Exception as e:
            logger.error(f"Ошибка при preview импорта: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при обработке файла: {str(e)}"
            )
    
    async def import_excel_data(
        self,
        file: UploadFile,
        table_template_id: int,
        mapping: Dict[str, str],
        skip_first_rows: int = 0
    ) -> ExcelImportResponse:
        """Импорт данных из Excel в таблицу"""
        try:
            # Читаем файл
            file_content = await file.read()
            
            # Получаем колонки таблицы
            table_columns = table_column_repository.get_by_template_id(self.db, table_template_id)
            if not table_columns:
                return ExcelImportResponse(
                    success=False,
                    imported_records=0,
                    errors=[{'type': 'template_error', 'message': 'Шаблон таблицы не найден'}],
                    message="Шаблон таблицы не найден"
                )
            
            # Проверяем существование шаблона
            table_template = table_template_repository.get_by_id(self.db, table_template_id)
            if not table_template:
                return ExcelImportResponse(
                    success=False,
                    imported_records=0,
                    errors=[{'type': 'template_error', 'message': 'Шаблон таблицы не найден'}],
                    message="Шаблон таблицы не найден"
                )
            
            # Обрабатываем импорт
            records_count, errors = ExcelService.process_excel_import(
                file_content, table_template_id, mapping, table_columns, skip_first_rows
            )
            
            if errors:
                return ExcelImportResponse(
                    success=False,
                    imported_records=0,
                    errors=errors,
                    message="Обнаружены ошибки валидации"
                )
            
            # Если ошибок нет, создаем записи в БД
            df = ExcelService.parse_excel_file(file_content)
            if skip_first_rows > 0:
                df = df.iloc[skip_first_rows:].reset_index(drop=True)
            
            records_data = ExcelService.transform_to_records(df, mapping, table_columns)
            created_count = 0
            errors = []
            
            for record_data in records_data:
                try:
                    # Создаем объект TableRecordCreate
                    record_create = TableRecordCreate(
                        table_template_id=table_template_id,
                        data=record_data['data']
                    )
                    table_record_repository.create(self.db, record_create)
                    created_count += 1
                except Exception as e:
                    logger.error(f"Ошибка при создании записи: {str(e)}")
                    errors.append({
                        'type': 'creation_error',
                        'message': f'Ошибка при создании записи: {str(e)}'
                    })
            
            success = created_count > 0 and len(errors) == 0
            
            return ExcelImportResponse(
                success=success,
                imported_records=created_count,
                errors=errors,
                message=f"Успешно импортировано {created_count} записей" if success else "Произошли ошибки при импорте"
            )
            
        except Exception as e:
            logger.error(f"Ошибка при импорте Excel: {str(e)}")
            return ExcelImportResponse(
                success=False,
                imported_records=0,
                errors=[{'type': 'import_error', 'message': str(e)}],
                message="Ошибка при импорте данных"
            )
    
    async def create_table_from_excel(
        self,
        file: UploadFile,
        table_name: str,
        skip_first_rows: int = 0
    ) -> Dict[str, Any]:
        """Создание новой таблицы из Excel файла"""
        try:
            file_content = await file.read()
            df = ExcelService.parse_excel_file(file_content)
            
            if skip_first_rows > 0:
                df = df.iloc[skip_first_rows:].reset_index(drop=True)
            
            # Создаем структуру таблицы и данные
            table_template_data, records_data = ExcelService.create_table_from_excel(df, table_name)
            
            # Создаем шаблон таблицы
            from ..schemas.table import TableTemplateCreate
            template_create = TableTemplateCreate(name=table_template_data['name'])
            db_template = table_template_repository.create(self.db, template_create)
            
            # Создаем колонки
            for column_data in table_template_data['columns']:
                from ..schemas.table import TableColumnCreate
                column_create = TableColumnCreate(
                    table_template_id=db_template.id,
                    **column_data
                )
                table_column_repository.create(self.db, column_create)
            
            # Создаем записи
            created_records = 0
            for record_data in records_data:
                record_create = TableRecordCreate(
                    table_template_id=db_template.id,
                    data=record_data['data']
                )
                table_record_repository.create(self.db, record_create)
                created_records += 1
            
            return {
                'success': True,
                'table_template_id': db_template.id,
                'created_columns': len(table_template_data['columns']),
                'created_records': created_records,
                'message': f'Таблица "{table_name}" успешно создана'
            }
            
        except Exception as e:
            logger.error(f"Ошибка при создании таблицы из Excel: {str(e)}")
            return {
                'success': False,
                'message': f'Ошибка при создании таблицы: {str(e)}'
            }

def get_excel_import_service(db: Session = Depends(get_db)):
    return ExcelImportService(db)