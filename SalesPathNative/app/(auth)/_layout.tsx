// app/(auth)/_layout.tsx
import { Slot, Stack } from "expo-router";
import { SafeAreaView } from "react-native";
import { Text } from "react-native-svg";

export default function AuthLayout() {
  return(
     <SafeAreaView style={{ flex: 1, backgroundColor: 'white' }}>
      <Slot />
    </SafeAreaView>
  );
}
