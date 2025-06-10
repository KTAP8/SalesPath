// components/Sidebar.tsx
import { AuthContext } from "@/contexts/authContext";
import { useContext } from 'react'
import { View, Text, Pressable, StyleSheet, Image } from "react-native";
import {
  NotebookPen,
  Home,
  DollarSign,
  AlertTriangle,
  User,
  LogOut,
  PackagePlus,
} from "lucide-react-native";
import { TABS } from "@/constants/Tabs";
import { useRouter, usePathname } from "expo-router";
import { Colors } from "@/constants/Colors";

const Sidebar = () => {
  const router = useRouter();
  const pathname = usePathname();
  const {user, login, logout} = useContext(AuthContext);

  return (
    <View style={styles.sidebar}>
      <View style={styles.sidebarContent}>
        <Text style={styles.username}>testuser123</Text>
        <View style={styles.divider} />

        <Section title="SALESMAN">
          <MenuItem
            icon={NotebookPen}
            label={TABS.LOGGING}
            active={pathname === "/"}
            onPress={() => router.push("/")}
          />
        </Section>

        <Section title="ADMIN">
          <MenuItem
            icon={Home}
            label={TABS.DASHBOARD}
            active={pathname === "/dashboard"}
            onPress={() => router.push("/dashboard")}
          />
          <MenuItem
            icon={DollarSign}
            label={TABS.SALES}
            active={pathname === "/sales"}
            onPress={() => router.push("/sales")}
          />
          <MenuItem
            icon={AlertTriangle}
            label={TABS.PROBLEM}
            active={pathname === "/problem"}
            onPress={() => router.push("/problem")}
          />
          <MenuItem
            icon={PackagePlus}
            label={TABS.PROSPECT}
            active={pathname === "/prospect"}
            onPress={() => router.push("/prospect")}
          />
        </Section>

        <Section title="PROFILE SETTINGS">
          <MenuItem
            icon={User}
            label={TABS.PROFILE}
            active={pathname === "/profile"}
            onPress={() => router.push("/profile")}
          />
          <MenuItem
            icon={LogOut}
            label={TABS.SIGNOUT}
            active={pathname === "/Logout"}
            onPress={() => logout()}
          />
        </Section>
      </View>

      <View style={styles.footer}>
        <Image
          source={require("@/assets/images/logo_SalesPath.png")}
          style={styles.logo}
          resizeMode="contain"
        />
      </View>
    </View>
  );
};

const Section = ({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) => (
  <View style={styles.section}>
    <Text style={styles.sectionTitle}>{title}</Text>
    {children}
  </View>
);

type MenuItemProps = {
  icon: React.ElementType;
  label: string;
  active?: boolean;
  onPress?: () => void;
};

const MenuItem = ({
  icon: Icon,
  label,
  active = false,
  onPress,
}: MenuItemProps) => (
  <Pressable
    onPress={onPress}
    style={[styles.menuItem, active && styles.activeMenuItem]}
  >
    <Icon
      color={active ? Colors.white : Colors.primaryGreen}
      size={15}
      style={active ? styles.iconActive : styles.icon}
    />
    <Text style={styles.menuLabel}>{label}</Text>
  </Pressable>
);

const styles = StyleSheet.create({
  // sidebar: {
  //   width: 260,
  //   backgroundColor: Colors.primaryBlue,
  //   paddingHorizontal: 19,
  //   paddingTop: 27,
  //   // justifyContent: "space-between",
  //   fontFamily: "Lexend",
  //   flex: 1,
  // },
  sidebar: {
    width: 260,
    height: "100%", // full vertical height
    backgroundColor: Colors.primaryBlue,
    paddingHorizontal: 19,
    paddingTop: 27,
    fontFamily: "Lexend",
    position: "relative",
  },
  username: {
    fontSize: 18,
    color: Colors.white,
    // fontWeight: "bold",
    marginBottom: 12,
    textAlign: "center",
    fontFamily: "Lexend",
  },
  divider: {
    height: 1,
    backgroundColor: Colors.white,
    // marginVertical: 8,
  },
  section: {
    marginTop: 17,
  },
  sectionTitle: {
    fontSize: 13,
    color: Colors.white,
    marginBottom: 8,
    fontWeight: "600",
    fontFamily: "Lexend",
  },
  menuItem: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    paddingHorizontal: 18,
    borderRadius: 12,
    // marginBottom: 6,
  },
  activeMenuItem: {
    backgroundColor: Colors.lightBlue,
  },
  menuLabel: {
    color: Colors.white,
    fontSize: 15,
    fontFamily: "Lexend",
    fontWeight: "400",
  },
  icon: {
    marginRight: 10,
    backgroundColor: Colors.lightBlue,
    padding: 10,
    borderRadius: 10,
  },
  iconActive: {
    marginRight: 10,
    backgroundColor: Colors.primaryGreen,
    padding: 10,
    borderRadius: 10,
  },
  footer: {
    position: "absolute",
    bottom: 30,
    left: 20, // ✅ adds horizontal margin from the left
    right: 20, // ✅ adds horizontal margin from the right
    alignItems: "center",
    backgroundColor: Colors.white,
    borderRadius: 20,
    // paddingVertical: 10,
    // paddingHorizontal: 16,
  },
  logo: {
    width: 120,
    height: 80,
  },
  sidebarContent: {},
});

export default Sidebar;
