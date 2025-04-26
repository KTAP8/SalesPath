import RNPickerSelect from "react-native-picker-select";
import { View, Text } from "react-native";
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
}) => (
  <View style={{ marginBottom: 15 }}>
    <Text style={{ marginBottom: 5 }}>{label}</Text>
    <RNPickerSelect
      onValueChange={(value) => setSelected(value)}
      items={options.map((opt) => ({ label: opt, value: opt }))}
      value={selected}
      placeholder={{
        label: disabled ? `Select salesman first` : `Select ${label}`,
        value: undefined,
      }}
      disabled={disabled}
      style={{
        inputIOS: {
          padding: 12,
          borderWidth: 1,
          borderColor: "#ccc",
          borderRadius: 8,
          backgroundColor: disabled ? "#eee" : "#fff",
        },
        inputAndroid: {
          padding: 12,
          borderWidth: 1,
          borderColor: "#ccc",
          borderRadius: 8,
          backgroundColor: disabled ? "#eee" : "#fff",
        },
      }}
    />
  </View>
);

export default Dropdown;
