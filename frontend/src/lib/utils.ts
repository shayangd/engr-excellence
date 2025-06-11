import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatError(error: any): string {
  if (error?.response?.data?.detail) {
    // Handle case where detail is a string
    if (typeof error.response.data.detail === "string") {
      return error.response.data.detail;
    }
    // Handle case where detail is an object - return fallback
    return "An unexpected error occurred";
  }
  if (error?.message) {
    return error.message;
  }
  return "An unexpected error occurred";
}
