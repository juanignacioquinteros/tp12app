# IA_LOG – Ficha de Transparencia de IA

**Proyecto:** Mascota Virtual "Antonio" – IPET 249 "Nicolás Copérnico"
**Asignatura:** Laboratorio de Aplicaciones II – 6° G – 2026
**Herramienta utilizada:** Claude (Anthropic)

Los prompts están copiados tal cual los escribí, con sus errores de tipeo.

## Interacciones clave

| Herramienta | Objetivo | Prompt exacto | Fundamentación (4 reglas) | Verificación / Pruebas |
|---|---|---|---|---|
| Claude | Generar el programa en Pygame con la mascota (dragón con los colores del colegio), las barras de estado, los botones y los 4 estados visuales | *(Con la consigna del TP adjunta)* "quiero que la mascota sea un dragon de color bordo con detalles amarillos y que use unos audiculares gamers y unos lentes de estrella" | **Claridad:** indiqué el animal, el color y los accesorios concretos. **Contexto:** adjunté el enunciado completo del TP (Pygame, IPET 249, paleta del colegio). **Fundamentación:** no la apliqué, porque no pedí que explicara sus decisiones. **Ejemplos:** no los pedí. | Se ejecutó el dibujo de los 4 estados (feliz, triste, cansado y programando) sin errores y se revisó la imagen generada. Prueba propia: *[completar: ejecuté `python mascota_dragon.py`, probé C, B y P y comprobé que las barras bajan solas]* |
| Claude | Agregar una animación cuando la mascota toma café y saber en qué lugar del código va cada cambio | "necesito una animacion para cuando toma el cafe dame donde le cambio o le agrego asi cuando toma el cafe hay una pequeña animacion" | **Claridad:** dije qué animación quería y que necesitaba saber dónde modificar. **Contexto:** la conversación ya tenía el código del programa. **Fundamentación:** no la apliqué. **Ejemplos:** no los pedí. | Se renderizó un cuadro de la animación y se revisó la imagen (taza en la boca, vapor y "¡Glup!"). Se comprobó que `C` activa el temporizador `t_cafe` y que el estado pasa a "feliz". Prueba propia: *[completar: presioné C varias veces y verifiqué que la animación dura 1,5 s y no se traba]* |
| Claude | Entender los 5 conceptos técnicos del proyecto: dibujar, animar, barras de estado, botones interactivos y escudo | "haz el ia log con las siguientes dudas:"<br>"como dibujar en pygame"<br>"como animarlo"<br>"como hacer las barras de salud, energia y animo"<br>"como hacer los botones interactivos"<br>"y como poner el escudo" | **Claridad:** nombré cinco temas concretos. **Contexto:** la conversación ya tenía el código de Antonio, pero no lo mencioné en el prompt. **Fundamentación:** no la apliqué. **Ejemplos:** no los pedí. | Se comparó cada explicación con las partes correspondientes de `mascota_dragon.py` (`dibujar_dragon`, `Mascota.actualizar`, `dibujar_barra`, `Boton`, `cargar_escudo`). Prueba propia: *[completar: modifiqué un color, el tamaño de una barra y la posición del escudo, y comprobé el cambio al ejecutar]* |

## Otras interacciones (apoyo en la documentación)

| Herramienta | Objetivo | Prompt exacto (inicio) | Verificación |
|---|---|---|---|
| Claude | Redactar el GDD | "ahora con esta informacion y todo lo que sabes del dragon que lo llame antonio quiero que hagas esto" *(seguido del punto 3 de la consigna, pegado textualmente)* | Se compararon los números del GDD (desgaste, valores de cada acción y umbrales de los estados) con los del código. |
| Claude | Redactar el README | "ahora el readme" *(seguido del punto 1 de la consigna, pegado textualmente)* | Se revisó que tuviera el encabezado institucional, el manual de uso y el concepto de la mascota. |

## Reflexión

- **Qué hizo la IA:** generó el código base, la animación del café y los borradores del GDD y del README.
- **Qué hice yo:** *[completar: qué cambié, probé o decidí. Por ejemplo: elegí al dragón y su aspecto, le puse el nombre Antonio, ajusté la velocidad de desgaste, revisé que el código funcione]*
- **Qué aprendí:** *[completar: por ejemplo, cómo funciona el Game Loop con `dt`, cómo se usa un temporizador para una animación, cómo se organizan las clases]*
