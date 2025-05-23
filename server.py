from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from typing import List

app = FastAPI()

@app.post("/data")
async def upload_excel_files(
    fileA: UploadFile = File(...),
    fileB: UploadFile = File(...),
    eps: float = Form(...),
    min_samples: int = Form(...)
):
    try:
        # Чтение Excel-файлов в DataFrame
        df1 = pd.read_excel(fileA.file)
        df2 = pd.read_excel(fileB.file)

        # Объединение данных (пример — вертикально по строкам)
        combined_df = pd.concat([df1, df2], ignore_index=True)

        # Преобразование в JSON-формат
        result = combined_df.to_dict(orient="records")

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обработке файлов: {str(e)}")