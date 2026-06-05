from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.recarga import calcular_recarga, MONTO_MINIMO, MONTO_MAXIMO

app = FastAPI(
    title="RecargaYa API",
    description="Módulo de cálculo de bonificaciones",
    version="1.0.0",
)

class RecargaRequest(BaseModel):
    monto:   int  = Field(..., ge=MONTO_MINIMO, le=MONTO_MAXIMO,
                          description="Monto en pesos (1.000 - 50.000)")
    premium: bool = Field(False, description="True si el cliente es premium")

class RecargaResponse(BaseModel):
    monto:            int
    bonificacion_pct: int
    datos_mb:         int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recarga", response_model=RecargaResponse)
def recargar(req: RecargaRequest):
    try:
        resultado = calcular_recarga(req.monto, premium=req.premium)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))