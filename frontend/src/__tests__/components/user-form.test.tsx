import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { UserForm } from "@/components/user-form";
import { User } from "@/types/user";

// Mock the UI components
jest.mock("@/components/ui/button", () => ({
  Button: ({ children, ...props }: any) => (
    <button {...props}>{children}</button>
  ),
}));

jest.mock("@/components/ui/input", () => {
  const React = require("react");
  return {
    Input: React.forwardRef((props: any, ref: any) => (
      <input ref={ref} {...props} />
    )),
  };
});

jest.mock("@/components/ui/card", () => ({
  Card: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  CardContent: ({ children, ...props }: any) => (
    <div {...props}>{children}</div>
  ),
  CardHeader: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  CardTitle: ({ children, ...props }: any) => <h2 {...props}>{children}</h2>,
}));

jest.mock("@/components/ui/loading", () => ({
  Loading: ({ size, className }: any) => (
    <span className={className}>Loading...</span>
  ),
}));

describe("UserForm", () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  const defaultProps = {
    onSubmit: mockOnSubmit,
    title: "Create User",
    submitText: "Create",
  };

  it("should render form with title and submit button", () => {
    render(<UserForm {...defaultProps} />);

    expect(screen.getByText("Create User")).toBeInTheDocument();
    expect(screen.getByLabelText("Name")).toBeInTheDocument();
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Create" })).toBeInTheDocument();
  });

  it("should populate form with user data when editing", () => {
    const user: User = {
      id: "1",
      name: "John Doe",
      email: "john@example.com",
    };

    render(
      <UserForm
        {...defaultProps}
        user={user}
        title="Edit User"
        submitText="Update"
      />
    );

    expect(screen.getByDisplayValue("John Doe")).toBeInTheDocument();
    expect(screen.getByDisplayValue("john@example.com")).toBeInTheDocument();
    expect(screen.getByText("Edit User")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Update" })).toBeInTheDocument();
  });

  it("should show validation errors for empty fields", async () => {
    const user = userEvent.setup();
    render(<UserForm {...defaultProps} />);

    const submitButton = screen.getByRole("button", { name: "Create" });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText("Name is required")).toBeInTheDocument();
      expect(screen.getByText("Email is required")).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it("should not submit form with invalid email", async () => {
    const user = userEvent.setup();
    render(<UserForm {...defaultProps} />);

    const nameInput = screen.getByLabelText("Name");
    const emailInput = screen.getByLabelText("Email");
    const submitButton = screen.getByRole("button", { name: "Create" });

    await user.type(nameInput, "John Doe");
    await user.type(emailInput, "invalid-email");
    await user.click(submitButton);

    // Wait a bit to ensure form processing
    await new Promise((resolve) => setTimeout(resolve, 100));

    // Form should not submit with invalid email
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it("should submit form with valid data", async () => {
    const user = userEvent.setup();
    mockOnSubmit.mockResolvedValue(undefined);

    render(<UserForm {...defaultProps} />);

    const nameInput = screen.getByLabelText("Name");
    const emailInput = screen.getByLabelText("Email");
    const submitButton = screen.getByRole("button", { name: "Create" });

    await user.type(nameInput, "John Doe");
    await user.type(emailInput, "john@example.com");
    await user.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        name: "John Doe",
        email: "john@example.com",
      });
    });
  });

  it("should disable form when loading", () => {
    render(<UserForm {...defaultProps} isLoading={true} />);

    const nameInput = screen.getByLabelText("Name");
    const emailInput = screen.getByLabelText("Email");
    const submitButton = screen.getByRole("button");

    expect(nameInput).toBeDisabled();
    expect(emailInput).toBeDisabled();
    expect(submitButton).toBeDisabled();
    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("should reset form after successful creation", async () => {
    const user = userEvent.setup();
    mockOnSubmit.mockResolvedValue(undefined);

    render(<UserForm {...defaultProps} />);

    const nameInput = screen.getByLabelText("Name");
    const emailInput = screen.getByLabelText("Email");
    const submitButton = screen.getByRole("button", { name: "Create" });

    await user.type(nameInput, "John Doe");
    await user.type(emailInput, "john@example.com");
    await user.click(submitButton);

    await waitFor(() => {
      expect(nameInput).toHaveValue("");
      expect(emailInput).toHaveValue("");
    });
  });

  it("should not reset form after successful update", async () => {
    const user = userEvent.setup();
    const existingUser: User = {
      id: "1",
      name: "John Doe",
      email: "john@example.com",
    };
    mockOnSubmit.mockResolvedValue(undefined);

    render(<UserForm {...defaultProps} user={existingUser} />);

    const nameInput = screen.getByLabelText("Name");
    const submitButton = screen.getByRole("button", { name: "Create" });

    await user.clear(nameInput);
    await user.type(nameInput, "Jane Doe");
    await user.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalled();
    });

    // Form should not reset when editing existing user
    expect(nameInput).toHaveValue("Jane Doe");
  });

  it("should handle submission errors gracefully", async () => {
    const user = userEvent.setup();
    mockOnSubmit.mockRejectedValue(new Error("Submission failed"));

    render(<UserForm {...defaultProps} />);

    const nameInput = screen.getByLabelText("Name");
    const emailInput = screen.getByLabelText("Email");
    const submitButton = screen.getByRole("button", { name: "Create" });

    await user.type(nameInput, "John Doe");
    await user.type(emailInput, "john@example.com");
    await user.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalled();
    });

    // Form should remain populated after error
    expect(nameInput).toHaveValue("John Doe");
    expect(emailInput).toHaveValue("john@example.com");
  });
});
