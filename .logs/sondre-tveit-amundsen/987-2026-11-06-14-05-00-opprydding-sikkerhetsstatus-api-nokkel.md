# Oppdatert sikkerhetsstatus: API-nøkkel ikke lenger aktiv

## 2026-11-06 kl. 14:05 — Sondre Tveit Amundsen

### Oppgave
Brukeren har manuelt kontrollert API-nøkler i OpenAI sitt dashbord og bekreftet at kun den nyeste, lokale nøkkelen står som Active — den gamle nøkkelen fra produksjonstesten på Vercel 06.11.2026 (dokumentert i [991-produksjonstest-normalmodus](991-2026-11-06-11-17-57-produksjonstest-normalmodus.md)) er ikke lenger aktiv. `README.md` og `issues.md` skulle oppdateres til å gjenspeile dette, uten å endre `.env`-filer, applikasjonskode eller Vercel-konfigurasjon, og uten API-kall. Forklaringen om hvorfor normalmodus er avslått på den offentlige Vercel-siden, og at en ny nøkkel ikke skal publiseres der uten tilgangskontroll, skulle beholdes.

### Plan
- Leste gjeldende tekst i `README.md` avsnitt «Status i produksjon» og «Manuelt i Vercel».
- Omskrev sikkerhetspunktet fra «ikke tilbakekalt, åpent» til «bekreftet inaktiv, løst», men beholdt begrunnelsen for at normalmodus likevel forblir avslått offentlig (ingen tilgangskontroll/innlogging i v1).
- Justerte trinn 1 i «Manuelt i Vercel»-lista: fra «tilbakekall den gamle nøkkelen» til «sett opp tilgangskontroll før en ny nøkkel publiseres», siden tilbakekallingsbehovet er bortfalt.
- Oppdaterte `issues.md`: lukket sikkerhetsrisiko-punktet fra [991-produksjonstest-normalmodus](991-2026-11-06-11-17-57-produksjonstest-normalmodus.md) som løst, og justerte det gjenstående beslutningspunktet (om normalmodus skal aktiveres permanent) til å vise at nøkkelen nå er bekreftet inaktiv, men at tilgangskontroll fortsatt er en forutsetning.
- Ingen `.env`-filer, applikasjonskode eller Vercel-konfigurasjon er rørt. Ingen API-kall er gjort.

### Resultat
- **`README.md`** (endret, ikke committet av meg): sikkerhetspunktet i «Status i produksjon» er omskrevet til å vise at nøkkelen er bekreftet inaktiv (manuell kontroll 06.11.2026), men normalmodus forblir avslått offentlig til tilgangskontroll er på plass. Trinn 1 i «Manuelt i Vercel»-lista er justert til å peke på tilgangskontroll i stedet for tilbakekalling av en allerede inaktiv nøkkel.
- **`issues.md`** (endret, committes av denne sesjonsloggens rutine): sikkerhetsrisiko-punktet fra 2026-11-06 er lukket med `[x]` og løsningsdato. Beslutningspunktet om permanent aktivering av normalmodus er oppdatert til å vise ny status og gjenstående forutsetning (tilgangskontroll).
- README-endringen er **ikke** committet av meg, per brukerens instruks («det gjør jeg selv»).

### Åpne punkter
- Beslutning utestående: når/om normalmodus skal aktiveres permanent i produksjon — krever tilgangskontroll/innlogging på plass først, ikke lenger en nøkkelrotasjon (se `issues.md`).
- Øvrige, tidligere åpne punkter er uendret.
