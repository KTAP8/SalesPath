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
import {Colors} from "@/constants/Colors";

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
  const [clients, setClients] = useState<string[]>([]);

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
        console.error("❌ Salesmen API Fetch Error:", err);
      });
  }, []);

  useEffect(()=> {
      axios
        .get(`${API_URL}/api/clients?sales=${selectedSalesman}`)
        .then((res) => {
          const clients = res.data;
          const newClients = [];
          {for(let x in clients){
            if(clients[x].SalesMan = selectedSalesman){
              newClients.push(clients[x].ClientId)
            }
          }}

          setClients(newClients);
          console.log(clients);
          console.log('New Clients: ' + newClients);
        })
        .catch((err) => console.error("Client regions error:", err));
    }
  , [selectedSalesman]);

  const handleExistingToggle = (newValue: boolean) => {
    setCheckExisting(newValue);
    if (newValue) {
      setCheckNew(false);
    }
  };
  const handleNewToggle = (newValue: boolean) => {
    setCheckNew(newValue);
    if (newValue) {
      setCheckExisting(false);
    }
  };

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
          onValueChange= {handleExistingToggle}
        ></CustomCheckbox>

        <CustomCheckbox 
          label={"NewClient"} 
          value={checkNew} 
          onValueChange= {handleNewToggle}
        ></CustomCheckbox>
      </View>

      {checkExisting == true && checkNew == false? (
        <View>
          <FilterTextInput
            label="Who are you?"
            options={clients}
            selected={selectedSalesman}
            setSelected={setSelectedSalesman}
          />

          <Text style = {styles.label}>What did you do?</Text>

          <View >
            <View style = {styles.checkBoxVertical}>
              <CustomCheckbox
                label={"Sale"} 
                value={sale} 
                onValueChange= {setSale}
              ></CustomCheckbox>
            </View>
            
            <View style = {styles.checkBoxVertical}></View>
              <CustomCheckbox
                label={"Customer Relation"} 
                value={custRelation} 
                onValueChange= {setCustRelation}
              ></CustomCheckbox>
            </View>

            <View style = {styles.checkBoxVertical}>
              <CustomCheckbox
                label={"Problem Report"} 
                value={probReport} 
                onValueChange= {setProbReport}
              ></CustomCheckbox>
            </View>

            <View style = {styles.checkBoxVertical}></View>
              <CustomCheckbox
                label={"Prospect Customer"} 
                value={prosCustomer} 
                onValueChange= {setProsCustomer}
              ></CustomCheckbox>
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
    justifyContent: 'space-evenly',
  },
  label: {
    marginBottom: 5,
    fontSize: 14,
    // fontWeight: "600",
    color: Colors.primaryBlue,
    fontFamily: "Lexend",
  }
});
