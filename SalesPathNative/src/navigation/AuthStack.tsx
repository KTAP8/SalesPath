// src/contexts/AuthContext.tsx
import React, { createContext, useState, useEffect, ReactNode } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import jwtDecode, { JwtPayload } from "jwt-decode";
import api from "../api";

type User = { id: number; email: string };   // mirror backend's to_dict()

interface AuthContextProps {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextProps>(null as any);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  // 1️⃣ Read token from storage on app launch
  useEffect(() => {
    const bootstrap = async () => {
      const token = await AsyncStorage.getItem("access_token");
      if (token && !isExpired(token)) {
        const decoded = jwtDecode<{ sub: number; email: string } & JwtPayload>(token);
        setUser({ id: decoded.sub, email: decoded.email });
      } else {
        await AsyncStorage.removeItem("access_token");
      }
    };
    bootstrap();
  }, []);

  // 2️⃣ Hit /api/login and stash token
  const login = async (email: string, password: string) => {
    const res = await api.post("/login", { email, password });
    const { access_token, user } = res.data;
    await AsyncStorage.setItem("access_token", access_token);
    setUser(user);
  };

  // 3️⃣ Clear storage + state
  const logout = async () => {
    await AsyncStorage.removeItem("access_token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// small helper
const isExpired = (token: string) => {
  const { exp } = jwtDecode<JwtPayload>(token);
  return !exp || Date.now() >= exp * 1000;
};
