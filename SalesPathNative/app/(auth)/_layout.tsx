// app/(auth)/_layout.tsx
import { Stack } from "expo-router";
import { Text } from "react-native-svg";

export default function AuthLayout() {
  return <Stack screenOptions={{ headerShown: false }} />;
  
}
