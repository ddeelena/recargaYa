# language: es

Característica: Cálculo de bonificación en recargas RecargaYa
  Como agente de ventas de RecargaYa
  Quiero saber qué bonificación recibe cada cliente
  Para informarle correctamente al momento de recargar

  Escenario: Recarga mínima sin bonificación
    Dado que el monto de recarga es 5000 pesos
    Y el cliente no tiene plan premium
    Cuando proceso la recarga
    Entonces la bonificación es 0 por ciento

  Escenario: Recarga con bonificación del 10 por ciento
    Dado que el monto de recarga es 10000 pesos
    Y el cliente no tiene plan premium
    Cuando proceso la recarga
    Entonces la bonificación es 10 por ciento

  Escenario: Recarga rechazada por monto inválido
    Dado que el monto de recarga es 500 pesos
    Y el cliente no tiene plan premium
    Cuando proceso la recarga
    Entonces la recarga es rechazada con error de rango

 Escenario: Cliente premium recibe bonificación adicional
    Dado que el monto de recarga es 10000 pesos
    Y el cliente tiene plan premium
    Cuando proceso la recarga
    Entonces la bonificación es 15 por ciento

  Escenario: Recarga máxima válida con bonificación alta
    Dado que el monto de recarga es 50000 pesos
    Y el cliente no tiene plan premium
    Cuando proceso la recarga
    Entonces la bonificación es 25 por ciento

  Esquema del escenario: Múltiples combinaciones de monto y plan
    Dado que el monto de recarga es <monto> pesos
    Y el cliente tiene plan <plan>
    Cuando proceso la recarga
    Entonces la bonificación es <bono> por ciento

    Ejemplos:
      | monto | plan    | bono |
      | 5000  | normal  | 0    |
      | 10000 | normal  | 10   |
      | 30000 | normal  | 25   |
      | 10000 | premium | 15   |
      | 30000 | premium | 30   |