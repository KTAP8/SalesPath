import React, { useState } from 'react';
import { View, Text, TextInput, Alert, StyleSheet, TouchableOpacity } from 'react-native';
import { router } from "expo-router";
import Button from "../../components/Button"
import axios from 'axios'
import PopupModal from '@/components/Popup';

export default function SignupScreen() {
  const [rePassword, setRePassword] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isInputValid, setIsInputValid] = useState(true); // State to track input validity
  const [errorMessage, setErrorMessage] = useState(''); // State to store the error message
  const [showModal, setShowModal] = useState(false);
  const [modalTitle, setModalTitle] = useState('');
  const [modalDescription, setModalDescription] = useState(''); 

  const validateEmail = (email: string) => {
    const re = /\S+@\S+\.\S+/;
    return re.test(email);
  };

  const redirect = () => {
    if (isInputValid == true){
      return router.replace('/(auth)/login');
    }
  }

  const handleSignup = async () => {
    // Manual validation
    if (!rePassword.trim()) {
      setErrorMessage('Invalid Passowrd !!!');
      setIsInputValid(false);
      return;
    }
    if (!validateEmail(email)) {
      setErrorMessage('Invalid Email!!');
      setIsInputValid(false);
      return;
    }
    if (password !== rePassword) {
      setErrorMessage('Password Does Not match !!!');
      setIsInputValid(false);
      return;
    }

    setIsInputValid(true); // inputs are valid, proceed

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/users', {
          'email': email,
          'password': password,
        });

        // Show modal on success
        setModalTitle('Registration Successful');
        setModalDescription('You can try to login.');
        setShowModal(true);
      } catch (error: any) {
        console.error("Registration error:", error.response?.data || error.message);
        setModalTitle('Registration Failed');
        setModalDescription(error.response?.data?.message || 'Please try again.');
        setShowModal(true);
      }
    };


  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sign Up</Text>


      <TextInput
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
        style={styles.input}
      />

      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        style={styles.input}
      />

      <TextInput
        placeholder="Re-Password"
        value={rePassword}
        onChangeText={setRePassword}
        secureTextEntry
        style={styles.input}
      />

      {!isInputValid && errorMessage && (
          <Text style={styles.errorText}>{errorMessage}</Text>
        )}

      <Button label ="Create Account" onPress={handleSignup} size ='M'/>
        <TouchableOpacity style={styles.title} onPress={() => router.replace('/(auth)/login')}>
            <Text style={{textAlign: "center", margin: 10}}>Go back to Login</Text>
        </TouchableOpacity>
      
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
    marginBottom: 15, 
    fontSize: 16, 
    color: "#1A2A36", 
    borderWidth: 1, 
    borderColor: "#ccc"
  },
  button: { 
    backgroundColor: "#1A2A36", 
    paddingVertical: 15, 
    paddingHorizontal: 40, 
    borderRadius: 10, 
    width: "100%", 
    alignItems: "center" 
  },
  buttonText:{ 
    color: "#fff", 
    fontWeight: "bold", 
    fontSize: 16 
  },
    errorText: {
    color: 'red',
    fontSize: 14,
    marginBottom: 10, // Space between error message and button
    alignSelf: 'flex-end', // Align to the right
  }
});
