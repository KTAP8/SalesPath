import { useEffect, useState } from "react";
import { View, Text, FlatList } from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import { SalesMan } from "@/constants/Types";

export default function SalesmenScreen() {
  const [salesmen, setSalesmen] = useState<SalesMan[]>([]);
  const API_URL =
    Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";

  useEffect(() => {
    axios
      .get(`${API_URL}/api/salesmen`)
      .then((res) => {
        console.log("✅ Full API Response:", res.data); // <- log full data here
        setSalesmen(res.data);
      })
      .catch((err) => {
        console.error("❌ API Fetch Error:", err);
      });
  }, []);

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 24, marginBottom: 10 }}>Salesmen</Text>
      <FlatList
        data={salesmen}
        keyExtractor={(item) => item.SalesName}
        renderItem={({ item }) => (
          <Text style={{ fontSize: 18 }}>{item.SalesName}</Text>
        )}
      />
    </View>
  );
}
