# Parcial-Programacion-Avanzada
Integrantes: Juan Manuel Chiesa, Magali Cristobo, Franco Losardo

## Punto 6 - Arbolado publico lineal (CABA)

La implementacion en `Parcial.py` ahora resuelve la consigna 6 usando el dataset oficial:

- Descarga el CSV desde Buenos Aires Data.
- Construye un arbol binario de busqueda por cada especie (`nombre_cientifico`), usando `nro_registro` como clave.
- Construye un arbol maestro que indexa cada especie y guarda su arbol correspondiente.
- Ejecuta dos busquedas de ejemplo y compara tiempos entre:
	- busqueda en arbol por especie,
	- busqueda a traves del arbol maestro,
	- busqueda lineal sobre el dataset crudo.

## Ejecucion

```bash
python3 Parcial.py
```

Notas:

- Por defecto usa el dataset completo.
- Si queres probar mas rapido, en `main()` podes cambiar `run_punto_6(max_rows=None, repetitions=20)` por un limite de filas, por ejemplo `max_rows=50000`.
