// Sporbarhet (FR7, NFR8, Story 3.2): viser hvilket utdrag fra CV-en og/eller
// stillingsannonsen et funn eller forslag bygger på.

function SourceTrace({ source }) {
  if (!source || (!source.cv_excerpt && !source.job_ad_excerpt)) {
    return null
  }

  return (
    <dl className="source-trace">
      {source.cv_excerpt && (
        <div>
          <dt>Fra CV-en</dt>
          <dd>«{source.cv_excerpt}»</dd>
        </div>
      )}
      {source.job_ad_excerpt && (
        <div>
          <dt>Fra stillingsannonsen</dt>
          <dd>«{source.job_ad_excerpt}»</dd>
        </div>
      )}
    </dl>
  )
}

export default SourceTrace
