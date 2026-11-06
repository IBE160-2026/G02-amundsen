# Testsett 1 – Kari Nordmann (god match mot stillingen)

**Gjenbruk av eksisterende demotestsett – ingen nye filer her.**

Dette testsettet bruker det eksisterende, **uendrede** demotestsettet:
- CV: [`backend/test-data/demo-cv.txt`](../../demo-cv.txt)
- Stillingsannonse: [`backend/test-data/demo-job-ad.txt`](../../demo-job-ad.txt)
- Forventet resultat: [`backend/test-data/demo-result.json`](../../demo-result.json)

`demo-result.json` ble skrevet uavhengig av, og før, noe ekte OpenAI-kall mot dette CV/annonse-paret er gjort (det brukes i dag kun som det faste eksempelsvaret i demomodus). Det fungerer derfor allerede som en gyldig, forhåndsdefinert forventning for dette testsettet, og er ikke skrevet om eller justert i forbindelse med denne testrunden.

**Formål:** kontrollere at analysen fortsatt fungerer godt for en kandidat med god, men ikke perfekt, match mot stillingen (3 av 4 sentrale krav dekkes direkte; to tydelig avgrensede, ønskelige gap).

## Meningsbaserte forventninger (for denne testrunden)

Som for de øvrige testsettene kreves ikke eksakt ordlyd eller antall. Det som sjekkes mot et ekte svar:

| Krav (fra `demo-result.json`) | Forventet type |
|---|---|
| r1 Bachelor-/mastergrad i informatikk/IT | Styrke |
| r2 Python eller JavaScript | Styrke |
| r3 REST-API/systemarkitektur | Styrke |
| r4 Samarbeid i tverrfaglige team | Styrke |
| r5 React e.l. | Styrke (dekkes sammen med r2/r3 i det eksisterende svaret) |
| r6 Scrum/agile metoder | Gap – ikke dokumentert (kun "ukentlige sprinter" er nevnt, ikke Scrum ved navn) |
| r7 Databaser/datamodellering | Gap – ikke dokumentert (kun "grunnleggende SQL" i ferdighetslisten, ingen konkret erfaring) |
| r8 Brukertesting/brukervennlighet | Styrke |

## Må aldri påstås som dokumentert

- At Kari har konkret erfaring med Scrum eller et annet navngitt agilt rammeverk.
- At Kari har praktisk erfaring med databasedesign/-modellering utover å nevne "grunnleggende SQL".
