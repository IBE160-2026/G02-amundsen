// Sentrale krav i stillingsannonsen (FR3, Story 2.3).

function JobRequirementsList({ requirements }) {
  return (
    <section aria-labelledby="requirements-heading">
      <h2 id="requirements-heading">Krav i stillingsannonsen</h2>
      {requirements.length === 0 ? (
        <p className="status status-empty">Ingen krav ble identifisert.</p>
      ) : (
        <ul className="requirements-list">
          {requirements.map((requirement) => (
            <li key={requirement.id}>
              <span
                className={`priority-badge priority-${requirement.priority === 'sentral' ? 'sentral' : 'onskelig'}`}
              >
                {requirement.priority === 'sentral' ? 'Sentralt' : 'Ønskelig'}
              </span>
              {requirement.description}
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

export default JobRequirementsList
