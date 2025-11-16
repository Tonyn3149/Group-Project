import { router } from "expo-router";
import { signInWithEmailAndPassword } from "firebase/auth";
import { useState } from "react";
import { Text, TextInput, TouchableOpacity, View } from "react-native";
import { auth } from "../config/firebaseConfig";
import { styles } from "./layout";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      alert("Logged in! Welcome " + userCredential.user.email);
      router.push("/"); 
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      alert(message);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity 
        style={styles.backButton} 
        onPress={() => router.back()}
      >
        <Text style={styles.backText}>Back</Text>
      </TouchableOpacity>
      <Text style={styles.title}>Sign In</Text>

      <TextInput
        placeholder="Email"
        placeholderTextColor="#777"
        style={styles.username}
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <TextInput
        placeholder="Password"
        placeholderTextColor="#777"
        style={styles.password}
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Login</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={() => router.push("/forgotpassword")}>
        <Text style={styles.buttonText}>Forgot Password</Text>
      </TouchableOpacity>
    </View>
  );
}