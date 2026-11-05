// Modusvalg (Story 1.3, FR12): i v1 er kun demomodus implementert.
// Normalmodus vises, men er tydelig merket som ikke implementert ennå,
// slik at brukeren forstår hvorfor den ikke kan velges.

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

      <label className="mode-option is-disabled" aria-disabled="true">
        <input type="radio" name="mode" value="normal" disabled />
        <span>
          <strong>Normalmodus</strong>
          <small>Ikke implementert ennå – kommer i en senere versjon.</small>
        </span>
      </label>
    </fieldset>
  )
}

export default ModeSelector
