# Sitio y mantenimiento

El repositorio público es [Case-Evil_Doggie](https://github.com/RogerF5-Security/Case-Evil_Doggie). La portada es `README.md` y el sitio es [Doggie House](https://rogerf5-security.github.io/Case-Evil_Doggie/).

## GitHub Pages

El sitio se sirve desde la rama `main`, carpeta `/ (root)`. `index.html` presenta el proyecto y el ensamblaje; `viewer/index.html` contiene el visor completo, incluida su geometría y arte de referencia. `.nojekyll` permite servir los archivos estáticos directamente.

En **Settings → Pages**, seleccionar **Deploy from a branch → main → / (root)**. La publicación de contenido nuevo sigue los commits de esa rama. No se necesitan cuentas externas, claves API ni CDN para el visor.

## Actualizar la documentación

1. Mantener alineados `README.md`, la portada HTML y las guías ES/EN.
2. Editar `viewer/template.html` y ejecutar `python tools/build_viewer.py --reuse-scene` para actualizar la interfaz sin regenerar la geometría.
3. Regenerar el PDF y la portada con `python tools/build_guide.py` después de instalar `requirements-docs.txt`.
4. Ejecutar `python tools/package_release.py` para actualizar las sumas y comprobar los enlaces y el paquete.

## Revisiones del modelo

La primera edición pública es **1.0.0**. El identificador interno `2.0.0-rc1` corresponde a la geometría conservada del taller. Un cambio editorial no requiere modificar ni volver a exportar los STL.

Para cambios mecánicos, seguir [CONTRIBUTING.md](../CONTRIBUTING.md), regenerar modelos y visor juntos, y registrar las comprobaciones digitales y físicas por separado.
