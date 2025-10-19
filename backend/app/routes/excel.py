# routers/excel.py
from fastapi import APIRouter, Depends, HTTPException, Path, status, UploadFile, File, Form
from typing import Dict, Any, List
import json

from ..services.excel_import_service import ExcelImportService, get_excel_import_service
from ..schemas.excel import ExcelImportResponse, ExcelPreviewResponse
from ..dependencies import get_current_user, get_admin_user, check_add_rows_permission, check_edit_structure_permission

router = APIRouter(prefix="/excel", tags=["excel"])

@router.post(
    "/preview-import/{table_id}",
    response_model=ExcelPreviewResponse,
    summary="Превью импорта Excel",
    description="Предварительный просмотр данных Excel и предложенный маппинг колонок"
)
async def preview_excel_import(
    table_id: int,
    file: UploadFile = File(..., description="Excel файл для импорта"),
    skip_first_rows: int = Form(0, description="Количество строк для пропуска"),
    excel_service: ExcelImportService = Depends(get_excel_import_service),
    current_user = Depends(get_current_user),
    _ = Depends(check_add_rows_permission)
):
    print("Превью импорта Excel файла в существующую таблицу")
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поддерживаются только Excel файлы (.xlsx, .xls)"
        )
    
    return await excel_service.preview_excel_import(file, table_id, skip_first_rows)

@router.post(
    "/import/{table_id}",
    response_model=ExcelImportResponse,
    summary="Импорт Excel в таблицу",
    description="Импорт данных из Excel файла в существующую таблицу"
)
async def import_excel_data(
    table_id: int,
    file: UploadFile = File(..., description="Excel файл для импорта"),
    mapping: str = Form(..., description="JSON маппинг колонок"),
    skip_first_rows: int = Form(0, description="Количество строк для пропуска"),
    excel_service: ExcelImportService = Depends(get_excel_import_service),
    current_user = Depends(get_current_user),
    _ = Depends(check_add_rows_permission)
):
    """Импорт данных из Excel в существующую таблицу"""
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поддерживаются только Excel файлы (.xlsx, .xls)"
        )
    
    try:
        mapping_dict = json.loads(mapping)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат маппинга. Ожидается JSON строка."
        )
    
    return await excel_service.import_excel_data(file, table_id, mapping_dict, skip_first_rows)

@router.post(
    "/create-table",
    summary="Создать таблицу из Excel",
    description="Создание новой таблицы из Excel файла"
)
async def create_table_from_excel(
    file: UploadFile = File(..., description="Excel файл для создания таблицы"),
    table_name: str = Form(..., description="Название новой таблицы"),
    skip_first_rows: int = Form(0, description="Количество строк для пропуска"),
    excel_service: ExcelImportService = Depends(get_excel_import_service),
    current_user = Depends(get_admin_user)  # Только администратор может создавать таблицы
):
    """Создание новой таблицы из Excel файла"""
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поддерживаются только Excel файлы (.xlsx, .xls)"
        )
    
    return await excel_service.create_table_from_excel(file, table_name, skip_first_rows)

@router.post(
    "/preview-create-table",
    response_model=Dict[str, Any],
    summary="Превью создания таблицы из Excel",
    description="Предварительный просмотр структуры таблицы из Excel файла"
)
async def preview_create_table_from_excel(
    file: UploadFile = File(..., description="Excel файл для создания таблицы"),
    skip_first_rows: int = Form(0, description="Количество строк для пропуска"),
    excel_service: ExcelImportService = Depends(get_excel_import_service),
    current_user = Depends(get_current_user)
):
    """Превью создания таблицы из Excel файла"""
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поддерживаются только Excel файлы (.xlsx, .xls)"
        )
    
    try:
        file_content = await file.read()
        
        # Используем ExcelService для анализа файла
        from ..services.excel_service import ExcelService
        df = ExcelService.parse_excel_file(file_content)
        
        if skip_first_rows > 0:
            df = df.iloc[skip_first_rows:].reset_index(drop=True)
        
        # Автоматически определяем структуру таблицы
        table_template_data, records_data = ExcelService.create_table_from_excel(df, "preview_table")
        
        # Получаем превью данных
        preview_data = ExcelService.get_preview_data(df)
        
        return {
            "success": True,
            "proposed_structure": table_template_data,
            "preview_data": preview_data,
            "total_rows": len(df),
            "excel_columns": df.columns.tolist(),
            "message": "Файл успешно проанализирован"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Ошибка при анализе файла: {str(e)}"
        }