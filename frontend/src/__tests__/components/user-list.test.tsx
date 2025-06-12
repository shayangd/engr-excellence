import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { UserList } from '@/components/user-list'
import { User } from '@/types/user'

// Mock the UI components
jest.mock('@/components/ui/button', () => ({
  Button: ({ children, onClick, variant, size, ...props }: any) => (
    <button onClick={onClick} data-variant={variant} data-size={size} {...props}>
      {children}
    </button>
  ),
}))

jest.mock('@/components/ui/card', () => ({
  Card: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  CardContent: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  CardHeader: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  CardTitle: ({ children, ...props }: any) => <h2 {...props}>{children}</h2>,
}))

jest.mock('@/components/ui/loading', () => ({
  LoadingSpinner: () => <div>Loading...</div>,
}))

jest.mock('@/components/ui/error', () => ({
  ErrorDisplay: ({ message, onRetry }: any) => (
    <div>
      <span>Error: {message}</span>
      <button onClick={onRetry}>Retry</button>
    </div>
  ),
}))

// Mock Lucide icons
jest.mock('lucide-react', () => ({
  Edit: () => <span>Edit Icon</span>,
  Trash2: () => <span>Delete Icon</span>,
  Plus: () => <span>Plus Icon</span>,
}))

describe('UserList', () => {
  const mockUsers: User[] = [
    { id: '1', name: 'John Doe', email: 'john@example.com' },
    { id: '2', name: 'Jane Smith', email: 'jane@example.com' },
  ]

  const defaultProps = {
    users: mockUsers,
    isLoading: false,
    error: null,
    onEdit: jest.fn(),
    onDelete: jest.fn(),
    onCreateNew: jest.fn(),
    onRetry: jest.fn(),
    currentPage: 1,
    totalPages: 1,
    onPageChange: jest.fn(),
    total: 2,
  }

  beforeEach(() => {
    jest.clearAllMocks()
    // Reset window.confirm mock
    ;(window.confirm as jest.Mock).mockReturnValue(true)
  })

  it('should render loading state', () => {
    render(<UserList {...defaultProps} isLoading={true} />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('should render error state', () => {
    const errorMessage = 'Failed to load users'
    render(<UserList {...defaultProps} error={errorMessage} />)

    expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument()
    expect(screen.getByText('Retry')).toBeInTheDocument()
  })

  it('should call onRetry when retry button is clicked', async () => {
    const user = userEvent.setup()
    render(<UserList {...defaultProps} error="Network error" />)

    const retryButton = screen.getByText('Retry')
    await user.click(retryButton)

    expect(defaultProps.onRetry).toHaveBeenCalledTimes(1)
  })

  it('should render users list with correct data', () => {
    render(<UserList {...defaultProps} />)

    expect(screen.getByText('Users')).toBeInTheDocument()
    expect(screen.getByText('2 users total')).toBeInTheDocument()
    expect(screen.getByText('John Doe')).toBeInTheDocument()
    expect(screen.getByText('john@example.com')).toBeInTheDocument()
    expect(screen.getByText('Jane Smith')).toBeInTheDocument()
    expect(screen.getByText('jane@example.com')).toBeInTheDocument()
  })

  it('should render singular user count correctly', () => {
    const singleUser = [mockUsers[0]]
    render(<UserList {...defaultProps} users={singleUser} total={1} />)

    expect(screen.getByText('1 user total')).toBeInTheDocument()
  })

  it('should render empty state when no users', () => {
    render(<UserList {...defaultProps} users={[]} total={0} />)

    expect(screen.getByText('No users found')).toBeInTheDocument()
    expect(screen.getByText('Create your first user')).toBeInTheDocument()
  })

  it('should call onCreateNew when Add User button is clicked', async () => {
    const user = userEvent.setup()
    render(<UserList {...defaultProps} />)

    const addButton = screen.getByText('Add User')
    await user.click(addButton)

    expect(defaultProps.onCreateNew).toHaveBeenCalledTimes(1)
  })

  it('should call onCreateNew when Create your first user button is clicked', async () => {
    const user = userEvent.setup()
    render(<UserList {...defaultProps} users={[]} total={0} />)

    const createButton = screen.getByText('Create your first user')
    await user.click(createButton)

    expect(defaultProps.onCreateNew).toHaveBeenCalledTimes(1)
  })

  it('should call onEdit when edit button is clicked', async () => {
    const user = userEvent.setup()
    render(<UserList {...defaultProps} />)

    const editButtons = screen.getAllByText('Edit Icon')
    await user.click(editButtons[0])

    expect(defaultProps.onEdit).toHaveBeenCalledWith(mockUsers[0])
  })

  it('should call onDelete when delete is confirmed', async () => {
    const user = userEvent.setup()
    render(<UserList {...defaultProps} />)

    const deleteButtons = screen.getAllByText('Delete Icon')
    await user.click(deleteButtons[0])

    expect(window.confirm).toHaveBeenCalledWith('Are you sure you want to delete this user?')
    expect(defaultProps.onDelete).toHaveBeenCalledWith('1')
  })

  it('should not call onDelete when delete is cancelled', async () => {
    const user = userEvent.setup()
    ;(window.confirm as jest.Mock).mockReturnValue(false)

    render(<UserList {...defaultProps} />)

    const deleteButtons = screen.getAllByText('Delete Icon')
    await user.click(deleteButtons[0])

    expect(window.confirm).toHaveBeenCalledWith('Are you sure you want to delete this user?')
    expect(defaultProps.onDelete).not.toHaveBeenCalled()
  })

  it('should handle delete operation with loading state', async () => {
    const user = userEvent.setup()
    let resolveDelete: () => void
    const deletePromise = new Promise<void>((resolve) => {
      resolveDelete = resolve
    })

    defaultProps.onDelete.mockReturnValue(deletePromise)

    render(<UserList {...defaultProps} />)

    const deleteButtons = screen.getAllByText('Delete Icon')
    await user.click(deleteButtons[0])

    // The component should handle the async delete operation
    expect(defaultProps.onDelete).toHaveBeenCalledWith('1')

    // Resolve the promise to complete the delete operation
    resolveDelete!()
    await waitFor(() => {
      expect(defaultProps.onDelete).toHaveBeenCalledTimes(1)
    })
  })
})
