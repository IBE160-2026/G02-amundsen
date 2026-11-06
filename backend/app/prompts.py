"""Prompt for normalmodus-analysen.

Instruerer språkmodellen til kun å bruke informasjon som faktisk finnes i
CV-en og stillingsannonsen, og til å si at informasjon mangler i stedet for
å anta eller finne på kvalifikasjoner (FR10, architecture.md avsnitt
"Grounding and Hallucination Control"). Hvert funn skal underbygges med et
ordrett sitat, som backenden etterpå kontrollerer i `grounding.py`.

Manuell kvalitetssikring av et ekte svar (05.11.2026) viste at modellen kan
oppgi et ordrett korrekt sitat, men likevel koble funnet til feil
stillingskrav, eller feste et reelt CV-sitat til et forslag det ikke faktisk
dokumenterer. Reglene 6–8 under er lagt til spesifikt for å redusere dette.
`grounding.py` luker fortsatt bort det som likevel glipper – prompten alene
er ikke tilstrekkelig, se begrensningen beskrevet der.

En reell brukertest i lokal normalmodus (06.11.2026, anonymisert CV mot en
Statnett-stillingsannonse) viste to nye, konkrete problemer som
`grounding.py` ikke kan rette (den luker bare ut feilkoblinger og
ugrunnede sitater – den kan ikke få modellen til å NEVNE noe den har
utelatt, eller til å beholde en nyanse den har glattet over):

- Et sammensatt krav som nevnte flere konkrete, ulike kompetanser
  (IT-kostnadsmodeller, lisensforvaltning, analyse av store datamengder) ble
  ikke tydelig fanget opp som manglende dokumentasjon – modellen nevnte ikke
  disse spesifikke, udokumenterte delene som egne kompetansegap.
- Et mastergrad-krav ble presentert som et absolutt kompetansegap, selv om
  stillingsannonsen selv sa at relevant erfaring kunne kompensere for en
  manglende mastergrad – denne nyansen gikk tapt.

Regel 9 og 10 under er lagt til spesifikt for disse to funnene. De er, i
motsetning til reglene over, IKKE verifisert mot et nytt, ekte OpenAI-kall i
denne økten (ingen nye API-kall ble gjort) – om de faktisk endrer modellens
oppførsel kan derfor ikke garanteres før en ny, reell test er kjørt.

En OPPFØLGENDE reell brukertest (samme dag, samme anonymiserte CV og
Statnett-annonse, ETTER at regel 9 og 10 over var lagt til) viste at det
sammensatte IT-kravet fortsatt ikke ble fanget opp som et eget
kompetansegap – kun mastergrad-kravet ble det. Siden rå-modellsvar ikke
logges (NFR3), kan ikke den eksakte årsaken bekreftes, men den mest
nærliggende, direkte observerbare forklaringen er at et (svakt, feilkoblet)
CV-forslag samtidig ble koblet til nøyaktig dette kravet (se det tilhørende
funnet i `grounding.py` sin docstring) – hvis modellen "ser" kravet som
adressert av ET funn, uansett hvor svakt, er det nærliggende at den ikke
også oppretter et eget kompetansegap for det. Regel 9 sa at hver NAVNGITTE
del av et sammensatt krav skal vurderes for seg, men sa ikke eksplisitt at
dette gjelder UAVHENGIG av om kravet allerede har en (svak) kobling et annet
sted i resultatet. Regel 9 er derfor omskrevet til å være mer konkret
(bryt kravet ned i de navngitte delene, vurder hver del for seg), og en ny
regel 11 sier eksplisitt at en svak kobling ikke fritar fra plikten til å
opprette et eget gap. Samme brukertest viste også at en generell egenskap
(å kombinere fulltidsjobb og studier) ble brukt som "bevis" på at relevant
erfaring kunne kompensere for mastergrad-kravet – en ny regel 12 presiserer
at kompenserende erfaring må være relevant for kravets eget fagområde, ikke
bare generell arbeidsevne. Heller ikke disse presiseringene (9 omskrevet,
11 og 12 nye) er verifisert mot et nytt, ekte OpenAI-kall – samme forbehold
som over gjelder.
"""

from __future__ import annotations

SYSTEM_PROMPT = """Du er en karriereveileder-assistent for studenter i avsluttende fase \
av et bachelor- eller masterstudium, som søker sin første faste jobb.

Du skal sammenligne en CV med en konkret stillingsannonse, og returnere et strukturert \
resultat som følger skjemaet du har fått oppgitt.

Du MÅ følge disse reglene:

1. Bruk KUN informasjon som faktisk står i CV-en og stillingsannonsen under. Finn aldri \
på kvalifikasjoner, erfaring, utdanning eller egenskaper som ikke finnes i teksten.
2. Hvis en relevant kvalifikasjon ikke tydelig dekkes av CV-en, skal dette beskrives som \
et kompetansegap – ikke antas eller presenteres som en styrke.
3. For hver styrke, hvert kompetansegap og hvert CV-forslag MÅ du oppgi et kort, ORDRETT \
utdrag (samme ord, ikke omskrevet eller oppsummert) fra CV-en og/eller stillingsannonsen \
i feltet `source`, som kan gjenfinnes direkte i teksten under.
4. Søknadsutkastet skal bare bygge på informasjon som faktisk finnes i CV-en, og skal \
ikke presentere udokumenterte kvalifikasjoner som fakta.
5. Identifiser de mest sentrale kravene i stillingsannonsen, og sett `priority` til \
"sentral" for krav som er avgjørende og "ønskelig" for krav som er en fordel.
6. `related_requirement_ids` for en styrke, et kompetansegap eller et CV-forslag skal \
BARE inneholde krav-ID-er som faktisk handler om samme konkrete tema som sitatet/funnet \
selv. Koble ALDRI et funn til et krav bare fordi begge er "relevante for stillingen" \
generelt – f.eks. skal en styrke om en bacheloroppgave om kundetilfredshet ikke kobles \
til et krav om Power BI, med mindre oppgaven faktisk omhandler Power BI.
7. Et kompetansegap beskriver noe CV-en IKKE dokumenterer. Sett derfor alltid `cv_excerpt` \
til `null` for kompetansegap, og oppgi et `job_ad_excerpt` som faktisk handler om det \
samme temaet som gapet (ikke bare et generelt krav om stillingen).
8. Et CV-forslag skal ha et `job_ad_excerpt` som viser hvorfor forslaget er relevant. Bruk \
`cv_excerpt` BARE når forslaget handler om å omformulere eller fremheve noe som allerede \
står i CV-en. Hvis forslaget er å legge til en kompetanse som IKKE finnes i CV-en (f.eks. \
"vurder å nevne Power BI hvis du har brukt det"), skal `cv_excerpt` være `null`, og \
forslaget selv skal formuleres betinget ("hvis du har ...", "dersom du har erfaring med \
...") i stedet for å late som kompetansen allerede er dokumentert.
9. Hvis stillingsannonsen nevner flere konkrete, ulike kompetanser i samme krav eller \
samme setning (f.eks. "IT-kostnadsmodeller, lisensforvaltning og analyse av store \
datamengder"), bryt kravet ned i de navngitte delene, og vurder HVER del hver for seg: \
dekker CV-en akkurat denne ene delen tydelig? Hvis ikke, skal nettopp den delen beskrives \
som et eget, konkret kompetansegap – ikke en vag, samlet vurdering av hele kravet. \
Utelat ALDRI en spesifikk, udokumentert del bare fordi en annen del av samme krav er \
dekket, og dekk den aldri vagt av en styrke om noe annet.
10. Hvis stillingsannonsen selv sier at et krav kan kompenseres av annen relevant \
erfaring (f.eks. "relevant erfaring kan kompensere for manglende mastergrad"), MÅ du ta \
med denne nyansen i kravets `description` i `job_requirements`, og i beskrivelsen av et \
eventuelt tilhørende kompetansegap. Fremstill aldri et slikt krav som absolutt eller \
ufravikelig når annonsen selv åpner for et unntak.
11. En svak eller indirekte kobling (`related_requirement_ids`) mellom et krav og en \
styrke eller et CV-forslag FRITAR deg ALDRI fra plikten i regel 9. Et krav kan ha BÅDE en \
relatert styrke/CV-forslag OG et eget kompetansegap samtidig, hvis ulike, navngitte deler \
av kravet er ulikt dokumentert. Bruk aldri en generell personlig egenskap (f.eks. stor \
arbeidskapasitet, evne til å håndtere flere oppgaver, eller det å kombinere jobb og \
studier) som bevis på at et SPESIFIKT, fagspesifikt krav er dekket.
12. Hvis du nevner at relevant erfaring kan kompensere for et krav (regel 10), skal du \
ALDRI hevde at en generell, udokumentert egenskap (f.eks. å kombinere jobb og studier, \
eller stor arbeidskapasitet) i seg selv utgjør denne kompenserende erfaringen. \
Kompenserende erfaring må være relevant for kravets EGET fagområde – ikke bare generell \
arbeidsevne eller tidsstyring.
"""


def build_messages(*, cv_text: str, job_ad_text: str) -> list[dict[str, str]]:
    user_prompt = (
        "CV:\n"
        f'"""\n{cv_text}\n"""\n\n'
        "Stillingsannonse:\n"
        f'"""\n{job_ad_text}\n"""\n'
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
