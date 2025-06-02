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
  const [searchTerm, setSearchTerm] = useState("");
  const [showOptions, setShowOptions] = useState(false);

  const filteredOptions = options.filter((opt) =>
    opt.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <View style={styles.wrapper}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        style={[styles.input, disabled && styles.disabledInput]}
        placeholder={disabled ? "Select salesman first" : `Select Client`}
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
        <>
          {/* Backdrop to detect outside touch */}
          <Pressable
            style={styles.backdrop}
            onPress={() => setShowOptions(false)}
          />
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
                    <Text
                      style={{
                        fontFamily: "Lexend",
                        color: Colors.primaryBlue,
                      }}
                    >
                      {opt}
                    </Text>
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
        </>
      )}
    </View>
  );
};

export default FilterTextInput;

const styles = StyleSheet.create({
  wrapper: {
    position: "relative",
    zIndex: 1,
  },
  label: {
    marginBottom: 10,
    fontSize: 14,
    color: Colors.primaryBlue,
    fontFamily: "Lexend",
    fontWeight: "600",
  },
  input: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderWidth: 1,
    borderColor: Colors.grey,
    borderRadius: 8,
    backgroundColor: "#fff",
    fontSize: 14,
    fontFamily: "Lexend",
  },
  disabledInput: {
    backgroundColor: "#eee",
  },
  dropdownContainer: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    marginTop: 5,
    backgroundColor: "#fff",
    zIndex: 10,
  },
  scrollBox: {
    maxHeight: 200,
  },
  option: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
  },
  backdrop: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: 5,
  },
});
