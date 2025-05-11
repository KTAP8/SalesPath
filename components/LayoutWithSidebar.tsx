// components/LayoutWithSidebar.tsx
import { View, StyleSheet } from "react-native";
import Sidebar from "./SideBar";
import { ReactNode } from "react";
import { Colors } from "@/constants/Colors";

export default function LayoutWithSidebar({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <View style={styles.container}>
      <Sidebar />
      <View style={styles.content}>{children}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "row",
  },
  content: {
    flex: 1,
    backgroundColor: Colors.background,
    padding: 20,
  },
});
