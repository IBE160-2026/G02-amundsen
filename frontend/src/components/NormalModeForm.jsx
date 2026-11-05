// Innliming av CV og stillingsannonse i normalmodus (FR1, FR2, Story 1.1,
// 1.2). Validerer at begge feltene faktisk har innhold før analysen
// startes, slik at brukeren får en umiddelbar, forståelig tilbakemelding i
// stedet for å vente på et unødvendig API-kall (NFR2, NFR7, Story 5.2).

import { useState } from 'react'
import { MAX_CV_LENGTH, MAX_JOB_AD_LENGTH } from '../constants'

function NormalModeForm({ onSubmit, disabled }) {
  const [cvText, setCvText] = useState('')
  const [jobAdText, setJobAdText] = useState('')
  const [validationError, setValidationError] = useState(null)

  function handleSubmit(event) {
    event.preventDefault()

    if (!cvText.trim() || !jobAdText.trim()) {
      setValidationError('Fyll inn både CV og stillingsannonse før du starter analysen.')
      return
    }

    setValidationError(null)
    onSubmit({ cvText: cvText.trim(), jobAdText: jobAdText.trim() })
  }

  return (
    <form className="normal-mode-form" onSubmit={handleSubmit}>
      <div className="form-field">
        <label htmlFor="cv-input">CV</label>
        <textarea
          id="cv-input"
          value={cvText}
          onChange={(event) => setCvText(event.target.value)}
          maxLength={MAX_CV_LENGTH}
          rows={10}
          placeholder="Lim inn CV-en din her …"
          disabled={disabled}
        />
      </div>

      <div className="form-field">
        <label htmlFor="job-ad-input">Stillingsannonse</label>
        <textarea
          id="job-ad-input"
          value={jobAdText}
          onChange={(event) => setJobAdText(event.target.value)}
          maxLength={MAX_JOB_AD_LENGTH}
          rows={10}
          placeholder="Lim inn stillingsannonsen her …"
          disabled={disabled}
        />
      </div>

      {validationError && (
        <p className="status status-error" role="alert">
          {validationError}
        </p>
      )}

      <button type="submit" className="button-primary" disabled={disabled}>
        {disabled ? 'Analyserer …' : 'Kjør analyse'}
      </button>
    </form>
  )
}

export default NormalModeForm
