import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import { AnalyzeApiError, fetchDemoAnalysis, fetchNormalAnalysis } from './api/analyzeApi'

vi.mock('./api/analyzeApi', async () => {
  const actual = await vi.importActual('./api/analyzeApi')
  return { ...actual, fetchDemoAnalysis: vi.fn(), fetchNormalAnalysis: vi.fn() }
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

const normalResponse = {
  ...demoResponse,
  mode: 'normal',
  cv_text: 'Min egen CV-tekst',
  job_ad_text: 'Min egen stillingsannonse',
}

async function selectNormalMode(user) {
  await user.click(screen.getByRole('radio', { name: /normalmodus/i }))
}

afterEach(() => {
  vi.resetAllMocks()
})

describe('App – demomodus', () => {
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

describe('App – normalmodus', () => {
  it('kan velges, og viser et skjema for CV og stillingsannonse i stedet for demo-knappen', async () => {
    const user = userEvent.setup()
    render(<App />)

    const normalRadio = screen.getByRole('radio', { name: /normalmodus/i })
    expect(normalRadio).not.toBeDisabled()

    await selectNormalMode(user)

    expect(normalRadio).toBeChecked()
    expect(screen.getByLabelText('CV')).toBeInTheDocument()
    expect(screen.getByLabelText('Stillingsannonse')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /kjør analyse/i })).toBeInTheDocument()
    expect(
      screen.queryByRole('button', { name: /kjør demoanalyse/i }),
    ).not.toBeInTheDocument()
  })

  it('viser en valideringsfeil og kaller ikke API-et når feltene er tomme', async () => {
    const user = userEvent.setup()
    render(<App />)
    await selectNormalMode(user)

    await user.click(screen.getByRole('button', { name: /kjør analyse/i }))

    expect(
      await screen.findByText(/fyll inn både cv og stillingsannonse/i),
    ).toBeInTheDocument()
    expect(fetchNormalAnalysis).not.toHaveBeenCalled()
  })

  it('viser en lastemelding mens normalmodus-analysen pågår', async () => {
    let resolveFetch
    fetchNormalAnalysis.mockImplementationOnce(
      () => new Promise((resolve) => { resolveFetch = resolve }),
    )
    const user = userEvent.setup()
    render(<App />)
    await selectNormalMode(user)

    await user.type(screen.getByLabelText('CV'), 'Min egen CV-tekst')
    await user.type(screen.getByLabelText('Stillingsannonse'), 'Min egen stillingsannonse')
    await user.click(screen.getByRole('button', { name: /kjør analyse/i }))

    expect(screen.getByRole('status')).toHaveTextContent(/analyserer/i)

    resolveFetch(normalResponse)
    await waitFor(() => {
      expect(screen.getByText('Relevant mastergrad')).toBeInTheDocument()
    })
  })

  it('sender inn CV og stillingsannonse og viser resultatet ved suksess', async () => {
    fetchNormalAnalysis.mockResolvedValueOnce(normalResponse)
    const user = userEvent.setup()
    render(<App />)
    await selectNormalMode(user)

    await user.type(screen.getByLabelText('CV'), 'Min egen CV-tekst')
    await user.type(screen.getByLabelText('Stillingsannonse'), 'Min egen stillingsannonse')
    await user.click(screen.getByRole('button', { name: /kjør analyse/i }))

    await waitFor(() => {
      expect(screen.getByText('Relevant mastergrad')).toBeInTheDocument()
    })

    expect(fetchNormalAnalysis).toHaveBeenCalledWith(
      expect.objectContaining({
        cvText: 'Min egen CV-tekst',
        jobAdText: 'Min egen stillingsannonse',
      }),
    )
    // Vises både i det ekkoede input-preview-feltet og i skjemaet selv.
    expect(screen.getAllByText('Min egen CV-tekst')).toHaveLength(2)
  })

  it('viser en forståelig feilmelding ved API-feil, og kan prøves igjen uten å tømme skjemaet', async () => {
    fetchNormalAnalysis
      .mockRejectedValueOnce(
        new AnalyzeApiError(
          'Normalmodus er ikke tilgjengelig: ingen gyldig API-nøkkel er konfigurert på serveren.',
        ),
      )
      .mockResolvedValueOnce(normalResponse)
    const user = userEvent.setup()
    render(<App />)
    await selectNormalMode(user)

    await user.type(screen.getByLabelText('CV'), 'Min egen CV-tekst')
    await user.type(screen.getByLabelText('Stillingsannonse'), 'Min egen stillingsannonse')
    await user.click(screen.getByRole('button', { name: /kjør analyse/i }))

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/ingen gyldig api-nøkkel/i)
    })

    // Teksten skal fortsatt stå i feltene etter en mislykket forespørsel.
    expect(screen.getByLabelText('CV')).toHaveValue('Min egen CV-tekst')

    await user.click(screen.getByRole('button', { name: /prøv igjen/i }))

    await waitFor(() => {
      expect(screen.getByText('Relevant mastergrad')).toBeInTheDocument()
    })
    expect(fetchNormalAnalysis).toHaveBeenCalledTimes(2)
  })

  it('nullstiller forrige resultat når brukeren bytter modus', async () => {
    fetchDemoAnalysis.mockResolvedValueOnce(demoResponse)
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('button', { name: /kjør demoanalyse/i }))
    await waitFor(() => {
      expect(screen.getByText('Relevant mastergrad')).toBeInTheDocument()
    })

    await selectNormalMode(user)

    expect(screen.queryByText('Relevant mastergrad')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: /kjør analyse/i })).toBeInTheDocument()
  })
})
