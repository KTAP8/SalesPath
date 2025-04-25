import { Colors } from "@/constants/Colors";
import { View, Text, StyleSheet } from "react-native";
import { DollarSign } from "lucide-react-native";
const SaleCard = ({
  data,
}: {
  data: {
    SalesName: string;
    TotalRevenue: number;
    ClientSoldCount: number;
  };
}) => {
  return (
    <View style={styles.card}>
      <Text style={styles.cardTitle}>{data.SalesName}</Text>
      <Text style={styles.cardText}>Client Sold: {data.ClientSoldCount}</Text>
      <View style={styles.revenueBox}>
        <View style={styles.revenueIcon}>
          <DollarSign size={25} color={Colors.white}></DollarSign>
        </View>
        <View style={styles.revenueContent}>
          <Text style={styles.revenueLabel}>Revenue Generated</Text>
          <Text style={styles.revenueValue}>{data.TotalRevenue}฿</Text>
        </View>
      </View>
    </View>
  );
};

export default SaleCard;

const styles = StyleSheet.create({
  card: {
    // width: 180,
    backgroundColor: Colors.primaryBlue,
    padding: 14,
    borderRadius: 18,
    marginRight: 14,
    alignItems: "center",
  },
  cardTitle: {
    fontSize: 16,
    color: Colors.white,
    fontWeight: "bold",
    marginBottom: 6,
    fontFamily: "Lexend",
  },
  cardText: {
    fontSize: 13,
    color: Colors.white,
    fontFamily: "Lexend",
  },
  revenueBox: {
    flex: 1,
    flexDirection: "row",
    backgroundColor: Colors.lightBlue,
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderRadius: 12,
    marginTop: 12,
    alignItems: "center",
    gap: 8,
  },
  revenueContent: {},
  revenueLabel: {
    fontSize: 12,
    color: Colors.grey,
    fontFamily: "Lexend",
    fontWeight: "400",
  },
  revenueValue: {
    fontSize: 18,
    color: Colors.white,
    fontWeight: "400",
    fontFamily: "Lexend",
  },
  revenueIcon: {
    backgroundColor: Colors.primaryGreen,
    padding: 5,
    borderRadius: 12,
  },
});
