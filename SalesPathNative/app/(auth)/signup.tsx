import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity } from 'react-native';
import { router } from "expo-router";
import { Formik, FormikHelpers } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';

import Button from "../../components/Button";
import PopupModal from '@/components/Popup';

interface SignupFormValues {
  email: string;
  password: string;
  rePassword: string;
}

const SignupSchema = Yup.object().shape({
  email: Yup.string()
    .email('Invalid email format')
    .required('Email is required'),
  password: Yup.string()
    .min(6, 'Password must be at least 6 characters')
    .required('Password is required'),
  rePassword: Yup.string()
    .oneOf([Yup.ref('password')], 'Passwords must match')
    .required('Please confirm your password'),
});

export default function SignupScreen(): JSX.Element {
  const [showModal, setShowModal] = useState<boolean>(false);
  const [modalTitle, setModalTitle] = useState<string>('');
  const [modalDescription, setModalDescription] = useState<string>('');

  const handleSignup = async (
    values: SignupFormValues,
    { setSubmitting, resetForm }: FormikHelpers<SignupFormValues>
  ) => {
    try {
      await axios.post('http://127.0.0.1:5000/api/users', {
        email: values.email,
        password: values.password,
      });

      setModalTitle('Registration Successful');
      setModalDescription('You can try to login.');
      setShowModal(true);
      resetForm();
    } catch (error: any) {
      console.error("Registration error:", error.response?.data || error.message);
      setModalTitle('Registration Failed');
      setModalDescription(error.response?.data?.message || 'Please try again.');
      setShowModal(true);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sign Up</Text>

      <Formik
        initialValues={{ email: '', password: '', rePassword: '' }}
        validationSchema={SignupSchema}
        onSubmit={handleSignup}
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
              placeholder="Email"
              value={values.email}
              onChangeText={handleChange('email')}
              onBlur={handleBlur('email')}
              autoCapitalize="none"
              keyboardType="email-address"
              style={styles.input}
            />
            {touched.email && errors.email && <Text style={styles.errorText}>{errors.email}</Text>}

            <TextInput
              placeholder="Password"
              value={values.password}
              onChangeText={handleChange('password')}
              onBlur={handleBlur('password')}
              secureTextEntry
              style={styles.input}
            />
            {touched.password && errors.password && <Text style={styles.errorText}>{errors.password}</Text>}

            <TextInput
              placeholder="Re-Password"
              value={values.rePassword}
              onChangeText={handleChange('rePassword')}
              onBlur={handleBlur('rePassword')}
              secureTextEntry
              style={styles.input}
            />
            {touched.rePassword && errors.rePassword && <Text style={styles.errorText}>{errors.rePassword}</Text>}

            <Button
              label="Create Account"
              onPress={handleSubmit as any}
              size="M"
              disabled={isSubmitting}
            />

            <TouchableOpacity style={styles.title} onPress={() => router.replace('/(auth)/login')}>
              <Text style={{ textAlign: "center", margin: 10 }}>Go back to Login</Text>
            </TouchableOpacity>
          </>
        )}
      </Formik>

      <PopupModal
        visible={showModal}
        title={modalTitle}
        description={modalDescription}
        onClose={() => {
          setShowModal(false);
          if (modalTitle === 'Registration Successful') {
            router.replace('/(auth)/login');
          }
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
    backgroundColor: "#E3E6E9"
  },
  title: {
    fontSize: 32,
    fontWeight: "bold",
    marginBottom: 40,
    color: "#1A2A36",
    textAlign: 'center',
    justifyContent: 'center'
  },
  input: {
    width: "100%",
    backgroundColor: "#fff",
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
    fontSize: 16,
    color: "#1A2A36",
    borderWidth: 1,
    borderColor: "#ccc"
  },
  errorText: {
    color: 'red',
    fontSize: 14,
    marginBottom: 10,
    alignSelf: 'flex-end',
  }
});
