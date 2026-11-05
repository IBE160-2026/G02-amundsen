import { afterEach, describe, expect, it, vi } from 'vitest'
import { AnalyzeApiError, fetchDemoAnalysis } from './analyzeApi'

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
