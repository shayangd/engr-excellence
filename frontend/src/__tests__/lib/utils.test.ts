import { cn, formatError } from "@/lib/utils";

describe("Utility Functions", () => {
  describe("cn", () => {
    it("should merge class names correctly", () => {
      const result = cn("text-red-500", "bg-blue-500");
      expect(result).toBe("text-red-500 bg-blue-500");
    });

    it("should handle conditional classes", () => {
      const result = cn(
        "base-class",
        true && "conditional-class",
        false && "hidden-class"
      );
      expect(result).toBe("base-class conditional-class");
    });

    it("should handle Tailwind conflicts", () => {
      const result = cn("text-red-500", "text-blue-500");
      expect(result).toBe("text-blue-500");
    });

    it("should handle empty inputs", () => {
      const result = cn();
      expect(result).toBe("");
    });

    it("should handle undefined and null values", () => {
      const result = cn("base-class", undefined, null, "other-class");
      expect(result).toBe("base-class other-class");
    });
  });

  describe("formatError", () => {
    it("should format API error with detail", () => {
      const error = {
        response: {
          data: {
            detail: "User not found",
          },
        },
      };

      const result = formatError(error);
      expect(result).toBe("User not found");
    });

    it("should format error with message", () => {
      const error = {
        message: "Network error",
      };

      const result = formatError(error);
      expect(result).toBe("Network error");
    });

    it("should handle error without response or message", () => {
      const error = {};

      const result = formatError(error);
      expect(result).toBe("An unexpected error occurred");
    });

    it("should handle null error", () => {
      const result = formatError(null);
      expect(result).toBe("An unexpected error occurred");
    });

    it("should handle undefined error", () => {
      const result = formatError(undefined);
      expect(result).toBe("An unexpected error occurred");
    });

    it("should prioritize response detail over message", () => {
      const error = {
        response: {
          data: {
            detail: "API error detail",
          },
        },
        message: "Generic error message",
      };

      const result = formatError(error);
      expect(result).toBe("API error detail");
    });

    it("should handle nested error structures", () => {
      const error = {
        response: {
          data: {
            detail: {
              message: "Nested error",
            },
          },
        },
      };

      const result = formatError(error);
      expect(result).toBe("An unexpected error occurred");
    });
  });
});
