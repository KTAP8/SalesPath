import {
  Platform,
  Text,
  View,
  TextInput,
  Pressable,
  StyleSheet,
} from "react-native";
import { useState } from "react";
import { Colors } from "@/constants/Colors";
import React from "react";

const Dropdown = ({
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
  const [showOptions, setShowOptions] = useState(false);

  if (Platform.OS === "web") {
    return (
      <View style={styles.wrapper}>
        <Text style={styles.label}>{label}</Text>
        <select
          value={selected}
          onChange={(e) => setSelected(e.target.value)}
          disabled={disabled}
          style={
            disabled
              ? { ...styles.webSelect, backgroundColor: Colors.white }
              : styles.webSelect
          }
        >
          <option value="">
            {disabled ? "Select salesman first" : `Select ${label}`}
          </option>
          {options.map((opt) => (
            <option key={opt} value={opt}>
              {opt}
            </option>
          ))}
        </select>
      </View>
    );
  }

  // Mobile Version
  return (
    <View style={styles.wrapper}>
      <Text style={styles.label}>{label}</Text>
      <Pressable
        style={[styles.input, disabled && styles.disabledInput]}
        onPress={() => !disabled && setShowOptions(!showOptions)}
      >
        <Text>
          {selected || (disabled ? "Select salesman first" : `Select ${label}`)}
        </Text>
      </Pressable>

      {showOptions &&
        !disabled &&
        options.map((opt) => (
          <Pressable
            key={opt}
            onPress={() => {
              setSelected(opt);
              setShowOptions(false);
            }}
            style={styles.option}
          >
            <Text>{opt}</Text>
          </Pressable>
        ))}
    </View>
  );
};

export default Dropdown;

const styles = StyleSheet.create({
  wrapper: {
    // marginBottom: 15,
  },
  label: {
    marginBottom: 5,
    fontSize: 14,
    // fontWeight: "600",
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
    fontSize: 13,
    fontFamily: "Lexend",
    backgroundColor: Colors.white,
    // paddingRight: 30,
  },
  option: {
    padding: 12,
    backgroundColor: "#fff",
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
  },
});
