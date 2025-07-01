import { useEffect, useState, useContext } from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import Dropdown from "@/components/dropdown";
import Button from "@/components/Button";
import { Colors } from "@/constants/Colors";
import TableReport from "@/components/TableReport";
import { AuthContext } from "@/contexts/authContext";

const API_URL = Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";

type ProspectRecord = {
  ProspectId: number; // ✅ number not string
  ProspectReg: string;
  ProspectSubReg: string;
  SalesName: string;
};
export default function ProspectReportScreen() {
  const [salesmen, setSalesmen] = useState<string[]>([]);
  const [regions, setRegions] = useState<string[]>([]);
  const [selectedSalesman, setSelectedSalesman] = useState<
    string | undefined
  >();
  const [selectedRegion, setSelectedRegion] = useState<string | undefined>();
  const [prospects, setProspects] = useState<ProspectRecord[]>([]);
  const {token} = useContext(AuthContext)

  const tableHead = [
    "Client Name",
    "Client Region",
    "Client Subregion",
    "Date Visited",
    "Salesman",
  ];

  const tableData = prospects.map((item) => [
    item.ProspectId, // ✅ correct
    item.ProspectReg,
    item.ProspectSubReg,
    "-", // No VisitDate field in Prospect
    item.SalesName,
  ]);

  useEffect(() => {
    // Load salesmen for dropdown
    axios
      .get(`${API_URL}/api/salesmen`,{
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then((res) => setSalesmen(res.data.map((s: any) => s.SalesName)))
      .catch((err) => console.error("Salesmen load error:", err));
  }, []);

  useEffect(() => {
    if (selectedSalesman) {
      // Load client regions if salesman selected
      axios
        .get(`${API_URL}/api/clients?sales=${selectedSalesman}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then((res) => {
          const regionList = [
            ...new Set(res.data.map((c: any) => c.ClientReg)),
          ] as string[];
          setRegions(regionList);
        })
        .catch((err) => console.error("Regions load error:", err));
    } else {
      setRegions([]);
    }
  }, [selectedSalesman]);

  const handleFilter = () => {
    let params = new URLSearchParams();
    if (selectedSalesman) params.append("sales", selectedSalesman);
    if (selectedRegion) params.append("region", selectedRegion);

    axios
      .get(`${API_URL}/api/prospects?${params.toString()}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then((res) => setProspects(res.data))
      .catch((err) => console.error("Prospects fetch error:", err));
  };

  return (
    <LayoutWithSidebar>
      <View style={styles.container}>
        <Text style={styles.title}>Prospect Report</Text>

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
          <Button label="Filter" onPress={handleFilter} size="S" />
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
