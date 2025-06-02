import { View, Text, StyleSheet } from "react-native";
import { Colors } from "@/constants/Colors";
const OverviewItem = ({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) => (
  <View style={styles.overviewItem}>
    <Text style={styles.overviewLabel}>{label}:</Text>
    <Text style={styles.overviewValue}>{value}</Text>
  </View>
);

export default OverviewItem;

const styles = StyleSheet.create({
  overviewItem: {
    backgroundColor: "#ffffff",
    paddingVertical: 14,
    paddingHorizontal: 18,
    borderRadius: 20,
    marginRight: 10,
    marginBottom: 10,
    elevation: 2,
    minWidth: 110,
    borderColor: Colors.primaryBlue,
    borderWidth: 2,
  },
  //   overviewHighlight: {
  //     borderColor: "red",
  //     borderWidth: 1,
  //   },
  overviewLabel: {
    fontSize: 14,
    color: Colors.primaryBlue,
    fontFamily: "Lexend",
  },
  overviewValue: {
    fontSize: 20,
    fontWeight: "bold",
    color: Colors.primaryBlue,
  },
});
