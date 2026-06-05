MONTO_MINIMO        = 1_000
MONTO_MAXIMO        = 50_000
UMBRAL_BONO_ALTO    = 30_000
UMBRAL_BONO_BAJO    = 10_000
PCT_BONO_ALTO       = 25
PCT_BONO_BAJO       = 10
PCT_PREMIUM_EXTRA   = 5

def calcular_recarga(monto: int, premium: bool = False) -> dict:

    if not (MONTO_MINIMO <= monto <= MONTO_MAXIMO):
        raise ValueError(
            f"Monto fuera del rango permitido "
            f"(${MONTO_MINIMO:,} - ${MONTO_MAXIMO:,})"
        )
    if monto >= UMBRAL_BONO_ALTO:
        bonificacion = PCT_BONO_ALTO
    elif monto >= UMBRAL_BONO_BAJO:
        bonificacion = PCT_BONO_BAJO
    else:
        bonificacion = 0

    if premium:
        bonificacion += PCT_PREMIUM_EXTRA

    datos_mb = int(monto * bonificacion / 100)

    return {
        "monto":          monto,
        "bonificacion_pct": bonificacion,
        "datos_mb":       datos_mb,
    }