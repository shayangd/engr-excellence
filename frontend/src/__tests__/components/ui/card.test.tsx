import React from 'react'
import { render, screen } from '@testing-library/react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

describe('Card Components', () => {
  describe('Card', () => {
    it('should render children correctly', () => {
      render(
        <Card>
          <div>Card content</div>
        </Card>
      )

      expect(screen.getByText('Card content')).toBeInTheDocument()
    })

    it('should apply custom className', () => {
      render(
        <Card className="custom-class">
          <div>Content</div>
        </Card>
      )

      const card = screen.getByText('Content').parentElement
      expect(card).toHaveClass('custom-class')
    })

    it('should forward ref correctly', () => {
      const ref = React.createRef<HTMLDivElement>()
      render(
        <Card ref={ref}>
          <div>Content</div>
        </Card>
      )

      expect(ref.current).toBeInstanceOf(HTMLDivElement)
    })
  })

  describe('CardHeader', () => {
    it('should render children correctly', () => {
      render(
        <CardHeader>
          <div>Header content</div>
        </CardHeader>
      )

      expect(screen.getByText('Header content')).toBeInTheDocument()
    })

    it('should apply custom className', () => {
      render(
        <CardHeader className="header-class">
          <div>Header</div>
        </CardHeader>
      )

      const header = screen.getByText('Header').parentElement
      expect(header).toHaveClass('header-class')
    })
  })

  describe('CardTitle', () => {
    it('should render as h3 by default', () => {
      render(<CardTitle>Title text</CardTitle>)

      const title = screen.getByRole('heading', { level: 3 })
      expect(title).toBeInTheDocument()
      expect(title).toHaveTextContent('Title text')
    })

    it('should apply custom className', () => {
      render(<CardTitle className="title-class">Title</CardTitle>)

      const title = screen.getByRole('heading')
      expect(title).toHaveClass('title-class')
    })
  })

  describe('CardContent', () => {
    it('should render children correctly', () => {
      render(
        <CardContent>
          <p>Content text</p>
        </CardContent>
      )

      expect(screen.getByText('Content text')).toBeInTheDocument()
    })

    it('should apply custom className', () => {
      render(
        <CardContent className="content-class">
          <div>Content</div>
        </CardContent>
      )

      const content = screen.getByText('Content').parentElement
      expect(content).toHaveClass('content-class')
    })
  })

  describe('Card composition', () => {
    it('should work together as a complete card', () => {
      render(
        <Card>
          <CardHeader>
            <CardTitle>Test Card</CardTitle>
          </CardHeader>
          <CardContent>
            <p>This is the card content</p>
          </CardContent>
        </Card>
      )

      expect(screen.getByRole('heading', { name: 'Test Card' })).toBeInTheDocument()
      expect(screen.getByText('This is the card content')).toBeInTheDocument()
    })
  })
})
