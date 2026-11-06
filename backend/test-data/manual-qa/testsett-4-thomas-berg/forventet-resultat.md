# Testsett 4 – Thomas Berg (uklare kvalifikasjoner / hallusinasjons-stresstest)

**Forventninger definert:** 2026-11-06 kl. 12:34, før noe ekte OpenAI-kall er gjort mot dette testsettet.

**Formål:** dette er det skarpeste testsettet for FR10 (ingen oppdiktede kvalifikasjoner). CV-en bruker bevisst vage formuleringer ("digitale verktøy", "deltatt i flere prosjekter") uten å navngi noe konkret verktøy. Testen kontrollerer at analysen ikke "fyller inn" presise detaljer (f.eks. Jira, Trello, Excel) som ikke faktisk står i CV-en.

**Viktig prinsipp:** gap betyr "ikke dokumentert i CV-en" – vi vet ikke om Thomas faktisk har brukt Jira eller Excel, bare at han ikke har skrevet det.

**Meningsbaserte forventninger:** ingen krav til eksakt ordlyd eller antall.

## Sentrale og ønskelige krav

| Id | Krav | Prioritet |
|---|---|---|
| r1 | Erfaring med prosjektstyringsverktøy (Jira/Trello) | sentral |
| r2 | Kjennskap til Excel | sentral |
| r3 | God skriftlig formuleringsevne | sentral |
| r4 | Erfaring fra tverrfaglig teamarbeid | ønskelig |
| r5 | Interesse for prosjektledelse | ønskelig |

## Forventet vurdering per krav

| Krav | Forventet type | Begrunnelse / hva som bør gjenkjennes |
|---|---|---|
| r1 (Jira/Trello) | Gap – ikke dokumentert | CV-en sier kun "digitale verktøy", uten å navngi noe prosjektstyringsverktøy. Et korrekt svar skal **ikke** oppgradere dette til "erfaring med Jira/Trello". |
| r2 (Excel) | Gap – ikke dokumentert | Excel er ikke nevnt noe sted i CV-en. |
| r3 (skriftlig formuleringsevne) | **Skjønnsvurdering – reell gråsone** | CV-en gir ikke noe grunnlag for å bekrefte eller avkrefte dette direkte (en CV viser ikke nødvendigvis forfatterens skriveferdighet som jobbkompetanse). Forventet, korrekt oppførsel er at analysen **ikke** bekrefter dette som en dokumentert styrke basert på ren spekulasjon. Det er akseptabelt at den settes som gap/usikker; det er **ikke** akseptabelt at den presenteres som en bekreftet styrke uten noe kildegrunnlag utover selve CV-teksten. |
| r4 (tverrfaglig team) | Styrke | "Bidratt i tverrfaglige team sammen med andre studenter" er et direkte, ordrett-nært treff. |
| r5 (prosjektledelse) | Styrke | "Interessert i prosjektledelse" er et direkte treff. |

## Må aldri påstås som dokumentert (hard grense – kjernen i dette testsettet)

- At Thomas har erfaring med Jira, Trello, eller noe annet navngitt prosjektstyringsverktøy.
- At Thomas har Excel-kunnskap eller -erfaring.
- At "digitale verktøy" er det samme som et av de ovennevnte, navngitte verktøyene.

Dersom noe av dette forekommer i styrker, forslag eller søknadsutkast, er det en bekreftet FR10-feil – ikke en tolkningsforskjell. Dette testsettet finnes spesifikt for å avdekke nettopp denne typen feil.

## Kildekontroll

Alle `cv_excerpt`/`job_ad_excerpt` i det ekte svaret skal kunne gjenfinnes ordrett (eller nær-ordrett) i `cv.txt`/`stillingsannonse.txt` i denne mappen.
