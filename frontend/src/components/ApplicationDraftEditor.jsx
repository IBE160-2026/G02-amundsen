// Søknadsutkast (FR8, FR9, Story 4.1, 4.2): brukeren kan lese og redigere
// utkastet videre i applikasjonen. Ingenting lagres – teksten finnes bare
// i nettleserens minne for den aktive økten (FR11, NFR3).
//
// Komponenten holder redigeringen i lokal state, initialisert fra `draft`.
// Når en ny demoanalyse kjøres, gir App.jsx komponenten en ny `key`, slik at
// React monterer en frisk instans i stedet for å synkronisere state i en
// effekt (se https://react.dev/learn/you-might-not-need-an-effect).

import { useState } from 'react'

function ApplicationDraftEditor({ draft }) {
  const [text, setText] = useState(draft)

  const isEdited = text !== draft

  return (
    <section aria-labelledby="draft-heading">
      <div className="draft-heading-row">
        <h2 id="draft-heading">Søknadsutkast</h2>
        {isEdited && (
          <button
            type="button"
            className="button-secondary"
            onClick={() => setText(draft)}
          >
            Tilbakestill til originalutkast
          </button>
        )}
      </div>
      <label htmlFor="application-draft" className="visually-hidden">
        Rediger søknadsutkastet
      </label>
      <textarea
        id="application-draft"
        className="application-draft"
        value={text}
        onChange={(event) => setText(event.target.value)}
        rows={12}
      />
    </section>
  )
}

export default ApplicationDraftEditor
