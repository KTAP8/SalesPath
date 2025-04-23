import { useEffect, useState } from "react";
import { Text, FlatList, StyleSheet } from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import { SalesMan } from "@/constants/Types";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";

export default function SalesmenScreen() {
  const [salesmen, setSalesmen] = useState<SalesMan[]>([]);
  const API_URL =
    Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";

  useEffect(() => {
    axios
      .get(`${API_URL}/api/salesmen`)
      .then((res) => {
        console.log("✅ Full API Response:", res.data);
        setSalesmen(res.data);
      })
      .catch((err) => {
        console.error("❌ API Fetch Error:", err);
      });
  }, []);

  return (
    <LayoutWithSidebar>
      <Text style={styles.header}>Salesmen</Text>
      <FlatList
        data={salesmen}
        keyExtractor={(item) => item.SalesName}
        renderItem={({ item }) => (
          <Text style={styles.salesman}>{item.SalesName}</Text>
        )}
      />
    </LayoutWithSidebar>
  );
}

const styles = StyleSheet.create({
  header: {
    fontSize: 24,
    marginBottom: 10,
    color: "#0b1c3e",
    fontWeight: "bold",
  },
  salesman: {
    fontSize: 18,
    marginBottom: 6,
    color: "#333",
  },
});
