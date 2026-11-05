// Tydelig tilbakemelding ved lasting og feil (NFR2, NFR7, Story 5.2).

function StatusMessage({ kind, message, onRetry }) {
  if (kind === 'loading') {
    return (
      <p className="status status-loading" role="status" aria-live="polite">
        <span className="spinner" aria-hidden="true" />
        {message || 'Analyserer CV og stillingsannonse …'}
      </p>
    )
  }

  if (kind === 'error') {
    return (
      <div className="status status-error" role="alert">
        <p>{message || 'Noe gikk feil under analysen.'}</p>
        {onRetry && (
          <button type="button" onClick={onRetry} className="button-secondary">
            Prøv igjen
          </button>
        )}
      </div>
    )
  }

  return (
    <p className="status status-empty">
      {message || 'Ingen analyse er kjørt ennå.'}
    </p>
  )
}

export default StatusMessage
