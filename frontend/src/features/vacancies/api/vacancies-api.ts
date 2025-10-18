import axios, { isAxiosError } from "axios";
import type { Job } from "../model/types";
const apiAddress = import.meta.env.VITE_API_URL;
console.log(apiAddress); // "https://mybackend.onrender.com"

const axiosClient = axios.create({
  baseURL: apiAddress,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getVacancies = async (): Promise<Job[]> => {
  try {
    const response = await axiosClient.get("/vacancies");

    return response.data;
  } catch (error) {
    if (isAxiosError(error)) {
      console.error(
        "Axios error fetching vacancies:",
        error.response?.data || error.message
      );
    } else console.error("Error fetching vacancies:", error);
    throw error;
  }
};
