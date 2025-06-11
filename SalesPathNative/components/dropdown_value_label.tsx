import {
  Platform,
  Text,
  View,
  Pressable,
  StyleSheet,
  FlatList,
} from "react-native";
import { useState } from "react";
import { Colors } from "@/constants/Colors";

type Option = { label: string; value: string };

type DropdownProps = {
  label: string;
  options: Option[];
  selected?: string;
  setSelected: (val: string) => void;
  disabled?: boolean;
  placeholder?: string;
};

const DropdownValue = ({
  label,
  options,
  selected,
  setSelected,
  disabled = false,
  placeholder,
}: DropdownProps) => {
  const [showOptions, setShowOptions] = useState(false);

  const getLabel = (value?: string) =>
    options.find((o) => o.value === value)?.label;

  if (Platform.OS === "web") {
    return (
      <View style={styles.wrapper}>
        <Text style={styles.label}>{label}</Text>
        <select
          value={selected ?? ""}
          onChange={(e) => setSelected(e.target.value)}
          disabled={disabled}
          style={
            disabled
              ? { ...styles.webSelect, backgroundColor: Colors.white }
              : styles.webSelect
          }
        >
          <option value="">
            {placeholder ??
              (disabled ? "Select salesman first" : `Select ${label}`)}
          </option>
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </View>
    );
  }

  // Mobile version
  return (
    <View style={styles.wrapper}>
      <Text style={styles.label}>{label}</Text>
      <Pressable
        style={[styles.input, disabled && styles.disabledInput]}
        onPress={() => !disabled && setShowOptions((prev) => !prev)}
      >
        <Text style={{ fontFamily: "Lexend" }}>
          {getLabel(selected) ||
            (placeholder ??
              (disabled ? "Select salesman first" : `Select ${label}`))}
        </Text>
      </Pressable>

      {showOptions && !disabled && (
        <View style={styles.dropdown}>
          <FlatList
            data={options}
            keyExtractor={(item) => item.value}
            renderItem={({ item }) => (
              <Pressable
                onPress={() => {
                  setSelected(item.value);
                  setShowOptions(false);
                }}
                style={styles.option}
              >
                <Text style={{ fontFamily: "Lexend" }}>{item.label}</Text>
              </Pressable>
            )}
          />
        </View>
      )}
    </View>
  );
};

export default DropdownValue;

const styles = StyleSheet.create({
  wrapper: {
    zIndex: 1,
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
    fontSize: 13,
    fontFamily: "Lexend",
    backgroundColor: Colors.white,
  },
  dropdown: {
    backgroundColor: "#fff",
    borderRadius: 8,
    marginTop: 4,
    overflow: "hidden",
    borderWidth: 1,
    borderColor: Colors.grey,
  },
  option: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
  },
});
