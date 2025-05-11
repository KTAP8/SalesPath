import { useState } from "react";
import {
  Platform,
  View,
  Text,
  Pressable,
  TextInput,
  StyleSheet,
} from "react-native";
import DateTimePicker from "@react-native-community/datetimepicker";
import { Colors } from "@/constants/Colors";

let WebDatePicker: any;
if (Platform.OS === "web") {
  WebDatePicker = require("react-datepicker").default;
  require("react-datepicker/dist/react-datepicker.css");
}

const DatePickerInput = ({
  label,
  value,
  setValue,
  setToDate, // ✅ optional
}: {
  label: string;
  value: string;
  setValue: (val: string) => void;
  setToDate?: (val: string) => void;
}) => {
  const [showPicker, setShowPicker] = useState(false);

  const parsedValue = value ? new Date(value) : new Date();

  if (Platform.OS === "web") {
    return (
      <View style={styles.wrapperWeb}>
        <Text style={styles.label}>{label}</Text>
        <WebDatePicker
          selected={parsedValue}
          onChange={(date: Date | null) => {
            if (date) {
              const isoDate = date.toISOString().split("T")[0];
              setValue(isoDate);

              if (setToDate) {
                const nextMonth = new Date(date);
                nextMonth.setMonth(nextMonth.getMonth() + 1);
                const nextMonthIso = nextMonth.toISOString().split("T")[0];
                setToDate(nextMonthIso);
              }
            } else {
              setValue("");
            }
          }}
          dateFormat="yyyy-MM-dd"
          popperPlacement="bottom-start"
          wrapperClassName="custom-datepicker-wrapper"
          customInput={<TextInput style={styles.input} />}
        />
      </View>
    );
  }

  return (
    <View style={styles.wrapperMobile}>
      <Text style={styles.label}>{label}</Text>
      <Pressable onPress={() => setShowPicker(true)} style={styles.input}>
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

const styles = StyleSheet.create({
  wrapperWeb: {
    // marginBottom: 15,
    zIndex: 10000, // ensure datepicker appears above everything
  },
  wrapperMobile: {
    marginBottom: 15,
  },
  label: {
    marginBottom: 5,
    fontFamily: "Lexend",
    fontSize: 14,
    color: Colors.primaryBlue,
  },
  input: {
    padding: 12,
    borderWidth: 1,
    borderColor: Colors.grey,
    borderRadius: 8,
    backgroundColor: Colors.white,
    fontFamily: "Lexend",
  },
});
