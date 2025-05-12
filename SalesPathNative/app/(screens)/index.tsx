import { useEffect, useState, useMemo } from "react";
import {
  Text, FlatList, StyleSheet, View, ScrollView, TextInput,
  Modal, TouchableOpacity,
} from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import { SalesMan } from "@/constants/Types";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import NoteBox from "@/components/notebox";
import Button from "@/components/Button";
import FilterTextInput from "@/components/FilterTextInput";

const API_URL = Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";
const thaiSubRegions = [
  "Northern",
  "Northeastern", // also called Isan
  "Central",
  "Eastern",
  "Western",
  "Southern"
];


export default function SalesmenScreen() {
  const [regions, setRegions] = useState<string[]>([]);
  const [selectedSubRegion, setselectedSubRegion]= useState<string>();
  const [selectedRegion, setselectedRegion]= useState<string>();
useEffect(()=>{
  axios
  .get(`${API_URL}/api/clients`)
  .then((res) => {
    const clients = res.data as { ClientReg: string }[];
    const clientRegions = [...new Set(clients.map((c) => c.ClientReg))];
    console.log(clientRegions);
    setRegions(clientRegions);
  })
  .catch((err) => console.error("Client regions error:", err));

},[])
  return (
    <LayoutWithSidebar>
      <Text style={styles.header}>Salesmen</Text>
      <View style={styles.filters}>
        <NoteBox title=" Client's Name" textAreaheight="15px" textAreawidth="120%" placeholder="Susan J. Carr"></NoteBox>
        <FilterTextInput label="Client Region Location" options={thaiSubRegions} setSelected={setselectedRegion}></FilterTextInput>
        <FilterTextInput label="Client Sub-Region Location" options={regions} setSelected={setselectedSubRegion}></FilterTextInput>
      </View>

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
  filters: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: 100,
    padding: 10,
    backgroundColor: "#dbe0e4", // matches the light gray background
    borderRadius: 12,
  },
  container: { padding: 16 },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    fontSize: 16
  },
  suggestionList: {
    marginTop: 4,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    maxHeight: 200
  },
  suggestionItem: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#eee'
  },
  resultItem: {
    paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: '#eee'
  }

});
