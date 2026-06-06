import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.recarga import calcular_recarga

scenarios("../features/recarga.feature")

@pytest.fixture
def ctx():
    return {}

@given(parsers.parse("que el monto de recarga es {monto:d} pesos"))
def set_monto(ctx, monto):
    ctx["monto"] = monto

@given("el cliente no tiene plan premium")
def sin_premium(ctx):
    ctx["premium"] = False

@given("el cliente tiene plan premium")
def con_premium(ctx):
    ctx["premium"] = True

@given(parsers.parse("el cliente tiene plan {plan}"))
def set_plan(ctx, plan):
    ctx["premium"] = (plan == "premium")

@when("proceso la recarga")
def procesar(ctx):
    try:
        ctx["resultado"] = calcular_recarga(
            ctx["monto"],
            premium=ctx.get("premium", False)
        )
        ctx["error"] = None
    except ValueError as e:
        ctx["resultado"] = None
        ctx["error"] = str(e)

@then(parsers.parse("la bonificación es {bono:d} por ciento"))
def verificar_bono(ctx, bono):
    assert ctx["error"] is None, f"Hubo error inesperado: {ctx['error']}"
    assert ctx["resultado"]["bonificacion_pct"] == bono

@then("la recarga es rechazada con error de rango")
def verificar_error(ctx):
    assert ctx["error"] is not None, "Se esperaba un error pero no hubo ninguno"
    assert "rango" in ctx["error"].lower()