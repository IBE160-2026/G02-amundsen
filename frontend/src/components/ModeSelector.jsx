// Modusvalg (Story 1.3, FR12). Demomodus bruker en fast, fiktiv CV og
// stillingsannonse og krever ingen API-nøkkel. Normalmodus sender brukerens
// egen CV og stillingsannonse til backenden, som videresender til en ekte
// språkmodell – og krever derfor at backenden har en konfigurert API-nøkkel.

function ModeSelector({ mode, onModeChange }) {
  return (
    <fieldset className="mode-selector">
      <legend>Velg modus</legend>

      <label className={`mode-option ${mode === 'demo' ? 'is-selected' : ''}`}>
        <input
          type="radio"
          name="mode"
          value="demo"
          checked={mode === 'demo'}
          onChange={() => onModeChange('demo')}
        />
        <span>
          <strong>Demomodus</strong>
          <small>
            Bruker en fast, fiktiv CV og stillingsannonse. Krever ingen
            API-nøkkel.
          </small>
        </span>
      </label>

      <label className={`mode-option ${mode === 'normal' ? 'is-selected' : ''}`}>
        <input
          type="radio"
          name="mode"
          value="normal"
          checked={mode === 'normal'}
          onChange={() => onModeChange('normal')}
        />
        <span>
          <strong>Normalmodus</strong>
          <small>
            Lim inn din egen CV og stillingsannonse. Krever at backenden har
            en konfigurert API-nøkkel.
          </small>
        </span>
      </label>
    </fieldset>
  )
}

export default ModeSelector
