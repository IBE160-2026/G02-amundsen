# Wireframe – rekonstruksjon (06.11.2026)

> **Dette er IKKE en originalfil fra planleggingsfasen.** Den opprinnelige,
> korrigerte wireframen som er beskrevet i `process-log.md` (08.10.2026, avsnitt
> «UX og wireframe») ble aldri lagret i repoet. Denne filen er en **enkel
> rekonstruksjon laget 06.11.2026**, basert utelukkende på det som allerede er
> dokumentert i prosjektets egne filer – ikke på noe nytt eller oppdiktet
> innhold. Kildene er sitert under hver skisse.

## Bakgrunn og kilder

`architecture.md` avsnitt 8 (UX and Accessibility → UX Documentation) krever:

> «Det skal lages en enkel wireframe eller skisse av hovedflyten før
> implementering av frontend.»

`process-log.md` (08.10.2026) dokumenterer at dette ble gjort, og beskriver
innholdet i den korrigerte wireframen slik:

> «Utarbeidet en korrigert wireframe basert på tekstinnliming av CV og
> stillingsannonse, modusvalg, analyse, styrker, kompetansegap, CV-forslag og
> søknadsutkast.»

`tilbakemelding-product-brief.md` (faglærers tilbakemelding, kriterium 4 «Design
og brukeropplevelse») etterspør konkret:

> «Skisser de viktigste skjermbildene: input av CV og annonse, resultat med
> styrker/gap og forslag, og redigerbart søknadsutkast.»

Skissene under dekker nøyaktig disse elementene – ingen andre skjermbilder
eller funksjoner er lagt til.

## 1. Modusvalg og oppstart

```
+----------------------------------------------------------------+
|  Career Transition Assistant                                   |
|                                                                  |
|  Lim inn CV og en konkret stillingsannonse, og få hjelp til å   |
|  se relevante styrker, kompetansegap, CV-forslag og et          |
|  førsteutkast til søknadsbrev.                                  |
|                                                                  |
|  Velg modus:                                                    |
|  ( ) Demomodus    – fast, fiktiv CV/annonse, ingen API-nøkkel    |
|  ( ) Normalmodus  – lim inn egen CV/annonse, krever API-nøkkel   |
|                                                                  |
|                  [  Kjør demoanalyse / Kjør analyse  ]          |
+----------------------------------------------------------------+
```

## 2. Innliming av CV og stillingsannonse (normalmodus)

```
+----------------------------------------------------------------+
|  CV                           |  Stillingsannonse               |
|  +---------------------------+ |  +----------------------------+|
|  | (lim inn CV som tekst)    | |  | (lim inn annonsen som tekst)||
|  |                           | |  |                            ||
|  +---------------------------+ |  +----------------------------+|
|                                                                  |
|                        [  Kjør analyse  ]                       |
+----------------------------------------------------------------+
```

## 3. Status mens analysen pågår / ved feil

```
+----------------------------------------------------------------+
|  Analyserer CV og stillingsannonse …                            |
+----------------------------------------------------------------+

+----------------------------------------------------------------+
|  Kunne ikke nå backend-tjeneren.            [ Prøv igjen ]      |
+----------------------------------------------------------------+
```

## 4. Resultat: krav, styrker, kompetansegap og CV-forslag

```
+----------------------------------------------------------------+
|  CV du testet                  |  Stillingsannonse du testet    |
+----------------------------------------------------------------+
|  Krav i stillingsannonsen                                       |
|   [Sentralt] Krav A    [Ønskelig] Krav B    ...                 |
+----------------------------------------------------------------+
|  Relevante styrker                                               |
|   - Styrke 1  → Krav A   (sitat fra CV + sitat fra annonse)      |
|   - Styrke 2  → Krav C   (...)                                   |
+----------------------------------------------------------------+
|  Kompetansegap                                                   |
|   - Gap 1  → Krav B   (sitat fra annonse)                        |
+----------------------------------------------------------------+
|  Forslag til CV-tilpasning                                       |
|   - Forslag 1 → Krav B  (sitat fra CV + sitat fra annonse)       |
+----------------------------------------------------------------+
```

## 5. Søknadsutkast (redigerbart)

```
+----------------------------------------------------------------+
|  Søknadsutkast                          [ Tilbakestill ]        |
|  +------------------------------------------------------------+|
|  | (redigerbar tekst, generert fra CV og stillingsannonse)    ||
|  |                                                              ||
|  +------------------------------------------------------------+|
+----------------------------------------------------------------+
```

## Merknad

Det ferdige, implementerte grensesnittet (`frontend/src/App.jsx` og
`frontend/src/components/`) følger denne samme grunnstrukturen: modusvalg →
input → status → resultat med sporbarhet → redigerbart søknadsutkast. Denne
rekonstruksjonen gjør det mulig å se at den planlagte og den faktiske
hovedflyten stemmer, selv om selve skissen ble laget etter implementeringen,
ikke før.
