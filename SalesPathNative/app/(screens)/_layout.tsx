// app/(app)/_layout.tsx
import { Redirect, Slot, useSegments } from "expo-router";
import React, { useContext } from "react";
import { AuthContext } from "@/contexts/authContext";


export default function AppProtectedLayout() {
  const { user } = useContext(AuthContext);
  const segments = useSegments();          // e.g. ['(app)', 'dashboard']

  // 1️⃣ If not logged-in and user tries to access  /dashboard etc → redirect
  if (!user) {
    return <Redirect href="/login" />;
  }

  // 2️⃣ For logged-in users, wrap every page with the sidebar
  return (
    
      <Slot />                              

  );
}
