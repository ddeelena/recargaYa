import pytest
from src.recarga import calcular_recarga

# -- VALIDACIÓN --
def test_monto_minimo_valido():
    r = calcular_recarga(1000)
    assert r["monto"] == 1000

def test_monto_maximo_valido():
    r = calcular_recarga(50000)
    assert r["monto"] == 50000

def test_monto_bajo_rechazado():
    with pytest.raises(ValueError, match="rango"):
        calcular_recarga(999)

def test_monto_alto_rechazado():
    with pytest.raises(ValueError, match="rango"):
        calcular_recarga(50001)

def test_monto_cero_rechazado():
    with pytest.raises(ValueError, match="rango"):
        calcular_recarga(0)

# -- BONIFICACIÓN --

def test_sin_bonificacion():
    r = calcular_recarga(5000)
    assert r["bonificacion_pct"] == 0
    assert r["datos_mb"] == 0

def test_bonificacion_10_pct():
    r = calcular_recarga(10000)
    assert r["bonificacion_pct"] == 10
    assert r["datos_mb"] == 1000

def test_limite_inferior_10pct():
    r = calcular_recarga(10000)
    assert r["bonificacion_pct"] == 10

def test_justo_antes_25pct():
    r = calcular_recarga(29999)
    assert r["bonificacion_pct"] == 10

def test_bonificacion_25_pct():
    r = calcular_recarga(30000)
    assert r["bonificacion_pct"] == 25
    assert r["datos_mb"] == 7500