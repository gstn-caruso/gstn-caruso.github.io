# gstn-caruso.github.io

Un blog. Cada entrada es una página de lectura y nada más: sin rastreadores, sin
analíticas, ocho líneas de JavaScript y una hoja de estilos.

Leerlo en **[castellano](https://gstn-caruso.github.io/)** o en
**[inglés](https://gstn-caruso.github.io/en/)**.

## Cómo está armado

Jekyll convierte el repositorio en el sitio con cada push a `main`, vía
`.github/workflows/pages.yml`. No hay nada que construir a mano ni un Gemfile
que mantener al día: el workflow usa `actions/jekyll-build-pages`, que trae su
propio Jekyll.

```
index.md               el índice, en castellano  →  /
en/index.md            el índice, en inglés      →  /en/
feed.xml, en/feed.xml  un feed Atom por idioma

_data/entries.yml      todas las entradas, en los dos idiomas
_data/strings.yml      el mobiliario: navegación, colofón, salto al contenido

_layouts/house.html    el <head>, el salto al contenido, el colofón, el script de idioma
_layouts/index.html    la lista de entradas
_layouts/article.html  una entrada escrita acá
_layouts/dpbs.html     el espejo de Ingalls, que trae su propia hoja de estilos
_layouts/feed.xml      los dos feeds
_includes/lang-nav.html

design-principles-behind-smalltalk/
                       el espejo mismo  →  /design-principles-behind-smalltalk/

assets/css/house.css   todo el diseño
assets/fonts/          Charis, subseteada
tools/                 de dónde sale assets/fonts/, y qué la custodia
```

Este es un *sitio de usuario*, así que se sirve desde la raíz y no tiene
`baseurl`. Las páginas de proyecto de la misma cuenta conservan el suyo, y nada
de esto las toca.

El castellano vive en la raíz y el inglés es la traducción. Por eso
`hreflang="x-default"` —la página que un buscador le ofrece a un lector cuyo
idioma no puede adivinar— nombra siempre la URL castellana.

## El diseño

La primera entrada es un espejo de *Design Principles Behind Smalltalk*, cuya
Figura 1 dibuja dos seres unidos por dos arcos. El arco sólido es *comunicación
explícita*: las palabras efectivamente dichas. El arco punteado es *comunicación
implícita*: el contexto compartido que hace que esas palabras signifiquen algo.

La página de ese artículo convirtió la figura en su sistema de reglas. Este
sitio lo hereda, y las reglas cargan información en lugar de decorar:

| regla | qué marca |
|---|---|
| sólida | la cosa misma: el nombre del sitio, una entrada, un título |
| punteada | el contexto alrededor: fechas, copetes, epígrafes, el colofón |

### La tipografía

Una sola familia para leer: **Charis**, la descendiente libre de la Charter que
Matthew Carter cortó en 1987 para impresoras de 300 ppp — la salida gruesa sobre
la que Smalltalk se leyó por primera vez.

La monoespaciada significa una cosa y una sola: *esto es código*. Nunca una
etiqueta, nunca un epígrafe. Rouge marca los tokens dentro de un bloque de
código y nada los colorea, porque la monoespaciada ya dijo lo que había que
decir.

La medida es de 66 caracteres, que Bringhurst llama ideal para una columna
única. Conviene notar que `1ch` es el ancho del `0`, y en Charis eso es
`0.563em` —más ancho que la letra minúscula promedio—, así que `66ch`
compondría unos 75 caracteres. El CSS dice `55ch`. Ese número se midió en un
navegador; no se adivinó.

La prosa se compone en bandera. Los navegadores no tienen el algoritmo de corte
de línea de Knuth-Plass, así que justificar solo abriría ríos de blanco. La
partición de palabras se enciende por debajo de `32rem`, donde la medida se
vuelve tan corta que la bandera quedaría fea.

### El año cuelga en el margen

No es un número de orden. Una numeración corrida renumeraría cada entrada de
abajo apenas se publique la próxima, y un número que cambia es un número que
miente. El año en que una entrada se escribió no se mueve nunca. Se imprime solo
cuando difiere del de la entrada de arriba, como lo imprime un archivo.

## Las fuentes, y lo que las custodia

`tools/subset-fonts.sh` construye `assets/fonts/` a partir de una release de
Charis. Los binarios están commiteados; el script es la razón por la que se los
puede verificar en lugar de creerles.

Dos cosas que hace bien y que es fácil hacer mal:

- **Las versalitas se pliegan en las dos direcciones.** `smcp` convierte las
  minúsculas en versalitas; `c2sc` convierte las mayúsculas en versalitas.
  `font-variant-caps: all-small-caps` pide las dos. Subsetear con solo `smcp` y
  cada mayúscula de un antetítulo queda a altura completa, sobresaliendo entre
  las versalitas que la rodean: legible, silencioso, mal.
- **Las ligaduras de f sobreviven.** `font-variant-ligatures: common-ligatures`
  necesita que los glifos `f_i` y `f_l` sigan en la fuente, no que la
  característica `liga` siga meramente listada.

El script verifica ambas, y verifica el kerning, leyendo los *lookups* en lugar
de los nombres de glifo: `pyftsubset` escribe una tabla `post` de formato 3.0,
así que la ligadura fi sale del otro lado llamándose `glyph00196`.

Charis no tiene `tnum`. No lo necesita: sus cifras lineales ya son tabulares,
todas de 1153/2048 de eme. `font-variant-numeric: tabular-nums` en la hoja de
estilos es entonces inocuo acá, y estructural para el respaldo Georgia, cuyas
cifras son antiguas y proporcionales.

`tools/charset.txt` fija lo que las fuentes cargan: ASCII, Latin-1 y la
puntuación que la prosa quiere — 210 caracteres. Un blog no puede subsetear al
texto exacto que tiene, como sí puede un artículo terminado, porque la próxima
entrada trae caracteres que la anterior nunca necesitó. Y un carácter que la
fuente no tiene no se anuncia: el navegador compone esa palabra en una serif del
sistema, a mitad de la oración, y el lector ve una costura que no sabe nombrar.

Por eso `tools/check-charset.py` lee cada página construida y falla si encuentra
uno. El workflow lo corre antes de desplegar.

```sh
python3 tools/check-charset.py _site
```

## Los colores, y lo que los custodia

Un gris que se lee bien en la notebook donde se lo eligió es un gris que
desaparece en un teléfono al sol. WCAG le pone un número, así que el número se
verifica en vez de confiarse.

`tools/check-contrast.py` lee los tokens de color de las dos hojas de estilos,
calcula la luminancia relativa según WCAG y falla si algún par debe más
contraste del que paga. No necesita build ni dependencias: solo las fuentes y la
biblioteca estándar.

```sh
python3 tools/check-contrast.py
```

El texto responde a 4,5:1 y los objetos gráficos a 3:1. Las reglas del sistema
sólido/punteado responden al segundo umbral, y no al de la decoración, porque
cargan información: un lector con baja visión que no puede distinguir la sólida
de la punteada perdió justamente lo que ellas dicen.

El enlace de idioma va subrayado siempre. `EN` y `ES` están a 1,02:1 —la misma
luminosidad, distinto matiz—, así que el color era lo único que separaba el
enlace de la palabra vecina, y el color es lo único que un lector daltónico, o
una pantalla al sol, no entrega. Ningún azul mejor existe a esa claridad.

El script verifica además algo que el ojo no puede: que la paleta de la casa y
la paleta inlineada del artículo sean los mismos ocho colores. Están copiadas,
no compartidas, y nada más notaría que se separan.

## Agregar una entrada

Una entrada es una página de lectura. Algunas se escriben acá; otras viven en un
repositorio propio. Al índice no le importa cuál: solo cambia la URL.

**Una que vive en otra parte:** agregarla a `_data/entries.yml` con
`away: true`. Nada más. El índice la dibuja con una flecha, y el feed apunta a
la dirección donde efectivamente responde.

**Una escrita acá:** ponerla en `<slug>/index.md` con `layout: article` y
`permalink: /<slug>/`, y nombrarla también en `_data/entries.yml`. Su front
matter lleva `lang`, `title`, `eyebrow`, `description` y `translation`.

Cada entrada de `_data/entries.yml` necesita un bloque `es:` y uno `en:` —
título, antetítulo, copete, url. Usar tipografía real adentro: son YAML, no
markdown, así que kramdown nunca tiene ocasión de convertir `'` en `’` por uno.

## Agregar un idioma

Agregar su bloque a `_data/strings.yml`, agregar un bloque por entrada en
`_data/entries.yml`, copiar `index.md` y `feed.xml` dentro de `<lang>/`, y
apuntar el `translation` de cada página a su contraparte.

Después, verificar que los caracteres del idioma nuevo estén en
`tools/charset.txt`. Cualquier cosa fuera de Latin-1 va a exigir agrandarlo, y
reconstruir las fuentes.

## Construir en local

```sh
gem install jekyll kramdown-parser-gfm
jekyll serve
```

El Jekyll local es 4.x; el del workflow es el que fija la gema `github-pages`.
El sitio no usa plugins, así que coinciden.

## Créditos

La tipografía es [Charis](https://software.sil.org/charis/), de SIL Global, bajo
la SIL Open Font License 1.1. La licencia viaja con las fuentes, en
`assets/fonts/OFL.txt`.

El sistema de reglas está tomado de *Design Principles Behind Smalltalk*, de
Daniel H. H. Ingalls, y de la figura que Dwight Hughes recreó para él.
