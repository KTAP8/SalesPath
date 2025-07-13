// app/(app)/_layout.tsx
import { Redirect, Slot, router } from "expo-router";
import React, { useContext, useEffect } from "react";
import { AuthContext } from "@/contexts/authContext";
import { View, ActivityIndicator } from "react-native";
// import { jwtDecode, JwtPayload } from "jwt-decode";
// import AsyncStorage from "@react-native-async-storage/async-storage";



export default function AppProtectedLayout() {
  const { user, isReady, token, logout } = useContext(AuthContext);    
  
  if (!isReady) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  // useEffect(() => {
  //   const checkTokenValidity = async () => {
  //     if (!token) {
  //       router.replace("/(auth)/login");
  //       return;
  //     }

  //     try {
  //       const { exp } = jwtDecode<JwtPayload>(token);
  //       if (!exp || Date.now() >= exp * 1000) {
  //         await logout(); // Clears token + user state
  //         router.replace("/(auth)/login");
  //       }
  //     } catch (e) {
  //       console.warn("Invalid token format");
  //       await logout();
  //       router.replace("/(auth)/login");
  //     }
  //   };

  //   checkTokenValidity();
  // }, [user, isReady]);
  
  // 1️⃣ If not logged-in and user tries to access  /dashboard etc → redirect
  if (isReady && !user) {
    return <Redirect href="/login" />;
  }

  // 2️⃣ For logged-in users, wrap every page with the sidebar
  return <Slot /> ;
}
