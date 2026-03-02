---
layout: page
permalink: /ambientacion/cronologia/
title: Cronología de Golarion
chapter: Ambientación
category: ambientacion
nav_order: 10
source: Guía de los Presagios Perdidos
---

<style>
.cronologia-intro {
  font-style: italic;
  color: var(--text-muted, #666);
  border-left: 3px solid var(--accent, #c0392b);
  padding-left: 1rem;
  margin-bottom: 2rem;
}

.era {
  margin: 2.5rem 0;
}

.era-titulo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid;
}

.era-oscuridad .era-titulo   { border-color: #2c2c2c; color: #2c2c2c; }
.era-angustia  .era-titulo   { border-color: #5d4037; color: #5d4037; }
.era-destino   .era-titulo   { border-color: #4a235a; color: #4a235a; }
.era-entronizacion .era-titulo { border-color: #1a5276; color: #1a5276; }
.era-presagios .era-titulo   { border-color: #922b21; color: #922b21; }

.era-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: bold;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 0.2rem 0.6rem;
  border-radius: 3px;
  white-space: nowrap;
}

.era-oscuridad   .era-badge { background: #2c2c2c; color: #fff; }
.era-angustia    .era-badge { background: #5d4037; color: #fff; }
.era-destino     .era-badge { background: #4a235a; color: #fff; }
.era-entronizacion .era-badge { background: #1a5276; color: #fff; }
.era-presagios   .era-badge { background: #922b21; color: #fff; }

.timeline {
  list-style: none;
  padding: 0;
  margin: 0;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 5.5rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, transparent, #ccc 5%, #ccc 95%, transparent);
}

.timeline li {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.85rem;
  position: relative;
  align-items: flex-start;
}

.timeline li::before {
  content: '';
  position: absolute;
  left: 5.1rem;
  top: 0.45rem;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #aaa;
  border: 2px solid #fff;
  box-shadow: 0 0 0 1px #aaa;
  flex-shrink: 0;
}

.era-oscuridad   .timeline li::before { background: #2c2c2c; box-shadow: 0 0 0 1px #2c2c2c; }
.era-angustia    .timeline li::before { background: #5d4037; box-shadow: 0 0 0 1px #5d4037; }
.era-destino     .timeline li::before { background: #4a235a; box-shadow: 0 0 0 1px #4a235a; }
.era-entronizacion .timeline li::before { background: #1a5276; box-shadow: 0 0 0 1px #1a5276; }
.era-presagios   .timeline li::before { background: #922b21; box-shadow: 0 0 0 1px #922b21; }

.timeline li.destacado::before {
  width: 14px;
  height: 14px;
  left: 4.9rem;
  top: 0.35rem;
}

.fecha {
  width: 4.5rem;
  text-align: right;
  font-size: 0.8rem;
  font-weight: bold;
  font-variant-numeric: tabular-nums;
  color: #888;
  flex-shrink: 0;
  padding-top: 0.15rem;
  line-height: 1.3;
}

.evento {
  flex: 1;
  padding-left: 1.25rem;
  font-size: 0.92rem;
  line-height: 1.5;
}

.evento strong {
  color: #333;
}

.timeline li.destacado .evento {
  font-weight: 500;
}

.timeline li.actual {
  background: #fff8e1;
  border-radius: 4px;
  padding: 0.4rem 0.5rem 0.4rem 0;
  margin-left: -0.5rem;
}

.timeline li.actual .evento {
  font-weight: 600;
}

.era-nota {
  font-size: 0.82rem;
  color: #888;
  font-style: italic;
  margin-top: 0.4rem;
  padding-left: 5.75rem;
}
</style>

<p class="cronologia-intro">Lo que sigue es un resumen incompleto de los acontecimientos principales de la historia de Golarion, centrado en los que afectan a la Región del Mar Interior. Todas las fechas se indican en el <strong>Recuento de Absalom (ra)</strong>, contando hacia delante (o hacia atrás) desde la fundación de dicha ciudad.</p>

---

## Eras anteriores

Antes de los registros verificables existieron tres grandes eras:

| Era | Suceso principal |
|-----|-----------------|
| **Era de la Creación** | Aparece por vez primera la vida mortal |
| **Era de las Serpientes** | Los hombres serpiente fundan el primer gran imperio de Golarion |
| **Era de las Leyendas** | Se alzan los primeros imperios humanos; destaca Azlant |

---

<div class="era era-oscuridad">
<div class="era-titulo">
  <span class="era-badge">Era de la Oscuridad</span>
  <span style="font-size:0.9rem; font-weight:normal;">ca. –5293 ra en adelante</span>
</div>

<ul class="timeline">
  <li class="destacado">
    <span class="fecha">–5293 ra</span>
    <span class="evento">Los <strong>alghollthus</strong> invocan la <strong>Gran Caída</strong>. Los meteoritos forman el Mar Interior, destruyen Azlant y Thassilon, y dan comienzo a mil años de oscuridad. Los elfos abandonan Golarion o se retiran a sus rincones más remotos.</span>
  </li>
  <li>
    <span class="fecha">–4987 ra</span>
    <span class="evento">Los <strong>enanos</strong> completan su <strong>Búsqueda del Cielo</strong>, emergiendo por primera vez a la superficie y empujando a los orcos ante ellos.</span>
  </li>
</ul>
</div>

---

<div class="era era-angustia">
<div class="era-titulo">
  <span class="era-badge">Era de la Angustia</span>
</div>

<ul class="timeline">
  <li>
    <span class="fecha">–4202 ra</span>
    <span class="evento">Los <strong>gnomos</strong> llegan por primera vez al Plano Material, huyendo de una calamidad olvidada en el Primer Mundo.</span>
  </li>
  <li>
    <span class="fecha">–4120 ra</span>
    <span class="evento">El <strong>Imperio Jistka</strong> surge en el norte de Garund: primer imperio humano en el Mar Interior desde la Gran Caída.</span>
  </li>
  <li>
    <span class="fecha">–3923 ra</span>
    <span class="evento">El <strong>Pozo de Gormuz</strong> se abre en Casmaron, liberando las enormes Semillas de Rovagug.</span>
  </li>
  <li class="destacado">
    <span class="fecha">–3502 ra</span>
    <span class="evento">El <strong>Viejo-Mago Jatembe</strong> y sus Diez Guerreros Mágicos devuelven la magia al Mar Interior por primera vez desde la Gran Caída.</span>
  </li>
</ul>
</div>

---

<div class="era era-destino">
<div class="era-titulo">
  <span class="era-badge">Era del Destino</span>
</div>

<ul class="timeline">
  <li>
    <span class="fecha">–3470 ra</span>
    <span class="evento">Se funda el <strong>Antiguo Osirion</strong>.</span>
  </li>
  <li>
    <span class="fecha">–2323 ra</span>
    <span class="evento">Los <strong>aeromantes shory</strong> fundan <strong>Kho</strong>, su primera ciudad voladora.</span>
  </li>
  <li>
    <span class="fecha">–1281 ra</span>
    <span class="evento">Descendientes de Azlant se unen con humanos locales para establecer <strong>Taldor</strong>, primer imperio humano de Avistan desde la Gran Caída.</span>
  </li>
  <li>
    <span class="fecha">–892 ra</span>
    <span class="evento">Las naciones de magos de <strong>Geb</strong> y <strong>Nex</strong> inician una guerra mágica de siglos.</span>
  </li>
  <li class="destacado">
    <span class="fecha">–632 ra</span>
    <span class="evento"><strong>La Tarasca</strong>, la mayor de las Semillas de Rovagug, devasta Avistan antes de ser derrotada y encerrada de nuevo.</span>
  </li>
</ul>
</div>

---

<div class="era era-entronizacion">
<div class="era-titulo">
  <span class="era-badge">Era de la Entronización</span>
  <span style="font-size:0.9rem; font-weight:normal;">1 ra – 4605 ra</span>
</div>

<ul class="timeline">
  <li class="destacado">
    <span class="fecha">1 ra</span>
    <span class="evento"><strong>Aroden</strong>, el último azlante, alza la Piedra Estelar y la isla de Kortos de las profundidades del Mar Interior, convirtiéndose en un dios viviente. Se funda <strong>Absalom</strong>.</span>
  </li>
  <li>
    <span class="fecha">1893 ra</span>
    <span class="evento"><strong>Norgorber</strong> supera la Prueba de la Piedra Estelar y alcanza la divinidad.</span>
  </li>
  <li>
    <span class="fecha">2632 ra</span>
    <span class="evento">Los <strong>elfos</strong> regresan a Golarion desde su refugio en Sovyrian, restableciendo la nación de <strong>Kyonin</strong>.</span>
  </li>
  <li>
    <span class="fecha">2765 ra</span>
    <span class="evento"><strong>Cayden Cailean</strong> sobrevive, borracho, a la Prueba de la Piedra Estelar y asciende a la divinidad.</span>
  </li>
  <li class="destacado">
    <span class="fecha">3203 ra</span>
    <span class="evento">El rey-mago <strong>Tar-Baphon</strong> vuelve como el liche conocido como el <strong>Tirano Susurrante</strong>, unificando hordas de orcos para aterrorizar Avistan.</span>
  </li>
  <li>
    <span class="fecha">3313 ra</span>
    <span class="evento">La <strong>Reina Bruja Baba Yaga</strong> conquista parte de las Tierras de los Reyes de los Linnorm, fundando el reino de <strong>Irrisen</strong>, encapsulado en el invierno eterno.</span>
  </li>
  <li>
    <span class="fecha">3660 ra</span>
    <span class="evento">La <strong>Plaga del Dragón</strong> asola Taldor durante una docena de años.</span>
  </li>
  <li class="destacado">
    <span class="fecha">3754 ra</span>
    <span class="evento">Taldor lanza la <strong>Cruzada Brillante</strong>, guerra de más de setenta años contra el Tirano Susurrante. El liche queda aprisionado en la <strong>Espira del Patíbulo</strong>, pero asesina a la heraldo de Aroden, la diosa guerrera <strong>Arazni</strong>. Se establece la nación de <strong>Última Muralla</strong>.</span>
  </li>
  <li>
    <span class="fecha">3832 ra</span>
    <span class="evento"><strong>Iomedae</strong>, heroína de la Cruzada Brillante, supera la Prueba de la Piedra Estelar y se convierte en la nueva heraldo de Aroden.</span>
  </li>
  <li>
    <span class="fecha">3980 ra</span>
    <span class="evento"><strong>El Desgarro.</strong> El Risco de Droskar entra en erupción, sacudiendo el sur de Avistan.</span>
  </li>
  <li>
    <span class="fecha">4081 ra</span>
    <span class="evento"><strong>Cheliax</strong> se separa de Taldor en la <strong>Conquista Bífida</strong>, llevándose consigo a Andoran, Galt e Isger. Inicia siglos de expansión imperial.</span>
  </li>
  <li>
    <span class="fecha">4307 ra</span>
    <span class="evento">Se funda la <strong>Sociedad Pathfinder</strong> en Absalom.</span>
  </li>
</ul>
</div>

---

<div class="era era-presagios">
<div class="era-titulo">
  <span class="era-badge">Era de los Presagios Perdidos</span>
  <span style="font-size:0.9rem; font-weight:normal;">4606 ra – presente</span>
</div>

<ul class="timeline">
  <li class="destacado">
    <span class="fecha">4606 ra</span>
    <span class="evento"><strong>Aroden muere misteriosamente</strong>. El Imperio de Cheliax queda desprovisto de su mandato divino. Iomedae adopta el legado de Aroden. El <strong>Ojo de Abendego</strong> ahoga las naciones de Lirgen y Yamasa. La <strong>Herida del Mundo</strong> se abre en el norte de Avistan: los demonios destruyen la nación de Sarkoris.</span>
  </li>
  <li>
    <span class="fecha">4622 ra</span>
    <span class="evento">La debilitada Iglesia de Aroden lanza la <strong>Primera Cruzada Mendeviana</strong> para intentar cerrar la Herida del Mundo.</span>
  </li>
  <li>
    <span class="fecha">4640 ra</span>
    <span class="evento">La <strong>Casa Thrune</strong> se alía con el Infierno para tomar el control de Cheliax tras décadas de guerra civil.</span>
  </li>
  <li>
    <span class="fecha">4667 ra</span>
    <span class="evento">Un fervor democrático barre el este de Avistan, promoviendo la interminable <strong>Revolución Roja de Galt</strong> y la <strong>Revuelta Popular de Andoran</strong> (4669 ra).</span>
  </li>
  <li>
    <span class="fecha">4697 ra</span>
    <span class="evento">Las <strong>Guerras de la Sangre Goblin</strong> asolan Isger.</span>
  </li>
  <li>
    <span class="fecha">4709 ra</span>
    <span class="evento">Golarion descubre la existencia de los <strong>drow</strong>, elfos subterráneos malignos.</span>
  </li>
  <li class="destacado">
    <span class="fecha">4713 ra</span>
    <span class="evento">La <strong>Quinta Cruzada Mendeviana</strong> derrota al señor demoníaco <strong>Deskari</strong> y cierra la Herida del Mundo mediante un ritual.</span>
  </li>
  <li>
    <span class="fecha">4714 ra</span>
    <span class="evento">En Numeria, la inteligencia artificial <strong>Casandalee</strong> alcanza la divinidad.</span>
  </li>
  <li>
    <span class="fecha">4715 ra</span>
    <span class="evento">Disturbios civiles en Cheliax conducen a la secesión de <strong>Ravounel</strong>. Un alzamiento similar es aplastado en Isger.</span>
  </li>
  <li>
    <span class="fecha">4717 ra</span>
    <span class="evento"><strong>Absalom</strong> prohíbe la esclavitud, reduciendo drásticamente el comercio de esclavos en el Mar Interior.</span>
  </li>
  <li>
    <span class="fecha">4718 ra</span>
    <span class="evento">Los <strong>Señores de las Runas</strong> regresan tras milenios de ocultamiento, estableciendo la nación de <strong>Nuevo Thassilon</strong> en Varisia.</span>
  </li>
  <li class="actual">
    <span class="fecha">4719 ra</span>
    <span class="evento">⚔ <strong>El año actual.</strong> <strong>Tar-Baphon</strong> se ha liberado recientemente de su prisión, destruyendo Última Muralla y asolando Avistan antes de ser devuelto a la Isla del Terror.</span>
  </li>
</ul>
</div>
