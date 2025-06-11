import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from '@/components/ui/button'

describe('Button', () => {
  it('should render with default props', () => {
    render(<Button>Click me</Button>)

    const button = screen.getByRole('button', { name: 'Click me' })
    expect(button).toBeInTheDocument()
    expect(button).toHaveClass('inline-flex', 'items-center', 'justify-center')
  })

  it('should apply default variant and size classes', () => {
    render(<Button>Default Button</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-primary', 'text-primary-foreground')
    expect(button).toHaveClass('h-10', 'px-4', 'py-2')
  })

  it('should apply destructive variant classes', () => {
    render(<Button variant="destructive">Delete</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-destructive', 'text-destructive-foreground')
  })

  it('should apply outline variant classes', () => {
    render(<Button variant="outline">Outline</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('border', 'border-input', 'bg-background')
  })

  it('should apply secondary variant classes', () => {
    render(<Button variant="secondary">Secondary</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-secondary', 'text-secondary-foreground')
  })

  it('should apply ghost variant classes', () => {
    render(<Button variant="ghost">Ghost</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('hover:bg-accent', 'hover:text-accent-foreground')
  })

  it('should apply link variant classes', () => {
    render(<Button variant="link">Link</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('text-primary', 'underline-offset-4')
  })

  it('should apply small size classes', () => {
    render(<Button size="sm">Small</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('h-9', 'rounded-md', 'px-3')
  })

  it('should apply large size classes', () => {
    render(<Button size="lg">Large</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('h-11', 'rounded-md', 'px-8')
  })

  it('should apply icon size classes', () => {
    render(<Button size="icon">Icon</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('h-10', 'w-10')
  })

  it('should merge custom className', () => {
    render(<Button className="custom-class">Custom</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveClass('custom-class')
    expect(button).toHaveClass('inline-flex') // Should still have base classes
  })

  it('should handle click events', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Clickable</Button>)

    const button = screen.getByRole('button')
    fireEvent.click(button)

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('should be disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>)

    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
    expect(button).toHaveClass('disabled:pointer-events-none', 'disabled:opacity-50')
  })

  it('should forward ref correctly', () => {
    const ref = React.createRef<HTMLButtonElement>()
    render(<Button ref={ref}>Ref Button</Button>)

    expect(ref.current).toBeInstanceOf(HTMLButtonElement)
    expect(ref.current?.textContent).toBe('Ref Button')
  })

  it('should pass through HTML button attributes', () => {
    render(
      <Button type="submit" data-testid="submit-button" aria-label="Submit form">
        Submit
      </Button>
    )

    const button = screen.getByRole('button')
    expect(button).toHaveAttribute('type', 'submit')
    expect(button).toHaveAttribute('data-testid', 'submit-button')
    expect(button).toHaveAttribute('aria-label', 'Submit form')
  })

  it('should render children correctly', () => {
    render(
      <Button>
        <span>Icon</span>
        <span>Text</span>
      </Button>
    )

    expect(screen.getByText('Icon')).toBeInTheDocument()
    expect(screen.getByText('Text')).toBeInTheDocument()
  })
})
