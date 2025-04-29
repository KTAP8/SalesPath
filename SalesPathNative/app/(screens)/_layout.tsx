import { Tabs } from "expo-router";

//we use tabs instead of stack so that the sidebar and pages doesn't gets re-render everytime
export default function ScreensLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: { display: "none" }, // Hides the bottom tab bar
      }}
    />
  );
}
