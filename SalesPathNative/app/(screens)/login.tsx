import { useState } from "react";
import { View, TextInput, Button, Text, Alert } from "react-native";
import axios from "axios";
import { saveSession } from "@/utils/auth";
import { router } from "expo-router";
import LayoutWithSidebar from "@/components/LayoutWithSidebar";
import Constants from "expo-constants";

export default function LoginScreen() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const API_URL =
    Constants.expoConfig?.extra?.API_URL || "http://127.0.0.1:5000";

  const handleLogin = async () => {
    try {
      const res = await axios.post(`${API_URL}/api/login`, {
        username,
        password,
      });

      const token = res.data.token;
      await saveSession(token);

      // Redirect based on role
      const role = JSON.parse(atob(token.split(".")[1])).Role;
      if (role === "admin") router.replace("/dashboard");
      else router.replace("/");
    } catch (err) {
      console.error(err);
      Alert.alert("Login failed", "Invalid username or password");
    }
  };

  return (
    <LayoutWithSidebar>
      <View style={{ padding: 20 }}>
        <Text>Username</Text>
        <TextInput
          value={username}
          onChangeText={setUsername}
          autoCapitalize="none"
        />
        <Text>Password</Text>
        <TextInput
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        <Button title="Login" onPress={handleLogin} />
      </View>
    </LayoutWithSidebar>
  );
}
