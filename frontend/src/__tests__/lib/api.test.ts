import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import { userApi } from "@/lib/api";
import { User, UserCreate, UserUpdate, UserListResponse } from "@/types/user";

// Create a mock adapter for the api instance
import api from "@/lib/api";
const mockAxios = new MockAdapter(api);

describe("User API", () => {
  beforeEach(() => {
    mockAxios.reset();
  });

  afterAll(() => {
    mockAxios.restore();
  });

  describe("getUsers", () => {
    it("should fetch users with pagination", async () => {
      const mockResponse: UserListResponse = {
        users: [
          { id: "1", name: "John Doe", email: "john@example.com" },
          { id: "2", name: "Jane Doe", email: "jane@example.com" },
        ],
        total: 2,
        page: 1,
        size: 10,
      };

      mockAxios.onGet("/users").reply(200, mockResponse);

      const result = await userApi.getUsers({ page: 1, size: 10 });

      expect(result).toEqual(mockResponse);
      expect(mockAxios.history.get[0].params).toEqual({ page: 1, size: 10 });
    });

    it("should handle API error", async () => {
      mockAxios.onGet("/users").reply(500, { detail: "Server error" });

      await expect(userApi.getUsers({ page: 1, size: 10 })).rejects.toThrow();
    });
  });

  describe("getUser", () => {
    it("should fetch a single user by ID", async () => {
      const mockUser: User = {
        id: "1",
        name: "John Doe",
        email: "john@example.com",
      };

      mockAxios.onGet("/users/1").reply(200, mockUser);

      const result = await userApi.getUser("1");

      expect(result).toEqual(mockUser);
    });

    it("should handle user not found", async () => {
      mockAxios.onGet("/users/999").reply(404, { detail: "User not found" });

      await expect(userApi.getUser("999")).rejects.toThrow();
    });
  });

  describe("createUser", () => {
    it("should create a new user", async () => {
      const userData: UserCreate = {
        name: "John Doe",
        email: "john@example.com",
      };

      const mockResponse: User = {
        id: "1",
        ...userData,
      };

      mockAxios.onPost("/users").reply(201, mockResponse);

      const result = await userApi.createUser(userData);

      expect(result).toEqual(mockResponse);
      expect(JSON.parse(mockAxios.history.post[0].data)).toEqual(userData);
    });

    it("should handle validation errors", async () => {
      const userData: UserCreate = {
        name: "",
        email: "invalid-email",
      };

      mockAxios.onPost("/users").reply(422, { detail: "Validation error" });

      await expect(userApi.createUser(userData)).rejects.toThrow();
    });
  });

  describe("updateUser", () => {
    it("should update an existing user", async () => {
      const userId = "1";
      const updateData: UserUpdate = {
        name: "Jane Doe",
      };

      const mockResponse: User = {
        id: userId,
        name: "Jane Doe",
        email: "john@example.com",
      };

      mockAxios.onPut(`/users/${userId}`).reply(200, mockResponse);

      const result = await userApi.updateUser(userId, updateData);

      expect(result).toEqual(mockResponse);
      expect(JSON.parse(mockAxios.history.put[0].data)).toEqual(updateData);
    });

    it("should handle user not found during update", async () => {
      mockAxios.onPut("/users/999").reply(404, { detail: "User not found" });

      await expect(
        userApi.updateUser("999", { name: "New Name" })
      ).rejects.toThrow();
    });
  });

  describe("deleteUser", () => {
    it("should delete a user", async () => {
      const userId = "1";

      mockAxios.onDelete(`/users/${userId}`).reply(204);

      await expect(userApi.deleteUser(userId)).resolves.toBeUndefined();
    });

    it("should handle user not found during deletion", async () => {
      mockAxios.onDelete("/users/999").reply(404, { detail: "User not found" });

      await expect(userApi.deleteUser("999")).rejects.toThrow();
    });
  });
});
