import React, {
  createContext,
  useState,
  useEffect,
  useMemo,
  ReactNode,
} from "react";
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

  /** b. On app launch, read token from storage & restore session */
  useEffect(() => {
    (async () => {
      const token = await AsyncStorage.getItem("access_token");
      if (token && !isExpired(token)) {
        const decoded = jwtDecode<{ sub: number; email: string } & JwtPayload>(token);
        setUser({ id: decoded.sub, email: decoded.email });
      }
    })();
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
  };

  /** e. useMemo so Provider only re-renders children when *user* changes */
  const value = useMemo(() => ({ user, login, logout }), [user]);

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
