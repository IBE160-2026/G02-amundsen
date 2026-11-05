import { afterEach, describe, expect, it, vi } from 'vitest'
import { AnalyzeApiError, fetchDemoAnalysis, fetchNormalAnalysis } from './analyzeApi'

describe('fetchDemoAnalysis', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('returnerer JSON-responsen når kallet lykkes', async () => {
    const payload = { mode: 'demo', cv_text: 'CV', job_ad_text: 'Annonse', result: {} }
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => payload,
    })
    vi.stubGlobal('fetch', fetchMock)

    const data = await fetchDemoAnalysis()

    expect(data).toEqual(payload)
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining('/api/analyze/demo'),
      expect.objectContaining({}),
    )
  })

  it('kaster en forståelig feil når backenden svarer med en feilkode', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({ detail: 'Kunne ikke laste demodata.' }),
    })
    vi.stubGlobal('fetch', fetchMock)

    await expect(fetchDemoAnalysis()).rejects.toMatchObject({
      name: 'AnalyzeApiError',
      message: 'Kunne ikke laste demodata.',
      status: 500,
    })
  })

  it('kaster en forståelig feil når nettverkskallet selv mislykkes', async () => {
    const fetchMock = vi.fn().mockRejectedValue(new TypeError('Failed to fetch'))
    vi.stubGlobal('fetch', fetchMock)

    await expect(fetchDemoAnalysis()).rejects.toBeInstanceOf(AnalyzeApiError)
  })
})

describe('fetchNormalAnalysis', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('poster cv_text og job_ad_text som JSON til /api/analyze', async () => {
    const payload = { mode: 'normal', cv_text: 'Min CV', job_ad_text: 'Min annonse', result: {} }
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => payload,
    })
    vi.stubGlobal('fetch', fetchMock)

    const data = await fetchNormalAnalysis({ cvText: 'Min CV', jobAdText: 'Min annonse' })

    expect(data).toEqual(payload)
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining('/api/analyze'),
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cv_text: 'Min CV', job_ad_text: 'Min annonse' }),
      }),
    )
  })

  it('bygger en lesbar feilmelding av FastAPI sin valideringsfeil-liste (422)', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 422,
      json: async () => ({
        detail: [
          {
            loc: ['body', 'cv_text'],
            msg: 'String should have at least 1 character',
            type: 'string_too_short',
          },
        ],
      }),
    })
    vi.stubGlobal('fetch', fetchMock)

    await expect(
      fetchNormalAnalysis({ cvText: '', jobAdText: 'Min annonse' }),
    ).rejects.toMatchObject({
      name: 'AnalyzeApiError',
      status: 422,
      message: expect.stringContaining('cv_text'),
    })
  })

  it('bruker backendens tekstmelding direkte for kjente feil (f.eks. manglende API-nøkkel)', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 503,
      json: async () => ({
        detail: 'Normalmodus er ikke tilgjengelig: ingen gyldig API-nøkkel er konfigurert på serveren.',
      }),
    })
    vi.stubGlobal('fetch', fetchMock)

    await expect(
      fetchNormalAnalysis({ cvText: 'CV', jobAdText: 'Annonse' }),
    ).rejects.toMatchObject({
      status: 503,
      message: 'Normalmodus er ikke tilgjengelig: ingen gyldig API-nøkkel er konfigurert på serveren.',
    })
  })

  it('kaster en forståelig feil når nettverkskallet selv mislykkes', async () => {
    const fetchMock = vi.fn().mockRejectedValue(new TypeError('Failed to fetch'))
    vi.stubGlobal('fetch', fetchMock)

    await expect(
      fetchNormalAnalysis({ cvText: 'CV', jobAdText: 'Annonse' }),
    ).rejects.toBeInstanceOf(AnalyzeApiError)
  })
})
