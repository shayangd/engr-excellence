import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Input } from "@/components/ui/input";

describe("Input", () => {
  it("should render with default props", () => {
    render(<Input />);

    const input = screen.getByRole("textbox");
    expect(input).toBeInTheDocument();
    expect(input).toHaveClass("flex", "h-10", "w-full", "rounded-md");
  });

  it("should apply base styling classes", () => {
    render(<Input />);

    const input = screen.getByRole("textbox");
    expect(input).toHaveClass(
      "border",
      "border-input",
      "bg-background",
      "px-3",
      "py-2",
      "text-sm"
    );
  });

  it("should handle different input types", () => {
    const { rerender } = render(<Input type="email" />);
    expect(screen.getByRole("textbox")).toHaveAttribute("type", "email");

    rerender(<Input type="password" />);
    const passwordInput = screen.getByDisplayValue("");
    expect(passwordInput).toHaveAttribute("type", "password");

    rerender(<Input type="number" />);
    expect(screen.getByRole("spinbutton")).toHaveAttribute("type", "number");
  });

  it("should merge custom className", () => {
    render(<Input className="custom-class" />);

    const input = screen.getByRole("textbox");
    expect(input).toHaveClass("custom-class");
    expect(input).toHaveClass("flex"); // Should still have base classes
  });

  it("should handle value and onChange", async () => {
    const user = userEvent.setup();
    const handleChange = jest.fn();
    render(<Input value="" onChange={handleChange} />);

    const input = screen.getByRole("textbox");
    await user.type(input, "test value");

    expect(handleChange).toHaveBeenCalled();
  });

  it("should handle placeholder text", () => {
    render(<Input placeholder="Enter your name" />);

    const input = screen.getByPlaceholderText("Enter your name");
    expect(input).toBeInTheDocument();
  });

  it("should be disabled when disabled prop is true", () => {
    render(<Input disabled />);

    const input = screen.getByRole("textbox");
    expect(input).toBeDisabled();
    expect(input).toHaveClass(
      "disabled:cursor-not-allowed",
      "disabled:opacity-50"
    );
  });

  it("should forward ref correctly", () => {
    const ref = React.createRef<HTMLInputElement>();
    render(<Input ref={ref} />);

    expect(ref.current).toBeInstanceOf(HTMLInputElement);
  });

  it("should pass through HTML input attributes", () => {
    render(
      <Input
        id="test-input"
        name="testName"
        required
        maxLength={50}
        data-testid="custom-input"
        aria-label="Test input"
      />
    );

    const input = screen.getByRole("textbox");
    expect(input).toHaveAttribute("id", "test-input");
    expect(input).toHaveAttribute("name", "testName");
    expect(input).toHaveAttribute("required");
    expect(input).toHaveAttribute("maxLength", "50");
    expect(input).toHaveAttribute("data-testid", "custom-input");
    expect(input).toHaveAttribute("aria-label", "Test input");
  });

  it("should handle focus and blur events", () => {
    const handleFocus = jest.fn();
    const handleBlur = jest.fn();
    render(<Input onFocus={handleFocus} onBlur={handleBlur} />);

    const input = screen.getByRole("textbox");

    fireEvent.focus(input);
    expect(handleFocus).toHaveBeenCalledTimes(1);

    fireEvent.blur(input);
    expect(handleBlur).toHaveBeenCalledTimes(1);
  });

  it("should handle controlled input", async () => {
    const user = userEvent.setup();
    const TestComponent = () => {
      const [value, setValue] = React.useState("");
      return (
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          data-testid="controlled-input"
        />
      );
    };

    render(<TestComponent />);

    const input = screen.getByTestId("controlled-input");
    await user.type(input, "controlled value");

    expect(input).toHaveValue("controlled value");
  });

  it("should handle uncontrolled input with defaultValue", () => {
    render(<Input defaultValue="default text" />);

    const input = screen.getByDisplayValue("default text");
    expect(input).toBeInTheDocument();
  });

  it("should apply focus styles classes", () => {
    render(<Input />);

    const input = screen.getByRole("textbox");
    expect(input).toHaveClass(
      "focus-visible:outline-none",
      "focus-visible:ring-2",
      "focus-visible:ring-ring",
      "focus-visible:ring-offset-2"
    );
  });
});
