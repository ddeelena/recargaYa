def calcular_recarga(monto, premium=False):
    if monto < 1000 or monto > 50000:
        raise ValueError("Monto fuera del rango permitido")
    b = 0
    if monto >= 30000:
        b = 25
    elif monto >= 10000:
        b = 10
    if premium:
        b += 5
    d = int(monto * b / 100)
    return {"monto": monto, "bonificacion_pct": b, "datos_mb": d}