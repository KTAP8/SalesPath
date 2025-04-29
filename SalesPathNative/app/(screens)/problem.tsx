// app/screens/ProblemReportScreen.tsx
import { useEffect, useState } from "react";
import { View, Text, StyleSheet, ScrollView, Switch } from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import Dropdown from "@/components/dropdown";
import DatePickerInput from "@/components/DatePicker";
import Button from "@/components/Button";
import { Colors } from "@/constants/Colors";
import TableReport from "@/components/TableReport";
import CustomSwitch from "@/components/CustomSwitch";

const API_URL = Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";

type VisitRecord = {
  ClientId: string;
  ClientReg: string;
  ClientType: string;
  VisitDateTime: string;
  VisitId: number;
  ProblemNotes: string;
  Resolved: number; // ⚡ Force it to be number (not string!)
  SalesName: string;
};

export default function ProblemReportScreen() {
  const [salesmen, setSalesmen] = useState<string[]>([]);
  const [regions, setRegions] = useState<string[]>([]);
  const [selectedSalesman, setSelectedSalesman] = useState<
    string | undefined
  >();
  const [selectedRegion, setSelectedRegion] = useState<string | undefined>();
  const [fromDate, setFromDate] = useState<string>("");
  const [toDate, setToDate] = useState<string>("");
  const [reportData, setReportData] = useState<any[]>([]);
  const [wasToDateManuallySet, setWasToDateManuallySet] = useState(false);

  const handleSetToDate = (val: string) => {
    setToDate(val);
    setWasToDateManuallySet(true);
  };

  const tableHead = [
    "Client ID",
    "Region",
    "Type",
    "Date Visited",
    "Sales Name",
    "Visit ID",
    "Problem",
    "Solved?",
  ];

  const tableData = reportData.map((item) => [
    item.ClientId,
    item.ClientReg,
    item.ClientType,
    item.VisitDateTime
      ? new Date(item.VisitDateTime).toLocaleString("en-GB")
      : "",
    item.SalesName,
    item.VisitId,
    item.ProblemNotes || "-",
    <View style={{ alignItems: "center", justifyContent: "center" }}>
      <CustomSwitch
        value={item.Resolved === 1}
        onValueChange={(val) => toggleSolved(item.VisitId, val)}
      />
    </View>,
  ]);

  // Load options
  useEffect(() => {
    axios
      .get(`${API_URL}/api/salesmen`)
      .then((res) => setSalesmen(res.data.map((s: any) => s.SalesName)))
      .catch((err) => console.error("Salesmen error:", err));

    if (selectedSalesman) {
      axios
        .get(`${API_URL}/api/clients?sales=${selectedSalesman}`)
        .then((res) => {
          const clients = res.data as { ClientReg: string }[];
          const salesmanRegions = [...new Set(clients.map((c) => c.ClientReg))];
          setRegions(salesmanRegions);
        })
        .catch((err) => console.error("Client regions error:", err));
    } else {
      setRegions([]);
    }
  }, [selectedSalesman]);

  const handleSearch = async () => {
    try {
      let params = new URLSearchParams();
      params.append("activity", "Problem");
      if (selectedSalesman) params.append("sales", selectedSalesman);
      if (selectedRegion) params.append("region", selectedRegion);
      if (fromDate) params.append("from", fromDate);
      if (toDate) params.append("to", toDate);

      const response = await axios.get(
        `${API_URL}/api/visits?${params.toString()}`
      );

      // Normalize Resolved to number 🔥
      const normalizedData: VisitRecord[] = response.data.map((item: any) => ({
        ...item,
        Resolved: Number(item.Resolved),
      }));

      setReportData(normalizedData);
    } catch (err) {
      console.error("Visit search error:", err);
    }
  };

  const toggleSolved = async (visitId: number, newResolved: boolean) => {
    // 1. Update UI immediately
    setReportData((prev) =>
      prev.map((item) =>
        item.VisitId === visitId
          ? { ...item, Resolved: newResolved ? 1 : 0 }
          : item
      )
    );

    try {
      // 2. Update backend (no need to wait before updating UI)
      await axios.put(`${API_URL}/api/visit/${visitId}/resolve`, {
        Resolved: newResolved ? 1 : 0,
      });
      console.log(newResolved);
    } catch (error) {
      console.error("Error updating resolve status:", error);

      // ❌ If error, revert UI back
      setReportData((prev) =>
        prev.map((item) =>
          item.VisitId === visitId
            ? { ...item, Resolved: newResolved ? 0 : 1 } // revert back
            : item
        )
      );
    }
  };

  return (
    <LayoutWithSidebar>
      <View style={styles.container}>
        <Text style={styles.title}>Problem Report</Text>

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
            disabled={!selectedSalesman}
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
          <Button label="Search" onPress={handleSearch} size="S" />
        </View>

        {/* Table */}
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
  filters: {
    marginBottom: 20,
    flex: 1,
    flexDirection: "row",
    gap: 40,
    alignItems: "center",
    zIndex: 1000,
  },
  tableScrollView: {
    maxHeight: 500,
    borderWidth: 1,
    borderColor: Colors.grey,
    borderRadius: 8,
    backgroundColor: Colors.white,
  },
});
