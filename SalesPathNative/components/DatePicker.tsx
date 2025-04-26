import { useState } from "react";
import { Platform, View, Text, Pressable, TextInput } from "react-native";
import DateTimePicker from "@react-native-community/datetimepicker";

let WebDatePicker: any;
if (Platform.OS === "web") {
  WebDatePicker = require("react-datepicker").default;
  require("react-datepicker/dist/react-datepicker.css");
}

const DatePickerInput = ({
  label,
  value,
  setValue,
}: {
  label: string;
  value: string;
  setValue: (val: string) => void;
}) => {
  const [showPicker, setShowPicker] = useState(false);

  const parsedValue = value ? new Date(value) : new Date();

  if (Platform.OS === "web") {
    return (
      <View style={{ marginBottom: 15, zIndex: 10000 }}>
        <Text style={{ marginBottom: 5 }}>{label}</Text>
        <WebDatePicker
          selected={parsedValue}
          onChange={(date: Date) => {
            const isoDate = date.toISOString().split("T")[0];
            setValue(isoDate);
          }}
          dateFormat="yyyy-MM-dd"
          popperPlacement="bottom-start" // ✅ appear below input
          wrapperClassName="custom-datepicker-wrapper" // optional class
          customInput={
            <TextInput
              style={{
                padding: 12,
                borderWidth: 1,
                borderColor: "#ccc",
                borderRadius: 8,
                backgroundColor: "#fff",
              }}
            />
          }
        />
      </View>
    );
  }

  return (
    <View style={{ marginBottom: 15 }}>
      <Text style={{ marginBottom: 5 }}>{label}</Text>
      <Pressable
        onPress={() => setShowPicker(true)}
        style={{
          padding: 12,
          borderWidth: 1,
          borderColor: "#ccc",
          borderRadius: 8,
          backgroundColor: "#fff",
        }}
      >
        <Text>{value || `Select ${label} Date`}</Text>
      </Pressable>

      {showPicker && (
        <DateTimePicker
          value={parsedValue}
          mode="date"
          display="default"
          onChange={(_, selectedDate) => {
            setShowPicker(false);
            if (selectedDate) {
              const isoDate = selectedDate.toISOString().split("T")[0];
              setValue(isoDate);
            }
          }}
        />
      )}
    </View>
  );
};

export default DatePickerInput;
