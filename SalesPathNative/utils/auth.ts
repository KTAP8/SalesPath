import * as SecureStore from "expo-secure-store";
import { jwtDecode } from "jwt-decode";
import { Platform } from "react-native";

type Decoded = {
  Role: string;
  SalesName: string;
};

export async function saveSession(token: string) {
  const decoded = jwtDecode(token) as Decoded;
  if (Platform.OS === "web") {
    localStorage.setItem("token", token);
    localStorage.setItem("role", decoded.Role);
    localStorage.setItem("salesName", decoded.SalesName);
  } else {
    await SecureStore.setItemAsync("token", token);
    await SecureStore.setItemAsync("role", decoded.Role);
    await SecureStore.setItemAsync("salesName", decoded.SalesName);
  }
}

export async function clearSession() {
  if (Platform.OS === "web") {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("salesName");
  } else {
    await SecureStore.deleteItemAsync("token");
    await SecureStore.deleteItemAsync("role");
    await SecureStore.deleteItemAsync("salesName");
  }
}

export async function getSession() {
  if (Platform.OS === "web") {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
    const salesName = localStorage.getItem("salesName");
    return { token, role, salesName };
  } else {
    const token = await SecureStore.getItemAsync("token");
    const role = await SecureStore.getItemAsync("role");
    const salesName = await SecureStore.getItemAsync("salesName");
    return { token, role, salesName };
  }
}
