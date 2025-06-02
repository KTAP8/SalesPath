// components/CustomSwitch.tsx

import { Pressable, StyleSheet, View, Animated } from "react-native";
import { useEffect, useRef } from "react";
import { Colors } from "@/constants/Colors";

type CustomSwitchProps = {
  value: boolean;
  onValueChange: (val: boolean) => void;
};

const CustomSwitch = ({ value, onValueChange }: CustomSwitchProps) => {
  const translateX = useRef(new Animated.Value(value ? 20 : 0)).current;

  useEffect(() => {
    Animated.timing(translateX, {
      toValue: value ? 20 : 0,
      duration: 200, // animation speed (ms)
      useNativeDriver: true,
    }).start();
  }, [value]);

  return (
    <Pressable
      style={[styles.switchContainer, value && styles.switchOn]}
      onPress={() => onValueChange(!value)}
    >
      <Animated.View style={[styles.thumb, { transform: [{ translateX }] }]} />
    </Pressable>
  );
};

export default CustomSwitch;

const styles = StyleSheet.create({
  switchContainer: {
    width: 50,
    height: 30,
    borderRadius: 15,
    backgroundColor: Colors.grey,
    justifyContent: "center",
    padding: 3,
  },
  switchOn: {
    backgroundColor: Colors.primaryGreen,
  },
  thumb: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: Colors.white,
  },
});
