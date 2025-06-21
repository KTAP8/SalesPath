// app/(app)/_layout.tsx
import { Redirect, Slot, useSegments } from "expo-router";
import React, { useContext } from "react";
import { AuthContext } from "@/contexts/authContext";
import { View, ActivityIndicator } from "react-native";



export default function AppProtectedLayout() {
  const { user, isReady } = useContext(AuthContext);    

  if (!isReady) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" />
      </View>
    );
  }
  
  // 1️⃣ If not logged-in and user tries to access  /dashboard etc → redirect
  if (isReady && !user) {
    return <Redirect href="/login" />;
  }

  // 2️⃣ For logged-in users, wrap every page with the sidebar
  return <Slot /> ;
}
