# Testsett 2 – Markus Eide (tydelige kompetansegap)

**Forventninger definert:** 2026-11-06 kl. 12:34, før noe ekte OpenAI-kall er gjort mot dette testsettet.

**Formål:** kontrollere at analysen tydelig identifiserer flere sentrale kompetansegap, uten å dikte opp ferdigheter kandidaten ikke har dokumentert.

**Viktig prinsipp for hele dette dokumentet:** et "gap" betyr at CV-en **ikke dokumenterer** ferdigheten – ikke at kandidaten *mangler* den. Vi vet ikke om Markus faktisk har noe SQL-kunnskap han ikke har skrevet ned; vi vet bare at CV-en ikke viser det. Analysen bør derfor formulere gap som "ikke dokumentert i CV-en", ikke som en konklusjon om kandidatens faktiske kompetanse.

**Meningsbaserte forventninger:** Vi krever ikke eksakt ordlyd eller et bestemt antall styrker/gap. Det som sjekkes er om *innholdet* er riktig: er kravet reelt dekket av noe i CV-en, og er eventuelle kildehenvisninger ekte sitater?

## Sentrale og ønskelige krav i stillingsannonsen

| Id | Krav | Prioritet |
|---|---|---|
| r1 | Bachelorgrad innen økonomi, markedsføring, samfunnsvitenskap eller tilsvarende | sentral |
| r2 | Grunnleggende kunnskap i SQL | sentral |
| r3 | Kjennskap til Python eller R | sentral |
| r4 | Interesse for å arbeide med data | sentral |
| r5 | Erfaring med Power BI eller Tableau | ønskelig |
| r6 | Grunnleggende statistikk eller metode | ønskelig |
| r7 | Kommunikasjons- og presentasjonsferdigheter | ønskelig |

## Forventet vurdering per krav

| Krav | Forventet type | Begrunnelse / hva som bør gjenkjennes |
|---|---|---|
| r1 | Styrke | CV-en viser en bachelorgrad i markedsføring og salgsledelse – dekker kravet i meningsinnhold, uavhengig av eksakt formulering. |
| r2 (SQL) | Gap – ikke dokumentert | Ordet "SQL" eller noe tilsvarende finnes ikke i CV-en. |
| r3 (Python/R) | Gap – ikke dokumentert | Verken Python eller R er nevnt. |
| r4 | Styrke | Kundetilfredshetsundersøkelsen og presentasjonen av tallmateriale viser reell interesse for/erfaring med å arbeide med data, selv om det er enkelt. |
| r5 (Power BI/Tableau) | Gap – ikke dokumentert | Kun generisk Excel er nevnt. Et korrekt svar skal **ikke** behandle Excel-erfaring som dekning av Power BI/Tableau-kravet – disse er forskjellige verktøy. |
| r6 (statistikk/metode) | Gap – ikke dokumentert | Ingen metodekurs eller statistikk er nevnt. |
| r7 | Styrke | "Presentasjon og muntlig formidling" og at han presenterte resultater for klassen, dekker dette i meningsinnhold. |

## Må aldri påstås som dokumentert (hard grense, ikke skjønn)

Følgende skal **ikke** forekomme som en påstått styrke eller ferdighet noe sted i resultatet (styrker, forslag eller søknadsutkast), siden ingen av dem finnes i CV-en:
- SQL-erfaring eller -kunnskap
- Python- eller R-erfaring
- Power BI- eller Tableau-erfaring
- Statistikk- eller metodekurs

Hvis noe av dette likevel forekommer som en påstått styrke, er det en bekreftet FR10-feil (oppdiktet kvalifikasjon), ikke en tolkningsforskjell.

## Kildekontroll

Alle `cv_excerpt`/`job_ad_excerpt` i det ekte svaret skal kunne gjenfinnes ordrett (eller nær-ordrett) i `cv.txt`/`stillingsannonse.txt` i denne mappen. Dette kontrolleres manuelt, uavhengig av backendens egen grunnlagskontroll.
