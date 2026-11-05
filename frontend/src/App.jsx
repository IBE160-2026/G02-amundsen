import { useEffect, useMemo, useState } from 'react'
import './App.css'
import { fetchDemoAnalysis, fetchNormalAnalysis } from './api/analyzeApi'
import ApplicationDraftEditor from './components/ApplicationDraftEditor'
import InputPreview from './components/InputPreview'
import JobRequirementsList from './components/JobRequirementsList'
import ModeSelector from './components/ModeSelector'
import NormalModeForm from './components/NormalModeForm'
import StatusMessage from './components/StatusMessage'
import TraceableItemList from './components/TraceableItemList'

function App() {
  const [mode, setMode] = useState('demo')
  const [status, setStatus] = useState('idle') // idle | loading | success | error
  const [response, setResponse] = useState(null)
  const [errorMessage, setErrorMessage] = useState(null)
  const [runId, setRunId] = useState(0)
  // Hva det pågående/siste kallet faktisk var – slik at useEffect under vet
  // hvilken API-funksjon den skal kalle, og "Prøv igjen" kan gjenta nøyaktig
  // samme forespørsel uten at brukeren må lime inn teksten på nytt.
  const [pendingRequest, setPendingRequest] = useState(null)

  useEffect(() => {
    if (status !== 'loading' || !pendingRequest) return

    const controller = new AbortController()

    const promise =
      pendingRequest.kind === 'demo'
        ? fetchDemoAnalysis({ signal: controller.signal })
        : fetchNormalAnalysis({
            cvText: pendingRequest.cvText,
            jobAdText: pendingRequest.jobAdText,
            signal: controller.signal,
          })

    promise
      .then((data) => {
        setResponse(data)
        setRunId((id) => id + 1)
        setStatus('success')
      })
      .catch((error) => {
        if (error?.name === 'AbortError') return
        setErrorMessage(
          error?.message || 'Noe gikk feil under analysen. Prøv igjen.',
        )
        setStatus('error')
      })

    return () => controller.abort()
  }, [status, pendingRequest])

  const requirementsById = useMemo(() => {
    const requirements = response?.result?.job_requirements ?? []
    return Object.fromEntries(requirements.map((req) => [req.id, req]))
  }, [response])

  function handleModeChange(newMode) {
    setMode(newMode)
    setStatus('idle')
    setResponse(null)
    setErrorMessage(null)
    setPendingRequest(null)
  }

  function runDemoAnalysis() {
    setErrorMessage(null)
    setPendingRequest({ kind: 'demo' })
    setStatus('loading')
  }

  function runNormalAnalysis({ cvText, jobAdText }) {
    setErrorMessage(null)
    setPendingRequest({ kind: 'normal', cvText, jobAdText })
    setStatus('loading')
  }

  function retry() {
    setErrorMessage(null)
    setStatus('loading')
  }

  const result = response?.result

  return (
    <div className="app">
      <header className="app-header">
        <h1>Career Transition Assistant</h1>
        <p>
          Lim inn en CV og en konkret stillingsannonse, og få hjelp til å se
          relevante styrker, kompetansegap, CV-forslag og et førsteutkast til
          søknadsbrev. Ingenting lagres etter at økten er avsluttet.
        </p>
      </header>

      <main>
        <section aria-labelledby="mode-heading" className="mode-section">
          <h2 id="mode-heading" className="visually-hidden">
            Modusvalg
          </h2>
          <ModeSelector mode={mode} onModeChange={handleModeChange} />

          {mode === 'demo' && (
            <button
              type="button"
              className="button-primary"
              onClick={runDemoAnalysis}
              disabled={status === 'loading'}
            >
              {status === 'loading' ? 'Analyserer …' : 'Kjør demoanalyse'}
            </button>
          )}

          {mode === 'normal' && (
            <NormalModeForm
              onSubmit={runNormalAnalysis}
              disabled={status === 'loading'}
            />
          )}
        </section>

        {status === 'loading' && <StatusMessage kind="loading" />}

        {status === 'error' && (
          <StatusMessage kind="error" message={errorMessage} onRetry={retry} />
        )}

        {status === 'idle' && mode === 'demo' && (
          <StatusMessage
            kind="empty"
            message="Velg demomodus og trykk «Kjør demoanalyse» for å se hovedflyten med fiktiv CV og stillingsannonse."
          />
        )}

        {status === 'success' && result && (
          <div className="results">
            <InputPreview
              cvText={response.cv_text}
              jobAdText={response.job_ad_text}
            />
            <JobRequirementsList requirements={result.job_requirements} />
            <TraceableItemList
              heading="Relevante styrker"
              headingId="strengths-heading"
              items={result.strengths}
              textKey="description"
              emptyText="Ingen relevante styrker ble identifisert."
              requirementsById={requirementsById}
            />
            <TraceableItemList
              heading="Kompetansegap"
              headingId="gaps-heading"
              items={result.competency_gaps}
              textKey="description"
              emptyText="Ingen kompetansegap ble identifisert."
              requirementsById={requirementsById}
            />
            <TraceableItemList
              heading="Forslag til CV-tilpasning"
              headingId="suggestions-heading"
              items={result.cv_suggestions}
              textKey="suggestion"
              emptyText="Ingen CV-forslag ble generert."
              requirementsById={requirementsById}
            />
            <ApplicationDraftEditor key={runId} draft={result.application_draft} />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>
          {mode === 'demo'
            ? 'Demomodus bruker en fast, fiktiv CV og stillingsannonse og gjør ingen kall til en ekstern språkmodell.'
            : 'Normalmodus sender CV-en og stillingsannonsen din via backenden til en ekstern språkmodell (OpenAI) for analyse. Ingenting lagres etter at økten er avsluttet.'}
        </p>
      </footer>
    </div>
  )
}

export default App
