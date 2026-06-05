
La empresa RecargaYa S.A.S. necesita un módulo para calcular el valor final de recargas de celular. Las reglas son: el monto de recarga debe estar entre $1.000 y $50.000, de lo contrario se rechaza; recargas de $10.000 o más reciben un 10% de datos de bonificación; recargas de $30.000 o más reciben un 25% de datos de bonificación; v los usuarios con plan premium obtienen un 5% adicional sobre cualquier bonificación. 

Construye este módulo usando TDD con los ciclos Red-Green-Refactor visibles en los commits, 

diseña una tabla de casos de prueba aplicando partición de equivalencia y valores límite para el campo de monto, escribe mínimo 5 escenarios BDD en Gherkin incluyendo un Scenario Outline, expón el módulo como API REST con FastAPI. 

agrega un script de Locust que verifique que el P95 sea menor a 300ms con 30 usuarios simultáneos, 

y conecta todo en un pipeline de GitHub Actions que corra los tests en cada push. 

La entrega es un repositorio GitHub público con el pipeline en verde y un README.md con los comandos para ejecutar cada tipo de prueba.

Regla 1 — Validación de monto:
  monto < $1.000   → RECHAZADA (error)
  monto > $50.000  → RECHAZADA (error)
  $1.000 - $50.000 → válida, continúa

Regla 2 — Bonificación de datos:
  $1.000 a $9.999  → 0% bonificación
  $10.000 a $29.999 → 10% bonificación
  $30.000 a $50.000 → 25% bonificación

Regla 3 — Plan premium:
  premium=True → +5% ADICIONAL sobre la bonificación ya calculada
  (NO es 5% del monto, es 5% más encima del porcentaje)

Particion 

Clase | Rango | Ejemplo | Esperado | Tipo
Bajo el mínimo       │ < 1.000      │ 500         │ ValueError│ Inválida │
│ Monto válido bajo    │ 1.000-9.999  │ 5.000  │ bono=0%   │ Válida   │
│ Monto con bono bajo  │ 10.000-29.999│ 20.000   │ bono=10%  │ Válida   │
│ Monto con bono alto  │ 30.000-50.000│ 40.000 │ bono=25%  │ Válida   │
│ Sobre el máximo  │ > 50.000     │ 60.000 │ ValueError│ Inválida │
│ Negativo   │ < 0  │ -100  │ ValueError│ Inválida │
│ Cero     │ = 0 │ 0 │ ValueError│ Inválida 


│ Descripción                 │ Monto    │ Esperado         │ Estado   │

│ Justo bajo el mínimo   │ 999      │ ValueError  │ Inválido │
│ Exactamente el mínimo │ 1.000    │ bono=0%, ok  │ Válido   │
│ Justo sobre el mínimo │ 1.001    │ bono=0%, ok  │ Válido   │
│ Justo bajo umbral 10%  │ 9.999    │ bono=0%    │ Válido   │
│ Exactamente umbral 10% │ 10.000   │ bono=10%  │ Válido   │
│ Justo sobre umbral 10%  │ 10.001   │ bono=10%    │ Válido   │
│ Justo bajo umbral 25% │ 29.999   │ bono=10%    │ Válido   │
│ Exactamente umbral 25% │ 30.000   │ bono=25%   │ Válido   │
│ Justo sobre umbral 25%  │ 30.001   │ bono=25%   │ Válido   │
│ Exactamente el máximo   │ 50.000   │ bono=25%, ok     │ Válido   │
│ Justo sobre el máximo   │ 50.001   │ ValueError  │ Inválido │


Casos de prueba 

IDRequerimiento | Descripción | PrecondiciónDatos de entrada | PasosResultado esperado

CP-01 | RQ-01 Validación de montoMonto por debajo del mínimo permitido | Sistema disponible | monto=500, premium=False1. | Llamar calcular_recarga(500) | ValueError: "Monto fuera del rango permitido"
CP-02 | RQ-01 Validación de montoMonto igual a cero | Sistema disponible | monto=0, premium=False1. | Llamar calcular_recarga(0) | ValueError: "Monto fuera del rango permitido"
CP-03 | RQ-01 Validación de montoMonto negativoSistema disponiblemonto=-100, premium=False1. Llamar calcular_recarga(-100)ValueError: "Monto fuera del rango permitido"
CP-04 | RQ-01 Validación de monto |Monto por encima del máximo permitido | Sistema disponible | monto=60000, premium=False1. | Llamar calcular_recarga(60000)ValueError: "Monto fuera del rango permitido"
CP-05 |RQ-02 Bonificación 0% |Monto válido sin bonificación | Monto dentro del rango| monto=5000, premium=False1. | Llamar calcular_recarga(5000)bonificacion_pct=0, datos_mb=0
CP-06 | RQ-03 Bonificación 10% | Monto en clase de bonificación media | Monto dentro del rango |monto=20000, premium=False1. |Llamar calcular_recarga(20000)bonificacion_pct=10, datos_mb=2000
CP-07 | RQ-04 Bonificación 25% | Monto en clase de bonificación alta | Monto dentro del rango | monto=40000, premium=False1. | Llamar calcular_recarga(40000)bonificacion_pct=25, datos_mb=10000
CP-08 | RQ-05 Plan premium | Usuario premium sin bono base | Monto dentro del rango | monto=5000, premium=True1. | Llamar calcular_recarga(5000, premium=True)bonificacion_pct=5, datos_mb=250
CP-09 | RQ-05 Plan premiumUsuario premium con bono 10% | Monto dentro del rangomonto=10000, premium=True1. | Llamar calcular_recarga(10000, premium=True)bonificacion_pct=15, datos_mb=1500
CP-10 | RQ-05 Plan premium | suario premium con bono 25% |Monto dentro del rango | monto=30000, premium=True1. | Llamar calcular_recarga(30000, premium=True)bonificacion_pct=30, datos_mb=9000

## comandos

tdd: uv run pytest -v
bdd: uv run pytest tests/bdd/steps/ -v

