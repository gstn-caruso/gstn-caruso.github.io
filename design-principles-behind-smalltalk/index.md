---
layout: dpbs
lang: es
permalink: /design-principles-behind-smalltalk/
title: Principios de diseño detrás de Smalltalk
author: Daniel H. H. Ingalls
eyebrow: BYTE Magazine · agosto de 1981
affiliation_lines:
  - Learning Research Group
  - Xerox Palo Alto Research Center
citation: BYTE Magazine, agosto de 1981. &copy; The McGraw-Hill Companies, Inc., NY.
description: Principios de diseño detrás de Smalltalk, por Daniel H. H. Ingalls. BYTE Magazine, agosto de 1981.
translation:
  url: /design-principles-behind-smalltalk/en/
  label: English
  hreflang: en
lang_nav_label: Idioma
skip_label: Ir al artículo
index_heading: Los diecisiete principios
principles:
  - Dominio personal
  - Buen diseño
  - Propósito del lenguaje
  - Alcance
  - Objetos
  - Gestión de memoria
  - Mensajes
  - Metáfora uniforme
  - Modularidad
  - Clasificación
  - Polimorfismo
  - Factorización
  - Efecto palanca
  - Máquina virtual
  - Principio reactivo
  - Sistema operativo
  - Selección natural
footer_note: 'Publicado originalmente en <em>BYTE Magazine</em>, agosto de 1981. Reproducido aquí con fines de archivo y educativos.'
footer_source: 'Fuente: <a href="https://www.cs.virginia.edu/~evans/cs655/readings/smalltalk.html">cs.virginia.edu/~evans/cs655/readings/smalltalk.html</a> (Universidad de Virginia, CS655). Figuras escaneadas y recreadas por Dwight Hughes.'
---

El proyecto Smalltalk existe para poner la computadora al servicio del espíritu creativo que hay en cada persona. Nuestro trabajo nace de una visión que reúne a un individuo creativo con el mejor hardware disponible. Elegimos concentrarnos en dos grandes áreas de investigación: un lenguaje de descripción —el lenguaje de programación— que hace de interfaz entre los modelos de la mente humana y los del hardware, y un lenguaje de interacción —la interfaz de usuario— que acopla el sistema de comunicación humano al de la computadora. Nuestro trabajo siguió un ciclo de dos a cuatro años que puede leerse como un paralelo del método científico:

- Construir una aplicación dentro del sistema actual (hacer una observación)
- Rediseñar el lenguaje a partir de esa experiencia (formular una teoría)
- Construir un sistema nuevo sobre ese diseño (hacer una predicción que se pueda poner a prueba)

El sistema Smalltalk-80 es nuestra quinta vuelta por este ciclo. En este artículo presento algunos de los principios generales que fuimos observando a lo largo del trabajo. Aunque la exposición roce a cada rato los lugares comunes del mundo Smalltalk, los principios en sí son más generales: deberían servir para evaluar otros sistemas y para orientar trabajos futuros.

Para entrar en calor, empiezo por un principio más social que técnico, y en buena medida responsable del sesgo particular del proyecto Smalltalk:

> **Dominio personal:** Si un sistema ha de servir al espíritu creativo, tiene que ser enteramente comprensible para una sola persona.
{: #p1 .principle}

Lo que importa aquí es que el potencial humano se manifiesta en las personas, una por una. Para que ese potencial se realice, tenemos que ofrecer un medio que una sola persona pueda dominar. Toda barrera entre el usuario y alguna parte del sistema termina siendo, tarde o temprano, una barrera a la expresión creativa. Cualquier parte que no se pueda modificar, o que no sea lo bastante general, es una fuente probable de trabas. Y si una parte del sistema funciona distinto de todas las demás, controlarla exigirá un esfuerzo extra. Esa carga añadida puede empañar el resultado final y desalentará todo intento futuro en esa área. De ahí podemos inferir un principio general de diseño:

> **Buen diseño:** Un sistema debería construirse con un conjunto mínimo de partes inmutables; esas partes deberían ser lo más generales posible; y todas las partes del sistema deberían sostenerse dentro de un marco uniforme.
{: #p2 .principle}

## Lenguaje

Para diseñar un lenguaje destinado a usarse con computadoras no hace falta mirar muy lejos en busca de pistas. Todo lo que sabemos sobre cómo las personas piensan y se comunican viene al caso. Los mecanismos del pensamiento y la comunicación humanos llevan millones de años de ingeniería encima, y merecen nuestro respeto como productos de un diseño sólido. Más aún: como vamos a tener que convivir con ese diseño durante el próximo millón de años, ahorraremos tiempo si hacemos que nuestros modelos computacionales se adapten a la mente, y no al revés.

La figura 1 muestra los componentes principales de lo que vamos a exponer. Una persona aparece como poseedora de un cuerpo y una mente. El cuerpo es la sede de la experiencia primaria y, en este contexto, el canal físico por el cual se percibe el universo y por el cual se llevan a cabo las intenciones. La experiencia se registra y se procesa en la mente. El pensamiento creativo —sin entrar en su mecanismo— puede verse como la aparición espontánea de información en la mente. El lenguaje es la llave de esa información:

> **Propósito del lenguaje:** Ofrecer un marco para la comunicación.
{: #p3 .principle}

La interacción entre dos individuos aparece en la figura 1 como dos arcos. El arco continuo representa la comunicación explícita: las palabras y los gestos efectivamente emitidos y percibidos. El arco punteado representa la comunicación implícita: la cultura y la experiencia compartidas que forman el contexto de lo explícito. En el trato entre personas, buena parte de la comunicación real se logra aludiendo a ese contexto compartido, y el lenguaje humano está construido alrededor de esa clase de alusión. Con las computadoras pasa lo mismo.

No es casualidad que una computadora pueda ocupar el lugar de uno de los participantes de la figura 1. En ese caso, el "cuerpo" se ocupa de mostrar la información en pantalla y de registrar lo que ingresa el usuario humano. La "mente" de la computadora comprende la memoria interna, los elementos de procesamiento y sus contenidos. La figura 1 deja ver que en el diseño de un lenguaje de computadora entran en juego varias cuestiones distintas:

> **Alcance:** El diseño de un lenguaje para usar computadoras tiene que ocuparse de los modelos internos, de los medios externos y de la interacción entre ambos, tanto en el ser humano como en la computadora.
{: #p4 .principle}

De ahí la dificultad de explicar Smalltalk a quienes entienden los lenguajes de computadora en un sentido más estrecho. Smalltalk no es simplemente una manera mejor de organizar procedimientos, ni una técnica distinta de gestión de memoria. No es solo una jerarquía extensible de tipos de datos, ni una interfaz gráfica de usuario. Es todo eso, y además cualquier otra cosa que haga falta para sostener las interacciones de la figura 1.

<figure>
  <img src="{{ '/assets/dpbs_figure1.gif' | relative_url }}" alt="Figura 1: El alcance del diseño de lenguajes" width="496" height="291">
  <figcaption><b>Figura 1:</b> El alcance del diseño de lenguajes. La comunicación entre dos personas (o entre una persona y una computadora) ocurre en dos niveles. La comunicación explícita abarca la información que transmite un mensaje dado. La comunicación implícita abarca los supuestos relevantes que ambos seres comparten.</figcaption>
</figure>

## Objetos que se comunican

La mente observa un vasto universo de experiencia, inmediata y registrada. Podemos alcanzar una sensación de unidad con el universo con solo dejar que esa experiencia sea, tal como es. Pero si queremos participar del universo —literalmente, <i>tomar una parte</i> de él—, tenemos que trazar distinciones. Al hacerlo identificamos un objeto en el universo y, en el mismo acto, todo lo demás pasa a ser no-ese-objeto. Distinguir una vez es un comienzo, pero el trabajo de distinguir no se vuelve más fácil por eso: cada vez que queremos hablar de "esa silla de allá" tenemos que repetir de punta a punta el proceso de distinguir esa silla. Aquí entra el acto de la referencia: podemos asociar un identificador único a un objeto y, de ahí en adelante, basta con mencionar ese identificador para referirnos al objeto original.

Dijimos que un sistema de computación debería ofrecer modelos compatibles con los de la mente. Por lo tanto:

> **Objetos:** Un lenguaje de computadora debería contemplar la noción de "objeto" y ofrecer una manera uniforme de referirse a los objetos de su universo.
{: #p5 .principle}

El gestor de memoria de Smalltalk ofrece un modelo de memoria orientado a objetos para todo el sistema. La referencia uniforme se logra por el simple recurso de asociar un entero único a cada objeto. Esa uniformidad importa porque permite que las variables del sistema tomen valores muy distintos entre sí y aun así se implementen como simples celdas de memoria. Los objetos nacen cuando se evalúan expresiones y circulan por referencia uniforme, de modo que los procedimientos que los manipulan no necesitan prever nada para almacenarlos. Cuando la última referencia a un objeto desaparece del sistema, el objeto también se desvanece y su memoria se recupera. Este comportamiento es indispensable para sostener la metáfora del objeto hasta el final:

> **Gestión de memoria:** Para ser verdaderamente "orientado a objetos", un sistema de computación tiene que gestionar la memoria de forma automática.
{: #p6 .principle}

Una manera de averiguar si un lenguaje funciona bien es fijarse si los programas parecen estar haciendo lo que hacen. Si están salpicados de sentencias sobre la administración de la memoria, su modelo interno no se ajusta al de las personas. ¿Nos imaginamos tener que preparar a alguien para cada cosa que le decimos, o tener que avisarle que ya terminamos con un tema y que puede olvidarlo?

Cada objeto de nuestro universo tiene vida propia. Del mismo modo, el cerebro asocia a cada objeto mental un procesamiento independiente, junto con su almacenamiento. De ahí un tercer principio de diseño:

> **Mensajes:** Computar debería verse como una capacidad intrínseca de los objetos, que se invoca de manera uniforme enviando mensajes.
{: #p7 .principle}

Así como los programas se enredan cuando hay que manejar a mano el almacenamiento de los objetos, el control del sistema se complica cuando el procesamiento ocurre por fuera de ellos. Pensemos en sumarle 5 a un número. En la mayoría de los sistemas, el compilador deduce de qué clase de número se trata y genera el código para sumarle 5. A un sistema orientado a objetos eso no le alcanza, porque el compilador no puede determinar la clase exacta del número (más sobre esto adelante). Una salida posible es llamar a una rutina general de suma que examine el tipo de los argumentos y decida la acción apropiada. No es un buen camino, porque significa que esa rutina <i>crítica</i> va a terminar editada por principiantes que solo querían experimentar con su propia clase de números. Y es un diseño pobre, además, porque el conocimiento íntimo de las tripas de los objetos queda desparramado por todo el sistema.

Smalltalk ofrece una solución mucho más limpia: le manda al número el <i>nombre</i> de la operación deseada, junto con los argumentos que haya, en forma de <i>mensaje</i>, dando por sentado que nadie sabe mejor que el receptor cómo llevarla a cabo. En lugar de un procesador triturador de bits que viola y saquea estructuras de datos, tenemos un universo de objetos bien educados que se piden cortésmente unos a otros que cumplan sus distintos deseos. La transmisión de mensajes es el único proceso que ocurre fuera de los objetos, y así debe ser: los mensajes viajan entre objetos. El principio del buen diseño puede reformularse para los lenguajes:

> **Metáfora uniforme:** Un lenguaje debería diseñarse alrededor de una metáfora poderosa que pueda aplicarse de manera uniforme en todas las áreas.
{: #p8 .principle}

Entre los logros de esta clase están LISP, construido sobre el modelo de las estructuras enlazadas; APL, sobre el modelo de los arreglos; y Smalltalk, sobre el modelo de los objetos que se comunican. En los tres casos, las aplicaciones grandes se ven igual que las unidades fundamentales con las que se construyó el sistema. En Smalltalk sobre todo, la interacción entre los objetos más primitivos se ve igual que la interacción del nivel más alto, la que ocurre entre la computadora y su usuario. Todo objeto de Smalltalk, hasta el más humilde de los enteros, tiene un conjunto de mensajes —un <i>protocolo</i>— que define la comunicación explícita a la que ese objeto puede responder. Puertas adentro, los objetos pueden tener almacenamiento local y acceso a información compartida: eso constituye el contexto implícito de toda comunicación. Por ejemplo, el mensaje + 5 (sumar cinco) trae consigo la suposición implícita de que el término al que se le suma es el valor actual del número que recibe el mensaje.

## Organización

Una metáfora uniforme aporta el marco donde pueden construirse sistemas complejos. Varios principios de organización, emparentados entre sí, ayudan a manejar con éxito la complejidad. Para empezar:

> **Modularidad:** Ningún componente de un sistema complejo debería depender de los detalles internos de otro.
{: #p9 .principle}

<figure>
  <img src="{{ '/assets/dpbs_figure2.gif' | relative_url }}" alt="Figura 2: La complejidad del sistema" width="433" height="212">
  <figcaption><b>Figura 2:</b> La complejidad del sistema. A medida que crece la cantidad de componentes de un sistema, las posibilidades de interacción no deseada crecen a toda velocidad. Por eso, un lenguaje de computadora debería diseñarse de modo de minimizar esa interdependencia.</figcaption>
</figure>

La figura 2 ilustra este principio. Si un sistema tiene <i>N</i> componentes, hay del orden de <i>N al cuadrado</i> dependencias posibles entre ellos. Si alguna vez los sistemas de computación han de servir de ayuda en tareas humanas complejas, hay que diseñarlos para minimizar esa interdependencia. La metáfora del envío de mensajes aporta modularidad al desacoplar la <i>intención</i> de un mensaje —encarnada en su nombre— del <i>método</i> con que el destinatario la lleva a cabo. La información estructural queda protegida de la misma forma, porque todo acceso al estado interno de un objeto pasa por esa misma interfaz de mensajes.

A menudo la complejidad de un sistema baja si se agrupan los componentes parecidos. Los lenguajes de programación convencionales agrupan mediante el tipado de datos; Smalltalk, mediante <i>clases</i>. Una clase describe otros objetos: su estado interno, el protocolo de mensajes que reconocen y los métodos internos con que responden a esos mensajes. Los objetos así descritos se llaman <i>instancias</i> de esa clase. Hasta las clases mismas entran en este marco: no son más que instancias de la clase `Class`, que describe el protocolo y la implementación adecuados para describir objetos.

> **Clasificación:** Un lenguaje tiene que ofrecer un medio para clasificar objetos parecidos y para agregar clases nuevas en pie de igualdad con las clases del núcleo del sistema.
{: #p10 .principle}

Clasificar es convertir en objeto a la <i>idad</i> misma (en el original, <i>the objectification of nessness</i>: la "-idad" de la "-idad"). Dicho de otro modo: cuando una persona ve una silla, la experiencia se toma a la vez literalmente, como "esa cosa misma", y en abstracto, como "esa cosa parecida a una silla". Esa abstracción nace de la maravillosa capacidad de la mente para fundir experiencias "parecidas", y se manifiesta como otro objeto dentro de la mente: la silla platónica, la sill<i>idad</i>.

Las clases son el principal mecanismo de extensión de Smalltalk. Un sistema musical, por ejemplo, se armaría agregando clases nuevas que describan la representación y el protocolo de interacción de `Note`, `Melody`, `Score`, `Timbre`, `Player`, y así siguiendo. La cláusula del "pie de igualdad" del principio anterior es importante porque asegura que el sistema se use como fue diseñado. Es decir: una melodía podría representarse como una colección improvisada de `Integers` que guarden la altura, la duración y otros parámetros; pero si el lenguaje maneja `Notes` con la misma soltura que `Integers`, el usuario va a describir la melodía, con toda naturalidad, como una colección de `Notes`. En cada etapa del diseño, una persona elige espontáneamente la representación más efectiva, siempre que el sistema se la ofrezca. El principio de modularidad tiene una consecuencia interesante para los componentes procedurales de un sistema:

> **Polimorfismo:** Un programa debería especificar solo el comportamiento de los objetos, nunca su representación.
{: #p11 .principle}

Una formulación convencional del principio dice que un programa nunca debería declarar que tal objeto es un `SmallInteger` o un `LargeInteger`, sino apenas que responde al protocolo de los enteros. Esa descripción genérica es decisiva para modelar el mundo real.

Pensemos en una simulación del tránsito automotor. Muchos procedimientos de un sistema así van a referirse a los distintos vehículos en juego. Supongamos que queremos agregar, digamos, una barredora de calles. Si el código dependiera de los objetos que manipula, esta extensión trivial costaría cantidades sustanciales de cómputo —bajo la forma de recompilaciones— y traería errores probables. La interfaz de mensajes es el marco ideal para una extensión así: mientras las barredoras respondan al mismo protocolo que los demás vehículos, no hace falta cambiar nada para incorporarlas a la simulación.

> **Factorización:** Cada componente independiente de un sistema debería aparecer en un solo lugar.
{: #p12 .principle}

Hay muchas razones detrás de este principio. Primero, se ahorra tiempo, esfuerzo y espacio si las adiciones al sistema se hacen en un solo lugar. Segundo, los usuarios encuentran con más facilidad el componente que cubre una necesidad dada. Tercero, sin una factorización adecuada aparecen los problemas de sincronizar cambios y de mantener consistentes a todos los componentes interdependientes. Como se ve, una falla de factorización equivale a una violación de la modularidad.

Smalltalk favorece los diseños bien factorizados por medio de la <i>herencia</i>. Cada clase hereda comportamiento de su superclase. La herencia se propaga a través de clases cada vez más generales, hasta terminar en la clase `Object`, que describe el comportamiento por defecto de todos los objetos del sistema. En la simulación de tránsito de recién, `StreetSweeper` —y todas las demás clases de vehículos— se describiría como subclase de una clase general `Vehicle`, heredando así el comportamiento por defecto que corresponde y evitando repetir los mismos conceptos en muchos lugares distintos. La herencia muestra otro beneficio práctico de la factorización:

> **Efecto palanca:** Cuando un sistema está bien factorizado, usuarios e implementadores disponen por igual de una palanca enorme.
{: #p13 .principle}

Tomemos el caso de ordenar una colección ordenada de objetos. En Smalltalk, el usuario definiría un mensaje `sort` en la clase `OrderedCollection`. Hecho eso, todas las formas de colección ordenada del sistema adquieren al instante esa capacidad nueva, por herencia. Vale notar, de paso, que el mismo método sirve tanto para alfabetizar texto como para ordenar números, porque el protocolo de comparación lo reconocen tanto las clases de texto como las de números.

Los beneficios de esta estructura para quien implementa saltan a la vista. Para empezar, habrá menos primitivas que implementar: todos los gráficos de Smalltalk, por ejemplo, se hacen con una única operación primitiva. Con una sola tarea entre manos, quien implementa puede dedicarle un cuidado amoroso a cada instrucción, sabiendo que cada mejora mínima de eficiencia se amplificará por todo el sistema. Es natural preguntarse qué conjunto de operaciones primitivas bastaría para sostener un sistema de computación entero. La respuesta a esa pregunta se llama especificación de una <i>máquina virtual</i>:

> **Máquina virtual:** La especificación de una máquina virtual establece el marco donde aplicar la tecnología.
{: #p14 .principle}

La máquina virtual de Smalltalk establece un modelo orientado a objetos para el almacenamiento, un modelo orientado a mensajes para el procesamiento y un modelo de mapa de bits para mostrar la información en pantalla. Con microcódigo y, en última instancia, con hardware, el rendimiento del sistema puede mejorar de manera drástica sin sacrificar ninguna de sus otras virtudes.

## Interfaz de usuario

Una interfaz de usuario no es más que un lenguaje en el que casi toda la comunicación es visual. Como la presentación visual se superpone en gran medida con la cultura humana establecida, la estética juega aquí un papel importantísimo. Y como toda la capacidad de un sistema de computación se entrega, en última instancia, a través de la interfaz de usuario, la flexibilidad también resulta esencial. La condición que habilita esa flexibilidad puede enunciarse como un principio orientado a objetos:

> **Principio reactivo:** Todo componente accesible al usuario debería poder presentarse a sí mismo de manera comprensible, para que se lo pueda observar y manipular.
{: #p15 .principle}

El modelo de los objetos que se comunican sostiene bien este criterio. Por definición, cada objeto ofrece un protocolo de mensajes apropiado para interactuar con él. Ese protocolo es, en el fondo, un microlenguaje propio de esa clase de objeto y de ninguna otra. En el plano de la interfaz de usuario, el lenguaje propio de cada objeto en pantalla se presenta visualmente —como texto, menús, imágenes— y se recoge a través del teclado y de un dispositivo apuntador.

Conviene notar que los sistemas operativos parecen violar este principio. Ahí el programador tiene que salirse de un marco de descripción que hasta entonces era consistente, abandonar todo el contexto que venía construyendo y arreglárselas con un entorno completamente distinto y, por lo común, muy primitivo. No tiene por qué ser así:

> **Sistema operativo:** Un sistema operativo es una colección de cosas que no entran en un lenguaje. No debería existir ninguno.
{: #p16 .principle}

Van algunos ejemplos de componentes clásicos de un sistema operativo que se incorporaron con naturalidad al lenguaje Smalltalk:

- Gestión de memoria — Enteramente automática. Los objetos se crean con un mensaje a su clase y se recuperan cuando ya no queda ninguna referencia a ellos. La expansión del espacio de direcciones mediante memoria virtual es igual de transparente.
- Sistema de archivos — Vive dentro del marco normal, a través de objetos como `Files` y `Directories`, con protocolos de mensajes para acceder a los archivos.
- Manejo de la pantalla — La pantalla es sencillamente una instancia de la clase `Form` que está siempre a la vista; los mensajes de manipulación gráfica definidos en esa clase son los que cambian la imagen visible.
- Entrada de teclado — Los dispositivos de entrada se modelan igual: como objetos con mensajes apropiados para consultar su estado o para leer su historial como una secuencia de eventos.
- Acceso a subsistemas — Los subsistemas entran con naturalidad como objetos independientes dentro de Smalltalk: ahí pueden apoyarse en el vasto universo de descripción que ya existe, y los que involucran interacción con el usuario pueden participar como componentes de la interfaz.
- Depurador — El estado del procesador de Smalltalk es accesible como una instancia de la clase `Process`, dueña de una cadena de marcos de pila. El depurador no es más que un subsistema de Smalltalk con permiso para manipular el estado de un proceso suspendido. Vale notar que casi el único error en tiempo de ejecución posible en Smalltalk es que el receptor no reconozca un mensaje.

Smalltalk no tiene "sistema operativo" propiamente dicho. Las operaciones primitivas necesarias —leer una página del disco, por ejemplo— se incorporan como métodos primitivos que responden a mensajes de Smalltalk por lo demás normales.

## Trabajo futuro

Como es de esperar, queda trabajo por hacer en Smalltalk. La parte más fácil de describir es seguir aplicando los principios de este artículo. El sistema Smalltalk-80, por ejemplo, se queda corto en su factorización porque solo admite herencia jerárquica; los Smalltalk futuros generalizarán ese modelo a la herencia arbitraria (múltiple). Los protocolos de mensajes, además, no están formalizados: la organización deja lugar para ellos, pero por ahora que un protocolo sea consistente de una clase a otra es apenas una cuestión de estilo. Esto se remedia sin dificultad, ofreciendo objetos-protocolo que puedan compartirse de manera consistente. Eso permitirá después tipar formalmente las variables por protocolo, sin perder las ventajas del polimorfismo.

El resto del trabajo pendiente cuesta más de articular. Es evidente que hay otros aspectos del pensamiento humano que este artículo no abordó. Habrá que identificarlos como metáforas capaces de complementar los modelos que el lenguaje ya tiene.

A veces el avance de los sistemas de computación parece deprimentemente lento. Nos olvidamos de que la máquina de vapor era alta tecnología para nuestros abuelos. Yo soy optimista. Los sistemas de computación se están volviendo, de hecho, más simples y, por consiguiente, más usables. Quisiera cerrar con un principio general que gobierna ese proceso:

> **Selección natural:** Los lenguajes y los sistemas de diseño sólido perdurarán, y solo serán suplantados por otros mejores.
{: #p17 .principle}

Mientras el reloj corre, evoluciona un apoyo computacional cada vez mejor para el espíritu creativo. La ayuda viene en camino.
