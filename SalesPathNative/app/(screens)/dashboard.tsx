import { Text } from "react-native";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";

export default function DashboardScreen() {
  return (
    <LayoutWithSidebar>
      <Text style={{ fontSize: 24 }}>📊 Dashboard</Text>
      <Text>This is a placeholder for the Dashboard screen.</Text>
    </LayoutWithSidebar>
  );
}
