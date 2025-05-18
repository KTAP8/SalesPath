import { Tabs, useSegments, Redirect, useRouter } from "expo-router";
import { useEffect, useState } from "react";
import * as SecureStore from "expo-secure-store";

// We use Tabs instead of Stack so the sidebar and pages don't rerender every time
export default function ScreensLayout() {
  const [role, setRole] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [ready, setReady] = useState(false);
  const segments = useSegments(); // e.g., ['dashboard']
  const router = useRouter();

  useEffect(() => {
    (async () => {
      try {
        const storedToken = await SecureStore.getItemAsync("token");
        const storedRole = await SecureStore.getItemAsync("role");

        setToken(storedToken);
        setRole(storedRole);
        setReady(true);

        if (!storedToken && segments[0] !== "login") {
          router.replace("/login");
        }
      } catch (error) {
        console.error("❌ SecureStore error:", error);
        setReady(true);
      }
    })();
  }, []);

  if (!ready) return null;

  // 🧱 Route guard: Only admin can access dashboard
  const isDashboard = segments[0] === "dashboard";
  if (isDashboard && role !== "admin") {
    return <Redirect href="/" />;
  }

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: { display: "none" }, // Hides bottom tab bar
      }}
    />
  );
}
