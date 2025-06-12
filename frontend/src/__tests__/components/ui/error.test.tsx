import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErrorDisplay } from "@/components/ui/error";

// Mock Lucide icons
jest.mock("lucide-react", () => ({
  AlertCircle: ({ className }: any) => (
    <span data-testid="alert-icon" className={className}>
      Alert Icon
    </span>
  ),
}));

// Mock Button component
jest.mock("@/components/ui/button", () => ({
  Button: ({ children, onClick, ...props }: any) => (
    <button onClick={onClick} {...props}>
      {children}
    </button>
  ),
}));

describe("ErrorDisplay", () => {
  const mockOnRetry = jest.fn();

  beforeEach(() => {
    mockOnRetry.mockClear();
  });

  it("should render error message", () => {
    render(
      <ErrorDisplay message="Custom error message" onRetry={mockOnRetry} />
    );

    expect(screen.getByText("Custom error message")).toBeInTheDocument();
    expect(screen.getByText("Something went wrong")).toBeInTheDocument(); // This is the heading
  });

  it("should render alert icon", () => {
    render(<ErrorDisplay message="Error message" onRetry={mockOnRetry} />);

    expect(screen.getByTestId("alert-icon")).toBeInTheDocument();
  });

  it("should render retry button", () => {
    render(<ErrorDisplay message="Error message" onRetry={mockOnRetry} />);

    const retryButton = screen.getByRole("button", { name: /try again/i });
    expect(retryButton).toBeInTheDocument();
  });

  it("should not render retry button when onRetry is not provided", () => {
    render(<ErrorDisplay message="Error message" />);

    const retryButton = screen.queryByRole("button", { name: /try again/i });
    expect(retryButton).not.toBeInTheDocument();
  });

  it("should call onRetry when retry button is clicked", async () => {
    const user = userEvent.setup();
    render(<ErrorDisplay message="Error message" onRetry={mockOnRetry} />);

    const retryButton = screen.getByRole("button", { name: /try again/i });
    await user.click(retryButton);

    expect(mockOnRetry).toHaveBeenCalledTimes(1);
  });

  it("should have proper styling classes", () => {
    render(<ErrorDisplay message="Error message" onRetry={mockOnRetry} />);

    const container = screen.getByText("Error message").closest("div");
    expect(container).toHaveClass(
      "flex",
      "flex-col",
      "items-center",
      "justify-center",
      "p-8"
    );
  });

  it("should handle long error messages", () => {
    const longMessage =
      "This is a very long error message that should still be displayed properly in the error component";
    render(<ErrorDisplay message={longMessage} onRetry={mockOnRetry} />);

    expect(screen.getByText(longMessage)).toBeInTheDocument();
  });

  it("should handle empty error message", () => {
    render(<ErrorDisplay message="" onRetry={mockOnRetry} />);

    // Should still render the component structure
    expect(screen.getByTestId("alert-icon")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /try again/i })
    ).toBeInTheDocument();
  });
});
