import { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  Platform,
  ScrollView,
  Pressable,
} from "react-native";
import { Table, Row, Rows } from "react-native-table-component";
import { Colors } from "@/constants/Colors";

type TableReportProps = {
  headers: string[];
  data: (string | number | null | JSX.Element)[][];
};

type SortConfig = {
  columnIndex: number;
  ascending: boolean;
} | null;

const TableReport = ({ headers, data }: TableReportProps) => {
  const [sortConfig, setSortConfig] = useState<SortConfig>(null);

  const handleSort = (columnIndex: number) => {
    setSortConfig((prev) => {
      if (prev && prev.columnIndex === columnIndex) {
        // Toggle ascending/descending
        return { columnIndex, ascending: !prev.ascending };
      } else {
        return { columnIndex, ascending: true };
      }
    });
  };

  const sortedData = [...data].sort((a, b) => {
    if (!sortConfig) return 0;

    const aVal = a[sortConfig.columnIndex];
    const bVal = b[sortConfig.columnIndex];

    // Skip sorting if value is a React element (like Switch)
    if (
      typeof aVal === "object" ||
      typeof bVal === "object" ||
      aVal == null ||
      bVal == null
    ) {
      return 0;
    }

    const isDateColumn = headers[sortConfig.columnIndex]
      .toLowerCase()
      .includes("date");

    if (isDateColumn) {
      const parseDate = (dateString: string) => {
        const [datePart, timePart] = dateString.split(", ");
        if (!datePart || !timePart) return new Date("Invalid Date");

        const [day, month, year] = datePart.split("/").map(Number);
        const [hours, minutes, seconds] = timePart.split(":").map(Number);

        return new Date(year, month - 1, day, hours, minutes, seconds);
      };

      if (typeof aVal !== "string" || typeof bVal !== "string") return 0;

      const aDate = parseDate(aVal);
      const bDate = parseDate(bVal);

      return sortConfig.ascending
        ? aDate.getTime() - bDate.getTime()
        : bDate.getTime() - aDate.getTime();
    }

    // Normal text/number compare
    if (typeof aVal === "number" && typeof bVal === "number") {
      return sortConfig.ascending ? aVal - bVal : bVal - aVal;
    }

    return sortConfig.ascending
      ? String(aVal).localeCompare(String(bVal))
      : String(bVal).localeCompare(String(aVal));
  });

  return (
    <View style={styles.outerWrapper}>
      <View style={styles.tableCard}>
        <ScrollView
          horizontal
          contentContainerStyle={styles.horizontalScrollContent}
        >
          <View style={styles.fullTable}>
            <Table borderStyle={{ borderWidth: 1, borderColor: "#ccc" }}>
              <Row
                data={headers.map((header, index) => (
                  <Pressable
                    key={index}
                    style={styles.headCell}
                    onPress={() => handleSort(index)}
                  >
                    <Text style={styles.headText}>
                      {header}{" "}
                      {sortConfig?.columnIndex === index
                        ? sortConfig.ascending
                          ? "↑"
                          : "↓"
                        : ""}
                    </Text>
                  </Pressable>
                ))}
                style={styles.head}
                flexArr={headers.map(() => 1)}
              />
              <Rows
                data={sortedData}
                textStyle={styles.text}
                style={styles.row}
                flexArr={headers.map(() => 1)}
              />
            </Table>
          </View>
        </ScrollView>
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
  outerWrapper: {
    flex: 1,
    width: "100%",
    alignItems: "center",
  },
  tableCard: {
    width: "100%",
    backgroundColor: "#fff",
    // borderRadius: 10,
    overflow: "hidden",
    // paddingHorizontal: 10, // control breathing room
  },
  horizontalScrollContent: {
    flexGrow: 1,
  },
  fullTable: {
    minWidth: "100%",
  },
  head: {
    height: 50,
    backgroundColor: Colors.primaryBlue,
    ...(Platform.OS === "web"
      ? { position: "sticky", top: 0, zIndex: 10 }
      : {}),
  },
  headCell: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingVertical: 12,
    paddingHorizontal: 8,
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
  row: {
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
