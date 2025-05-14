import * as SecureStore from "expo-secure-store";
import { jwtDecode } from "jwt-decode";

type Decoded = {
  Role: string;
  SalesName: string;
};

export async function saveSession(token: string) {
  const decoded = jwtDecode(token) as Decoded;
  await SecureStore.setItemAsync("token", token);
  await SecureStore.setItemAsync("role", decoded.Role);
  await SecureStore.setItemAsync("salesName", decoded.SalesName);
}

export async function clearSession() {
  await SecureStore.deleteItemAsync("token");
  await SecureStore.deleteItemAsync("role");
  await SecureStore.deleteItemAsync("salesName");
}

export async function getSession() {
  const token = await SecureStore.getItemAsync("token");
  const role = await SecureStore.getItemAsync("role");
  const salesName = await SecureStore.getItemAsync("salesName");
  return { token, role, salesName };
}
