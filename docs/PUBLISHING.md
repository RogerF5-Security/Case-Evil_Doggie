# Subir el proyecto a Git

El paquete es un repositorio local preparado; no se ha publicado ni enviado a terceros.
`README.md` será la portada de GitHub. Elegir el nombre que se desee para el repositorio;
propuesta: `doggie-house`.

## Antes del primer push

Revisar [la validación física](RELEASE_CHECKLIST.md). Se puede subir esta revisión
para colaboración como `2.0.0-rc1`, indicando las pruebas pendientes. No presentarla
como v2 impresa hasta completar la comprobación. Las fotografías incluidas son v1.

Revisar créditos y licencia MIT propuesta para la carcasa. El texto de presentación
se puede tomar del README. El arte original mantiene su atribución Faraday/Kalpa.

## Terminal

Desde la carpeta del proyecto, con Git instalado y un repositorio remoto vacío
creado en la cuenta elegida:

```sh
git status
# Si se parte del ZIP, inicializar primero: git init -b main
git add .
git commit -m "Add Doggie House v2 release candidate"
# Sustituir por la URL real del repositorio creado por el propietario:
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```

El repositorio local no incorpora email o credenciales inventados. Git usará la
identidad que tenga configurada el propietario. Nunca añadir `.venv`, cachés o G-code.

## Visor público con GitHub Pages

En la configuración del repositorio, Pages, elegir despliegue desde rama `main`,
carpeta `/ (root)`. El archivo `.nojekyll` evita procesamiento de las fuentes.
La página raíz dirige al visor `viewer/index.html`. El HTML ya incluye su geometría
y no necesita servicios externos. No se habilitó Pages automáticamente.

El flujo `.github/workflows/cad.yml` valida CAD en push y pull request y guarda
STL/3MF/visor como artefactos; no publica una web ni envía mensajes a Faraday.

## Entrega a Faraday

Compartir el enlace al repositorio o el ZIP después de revisarlo. Una presentación
breve puede decir:

> De un viaje a la EKO nos trajimos un EvilDoggie que nos regaló el equipo de
> Faraday. De regreso a Guate le hicimos su casita para cuidarlo como se debe.
> Aquí va Doggie House: perro visible, puertos accesibles y cierre sin tornillos.
> Gracias por el regalo y por ayudarnos a compartirlo con la comunidad.

Si se comparte antes de la segunda impresión, adjuntar el estado `rc1` y las pruebas
pendientes. Este borrador no se ha enviado.
