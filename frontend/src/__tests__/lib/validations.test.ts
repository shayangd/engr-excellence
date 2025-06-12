import { userCreateSchema, userUpdateSchema } from "@/lib/validations";

describe("Validation Schemas", () => {
  describe("userCreateSchema", () => {
    it("should validate valid user data", () => {
      const validData = {
        name: "John Doe",
        email: "john.doe@example.com",
      };

      const result = userCreateSchema.safeParse(validData);
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.name).toBe("John Doe");
        expect(result.data.email).toBe("john.doe@example.com");
      }
    });

    it("should trim name and email", () => {
      const data = {
        name: "  John Doe  ",
        email: "john.doe@example.com",
      };

      const result = userCreateSchema.safeParse(data);
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.name).toBe("John Doe");
        expect(result.data.email).toBe("john.doe@example.com");
      }
    });

    it("should reject empty name", () => {
      const invalidData = {
        name: "",
        email: "john.doe@example.com",
      };

      const result = userCreateSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.issues[0].message).toBe("Name is required");
      }
    });

    it("should reject name that is too long", () => {
      const invalidData = {
        name: "a".repeat(101),
        email: "john.doe@example.com",
      };

      const result = userCreateSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.issues[0].message).toBe(
          "Name must be less than 100 characters"
        );
      }
    });

    it("should reject invalid email format", () => {
      const invalidData = {
        name: "John Doe",
        email: "invalid-email",
      };

      const result = userCreateSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.issues[0].message).toBe(
          "Please enter a valid email address"
        );
      }
    });

    it("should reject empty email", () => {
      const invalidData = {
        name: "John Doe",
        email: "",
      };

      const result = userCreateSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.issues[0].message).toBe("Email is required");
      }
    });

    it("should reject missing fields", () => {
      const invalidData = {};

      const result = userCreateSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.issues).toHaveLength(2);
      }
    });
  });

  describe("userUpdateSchema", () => {
    it("should validate valid partial user data", () => {
      const validData = {
        name: "Jane Doe",
      };

      const result = userUpdateSchema.safeParse(validData);
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.name).toBe("Jane Doe");
        expect(result.data.email).toBeUndefined();
      }
    });

    it("should validate email only update", () => {
      const validData = {
        email: "jane.doe@example.com",
      };

      const result = userUpdateSchema.safeParse(validData);
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.email).toBe("jane.doe@example.com");
        expect(result.data.name).toBeUndefined();
      }
    });

    it("should validate empty object", () => {
      const validData = {};

      const result = userUpdateSchema.safeParse(validData);
      expect(result.success).toBe(true);
    });

    it("should reject invalid email in update", () => {
      const invalidData = {
        email: "invalid-email",
      };

      const result = userUpdateSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.issues[0].message).toBe(
          "Please enter a valid email address"
        );
      }
    });

    it("should reject empty name in update", () => {
      const invalidData = {
        name: "",
      };

      const result = userUpdateSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.issues[0].message).toBe("Name is required");
      }
    });
  });
});
