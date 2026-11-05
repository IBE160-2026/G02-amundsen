// API-klient mot Career Transition Assistant-backenden.
//
// All kommunikasjon med en ekstern språkmodell skjer fra backenden
// (architecture.md, avsnitt "Backend"). Frontenden snakker kun med
// backendens REST-API, aldri direkte med en språkmodell-leverandør, og har
// ingen API-nøkkel eller annen hemmelig konfigurasjon (NFR4).

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

export class AnalyzeApiError extends Error {
  constructor(message, { status } = {}) {
    super(message)
    this.name = 'AnalyzeApiError'
    this.status = status
  }
}

const NETWORK_ERROR_MESSAGE =
  'Kunne ikke nå backend-tjeneren. Kontroller at den kjører og at adressen er riktig.'

// FastAPI returnerer `detail` som en liste av valideringsfeil (422) eller
// som en enkelt, lesbar tekststreng (andre feil fra backendens egne
// HTTPException-svar, f.eks. manglende API-nøkkel eller tidsavbrudd).
function describeError(status, detail) {
  if (Array.isArray(detail)) {
    const fields = detail
      .map((item) => {
        const field = Array.isArray(item?.loc) ? item.loc[item.loc.length - 1] : null
        return field && item?.msg ? `${field}: ${item.msg}` : item?.msg
      })
      .filter(Boolean)
    if (fields.length > 0) {
      return `Kontroller input før du prøver igjen: ${fields.join('; ')}.`
    }
  }

  if (typeof detail === 'string' && detail.trim()) {
    return detail
  }

  return `Analysen mislyktes (HTTP ${status}).`
}

async function requestJson(url, init) {
  let response
  try {
    response = await fetch(url, init)
  } catch (cause) {
    if (cause?.name === 'AbortError') throw cause
    throw new AnalyzeApiError(NETWORK_ERROR_MESSAGE)
  }

  if (!response.ok) {
    let detail
    try {
      detail = (await response.json())?.detail
    } catch {
      // Svaret var ikke gyldig JSON – bruk standardmeldingen under.
    }
    throw new AnalyzeApiError(describeError(response.status, detail), {
      status: response.status,
    })
  }

  return response.json()
}

/**
 * Kjører demomodus (FR12): kaller GET /api/analyze/demo, som bruker en
 * fast, fiktiv CV og stillingsannonse og returnerer et fast
 * eksempelresultat uten noe kall til en ekstern språkmodell.
 */
export async function fetchDemoAnalysis({ signal } = {}) {
  return requestJson(`${API_BASE_URL}/api/analyze/demo`, { signal })
}

/**
 * Kjører normalmodus (FR1-FR10): sender brukerens CV og stillingsannonse
 * til POST /api/analyze, som bruker en ekte språkmodell i backenden.
 */
export async function fetchNormalAnalysis({ cvText, jobAdText, signal } = {}) {
  return requestJson(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cv_text: cvText, job_ad_text: jobAdText }),
    signal,
  })
}
