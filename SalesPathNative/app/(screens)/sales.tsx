import { useEffect, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Pressable,
  FlatList,
  TextInput,
} from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import Dropdown from "@/components/dropdown";
import DatePickerInput from "@/components/DatePicker";

const API_URL = Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";

export default function SalesmanReportScreen() {
  const [salesmen, setSalesmen] = useState<string[]>([]);
  const [regions, setRegions] = useState<string[]>([]);
  const [selectedSalesman, setSelectedSalesman] = useState<
    string | undefined
  >();
  const [selectedRegion, setSelectedRegion] = useState<string | undefined>();
  const [fromDate, setFromDate] = useState<string>("");
  const [toDate, setToDate] = useState<string>("");

  const [reportData, setReportData] = useState<any[]>([]);

  // Load options (salesmen and regions)
  useEffect(() => {
    axios
      .get(`${API_URL}/api/salesmen`)
      .then((res) => setSalesmen(res.data.map((s: any) => s.SalesName)))
      .catch((err) => console.error("Salesmen error:", err));
    if (selectedSalesman) {
      // Only fetch when salesman selected
      axios
        .get(`${API_URL}/api/clients?sales=${selectedSalesman}`)
        .then((res) => {
          const clients = res.data as { ClientReg: string }[];
          const salesmanRegions = [...new Set(clients.map((c) => c.ClientReg))];
          setRegions(salesmanRegions);
        })
        .catch((err) => console.error("Client regions error:", err));
    } else {
      setRegions([]); // Clear regions if salesman unselected
    }
  }, [selectedSalesman]);

  const handleSearch = () => {
    let params = new URLSearchParams();
    if (selectedSalesman) params.append("sales", selectedSalesman);
    if (selectedRegion) params.append("region", selectedRegion);
    if (fromDate) params.append("from", fromDate);
    if (toDate) params.append("to", toDate);

    axios
      .get(`${API_URL}/api/visits?${params.toString()}`)
      .then((res) => setReportData(res.data))
      .catch((err) => console.error("Visit search error:", err));
  };

  return (
    <LayoutWithSidebar>
      <ScrollView style={styles.container}>
        <Text style={styles.title}>Salesman Report</Text>

        {/* Filters */}
        <View style={styles.filters}>
          <Dropdown
            label="Salesman"
            options={salesmen}
            selected={selectedSalesman}
            setSelected={setSelectedSalesman}
          />
          <Dropdown
            label="Region"
            options={regions}
            selected={selectedRegion}
            setSelected={setSelectedRegion}
            disabled={!selectedSalesman} // ✅
          />
          <View style={{ zIndex: 999, flex: 1, flexDirection: "row", gap: 10 }}>
            <DatePickerInput
              label="From"
              value={fromDate}
              setValue={setFromDate}
            />

            <DatePickerInput label="To" value={toDate} setValue={setToDate} />
          </View>

          <Pressable style={styles.searchButton} onPress={handleSearch}>
            <Text style={styles.searchButtonText}>Search</Text>
          </Pressable>
        </View>

        {/* Report Table */}
        <FlatList
          data={reportData}
          keyExtractor={(item) => item.VisitId.toString()}
          renderItem={({ item }) => (
            <View style={styles.row}>
              <Text style={styles.cell}>{item.ClientId}</Text>
              <Text style={styles.cell}>{item.ClientReg}</Text>
              <Text style={styles.cell}>{item.ClientType}</Text>
              <Text style={styles.cell}>
                {item.VisitDateTime?.split("T")[0]}
              </Text>
              <Text style={styles.cell}>{item.Activity}</Text>
              <Text style={styles.cell}>
                {item.InvoiceAmount ? `${item.InvoiceAmount}฿` : "-"}
              </Text>
              <Text style={styles.cell}>{item.Notes}</Text>
            </View>
          )}
          ListEmptyComponent={
            <Text style={{ marginTop: 20, textAlign: "center" }}>
              No data. Use the filter and press Search.
            </Text>
          }
        />
      </ScrollView>
    </LayoutWithSidebar>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, backgroundColor: "#e8eeee" },
  title: {
    fontSize: 26,
    fontWeight: "bold",
    marginBottom: 20,
    color: "#0b1c3e",
  },
  filters: { marginBottom: 20 },
  searchButton: {
    backgroundColor: "#3fd47c",
    padding: 10,
    borderRadius: 8,
    marginTop: 10,
  },
  searchButtonText: { textAlign: "center", color: "#fff", fontWeight: "bold" },
  row: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginBottom: 12,
    borderBottomWidth: 1,
    borderColor: "#ccc",
    paddingBottom: 8,
  },
  cell: { width: "40%", marginBottom: 5 },
  dropdown: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 5,
    marginTop: 4,
  },
  dropdownItem: { padding: 6 },
  selectedDropdownItem: { backgroundColor: "#3fd47c", color: "#fff" },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 8,
    borderRadius: 8,
    marginTop: 4,
  },
});
