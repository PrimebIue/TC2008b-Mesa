# Reporte  Roomba

Jorge Cabiedes Acosta - A01024053

## Opciones de mejora

- Hacer que los roombas identifiquen celdas sucias
- Hacer que los roombas recuerdas celdas ya visitadas
- Que los roombas se comuniquen entre sí para transmitir celdas ya visitadas

## Análisis

Al inicio podemos ver en las gráficas que los roombas limpian un porcentaje alto de las celdas sucias y a lo largo de la vida del modelo baja la cantidad de celdas limpiadas por cada "step".

Al final, cuando solo quedan unas pocas celdas sucias es cuando más tiempo se tardan los Roombas ya que el movimiento es random y la probabilidad de llegar a una celda específica es baja. Esto se ve claramente reflejado en la siguiente imagen, en donde las últimas celdas sucias son las que más se tardan en limpiar los Roombas.

<img src='https://github.com/PrimebIue/TC2008b-Mesa/blob/main/assets/Floor_Chart.png' title='Video Walkthrough' width='' alt='Video Walkthrough' />

Por cada agente que se agrega, el promedio de tiempo que tardan los agentes en limpiar todo el piso en teoría se debe de disminuir a la mitad, pero dado a que es completamente aleatorio el movimiento de los agentes hay una varianza de tiempo muy elevada. Por ejemplo, en la siguiente tabla, podemos ver que 6 agentes tardaron más que 5 agentes.

   | Agentes      | Steps     | Grid     |Densidad    |
   | ------------- | -------- | -------- |-------- |
   | 1      | 843| 8x8  |60% |
   | 2      | 500   |8x8  |60% |
   | 3      | 257   |8x8  |60% |
   | 4      | 202   |8x8  |60% |
   | 5      | 98   |8x8  |60% |
   | 6      | 213   |8x8  |60% |

## Video

<img src='https://github.com/PrimebIue/TC2008b-Mesa/blob/main/assets/roomba.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

