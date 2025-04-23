// components/Sidebar.tsx

import { View, Text, Pressable, StyleSheet, Image } from "react-native";
import {
  ClipboardEdit,
  Home,
  DollarSign,
  AlertTriangle,
  User,
  LogOut,
} from "lucide-react-native";
import { TABS } from "@/constants/Tabs";
import { useRouter, usePathname } from "expo-router";

const Sidebar = () => {
  const router = useRouter();
  const pathname = usePathname();
  return (
    <View style={styles.sidebar}>
      <Text style={styles.username}>testuser123</Text>
      <View style={styles.divider} />

      <Section title="SALESMAN">
        <MenuItem
          icon={ClipboardEdit}
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
          onPress={() => router.push("/")}
        />
      </Section>

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
    <Icon color="#3fd47c" size={20} style={styles.icon} />
    <Text style={styles.menuLabel}>{label}</Text>
  </Pressable>
);

const styles = StyleSheet.create({
  sidebar: {
    width: 260,
    backgroundColor: "#0b1c3e",
    padding: 20,
    justifyContent: "space-between",
  },
  username: {
    fontSize: 18,
    color: "#fff",
    fontWeight: "bold",
    marginBottom: 12,
    textAlign: "center",
  },
  divider: {
    height: 1,
    backgroundColor: "#fff",
    marginVertical: 8,
  },
  section: {
    marginTop: 16,
  },
  sectionTitle: {
    fontSize: 12,
    color: "#fff",
    marginBottom: 8,
    fontWeight: "bold",
  },
  menuItem: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderRadius: 12,
    marginBottom: 6,
  },
  activeMenuItem: {
    backgroundColor: "#1b2b4e",
  },
  menuLabel: {
    color: "#fff",
    fontSize: 14,
  },
  icon: {
    marginRight: 10,
  },
  footer: {
    alignItems: "center",
    marginTop: 40,
  },
  logo: {
    width: 120,
    height: 40,
  },
});

export default Sidebar;
