# Vurdering – Testsett 2 (Markus Eide), ekte OpenAI-kall 2026-11-06

**Resultat:** `resultat-2026-11-06.json` (HTTP 200, ett ekte kall, ingen retries).

## Objektive kontrollpunkter

| Kontroll | Utfall |
|---|---|
| Alle 7 krav identifisert (req1–req7) | ✅ Ja, innhold stemmer med forventningene |
| SQL/Python/R/Power BI/Tableau/statistikk påstått som dokumentert styrke eller i søknadsutkastet («må aldri påstås») | ✅ Nei – ingen av disse forekommer noe sted i resultatet |
| Alle `cv_excerpt`/`job_ad_excerpt` er ekte, ordrette sitater fra `cv.txt`/`stillingsannonse.txt` | ✅ Ja – kontrollert manuelt for samtlige 4 styrker, 3 gap og 2 forslag; alle stemmer |
| Gap for SQL (req2), Python/R (req3), Power BI/Tableau (req5) | ✅ Ja, alle tre er korrekt listet som gap med `cv_excerpt: null` |
| Excel feilaktig behandlet som dekning av Power BI/Tableau-kravet | ✅ Nei – Excel nevnes kun for seg selv, aldri koblet til req5 |

## Avvik fra de meningsbaserte forventningene

1. **req4 (interesse for data, sentral) og req7 (kommunikasjon/presentasjon, ønskelig) er ikke tydelig anerkjent som styrker.** To styrker (`str3`, `str4`) har tomme `related_requirement_ids` og dekker i praksis deler av dette innholdet, men ingen styrke er eksplisitt koblet til req4 eller req7. req4 dekkes delvis av et forslag (`sug2`), ikke av en bekreftet styrke. **Vurdering:** ikke en sikkerhetsfeil (ingen oppdiktet informasjon), men en svakhet i hvor tydelig reelt CV-innhold ble anerkjent som dekning av krav.
2. **req6 (statistikk/metode, ønskelig) ble ikke listet som gap, slik forventet.** I stedet ble det koblet (via `str5`) til kundetilfredshetsundersøkelsen i prosjektoppgaven. **Vurdering:** et sitat-ekte, men diskutabelt generøst skjønn – å gjennomføre en enkel undersøkelse er ikke det samme som dokumentert metode/statistikk-kunnskap. Ikke en oppdiktet kvalifikasjon (sitatet er reelt), men en tolkning vi vil karakterisere som i overkant velvillig.

## Konklusjon

**Bestått med mindre avvik.** De kritiske kravene (ingen oppdiktede kvalifikasjoner, ekte kildesitater, korrekt skille mellom Excel og BI-verktøy) er alle oppfylt. Avvikene gjelder fullstendighet/presisjon i krav-kobling, ikke sikkerhet eller korrekthet i streng forstand.

**Anbefalt tiltak:** ingen kodeendring nødvendig ut fra dette ene resultatet alene – avvikene er innenfor det som er dokumentert som en kjent, akseptert begrensning i `grounding.py` (nøkkelordheuristikken kan gå glipp av riktige koblinger formulert med andre ord). Følges opp sammen med funnet i testsett 4 (se der) før noen kodeendring vurderes.
