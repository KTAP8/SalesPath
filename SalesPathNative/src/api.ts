// src/api.ts
import axios from "axios";
import { router } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";

import Constants from "expo-constants";

const api = axios.create({
  baseURL: `${Constants.expoConfig?.extra?.API_URL}/api`,
});

// ──────────── Attach token before every request ────────────
api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    if (err.response?.status === 401) {
      console.warn("🔐 401 received — logging out and refreshing");

      // Clean up token
      await AsyncStorage.removeItem("access_token");

      // Refresh the root layout
      router.reload(); // or use `router.reload()` if using Expo Router v3+
    }

    return Promise.reject(err);
  }
);

export default api;
