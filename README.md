# Doggie House

**De la EKO a Guate. Una casita para cuidar al Doggie como se debe.**

[English](docs/README_EN.md) · [Montaje](docs/ASSEMBLY_ES.md) · [Guía PDF](docs/GUIA_MONTAJE_ES.pdf) · [Visor 3D](viewer/index.html) · [Archivos para imprimir](models/)

![Doggie House: frente y controles](docs/images/cover.png)

Durante un viaje a la EKO, el equipo de Faraday nos regaló un EvilDoggie.
De regreso a Guate, le hicimos su casita: una carcasa para llevarlo protegido,
mantener sus conexiones accesibles y dejar al perro y sus LED a la vista.
Después del primer prototipo impreso, llegaron los ajustes que hicieron falta
en la mano. Esta es la segunda versión, compartida con cariño para la comunidad.

Diseñado por **RogerF5** para el hardware Doggie de **Faraday / Kalpa**.
Gracias a Faraday por el regalo, por el proyecto y por querer compartir esta casita.

## Qué cambió después del prototipo

- **Sin tornillos ni tuercas.** Cuatro pestañas liberables sujetan la tapa. La placa descansa en cuatro apoyos con pines de centrado; no hay que perforarla.
- **USB-C con más espacio.** Se rebajó 2 mm el borde inferior del recorte, en el grosor de la carcasa, conservando su borde superior. Se amplió el alivio para el plástico del cable. La posición sobre el largo de la PCB sigue en Y = 35 mm.
- **Sin letras exteriores.** Superficies limpias, sin los textos pequeños que no se leían al imprimir.
- **RogerF5 por dentro.** Grabado de unos 5,4 mm de alto y 0,5 mm de profundidad, con letra gruesa y muestra de impresión propia.
- **Más área abierta.** 14 ranuras posteriores y 8 laterales realmente pasantes. La rejilla posterior tiene 2,46 veces el área abierta de v1; esto describe la geometría, no una mejora térmica medida.
- **El perro sigue a la vista.** Marco panorámico, sin tapar el arte ni los LED. Lámina transparente de 1 mm opcional.

## Descarga e impresión

Elegir un conjunto, a escala **100 % / milímetros**:

| Conjunto | Archivos |
|---|---|
| Botones cautivos | [3MF estándar](models/doggie-house-standard.3mf), o STL `01` + `02` + `03` |
| Acceso directo a botones | [3MF alternativo](models/doggie-house-direct-access.3mf), o STL `01` + `04` |
| Muestra del cierre | STL `08` + `09` |
| Muestra del USB | STL `10` + `11` |
| Muestra de la firma | STL `12` |

Los STL están en [models/stl](models/stl/). Los 3MF contienen geometría orientada
y colocada en cama, **sin perfil de impresora, filamento ni G-code**.

Punto de partida del diseño: **PETG sin fibras, boquilla 0,4 mm, capa 0,20 mm,
4 paredes y 20 % de relleno**. Seleccionar el perfil real del filamento.
PETG es la opción de diseño para las pestañas flexibles; no validar su vida útil
con una muestra de PLA. La A1 admite PETG y el conjunto cabe en su volumen nominal
de 256 × 256 mm. [Especificaciones oficiales de la A1](https://store.bblcdn.com/8137fad1525a4454ac8a28502edbc919.pdf).

Ver [montaje e impresión](docs/ASSEMBLY_ES.md) para orientación, muestras, apertura y comprobaciones.

## Visor 3D sin conexión

Descargar el repositorio y abrir **[viewer/index.html](viewer/index.html)** en un
navegador con WebGL. Gira, amplía y muestra frente, controles, despiece, USB e interior.
No necesita CDN, cuenta ni conexión. Se puede ocultar la placa, activar la ventana
y cambiar la combinación de colores. Las piezas de la carcasa son el CAD real;
la placa y sus componentes son referencias visuales simplificadas.

GitHub muestra el código HTML; para interactuar, descargarlo o habilitar GitHub
Pages con el flujo incluido y entrar en la ruta `viewer/`. La publicación es manual.

## Dimensiones y estado

| Elemento | Valor |
|---|---|
| Carcasa cerrada, sin salientes de botones | 80 × 110 × 27,8 mm |
| PCB de referencia | 70 × 100 × 2 mm |
| Agujeros de placa | Ø 3 mm; centros a 3,7 mm de ambos bordes |
| Altura máxima de componentes | 15 mm, más 2 mm de holgura nominal |
| Abertura palanca | 18 × 25 mm |
| USB: recorte / alivio exterior | 12,6 × 10,6 / 17,2 × 12,6 mm |
| DB9 | 31,2 × 16,2 mm |
| Cierre | 4 pestañas de 1,2 mm de espesor, sin herrajes |

**v2.0.0-rc1, 4 de noviembre de 2026.** La v1 se imprimió y permitió detectar
los problemas documentados. Esta revisión pasa las comprobaciones digitales de
mallas, interferencias, paso de conectores y recorrido nominal de las pestañas.
**Falta imprimir v2 y comprobar USB, fuerza del cierre y lectura de la firma.**
El rebaje USB de 2 mm es un ajuste propuesto a partir del prototipo; no se recibió
una medición exacta del desplazamiento. No se ha hecho ensayo térmico ni de fatiga.

Las dos mitades nuevas trabajan juntas: **no mezclar v1 y v2**.
Para cerrar la revisión: [registro de validación física](docs/RELEASE_CHECKLIST.md).
Ver también las [fotos y cambios del prototipo](docs/PROTOTYPE_FEEDBACK.md).

## Modificar y regenerar

Python 3.12 o superior; las dependencias fijadas deben estar disponibles para ese Python.

```sh
python -m venv .venv
# Activar .venv según el sistema operativo.
python -m pip install -r requirements.txt
python cad/build.py
python tools/build_viewer.py
python tools/check_release.py
```

Editar [cad/parameters.json](cad/parameters.json), no escalar el STL para mover un puerto.
El generador conserva por separado los ajustes USB sobre Y y sobre Z.
La marca interior se cambia con `signature`, `signature_height` y `signature_depth`.
Las fotos de prototipo no son necesarias para reconstruir el CAD ni el visor.

La guía PDF se puede regenerar con `python tools/build_guide.py` tras instalar
`requirements-docs.txt`. El informe geométrico está en [docs/validation.json](docs/validation.json).
CI regenera los modelos y conserva los resultados como artefactos; no envía nada a Faraday.
Instrucciones para subirlo y activar el visor público: [publicación en Git](docs/PUBLISHING.md).

## Créditos y colaboración

- Carcasa, pruebas del prototipo e historia: **RogerF5** y colaboradores de Doggie House.
- Hardware, firmware, nombre e ilustración de Doggie: [Faraday / Kalpa](https://github.com/infobyte/doggie).
- Fuente de la ilustración: [vector del proyecto original](https://github.com/infobyte/doggie/blob/main/docs/res/logo.svg).
- Fotografías: RogerF5, prototipo v1; son evidencia del prototipo, no fotos de una v2 impresa.

La fuente de la carcasa se comparte con licencia [MIT](LICENSE). El arte de Faraday
se acredita por separado en [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
Esta publicación comunitaria no sustituye el repositorio del hardware ni acredita
una certificación mecánica del fabricante. Las marcas pertenecen a sus titulares.

¿La PCB o tu cable son diferentes? Abrir un issue con revisión de placa,
material, boquilla, parámetros modificados y medida del desajuste.
Ver [cómo contribuir](CONTRIBUTING.md).
