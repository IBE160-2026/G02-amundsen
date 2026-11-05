// API-klient mot Career Transition Assistant-backenden.
//
// All kommunikasjon med en ekstern språkmodell skjer fra backenden
// (architecture.md, avsnitt "Backend"). Frontenden snakker kun med
// backendens REST-API, aldri direkte med en språkmodell-leverandør.

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

export class AnalyzeApiError extends Error {
  constructor(message, { status } = {}) {
    super(message)
    this.name = 'AnalyzeApiError'
    this.status = status
  }
}

/**
 * Kjører demomodus (FR12): kaller GET /api/analyze/demo, som bruker en
 * fast, fiktiv CV og stillingsannonse og returnerer et fast
 * eksempelresultat uten noe kall til en ekstern språkmodell.
 */
export async function fetchDemoAnalysis({ signal } = {}) {
  let response
  try {
    response = await fetch(`${API_BASE_URL}/api/analyze/demo`, { signal })
  } catch (cause) {
    if (cause?.name === 'AbortError') throw cause
    throw new AnalyzeApiError(
      'Kunne ikke nå backend-tjeneren. Kontroller at den kjører og at adressen er riktig.',
      { status: undefined },
    )
  }

  if (!response.ok) {
    let detail
    try {
      detail = (await response.json())?.detail
    } catch {
      // Svaret var ikke gyldig JSON – bruk standardmeldingen under.
    }
    throw new AnalyzeApiError(
      detail || `Demoanalysen mislyktes (HTTP ${response.status}).`,
      { status: response.status },
    )
  }

  return response.json()
}
