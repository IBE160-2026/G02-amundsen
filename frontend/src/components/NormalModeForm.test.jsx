import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import NormalModeForm from './NormalModeForm'

describe('NormalModeForm', () => {
  it('kaller onSubmit med trimmet CV og stillingsannonse når begge er fylt ut', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()
    render(<NormalModeForm onSubmit={onSubmit} disabled={false} />)

    await user.type(screen.getByLabelText('CV'), '  Min CV  ')
    await user.type(screen.getByLabelText('Stillingsannonse'), '  Min annonse  ')
    await user.click(screen.getByRole('button', { name: /kjør analyse/i }))

    expect(onSubmit).toHaveBeenCalledWith({ cvText: 'Min CV', jobAdText: 'Min annonse' })
  })

  it('viser en valideringsfeil og kaller ikke onSubmit når CV er tom', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()
    render(<NormalModeForm onSubmit={onSubmit} disabled={false} />)

    await user.type(screen.getByLabelText('Stillingsannonse'), 'Min annonse')
    await user.click(screen.getByRole('button', { name: /kjør analyse/i }))

    expect(
      screen.getByText(/fyll inn både cv og stillingsannonse/i),
    ).toBeInTheDocument()
    expect(onSubmit).not.toHaveBeenCalled()
  })

  it('viser en valideringsfeil når feltene bare består av mellomrom', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()
    render(<NormalModeForm onSubmit={onSubmit} disabled={false} />)

    await user.type(screen.getByLabelText('CV'), '   ')
    await user.type(screen.getByLabelText('Stillingsannonse'), '   ')
    await user.click(screen.getByRole('button', { name: /kjør analyse/i }))

    expect(
      screen.getByText(/fyll inn både cv og stillingsannonse/i),
    ).toBeInTheDocument()
    expect(onSubmit).not.toHaveBeenCalled()
  })

  it('deaktiverer feltene og knappen når disabled er true', () => {
    render(<NormalModeForm onSubmit={vi.fn()} disabled={true} />)

    expect(screen.getByLabelText('CV')).toBeDisabled()
    expect(screen.getByLabelText('Stillingsannonse')).toBeDisabled()
    expect(screen.getByRole('button', { name: /analyserer/i })).toBeDisabled()
  })
})
