import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import { AnalyzeApiError, fetchDemoAnalysis } from './api/analyzeApi'

vi.mock('./api/analyzeApi', async () => {
  const actual = await vi.importActual('./api/analyzeApi')
  return { ...actual, fetchDemoAnalysis: vi.fn() }
})

const demoResponse = {
  mode: 'demo',
  cv_text: 'Kari Nordmann ... Master i informatikk ...',
  job_ad_text: 'Junior systemutvikler - Fjord Digital AS ...',
  result: {
    job_requirements: [
      { id: 'r1', description: 'Mastergrad i informatikk', priority: 'sentral' },
      { id: 'r5', description: 'Erfaring med React', priority: 'ønskelig' },
    ],
    strengths: [
      {
        id: 's1',
        description: 'Relevant mastergrad',
        related_requirement_ids: ['r1'],
        source: { cv_excerpt: 'Master i informatikk', job_ad_excerpt: 'Mastergrad i informatikk' },
      },
    ],
    competency_gaps: [
      {
        id: 'g1',
        description: 'Manglende dokumentert databaseerfaring',
        related_requirement_ids: ['r5'],
        source: { cv_excerpt: null, job_ad_excerpt: 'Erfaring med React' },
      },
    ],
    cv_suggestions: [
      {
        id: 'c1',
        suggestion: 'Fremhev Python-ferdighetene tidligere i CV-en',
        related_requirement_ids: ['r1'],
        source: { cv_excerpt: 'Python, JavaScript', job_ad_excerpt: 'Mastergrad i informatikk' },
      },
    ],
    application_draft: 'Jeg søker på stillingen ...',
  },
}

afterEach(() => {
  vi.resetAllMocks()
})

describe('App – demomodus', () => {
  it('viser normalmodus som ikke implementert', () => {
    render(<App />)

    const normalRadio = screen.getByRole('radio', { name: /normalmodus/i })
    expect(normalRadio).toBeDisabled()
  })

  it('viser en tom-tilstand før analysen er kjørt', () => {
    render(<App />)

    expect(screen.getByText(/velg demomodus og trykk/i)).toBeInTheDocument()
  })

  it('viser en lastemelding mens kallet pågår', async () => {
    let resolveFetch
    fetchDemoAnalysis.mockImplementationOnce(
      () => new Promise((resolve) => { resolveFetch = resolve }),
    )
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('button', { name: /kjør demoanalyse/i }))

    expect(screen.getByRole('status')).toHaveTextContent(/analyserer/i)

    resolveFetch(demoResponse)
    await waitFor(() => {
      expect(screen.getByText('Relevant mastergrad')).toBeInTheDocument()
    })
  })

  it('kjører demoanalysen og viser resultatet når brukeren trykker på knappen', async () => {
    fetchDemoAnalysis.mockResolvedValueOnce(demoResponse)
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('button', { name: /kjør demoanalyse/i }))

    await waitFor(() => {
      expect(screen.getByText('Relevant mastergrad')).toBeInTheDocument()
    })

    expect(screen.getAllByText(/mastergrad i informatikk/i).length).toBeGreaterThan(0)
    expect(screen.getByText('Manglende dokumentert databaseerfaring')).toBeInTheDocument()
    expect(screen.getByText('Fremhev Python-ferdighetene tidligere i CV-en')).toBeInTheDocument()
    expect(screen.getByDisplayValue(/jeg søker på stillingen/i)).toBeInTheDocument()
  })

  it('viser en forståelig feilmelding når kallet mislykkes', async () => {
    fetchDemoAnalysis.mockRejectedValueOnce(
      new AnalyzeApiError('Kunne ikke nå backend-tjeneren.'),
    )
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('button', { name: /kjør demoanalyse/i }))

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(
        'Kunne ikke nå backend-tjeneren.',
      )
    })

    expect(
      screen.getByRole('button', { name: /prøv igjen/i }),
    ).toBeInTheDocument()
  })
})
