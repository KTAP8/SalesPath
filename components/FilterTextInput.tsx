import React, { useState } from "react";
import {
  Platform,
  Text,
  View,
  TextInput,
  Pressable,
  StyleSheet,
  ScrollView,
} from "react-native";
import { Colors } from "@/constants/Colors";

const FilterTextInput = ({
  label,
  options,
  selected,
  setSelected,
  disabled = false,
}: {
  label: string;
  options: string[];
  selected?: string;
  setSelected: (val: string) => void;
  disabled?: boolean;
}) => {
  const [searchTerm, setSearchTerm] = useState(selected || "");
  const [showOptions, setShowOptions] = useState(false);

  const filteredOptions = options.filter((opt) =>
    opt.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <View style={styles.wrapper}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        style={[
          styles.input,
          disabled && styles.disabledInput,
        ]}
        placeholder={disabled ? "Select salesman first" : `Select ${label}`}
        value={searchTerm}
        onChangeText={(text) => {
          setSearchTerm(text);
          setShowOptions(true);
        }}
        onFocus={() => {
          if (!disabled) setShowOptions(true);
        }}
        editable={!disabled}
      />

      {showOptions && !disabled && (
        <View style={styles.dropdownContainer}>
          <ScrollView style={styles.scrollBox}>
            {filteredOptions.length > 0 ? (
              filteredOptions.map((opt) => (
                <Pressable
                  key={opt}
                  onPress={() => {
                    setSelected(opt);
                    setSearchTerm(opt);
                    setShowOptions(false);
                  }}
                  style={styles.option}
                >
                  <Text>{opt}</Text>
                </Pressable>
              ))
            ) : (
              <View style={styles.option}>
                <Text style={{ color: "#aaa", fontStyle: "italic" }}>
                  No match found
                </Text>
              </View>
            )}
          </ScrollView>
        </View>
      )}
    </View>
  );
};

export default FilterTextInput;

const styles = StyleSheet.create({
  wrapper: {
    //marginBottom: 15,
  },
  label: {
    marginBottom: 5,
    fontSize: 14,
    color: Colors.primaryBlue,
    fontFamily: "Lexend",
  },
  input: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderWidth: 1,
    borderColor: Colors.grey,
    borderRadius: 8,
    backgroundColor: "#fff",
    fontSize: 16,
    fontFamily: "Lexend",
  },
  disabledInput: {
    backgroundColor: "#eee",
  },
  webSelect: {
    width: "100%",
    padding: 12,
    borderWidth: 1,
    borderColor: Colors.grey,
    borderRadius: 8,
    fontSize: 16,
    fontFamily: "Lexend",
    backgroundColor: Colors.white,
  },
  dropdownContainer: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    marginTop: 5,
    backgroundColor: "#fff",
  },
  scrollBox: {
    maxHeight: 200,
  },
  option: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
  },
});
