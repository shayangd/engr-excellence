export interface User {
  id: string;
  name: string;
  email: string;
}

export interface UserCreate {
  name: string;
  email: string;
}

export interface UserUpdate {
  name?: string;
  email?: string;
}

export interface UserListResponse {
  users: User[];
  total: number;
  page: number;
  size: number;
}

export interface ApiError {
  detail: string;
}

export interface PaginationParams {
  page: number;
  size: number;
}
