import { Pressable, Text, StyleSheet } from "react-native";
import { Colors } from "@/constants/Colors";

type ButtonProps = {
  label: string;
  onPress: () => void;
  disabled?: boolean;
  size: "S" | "M" | "L";
  color?: string; // ✅ Optional color
};

const Button = ({
  label,
  onPress,
  disabled = false,
  size,
  color,
}: ButtonProps) => {
  const backgroundColor = disabled
    ? styles.disabledButton.backgroundColor
    : color || Colors.primaryGreen;

  return (
    <Pressable
      onPress={onPress}
      style={[
        styles.button,
        { backgroundColor }, // ✅ Inline background color override
        size === "S" && styles.smallButton,
        size === "M" && styles.mediumButton,
        size === "L" && styles.largeButton,
      ]}
      disabled={disabled}
    >
      <Text
        style={[
          styles.buttonText,
          size === "S" && styles.smallText,
          size === "M" && styles.mediumText,
          size === "L" && styles.largeText,
        ]}
      >
        {label}
      </Text>
    </Pressable>
  );
};

export default Button;

const styles = StyleSheet.create({
  button: {
    borderRadius: 8,
    alignItems: "center",
    justifyContent: "center",
  },

  // Sizes for Button padding
  smallButton: {
    paddingVertical: 6,
    paddingHorizontal: 14,
  },
  mediumButton: {
    paddingVertical: 10,
    paddingHorizontal: 20,
  },
  largeButton: {
    paddingVertical: 14,
    paddingHorizontal: 28,
  },

  disabledButton: {
    backgroundColor: "#ccc",
  },

  // Sizes for Text
  buttonText: {
    color: Colors.white,
    fontFamily: "Lexend",
    fontWeight: "400",
  },
  smallText: {
    fontSize: 14,
  },
  mediumText: {
    fontSize: 16,
  },
  largeText: {
    fontSize: 18,
  },
});
