# User Management Frontend

A modern Next.js frontend application for user management with full CRUD operations.

## Features

- ✅ **Modern UI**: Built with Next.js 14 and Tailwind CSS
- ✅ **TypeScript**: Full type safety throughout the application
- ✅ **User CRUD**: Create, Read, Update, Delete users
- ✅ **Form Validation**: Client-side validation with Zod
- ✅ **API Integration**: Seamless integration with FastAPI backend
- ✅ **Responsive Design**: Mobile-first responsive design
- ✅ **Error Handling**: Comprehensive error handling and user feedback
- ✅ **Loading States**: Better UX with loading indicators
- ✅ **Pagination**: Built-in pagination for user listings
- ✅ **Docker Support**: Complete containerization
- ✅ **Comprehensive Testing**: 110+ unit tests with Jest and React Testing Library

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **TanStack Query** - Data fetching and caching
- **Axios** - HTTP client
- **Lucide React** - Icons
- **Jest** - Testing framework
- **React Testing Library** - Component testing utilities

## Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- FastAPI backend running on port 8000

### Development

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Docker

Build and run with Docker:

```bash
docker build -t user-management-frontend .
docker run -p 3000:3000 user-management-frontend
```

Or use the complete docker-compose setup from the root directory:

```bash
docker-compose up
```

## Project Structure

```
frontend/
├── src/
│   ├── __tests__/             # Test files
│   │   ├── components/       # Component tests
│   │   ├── lib/             # Library function tests
│   │   └── setup/           # Test configuration
│   ├── app/                  # Next.js App Router
│   │   ├── globals.css      # Global styles
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page
│   │   └── providers.tsx    # React Query provider
│   ├── components/          # React components
│   │   ├── ui/             # Reusable UI components
│   │   ├── user-form.tsx   # User form component
│   │   └── user-list.tsx   # User list component
│   ├── lib/                # Utilities
│   │   ├── api.ts         # API client
│   │   ├── utils.ts       # Utility functions
│   │   └── validations.ts # Zod schemas
│   └── types/             # TypeScript types
│       └── user.ts        # User type definitions
├── public/                # Static assets
├── jest.config.js         # Jest configuration
├── TESTING.md            # Testing documentation
├── Dockerfile            # Docker configuration
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind configuration
└── package.json         # Dependencies
```

## API Integration

The frontend connects to the FastAPI backend running on port 8570. The API endpoints used:

- `GET /api/v1/users` - List users with pagination
- `POST /api/v1/users` - Create new user
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8570
```

## Available Scripts

### Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Testing

- `npm test` - Run all tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage report

For detailed testing instructions including Docker usage, see [TESTING.md](./TESTING.md).
