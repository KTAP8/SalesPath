import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons'; // Uses Expo icon set
import { useState } from 'react';

type Props = {
  label: string;
  value: boolean;
  onValueChange: (val: boolean) => void;
};

export default function CustomCheckbox({ label, value, onValueChange }: Props) {
  return (
    <TouchableOpacity style={styles.container} onPress={() => onValueChange(!value)}>
      <View style={[styles.checkbox, value && styles.checked]}>
        {value && <Ionicons name="checkmark" size={16} color="#fff" />}
      </View>
      <Text style={styles.label}>{label}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkbox: {
    width: 24,
    height: 24,
    borderWidth: 2,
    borderColor: '#0A1D3B', // Colors.primaryBlue equivalent
    borderRadius: 6,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  checked: {
    backgroundColor: '#0A1D3B',
  },
  label: {
    marginLeft: 10,
    fontSize: 16,
    color: '#0A1D3B',
    fontFamily: 'Lexend',
  },
});

