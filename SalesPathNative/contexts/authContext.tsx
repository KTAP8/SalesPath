import React, {
  createContext,
  useState,
  useEffect,
  useMemo,
  ReactNode,
} from "react";
import {router} from 'expo-router'
import AsyncStorage from "@react-native-async-storage/async-storage";
import { jwtDecode, JwtPayload } from "jwt-decode";
import api from "../src/api";                 // ← Axios instance with interceptor

/*───────────────────────────────────────────────────────────────────*/
/* 1) Type declarations                                             */
/*───────────────────────────────────────────────────────────────────*/
type User = { id: number; email: string };

interface AuthContextShape {
  user: User | null;
  login: (email: string, pwd: string) => Promise<void>;
  logout: () => Promise<void>;
  isReady: boolean | undefined;
}

/*───────────────────────────────────────────────────────────────────*/
/* 2) Create the context (empty bucket)                             */
/*───────────────────────────────────────────────────────────────────*/
export const AuthContext = createContext<AuthContextShape>(null as any);

/*───────────────────────────────────────────────────────────────────*/
/* 3) Provider component                                            */
/*───────────────────────────────────────────────────────────────────*/
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  /** a. internal state  — current user object or null */
  const [user, setUser] = useState<User | null>(null);
  const [ isReady, setIsReady] = useState<boolean | undefined>(undefined);

  /** b. On app launch, read token from storage & restore session */
  useEffect(() => {
    const restoreSession = async () => {
      try {
        const token = await AsyncStorage.getItem("access_token");
        console.log("Retrieved token:", token); // 🔍
  
        if (token && !isExpired(token)) {
          const decoded = jwtDecode<{ sub: number; email: string } & JwtPayload>(token);
          console.log("Decoded token:", decoded); // 🔍
          
          if (decoded?.sub) {
            setUser({ id: decoded.sub, email: decoded.email }); // or a placeholder
          } else {
            console.warn("Token missing required fields"); // 🔍
          }
        } else {
          console.warn("No token or token expired"); // 🔍
        }
      } catch (e) {
        console.error("Failed to restore session", e);
      } finally {
        setIsReady(true); // happens even if no user is set
      }
    };
    restoreSession();
  }, []);
  
  

  /** c. function to call backend, save token, update state */
  const login = async (email: string, password: string) => {
    const { data } = await api.post("/login", { email, password });
    await AsyncStorage.setItem("access_token", data.access_token);
    setUser(data.user);
  };

  /** d. gfunction to clear everythin */
  const logout = async () => {
    await AsyncStorage.removeItem("access_token");
    setUser(null);
    router.replace('/(auth)/login');
  };

  /** e. useMemo so Provider only re-renders children when *user* changes */
  const value = useMemo(() => ({ user, login, logout, isReady }), [user, isReady]);

  /** f. Provide!  Everything inside can call useContext(AuthContext) */
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
// children is a speical prop  in react that represents whatever  you wrap  inside  a component. 

//____________________________________________________________________
/* 4) Helper: JWT expiry check                                      */
/*───────────────────────────────────────────────────────────────────*/
const isExpired = (token: string) => {
  const { exp } = jwtDecode<JwtPayload>(token);
  return !exp || Date.now() >= exp * 1000;
};
