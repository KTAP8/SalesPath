// components/TableReport.tsx

import { View, Text, StyleSheet, Platform } from "react-native";
import { Table, Row, Rows } from "react-native-table-component";
import { Colors } from "@/constants/Colors";

type TableReportProps = {
  headers: string[];
  data: (string | number | null)[][];
};

const TableReport = ({ headers, data }: TableReportProps) => {
  return (
    <View style={styles.tableWrapper}>
      <View style={styles.tableContainer}>
        <Table borderStyle={{ borderWidth: 1, borderColor: "#ccc" }}>
          <Row data={headers} style={styles.head} textStyle={styles.headText} />
          {data.map((rowData, rowIndex) => (
            <Row
              key={rowIndex}
              data={rowData}
              textStyle={styles.text}
              style={rowIndex % 2 === 0 ? styles.rowEven : styles.rowOdd}
            />
          ))}
        </Table>
      </View>

      {data.length === 0 && (
        <Text style={styles.emptyText}>
          No data. Use the filter and press Search.
        </Text>
      )}
    </View>
  );
};

export default TableReport;

const styles = StyleSheet.create({
  tableWrapper: {
    flex: 1,
    // marginTop: 20,
  },
  tableContainer: {
    maxHeight: 400,
  },
  head: {
    height: 50,
    backgroundColor: Colors.primaryBlue,
    position: Platform.OS === "web" ? "sticky" : "relative",
    top: Platform.OS === "web" ? 0 : undefined,
    zIndex: Platform.OS === "web" ? 10 : undefined,
  },
  headText: {
    color: Colors.white,
    fontWeight: "bold",
    textAlign: "center",
    fontSize: 14,
    fontFamily: "Lexend",
  },
  text: {
    margin: 6,
    textAlign: "center",
    fontSize: 13,
    fontFamily: "Lexend",
  },
  rowEven: {
    backgroundColor: "#f8f9fa",
  },
  rowOdd: {
    backgroundColor: "#fff",
  },
  emptyText: {
    textAlign: "center",
    marginTop: 20,
    color: Colors.primaryBlue,
    fontSize: 16,
    fontFamily: "Lexend",
  },
});
