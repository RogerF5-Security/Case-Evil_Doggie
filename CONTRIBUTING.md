# Contribuir / Contributing

Probar, medir y compartir mejoras al ajuste es la mejor forma de ayudar.
Mantener separadas las medidas de la PCB, las tolerancias de impresión y la
geometría ilustrativa del visor.

1. Indicar la revisión de placa y el material/perfil de impresión.
2. Editar `cad/parameters.json` o `cad/model.py`; evitar correcciones solo al STL.
3. Ejecutar `python cad/build.py` y `python tools/build_viewer.py`.
4. Si afecta a cierres, USB o letras, imprimir la muestra correspondiente.
5. Actualizar las cotas, el changelog y las fotos de validación; ejecutar `python tools/check_release.py`.
6. Abrir un pull request con problema, cambio y evidencia de validación.

English: include board revision, printer/material, parameter changes and actual
measurements. Regenerate exported geometry and the viewer together. Report digital
and physical checks separately. Do not claim tested fit for a board you have not tried.

No publicar credenciales, identificadores de vehículos ni capturas privadas.
Para la carcasa basta con medidas y fotos de la placa y del ajuste mecánico.
