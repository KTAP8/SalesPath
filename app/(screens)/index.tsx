import { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import { SalesMan } from "@/constants/Types";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import React from "react";
import { Picker } from '@react-native-picker/picker';
import Dropdown from "@/components/dropdown";
import CustomCheckbox from "@/components/CustomCheckBox";
import CustomSwitch from "@/components/CustomSwitch";
import FilterTextInput from "@/components/FilterTextInput";

export default function SalesmenScreen() {
  const [salesmen, setSalesmen] = useState<SalesMan[]>([]);
 const [selectedSalesman, setSelectedSalesman] = useState<
    string
  >("");
  const [checkExisting, setCheckExisting] = useState(false);
  const [checkNew, setCheckNew] = useState(false);
  const [sale, setSale] = useState(false);
  const [custRelation, setCustRelation] = useState(false);
  const [probReport, setProbReport] = useState(false);
  const [prosCustomer, setProsCustomer] = useState(false);


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
      <Dropdown
          label = "Who are you?"
          options = {salesmen.map(item => item.SalesName)}
          selected = {selectedSalesman}
          setSelected = {setSelectedSalesman} 
      />


      <View style={styles.checkbox}>
        <CustomCheckbox 
          label={"Existing Client"} 
          value={checkExisting} 
          onValueChange= {setCheckExisting}
        ></CustomCheckbox>

        <CustomCheckbox 
          label={"NewClient"} 
          value={checkNew} 
          onValueChange= {setCheckNew}
        ></CustomCheckbox>
      </View>

      {checkExisting == true && checkNew == false? (
        <View>
          <FilterTextInput
            label="Who are you?"
            options={["Prahil", "Alex", "Joe", "John"]}
            selected={selectedSalesman}
            setSelected={setSelectedSalesman}
          />

          <Text style = {styles.salesman}>What did you do?</Text>

          <View style = {styles.checkBoxVertical}>
            
            <CustomCheckbox
              label={"Sale"} 
              value={sale} 
              onValueChange= {setSale}
            />

            <CustomCheckbox
              label={"Customer Relation"} 
              value={custRelation} 
              onValueChange= {setCustRelation}
            />

            <CustomCheckbox
              label={"Problem Report"} 
              value={probReport} 
              onValueChange= {setProbReport}
            />

            <CustomCheckbox
              label={"Prospect Customer"} 
              value={prosCustomer} 
              onValueChange= {setProsCustomer}
            />
          </View>

        </View>
      ): checkExisting == false && checkNew == true ?(
        <View>
          <Text>New</Text>
        </View>
      ):(
        <View></View>
      )}
      
      {/* <FlatList
        data={salesmen}
        keyExtractor={(item) => item.SalesName}
        renderItem={({ item }) => (
          <Text style={styles.salesman}>{item.SalesName}</Text>
        )}
      /> */}
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
  checkbox: {
    margin: 20,
    flexDirection: 'row',
    justifyContent: 'space-evenly'
  },
  checkBoxVertical:{
    margin: 15,
    flex: 1,
    flexDirection: 'column',
  }
});
