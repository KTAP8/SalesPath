import { useEffect, useState } from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import OverviewItem from "@/components/dashboard/OverviewItem";
import VisitCard from "@/components/dashboard/VisitCard";
import SaleCard from "@/components/dashboard/SaleCard";
import { Colors } from "@/constants/Colors";

const API_URL = Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";

type ClientStats = {
  SalesName: string;
  TotalClients: number;
  VisitedClients: number;
};

type RevenueStats = {
  SalesName: string;
  TotalRevenue: number;
  ClientSoldCount: number; // ✅ Add this line
};

export default function DashboardScreen() {
  const [clientStats, setClientStats] = useState<ClientStats[]>([]);
  const [revenueStats, setRevenueStats] = useState<RevenueStats[]>([]);

  useEffect(() => {
    axios
      .get(`${API_URL}/api/clients-per-salesman?from=2024-04-01&to=2024-04-30`)
      .then((res) => setClientStats(res.data))
      .catch((err) => console.error("Clients error:", err));

    axios
      .get(`${API_URL}/api/revenue?from=2024-04-01&to=2024-04-30`)
      .then((res) => setRevenueStats(res.data))
      .catch((err) => console.error("Revenue error:", err));
  }, []);

  return (
    <LayoutWithSidebar>
      <ScrollView style={styles.container}>
        <Text style={styles.title}>Dashboard</Text>

        {/* Overview counters */}
        <View style={styles.overviewContainer}>
          <OverviewItem
            label="Total Client"
            value={sum(clientStats.map((c) => c.TotalClients))}
          />
          <OverviewItem
            label="Total Client Visited"
            value={sum(clientStats.map((c) => c.VisitedClients))}
          />
          <OverviewItem
            label="Total Revenue"
            value={`${sum(
              revenueStats.map((r) => r.TotalRevenue)
            ).toLocaleString("en-US")} ฿`}
          />
        </View>

        {/* Visit Overview */}
        <Text style={styles.sectionTitle}>Visits Overview</Text>
        <ScrollView horizontal style={styles.cardRow}>
          {clientStats.map((item, index) => (
            <VisitCard key={index} data={item} />
          ))}
        </ScrollView>

        {/* Sale Overview */}
        <Text style={styles.sectionTitle}>Sale Overview</Text>
        <ScrollView horizontal style={styles.cardRow}>
          {revenueStats.map((item, index) => (
            <SaleCard key={index} data={item} />
          ))}
        </ScrollView>
      </ScrollView>
    </LayoutWithSidebar>
  );
}

const sum = (arr: number[]) => arr.reduce((acc, curr) => acc + curr, 0);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    paddingHorizontal: 20,
    // paddingTop: 30,
    // gap: 20,
  },
  title: {
    fontSize: 35,
    fontWeight: "bold",
    color: Colors.primaryBlue,
    marginBottom: 13,
    fontFamily: "Lexend",
  },

  // Overview summary
  overviewContainer: {
    flexDirection: "row",
    // justifyContent: "space-between",
    marginBottom: 20,
    flexWrap: "wrap",
  },

  // Sections
  sectionTitle: {
    fontSize: 25,
    fontWeight: "500",
    color: Colors.primaryBlue,
    marginBottom: 10,
    fontFamily: "Lexend",
  },
  cardRow: {
    marginBottom: 20,
  },
});
