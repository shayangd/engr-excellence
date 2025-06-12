import React from "react";
import { render, screen } from "@testing-library/react";
import { Loading, LoadingSpinner } from "@/components/ui/loading";

// Mock Lucide icons
jest.mock("lucide-react", () => ({
  Loader2: ({ className }: any) => (
    <div data-testid="loader-icon" className={className}>
      Loading...
    </div>
  ),
}));

describe("Loading Components", () => {
  describe("Loading", () => {
    it("should render with default size", () => {
      render(<Loading />);

      const loading = screen.getByTestId("loader-icon");
      expect(loading).toBeInTheDocument();
      expect(loading).toHaveClass("h-6", "w-6");
    });

    it("should render with small size", () => {
      render(<Loading size="sm" />);

      const loading = screen.getByTestId("loader-icon");
      expect(loading).toHaveClass("h-4", "w-4");
    });

    it("should render with large size", () => {
      render(<Loading size="lg" />);

      const loading = screen.getByTestId("loader-icon");
      expect(loading).toHaveClass("h-8", "w-8");
    });

    it("should apply custom className to container", () => {
      render(<Loading className="custom-loading" />);

      const container = screen.getByTestId("loader-icon").parentElement;
      expect(container).toHaveClass("custom-loading");
    });

    it("should have spinning animation class", () => {
      render(<Loading />);

      const loading = screen.getByTestId("loader-icon");
      expect(loading).toHaveClass("animate-spin");
    });
  });

  describe("LoadingSpinner", () => {
    it("should render loading spinner", () => {
      render(<LoadingSpinner />);

      const spinner = screen.getByTestId("loader-icon");
      expect(spinner).toBeInTheDocument();
    });

    it("should have proper styling classes", () => {
      render(<LoadingSpinner />);

      const container = screen.getByTestId("loader-icon").parentElement;
      expect(container).toHaveClass(
        "flex",
        "items-center",
        "justify-center",
        "p-8"
      );
    });

    it("should apply custom className", () => {
      render(<LoadingSpinner className="custom-spinner" />);

      const container = screen.getByTestId("loader-icon").parentElement;
      expect(container).toHaveClass("custom-spinner");
    });
  });
});
