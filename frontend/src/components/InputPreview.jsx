// Viser CV-en og stillingsannonsen analysen bygger på (Story 1.1, 1.2),
// slik at brukeren kan kontrollere at forslagene faktisk kan spores
// tilbake til denne inputen (NFR8).

function InputPreview({ cvText, jobAdText }) {
  return (
    <section className="input-preview" aria-label="Input som analysen bygger på">
      <article className="input-preview-column">
        <h3>CV</h3>
        <pre>{cvText}</pre>
      </article>
      <article className="input-preview-column">
        <h3>Stillingsannonse</h3>
        <pre>{jobAdText}</pre>
      </article>
    </section>
  )
}

export default InputPreview
