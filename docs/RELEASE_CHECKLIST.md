# Registro de ajuste de una impresión

Estado de la geometría compartida: **comprobación física pendiente**.
Edición comunitaria 1.0.0; revisión interna de CAD 2.0.0-rc1.
No marcar estas casillas por el resultado del CAD o por las fotografías de v1.

Datos de la prueba:

| Campo | Completar |
|---|---|
| Fecha / responsable | Pendiente |
| Revisión de PCB | Pendiente |
| Impresora / boquilla | Pendiente |
| Marca y tipo de PETG | Pendiente |
| Capas / paredes / ancho de línea | Pendiente |
| Parámetros modificados / commit | Pendiente |
| Cable USB utilizado | Pendiente |

- [ ] Muestra del cierre `08` + `09`: engancha, retiene y libera; sin raíz blanca, grietas ni deformación permanente.
- [ ] Cuatro pestañas del conjunto completo: junta cerrada, todos los ganchos asentados y apertura con punta plástica.
- [ ] Registrar cuántos ciclos de apertura se probaron; no atribuir vida útil no ensayada.
- [ ] USB-C insertado a fondo con el cable real; no roza la abertura ni desplaza el PCB.
- [ ] Confirmar o ajustar los 2 mm de rebaje del borde inferior USB.
- [ ] DB9 con cable instalado, fijaciones accesibles.
- [ ] Borneras utilizables, sin cable pellizcado al cerrar.
- [ ] GOOD y EVIL alcanzan ambos topes sin rozar.
- [ ] BOOT y RESET regresan libres; ningún botón permanece activado.
- [ ] Placa apoyada en las cuatro esquinas, sin flexión forzada.
- [ ] Ventana opcional fijada y separada de LED/componentes.
- [ ] Ventilación libre; registrar temperatura si se evalúa, con carga y ambiente descritos.
- [ ] Fotos del conjunto v2, del USB conectado y del interior añadidas al repositorio.

Si se cambia el CAD después de esta prueba, regenerar STL, 3MF y visor, revisar
la parte afectada y actualizar `CHANGELOG.md` y el informe. Cuando el ajuste y
el cierre estén comprobados, sustituir `2.0.0-rc1` por `2.0.0` en parámetros y
documentación y crear la etiqueta de publicación que corresponda.
