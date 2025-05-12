import { useEffect, useState } from "react";
import { View, Text, ScrollView, StyleSheet } from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import { SalesMan } from "@/constants/Types";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import React from "react";
import Dropdown from "@/components/dropdown";
import CustomCheckbox from "@/components/CustomCheckBox";
import FilterTextInput from "@/components/FilterTextInput";
import {Colors} from "@/constants/Colors";
import NoteBox from "@/components/NoteBox";
import Button from "@/components/Button";

export default function SalesmenScreen() {
  const [salesmen, setSalesmen] = useState<SalesMan[]>([]);
  const [selectedSalesman, setSelectedSalesman] = useState<string>("");
  const [checkExisting, setCheckExisting] = useState(false);
  const [checkNew, setCheckNew] = useState(false);
  const [client, setClient] = useState<string>("");
  const [sale, setSale] = useState(false);
  const [custRelation, setCustRelation] = useState(false);
  const [probReport, setProbReport] = useState(false);
  const [clients, setClients] = useState<string[]>([]);
  const [note, setNote] = useState<string>("");
  const [pnote, setPnote] = useState<string>("");
  
  const [prosCustomer, setProsCustomer] = useState<string>("");
  const [regions, setRegions] = useState<string[]>([]);
  const [selectedSubRegion, setselectedSubRegion]= useState<string>("");
  const [selectedRegion, setselectedRegion]= useState<string>("");
  const [postResult, setPostResult] = useState<string | null>(null);
  const [postNewResult, setPostNewResult] = useState<string|null>(null);
  const API_URL =
    Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";

  const thaiSubRegions = [
    "Northern",
    "Northeastern", // also called Isan
    "Central",
    "Eastern",
    "Western",
    "Southern"
  ];

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

  const handleSalesToggle = (newValue: boolean) => {
    setSale(newValue);
    if (newValue) {
      setProbReport(false);
      setCustRelation(false);
    }
  };

  const handleRelationToggle = (newValue: boolean) => {
    setCustRelation(newValue);
    if (newValue) {
      setSale(false);
      setProbReport(false);
    }
  };

  const handleProblemToggle = (newValue: boolean) => {
    setProbReport(newValue);
    if (newValue) {
      setSale(false);
      setCustRelation(false);
    }
  };

  const isFormValid = selectedSalesman !== "" &&
                      (checkExisting || checkNew) &&
                      (sale || custRelation || probReport || prosCustomer)&&
                      note.trim().length > 0 &&
                      (!probReport || (probReport && pnote.trim().length > 0));

  const isNewFormValid = selectedSalesman !== "" &&
                         prosCustomer != "" &&
                         selectedRegion != "" &&
                         selectedSubRegion != "";

  const handleSubmit = () => {
    setPostResult(null); // Clear previous result
    const url = `${API_URL}/api/visits`; // Replace with your actual API endpoint

    const now = new Date();
    const isoString = now.toISOString();

    const data = {
      SalesName: selectedSalesman,
      ClientId: client,
      Activity: sale == true ? "Sale" : custRelation == true ? "Relation" : probReport == true ? "Problem": "",
      Notes: note,
      ProblemNotes: pnote,
      Resolved: 0,
      VisitDateTime: isoString,
    };

    axios
      .post(url, data, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response) => {
        setPostResult(JSON.stringify(response.data, null, 2));
      })
      .catch((error: any) => {
        if (axios.isAxiosError(error)) {
          setPostResult(`Error: ${error.message},  ${error.response?.data?.message || 'No server response'}`);
        } else {
          setPostResult(`Unexpected Error: ${error.message}`);
        }
      })
  }

  const handleNewSubmit = () => {
    setPostNewResult(null); // Clear previous result
    const url = `${API_URL}/api/prospects`; // Replace with your actual API endpoint


    const data = {
      ProspectReg: selectedRegion,
      ProspectSubReg: selectedSubRegion,
      SalesName: selectedSalesman,
      ProspectId: prosCustomer
    };

    axios
      .post(url, data, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response) => {
        setPostNewResult(JSON.stringify(response.data, null, 2));
      })
      .catch((error: any) => {
        if (axios.isAxiosError(error)) {
          setPostNewResult(`Error: ${error.message},  ${error.response?.data?.message || 'No server response'}`);
        } else {
          setPostNewResult(`Unexpected Error: ${error.message}`);
        }
      })
      console.log('data', data);
      console.log(postNewResult);
  }


  return (
    <LayoutWithSidebar>
      <ScrollView>
        <Text style={styles.header}>Salesmen</Text>
        <View style = {styles.dropdown}>
          <Dropdown 
              label = "Who are you?"
              options = {salesmen.map(item => item.SalesName)}
              selected = {selectedSalesman}
              setSelected = {setSelectedSalesman} 
          />
        </View>

        <View style={styles.checkbox}>
          <CustomCheckbox 
            label={"Existing Client"} 
            value={checkExisting} 
            onValueChange= {handleExistingToggle}
          ></CustomCheckbox>

          <View style={{marginLeft: 20}}>
          <CustomCheckbox 
            label={"NewClient"} 
            value={checkNew} 
            onValueChange= {handleNewToggle}
          ></CustomCheckbox>
          </View>
        </View>

        {checkExisting == true && checkNew == false? (
          <View style = {styles.dropdown}>
            <FilterTextInput
              label="Where did you go?"
              options={clients}
              selected={client}
              setSelected={setClient}
              disabled = {selectedSalesman == undefined ? true : false}
            />
            <Text style = {styles.label}>What did you do?</Text>

            <View >
              <View style = {styles.checkBoxVertical}>
                <CustomCheckbox
                  label={"Sale"} 
                  value={sale} 
                  onValueChange= {handleSalesToggle}
                ></CustomCheckbox>
              </View>
              
              <View style = {styles.checkBoxVertical}>
                <CustomCheckbox
                  label={"Customer Relation"} 
                  value={custRelation} 
                  onValueChange= {handleRelationToggle}
                ></CustomCheckbox>
              </View>

              <View style = {styles.checkBoxVertical}>
                <CustomCheckbox
                  label={"Problem Report"} 
                  value={probReport} 
                  onValueChange= {handleProblemToggle}
                ></CustomCheckbox>
              </View>

            </View>
            <NoteBox
              title= "Note"
              placeholder= "Enter your notes"
              textAreawidth= "220%"
              note = {note}
              setNote= {setNote}
            />
            {probReport == true ? (
            <View>
              <NoteBox
                title= "Problem Notes"
                placeholder= "Enter your Problem Notes"
                textAreawidth= "220%"
                note= {pnote}
                setNote= {setPnote}
              />
            </View>
            ):( <View></View>)}
            <View style = {{width: '15%'}}>
            <Button 
              label="Submit" 
              onPress = {handleSubmit} 
              size="S" 
              disabled = {!isFormValid}
            />
            </View>
          </View>

        ): checkExisting == false && checkNew == true ?(
          <View>
              <View style={styles.filters}>
                <NoteBox 
                  title="New Client's Name" 
                  textAreaheight="15px" 
                  textAreawidth="120%" 
                  placeholder="Enter new Client's Name"
                  note = {prosCustomer}
                  setNote = {setProsCustomer}
                ></NoteBox>
                <View style={styles.filterText}>
                  <FilterTextInput label="Client Region Location" options={thaiSubRegions} setSelected={setselectedRegion}></FilterTextInput>
                  <FilterTextInput label="Client Sub-Region Location" options={regions} setSelected={setselectedSubRegion}></FilterTextInput>
                 </View> 
              </View>
              <View style={{width: '15%'}}>
                <Button 
                  label="Submit" 
                  onPress = {handleNewSubmit} 
                  size="S" 
                  disabled = {!isNewFormValid}
                />
              </View>
          </View>
        ):(
          <View></View>
        )}
      </ScrollView>
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
    margin: 15,
    flexDirection: 'row',
    justifyContent: 'flex-start',
    width: '60%'
  },
  checkBoxVertical:{
    margin: 15,
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'space-evenly',
  },
  label: {
    marginTop: 5,
    marginBottom: 5,
    fontSize: 14,
    // fontWeight: "600",
    color: Colors.primaryBlue,
    fontFamily: "Lexend",
  }, dropdown: {
    width: "100%"
  },
  filters: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: 100,
    padding: 10,
    backgroundColor: "#dbe0e4", // matches the light gray background
    borderRadius: 12,
  }, filterText :{
    flexDirection: "row",
    gap: 100,
    padding: 38,
  }
})
