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

