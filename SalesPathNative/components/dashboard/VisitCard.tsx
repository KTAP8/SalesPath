import { StyleSheet, View, Text } from "react-native";
import { ProgressChart } from "react-native-chart-kit";
import { Dimensions } from "react-native";
import { Colors } from "@/constants/Colors";

const screenWidth = Dimensions.get("window").width;

const VisitCard = ({
  data,
}: {
  data: { SalesName: string; TotalClients: number; VisitedClients: number };
}) => {
  const percentage =
    data.TotalClients > 0
      ? Math.min(data.VisitedClients / data.TotalClients, 1)
      : 0;

  // ✅ Debug log to check if percentage is correct
  //   console.log(`SalesName: ${data.SalesName}, Percentage: ${percentage}`);

  const datas = {
    data: [percentage],
  };

  return (
    <View style={styles.card}>
      <Text style={styles.cardTitle}>{data.SalesName}</Text>
      <Text style={styles.cardText}>Total Client: {data.TotalClients}</Text>
      <Text style={styles.cardText}>visited: {data.VisitedClients}</Text>

      <View style={styles.content}>
        <ProgressChart
          data={datas}
          width={100}
          height={100}
          strokeWidth={16}
          radius={32}
          chartConfig={{
            backgroundGradientFrom: Colors.primaryBlue,
            backgroundGradientFromOpacity: 0,
            backgroundGradientTo: Colors.primaryBlue,
            backgroundGradientToOpacity: 1,
            color: (opacity = 1) => `rgba(0, 255, 17, ${opacity})`,
            useShadowColorFromDataset: false,
          }}
          hideLegend={true}
        />
        <Text style={styles.donutText}>{Math.round(percentage * 100)}%</Text>
      </View>
    </View>
  );
};

export default VisitCard;

const styles = StyleSheet.create({
  card: {
    width: 180,
    backgroundColor: Colors.primaryBlue,
    padding: 14,
    borderRadius: 18,
    marginRight: 14,
    alignItems: "center",
    // height: 200,
  },
  cardTitle: {
    fontSize: 16,
    color: "#fff",
    fontWeight: "bold",
    marginBottom: 10,
    fontFamily: "Lexend",
  },
  cardText: {
    fontSize: 13,
    color: "#fff",
    fontFamily: "Lexend",
  },
  content: {
    alignItems: "center",
    // marginTop: 10,
    // paddingBottom: 10,
  },
  donutPlaceholder: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: "#fff",
    justifyContent: "center",
    alignItems: "center",
    // marginTop: 10,
  },
  donutText: {
    color: Colors.lightGreen,
    fontWeight: "bold",
    fontSize: 16,
    // marginTop: 10,
    fontFamily: "Lexend",
  },
});
