# Åpne punkter

- [ ] 2026-11-05 [backend-pydantic-og-demomodus](999-2026-11-05-12-02-03-backend-pydantic-og-demomodus.md) — fjern ubrukt rest `backend/src/backend/__init__.py` fra `uv init`
- [x] 2026-11-05 [backend-pydantic-og-demomodus](999-2026-11-05-12-02-03-backend-pydantic-og-demomodus.md) — vurder å bytte testklient-avhengighet når `httpx2` blir et reelt alternativ til `httpx` (løst 2026-11-05: `openai`-pakken trekker inn `httpx2` transitivt, og Starlette-deprecation-warningen er borte – se [normalmodus-backend-openai](997-2026-11-05-13-46-12-normalmodus-backend-openai.md))
- [ ] 2026-11-05 [frontend-demomodus](998-2026-11-05-12-32-31-frontend-demomodus.md) — gjør en ekte visuell/interaktiv browser-test av frontend (klikk-gjennom), siden brukeren avslo Claude-in-Chrome-utvidelsen denne økten
- [ ] 2026-11-05 [frontend-demomodus](998-2026-11-05-12-32-31-frontend-demomodus.md) — moderate `minimatch`-sårbarhet i eslint sin avhengighetskjede krever en brytende eslint-oppgradering (`npm audit fix --force`), ikke gjort
- [ ] 2026-11-05 [frontend-demomodus](998-2026-11-05-12-32-31-frontend-demomodus.md) — vurder å slette ubrukte asset-filer `frontend/src/assets/hero.png`, `react.svg`, `vite.svg` fra Vite-malen, som ikke lenger brukes
- [ ] 2026-11-05 [normalmodus-backend-openai](997-2026-11-05-13-46-12-normalmodus-backend-openai.md) — frontend har ikke støtte for normalmodus ennå; kan foreløpig bare testes direkte mot backend
- [ ] 2026-11-05 [normalmodus-backend-openai](997-2026-11-05-13-46-12-normalmodus-backend-openai.md) — normalmodus er ikke testet mot en ekte, betalt OpenAI-nøkkel ennå
