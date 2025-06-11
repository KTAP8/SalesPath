import { useEffect, useState } from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import OverviewItem from "@/components/dashboard/OverviewItem";
import VisitCard from "@/components/dashboard/VisitCard";
import SaleCard from "@/components/dashboard/SaleCard";
import { Colors } from "@/constants/Colors";
import { Modal, Pressable, Platform } from "react-native";
import DateTimePicker from "@react-native-community/datetimepicker";
import RNPickerSelect from "react-native-picker-select";
import * as FileSystem from "expo-file-system";
import * as Sharing from "expo-sharing";
import DatePickerInput from "@/components/DatePicker";
import Button from "@/components/Button";
import DropdownValue from "@/components/dropdown_value_label";

const API_URL = Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";

type ClientStats = {
  SalesId: number; // <-- Add this
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
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedSalesName, setSelectedSalesName] = useState<string | null>(
    null
  );
  const [selectedMonth, setSelectedMonth] = useState<string>(
    new Date().toISOString().split("T")[0]
  );
  const [showPicker, setShowPicker] = useState(false);

  useEffect(() => {
    axios
      .get(`${API_URL}/api/clients-per-salesman?from=2025-04-01&to=2025-05-30`)
      .then((res) => setClientStats(res.data))
      .catch((err) => console.error("Clients error:", err));

    axios
      .get(`${API_URL}/api/revenue?from=2025-04-01&to=2025-05-30`)
      .then((res) => setRevenueStats(res.data))
      .catch((err) => console.error("Revenue error:", err));
  }, []);

  const handleGeneratePDF = async () => {
    const selectedSales = clientStats.find(
      (c) => c.SalesName === selectedSalesName
    );
    if (!selectedSales) return alert("Please select a salesman");

    const [year, month] = selectedMonth.split("-");

    const url = `${API_URL}/api/sales-report?salesman_id=${selectedSales.SalesId}&month=${year}-${month}`;

    try {
      const response = await axios.get(url, { responseType: "blob" });
      if (Platform.OS === "web") {
        const blob = new Blob([response.data], { type: "application/pdf" });
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = `sales_report_${year}_${month}.pdf`;
        link.click();
      } else {
        const path = `${FileSystem.documentDirectory}sales_report_${year}_${month}.pdf`;
        await FileSystem.writeAsStringAsync(path, response.data, {
          encoding: FileSystem.EncodingType.Base64,
        });
        await Sharing.shareAsync(path);
      }
    } catch (error) {
      console.error("Download error:", error);
      alert(`Failed to generate PDF. ${error}`);
    }
  };

  return (
    <LayoutWithSidebar>
      <ScrollView style={styles.container}>
        <Text style={styles.title}>Dashboard</Text>
        {/* Button to open modal */}
        <Pressable
          style={{
            backgroundColor: Colors.primaryGreen,
            padding: 10,
            borderRadius: 10,
            marginBottom: 20,
          }}
          onPress={() => setModalVisible(true)}
        >
          <Text
            style={{ color: "white", textAlign: "center", fontWeight: "bold" }}
          >
            Generate Sales Report (PDF)
          </Text>
        </Pressable>

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

        {/* Visit and Sale Cards */}
        <Text style={styles.sectionTitle}>Visits Overview</Text>
        <ScrollView horizontal style={styles.cardRow}>
          {clientStats.map((item, index) => (
            <VisitCard key={index} data={item} />
          ))}
        </ScrollView>

        <Text style={styles.sectionTitle}>Sale Overview</Text>
        <ScrollView horizontal style={styles.cardRow}>
          {revenueStats.map((item, index) => (
            <SaleCard key={index} data={item} />
          ))}
        </ScrollView>
      </ScrollView>

      {/* Modal */}
      <Modal visible={modalVisible} transparent animationType="fade">
        <View
          style={{
            backgroundColor: "rgba(0,0,0,0.5)",
            justifyContent: "center",
            alignItems: "center",
            height: "100%",
            padding: 50,
          }}
        >
          <View
            style={{
              width: "50%",
              backgroundColor: "white",
              borderRadius: 10,
              flex: 1,
              padding: 50,
              gap: 20,
              justifyContent: "space-between",
            }}
          >
            <View>
              <Text
                style={{
                  fontSize: 30,
                  fontWeight: "bold",
                  marginBottom: 10,
                  color: Colors.primaryBlue,
                  fontFamily: "Lexend",
                }}
              >
                Generate PDF Report
              </Text>
              <View style={{ gap: 30 }}>
                <View style={{ gap: 10 }}>
                  <DropdownValue
                    label="Salesman"
                    selected={selectedSalesName ?? undefined} // ✅ Convert null to undefined
                    setSelected={setSelectedSalesName}
                    options={clientStats.map((c) => ({
                      label: c.SalesName,
                      value: c.SalesName,
                    }))}
                    placeholder="Select Salesman"
                  />
                </View>

                <DatePickerInput
                  label="Select Month"
                  value={selectedMonth}
                  setValue={setSelectedMonth}
                />
              </View>
            </View>
            <View
              style={{
                flexDirection: "row",
                justifyContent: "space-between",
                marginTop: 20,
              }}
            >
              <Button
                label="Cancel"
                onPress={() => setModalVisible(false)}
                size="M"
                color={Colors.error}
              />
              <Button label="Generate" onPress={handleGeneratePDF} size="M" />
            </View>
          </View>
        </View>
      </Modal>
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
