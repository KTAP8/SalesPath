// components/LayoutWithSidebar.tsx
import { View, StyleSheet } from "react-native";
import Sidebar from "./SideBar";
import { ReactNode } from "react";

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
    backgroundColor: "#e8eeee",
    padding: 20,
  },
});
