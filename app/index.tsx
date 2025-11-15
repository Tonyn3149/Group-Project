import { Image, Text, TouchableOpacity, View } from "react-native";
import { styles } from "./_layout";

export default function Index() {
  return (
    <View style={styles.container}>

      {/* Title */}
      <Text style={styles.title}>Welcome to Fantasy Winner's</Text>
      
      {/* White bar */}
      <View style={styles.bar}>
      
      {/* Logo Image */}
      <Image
        source={require("../assets/Logo.png")}
        style={{ width: 150, height: 150, marginBottom: 30 }}
        resizeMode="contain"
      />
      
      {/* Button */}
      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Sign up</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Sign in</Text>
      </TouchableOpacity>
      </View>
    </View>
  );
}



