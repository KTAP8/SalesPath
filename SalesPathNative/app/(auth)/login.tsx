import React, { useState, useContext } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
  GestureResponderEvent,
} from "react-native";
import { Redirect, router } from "expo-router";
import { AuthContext } from "@/contexts/authContext";
import Ionicons from '@expo/vector-icons/Ionicons';


export default function LoginScreen() {
  const { login } = useContext(AuthContext);          // ← call our context
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert("Error", "Please enter both email and password.");
      return;
    }


    try {
      /** 1️⃣  let AuthContext talk to Flask via api.ts */
      await login(email, password);                   // <-- throws on 401

      /** 2️⃣  success → go to first protected page */
      router.replace("/");                   // matches (app)/dashboard.tsx
    } catch (err: any) {
      const msg =
        err?.response?.data?.error || "Invalid credentials or server error.";
      Alert.alert("Login failed", msg);
    }
  };

  function handleCreateNew(event: GestureResponderEvent): void {
    router.replace('/(auth)/signup');
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <Text style={styles.title}>SalesPath</Text>

      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
      />

      {/* <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      /> */}
      <View style={{ width: '100%', position: 'relative' }}>
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        returnKeyType="done"
        onSubmitEditing={handleLogin}
        secureTextEntry={!showPassword}
      />
      <TouchableOpacity
        onPress={() => setShowPassword(prev => !prev)}
        style={{
          position: 'absolute',
          right: 15,
          top: 18,
          zIndex: 1,
        }}
      >
        <Ionicons
          name={showPassword ? "eye-off" : "eye"}
          size={22}
          color="#1A2A36"
        />
      </TouchableOpacity>
    </View>

      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Log In</Text>
      </TouchableOpacity>

      <View>
        <TouchableOpacity style={styles.title}onPress={handleCreateNew}>
          <Text>Create new User</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

/* ––––– Styles copied from your original file ––––– */
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#E3E6E9", alignItems: "center", justifyContent: "center", paddingHorizontal: 30 },
  title:     { fontSize: 32, fontWeight: "bold", marginBottom: 40, color: "#1A2A36", margin: 10 },
  input:     { width: "100%", backgroundColor: "#fff", borderRadius: 10, padding: 15, marginBottom: 15, fontSize: 16, color: "#1A2A36", borderWidth: 1, borderColor: "#ccc" },
  button:    { backgroundColor: "#1A2A36", paddingVertical: 15, paddingHorizontal: 40, borderRadius: 10, width: "100%", alignItems: "center" },
  buttonText:{ color: "#fff", fontWeight: "bold", fontSize: 16 },
});
