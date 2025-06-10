import { Text, View } from "react-native";
import { useContext } from "react";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import { AuthContext } from "@/contexts/authContext";

export default function ProfileScreen() {
  const { user } = useContext(AuthContext);
  return (
    <LayoutWithSidebar>
      <Text style={{ fontSize: 24 }}>👤 Profile</Text>
      <Text>Email: {user?.email}</Text>
      <Text>This is a placeholder for the Profile screen.</Text>
    </LayoutWithSidebar>
  );
}
