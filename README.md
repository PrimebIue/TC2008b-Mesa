# Reporte  Roomba

## Opciones de mejora

- Hacer que los roombas identifiquen celdas sucias
- Hacer que los roombas recuerdas celdas ya visitadas
- Que los roombas se comuniquen entre sí para transmitir celdas ya visitadas

## Análisis

Al inicio podemos ver en las gráficas que los roombas limpian un porcentaje alto de las celdas sucias y a lo largo de la vida del modelo baja la cantidad de celdas limpiadas por cada "step".

Al final, cuando solo quedan unas pocas celdas sucias es cuando más tiempo se tardan los Roombas ya que el movimiento es random y la probabilidad de llegar a una celda específica es baja.

Por cada agente que agregas se reduce la cantidad de pasos necesario aproximadamente por la mitad. Mientras más Roombas agregamos se aumenta la proporcion de acuerdo a mi modelo, pero esto podría ser por la naturaleza aleatoria del movimiento, se requerirían más datos para confirmarlo.
