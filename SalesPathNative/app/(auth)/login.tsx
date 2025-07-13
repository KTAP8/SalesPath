import React, { useContext, useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from "react-native";
import { Redirect, router } from "expo-router";
import { AuthContext } from "@/contexts/authContext";
import Ionicons from '@expo/vector-icons/Ionicons';
import PopupModal from '@/components/Popup';


import { Formik, FormikHelpers } from 'formik';
import * as Yup from 'yup';

interface LoginFormValues {
  email: string;
  password: string;
}

const LoginSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email format').required('Email is required'),
  password: Yup.string().required('Password is required'),
});

export default function LoginScreen() {
  const { login } = useContext(AuthContext);
  const [showPassword, setShowPassword] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [modalTitle, setModalTitle] = useState('');
  const [modalDescription, setModalDescription] = useState('');


  const handleLogin = async (
    values: LoginFormValues,
    { setSubmitting, setErrors }: FormikHelpers<LoginFormValues>
  ) => {
    try {
      await login(values.email, values.password);
      router.replace("/");
    } catch (err: any) {
      const msg = err?.response?.data?.error || "Invalid credentials or server error.";
      setErrors({ email: '', password: '' });
  
      // 🧩 Use modal instead of Alert
      setModalTitle("Login Failed");
      setModalDescription(msg);
      setShowModal(true);
    } finally {
      setSubmitting(false);
    }
  };
  

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <Text style={styles.title}>SalesPath</Text>

      <Formik
        initialValues={{ email: '', password: '' }}
        validationSchema={LoginSchema}
        onSubmit={handleLogin}
      >
        {({
          handleChange,
          handleBlur,
          handleSubmit,
          values,
          errors,
          touched,
          isSubmitting
        }) => (
          <>
            <TextInput
              style={styles.input}
              placeholder="Email"
              value={values.email}
              onChangeText={handleChange('email')}
              onBlur={handleBlur('email')}
              autoCapitalize="none"
              keyboardType="email-address"
            />
            {touched.email && errors.email && (
              <Text style={styles.errorText}>{errors.email}</Text>
            )}

            <View style={{ width: '100%', position: 'relative' }}>
              <TextInput
                style={styles.input}
                placeholder="Password"
                value={values.password}
                onChangeText={handleChange('password')}
                onBlur={handleBlur('password')}
                secureTextEntry={!showPassword}
                returnKeyType="done"
                onSubmitEditing={() => handleSubmit()}
              />
              <TouchableOpacity
                onPress={() => setShowPassword(prev => !prev)}
                style={{ position: 'absolute', right: 15, top: 18, zIndex: 1 }}
              >
                <Ionicons
                  name={showPassword ? "eye-off" : "eye"}
                  size={22}
                  color="#1A2A36"
                />
              </TouchableOpacity>
            </View>
            {touched.password && errors.password && (
              <Text style={styles.errorText}>{errors.password}</Text>
            )}

            <TouchableOpacity
              style={styles.button}
              onPress={() => handleSubmit()}
              disabled={isSubmitting}
            >
              <Text style={styles.buttonText}>Log In</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.title} onPress={() => router.replace('/(auth)/signup')}>
              <Text>Create new User</Text>
            </TouchableOpacity>
          </>
        )}
      </Formik>
      
      <PopupModal
        visible={showModal}
        title={modalTitle}
        description={modalDescription}
        onClose={() => setShowModal(false)}
      />

    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#E3E6E9", alignItems: "center", justifyContent: "center", paddingHorizontal: 30 },
  title:     { fontSize: 32, fontWeight: "bold", marginBottom: 40, color: "#1A2A36", margin: 10 },
  input:     { width: "100%", backgroundColor: "#fff", borderRadius: 10, padding: 15, marginBottom: 10, fontSize: 16, color: "#1A2A36", borderWidth: 1, borderColor: "#ccc" },
  button:    { backgroundColor: "#1A2A36", paddingVertical: 15, paddingHorizontal: 40, borderRadius: 10, width: "100%", alignItems: "center", marginTop: 10 },
  buttonText:{ color: "#fff", fontWeight: "bold", fontSize: 16 },
  errorText: { color: 'red', fontSize: 14, marginBottom: 10, alignSelf: 'flex-end' }
});
