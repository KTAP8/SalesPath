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
import Button from "@/components/Button";
import { Colors } from "@/constants/Colors";
import TableReport from "@/components/TableReport";

const API_URL = Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";

export default function SalesmanReportScreen() {
  const [salesmen, setSalesmen] = useState<string[]>([]);
  const [regions, setRegions] = useState<string[]>([]);
  const [selectedSalesman, setSelectedSalesman] = useState<
    string | undefined
  >();
  const [selectedActivity, setSelectedActivity] = useState<
    string | undefined
  >();
  const [selectedRegion, setSelectedRegion] = useState<string | undefined>();
  const [fromDate, setFromDate] = useState<string>("");
  const [toDate, setToDate] = useState<string>("");

  const [reportData, setReportData] = useState<any[]>([]);
  const [wasToDateManuallySet, setWasToDateManuallySet] = useState(false);
  const handleSetToDate = (val: string) => {
    setToDate(val);
    setWasToDateManuallySet(true); // 🛡️ Mark that user edited it manually
  };

  const tableHead = [
    "Client ID",
    "Region",
    "Type",
    "Date Visited",
    "Sales Name",
    "Activity",
    "Items Sold",
    // "Revenue",
    "Notes",
  ];

  const tableData = reportData.map((item) => [
    item.ClientId,
    item.ClientReg,
    item.ClientType,
    item.VisitDateTime
      ? new Date(item.VisitDateTime).toLocaleString("en-GB")
      : "",
    item.SalesName,
    item.Activity,
    item.Sales ? JSON.stringify(item.Sales) : "-",
    // item.InvoiceAmount ? `${item.InvoiceAmount}฿` : "-",
    item.Notes,
  ]);

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
    if (selectedActivity) params.append("activity", selectedActivity);
    if (fromDate) params.append("from", fromDate);
    if (toDate) params.append("to", toDate);

    axios
      .get(`${API_URL}/api/visits?${params.toString()}`)
      .then((res) => setReportData(res.data))
      .catch((err) => console.error("Visit search error:", err));

    console.log(params.toString());
  };

  return (
    <LayoutWithSidebar>
      <View style={styles.container}>
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
          <Dropdown
            label="Activity"
            options={["Sale", "Problem", "Relation"]}
            selected={selectedActivity}
            setSelected={setSelectedActivity}
          />
          <DatePickerInput
            label="From"
            value={fromDate}
            setValue={setFromDate}
            setToDate={(newToDate) => {
              if (!wasToDateManuallySet) {
                setToDate(newToDate);
              }
            }}
          />

          <DatePickerInput
            label="To"
            value={toDate}
            setValue={handleSetToDate}
          />
          <Button label="Search" onPress={handleSearch} size="S"></Button>
        </View>

        {/* Report Table */}
        <View style={{ marginTop: 20 }}>
          <ScrollView style={styles.tableScrollView}>
            <TableReport headers={tableHead} data={tableData} />
          </ScrollView>
        </View>
      </View>
    </LayoutWithSidebar>
  );
}

const styles = StyleSheet.create({
  container: { paddingHorizontal: 20, backgroundColor: Colors.background },
  title: {
    fontSize: 35,
    fontWeight: "bold",
    marginBottom: 13,
    color: Colors.primaryBlue,
    fontFamily: "Lexend",
  },
  tableScrollView: {
    maxHeight: 500,
    borderWidth: 1,
    borderColor: Colors.grey,
    borderRadius: 8,
    backgroundColor: Colors.white,
  },
  filters: {
    marginBottom: 20,
    flex: 1,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-end",
    zIndex: 1000,
  },
  dropdown: {
    borderWidth: 1,
    borderColor: Colors.grey,
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
