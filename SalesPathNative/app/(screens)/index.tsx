import { useEffect, useState, useContext } from "react";
import { View, Text, ScrollView, StyleSheet, Modal, Pressable, } from "react-native";
import axios from "axios";
import Constants from "expo-constants";
import { SalesMan } from "@/constants/Types";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import React from "react";
import Dropdown from "@/components/dropdown";
import CustomCheckbox from "@/components/CustomCheckBox";
import FilterTextInput from "@/components/FilterTextInput";
import { Colors } from "@/constants/Colors";
import NoteBox from "@/components/NoteBox";
import Button from "@/components/Button";
import { AuthContext } from "@/contexts/authContext";

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
  const [provinces, setProvinces] = useState<any[]>([]);
  const [amphures, setAmphures] = useState<any[]>([]);
  const [selectedRegion, setselectedRegion] = useState<string>("");
  const [selectedSubRegion, setselectedSubRegion] = useState<string>("");
  const [postResult, setPostResult] = useState<string | null>(null);
  const [postNewResult, setPostNewResult] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [modalMessage, setModalMessage] = useState("");
  const API_URL =
    Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";
  const {token} = useContext(AuthContext)

  useEffect(() => {
    axios
      .get(`${API_URL}/api/salesmen`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then((res) => {
        console.log("✅ Full API Response:", res.data);
        setSalesmen(res.data);
      })
      .catch((err) => {
        console.error("❌ Salesmen API Fetch Error:", err);
      });
  }, []);

  useEffect(() => {
    axios
      .get(`${API_URL}/api/clients?sales=${selectedSalesman}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then((res) => {
        const clients = res.data;
        const newClients = [];
        {
          for (let x in clients) {
            if ((clients[x].SalesMan = selectedSalesman)) {
              newClients.push(clients[x].ClientId);
            }
          }
        }

        setClients(newClients);
        console.log(clients);
        console.log("New Clients: " + newClients);
      })
      .catch((err) => console.error("Client regions error:", err));
  }, [selectedSalesman]);

  useEffect(() => {
    fetch(
      "https://raw.githubusercontent.com/kongvut/thai-province-data/master/api_province_with_amphure_tambon.json"
    )
      .then((response) => response.json())
      .then((result) => {
        setProvinces(result);
      })
      .catch((err) => console.error("Province fetch error", err));
  }, []);

  const handleProvinceSelect = (provinceNameEn: string) => {
    setselectedRegion(provinceNameEn);
    const selectedProvince = provinces.find(
      (p) => p.name_en === provinceNameEn
    );
    setAmphures(selectedProvince?.amphure || []);
    setselectedSubRegion(""); // reset sub-region when province changes
  };

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

  const isFormValid =
    selectedSalesman !== "" &&
    (checkExisting || checkNew) &&
    (sale || custRelation || probReport || prosCustomer) &&
    note.trim().length > 0 &&
    (!probReport || (probReport && pnote.trim().length > 0));

  const isNewFormValid =
    selectedSalesman !== "" &&
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
      Activity:
        sale == true
          ? "Sale"
          : custRelation == true
            ? "Relation"
            : probReport == true
              ? "Problem"
              : "",
      Notes: note,
      ProblemNotes: pnote,
      Resolved: 0,
      VisitDateTime: isoString,
    };

    axios
      .post(url, data, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
      })
      .then((response) => {
        setPostResult(JSON.stringify(response.data, null, 2));
        setModalMessage("✅ Visit logged successfully!");
        setShowModal(true);
      })
      .catch((error: any) => {
        const message = axios.isAxiosError(error)
          ? `❌ Error: ${error.message}, ${error.response?.data?.message || "No server response"
          }`
          : `❌ Unexpected Error: ${error.message}`;

        setPostResult(message);
        setModalMessage(message);
        setShowModal(true);
      });
  };

  const handleNewSubmit = () => {
    setPostNewResult(null); // Clear previous result
    const url = `${API_URL}/api/prospects`; // Replace with your actual API endpoint

    const data = {
      ProspectReg: selectedRegion,
      ProspectSubReg: selectedSubRegion,
      SalesName: selectedSalesman,
      ProspectId: prosCustomer,
    };

    axios
      .post(url, data, {
        headers: {
          "Content-Type": "application/json",
           Authorization: `Bearer ${token}`
        },
      })
      .then((response) => {
        setPostNewResult(JSON.stringify(response.data, null, 2));
        setModalMessage("✅ New client visit logged successfully!");
        setShowModal(true);
      })
      .catch((error: any) => {
        const message = axios.isAxiosError(error)
          ? `❌ Error: ${error.message}, ${error.response?.data?.message || "No server response"
          }`
          : `❌ Unexpected Error: ${error.message}`;

        setPostNewResult(message);
        setModalMessage(message);
        setShowModal(true);
      });
    console.log("data", data);
    console.log(postNewResult);
  };

  return (
    <LayoutWithSidebar>
      <ScrollView style={{ paddingHorizontal: 20 }}>
        <Text style={styles.header}>Salesmen</Text>
        <View style={styles.dropdown}>
          <Dropdown
            label="Who are you?"
            options={salesmen.map((item) => item.SalesName)}
            selected={selectedSalesman}
            setSelected={setSelectedSalesman}
          />
        </View>

        <View style={styles.checkbox}>
          <CustomCheckbox
            label={"Existing Client"}
            value={checkExisting}
            onValueChange={handleExistingToggle}
          ></CustomCheckbox>

          <View style={{ marginLeft: 20 }}>
            <CustomCheckbox
              label={"New Client"}
              value={checkNew}
              onValueChange={handleNewToggle}
            ></CustomCheckbox>
          </View>
        </View>

        {checkExisting == true && checkNew == false ? (
          <View style={styles.dropdown}>
            <FilterTextInput
              label="Where did you go?"
              options={clients}
              selected={client}
              setSelected={setClient}
              disabled={selectedSalesman == undefined ? true : false}
            />
            <Text style={styles.label}>What did you do?</Text>

            <View>
              <View style={styles.checkBoxVertical}>
                <CustomCheckbox
                  label={"Sale"}
                  value={sale}
                  onValueChange={handleSalesToggle}
                ></CustomCheckbox>
              </View>

              <View style={styles.checkBoxVertical}>
                <CustomCheckbox
                  label={"Customer Relation"}
                  value={custRelation}
                  onValueChange={handleRelationToggle}
                ></CustomCheckbox>
              </View>

              <View style={styles.checkBoxVertical}>
                <CustomCheckbox
                  label={"Problem Report"}
                  value={probReport}
                  onValueChange={handleProblemToggle}
                ></CustomCheckbox>
              </View>
            </View>
            <NoteBox
              title="Note"
              placeholder="Enter your notes"
              textAreawidth="220%"
              note={note}
              setNote={setNote}
            />
            {probReport == true ? (
              <View>
                <NoteBox
                  title="Problem Notes"
                  placeholder="Enter your Problem Notes"
                  textAreawidth="220%"
                  note={pnote}
                  setNote={setPnote}
                />
              </View>
            ) : (
              <View></View>
            )}
            <View style={{ width: "15%", marginTop: 10 }}>
              <Button
                label="Submit"
                onPress={handleSubmit}
                size="S"
                disabled={!isFormValid}
              />
            </View>
          </View>
        ) : checkExisting == false && checkNew == true ? (
          <View>
            <View style={styles.filters}>
              <NoteBox
                title="New Client's Name"
                textAreaheight="15px"
                textAreawidth="120%"
                placeholder="Enter new Client's Name"
                note={prosCustomer}
                setNote={setProsCustomer}
              ></NoteBox>
              <View style={styles.filterText}>
                <FilterTextInput
                  label="Client Region Location"
                  options={provinces.map((p) => p.name_en)}
                  selected={selectedRegion}
                  setSelected={(val) => handleProvinceSelect(val)}
                />

                <FilterTextInput
                  label="Client Sub-Region Location"
                  options={amphures.map((a) => a.name_en)}
                  selected={selectedSubRegion}
                  setSelected={(val) => setselectedSubRegion(val)}
                />
              </View>
            </View>
            <View style={{ width: "15%" }}>
              <Button
                label="Submit"
                onPress={handleNewSubmit}
                size="S"
                disabled={!isNewFormValid}
              />
            </View>
          </View>
        ) : (
          <View></View>
        )}
        <Modal
          animationType="fade"
          transparent={true}
          visible={showModal}
          onRequestClose={() => setShowModal(false)}
        >
          <View style={styles.overlay}>
            <View style={styles.modalBox}>
              <Text style={styles.message}>{modalMessage}</Text>
              <Pressable
                onPress={() => setShowModal(false)}
                style={styles.button}
              >
                <Text style={styles.buttonText}>OK</Text>
              </Pressable>
            </View>
          </View>
        </Modal>
      </ScrollView>
    </LayoutWithSidebar>
  );
}

const styles = StyleSheet.create({
  header: {
    fontSize: 35,
    marginBottom: 10,
    color: "#0b1c3e",
    fontWeight: "bold",
    fontFamily: "Lexend",
  },
  salesman: {
    fontSize: 18,
    marginBottom: 6,
    color: "#333",
  },
  checkbox: {
    marginVertical: 15,
    flexDirection: "row",
    justifyContent: "flex-start",
    width: "60%",
  },
  checkBoxVertical: {
    margin: 15,
    flex: 1,
    flexDirection: "column",
    justifyContent: "space-evenly",
  },
  label: {
    marginTop: 5,
    marginBottom: 5,
    fontSize: 14,
    fontWeight: "600",
    color: Colors.primaryBlue,
    fontFamily: "Lexend",
  },
  dropdown: {
    width: "100%",
  },
  filters: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: 100,
    // padding: 10,
    backgroundColor: "#dbe0e4", // matches the light gray background
    borderRadius: 12,
  },
  filterText: {
    flexDirection: "row",
    gap: 100,
    padding: 38,
  },
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.4)",
    justifyContent: "center",
    alignItems: "center",
  },
  modalBox: {
    backgroundColor: "#fff",
    borderRadius: 10,
    padding: 20,
    width: "80%",
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 5,
  },
  message: {
    fontSize: 16,
    textAlign: "center",
    marginBottom: 20,
    fontFamily: "Lexend",
  },
  button: {
    backgroundColor: Colors.primaryBlue,
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 6,
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
    fontFamily: "Lexend",
  },
});
