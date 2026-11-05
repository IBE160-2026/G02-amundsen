// Gjenbrukbar liste for styrker, kompetansegap og CV-forslag – alle har
// samme form: en beskrivende tekst, hvilke krav de knytter seg til, og
// sporbarhet til CV og/eller stillingsannonse (FR4, FR5, FR6, FR7).

import SourceTrace from './SourceTrace'

function TraceableItemList({
  heading,
  headingId,
  items,
  textKey,
  emptyText,
  requirementsById,
}) {
  return (
    <section aria-labelledby={headingId}>
      <h2 id={headingId}>{heading}</h2>
      {items.length === 0 ? (
        <p className="status status-empty">{emptyText}</p>
      ) : (
        <ul className="traceable-list">
          {items.map((item) => (
            <li key={item.id}>
              <p className="traceable-text">{item[textKey]}</p>
              {item.related_requirement_ids?.length > 0 && (
                <ul className="related-requirements">
                  {item.related_requirement_ids.map((reqId) => (
                    <li key={reqId}>
                      {requirementsById[reqId]?.description ?? reqId}
                    </li>
                  ))}
                </ul>
              )}
              <SourceTrace source={item.source} />
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

export default TraceableItemList
