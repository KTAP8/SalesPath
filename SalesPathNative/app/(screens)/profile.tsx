import { Text } from "react-native";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";

export default function ProfileScreen() {
  return (
    <LayoutWithSidebar>
      <Text style={{ fontSize: 24 }}>👤 Profile</Text>
      <Text>This is a placeholder for the Profile screen.</Text>
    </LayoutWithSidebar>
  );
}
