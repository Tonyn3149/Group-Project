import { router } from "expo-router";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { useState } from "react";
import { Text, TextInput, TouchableOpacity, View } from "react-native";
import { auth } from "../config/firebaseConfig"; // your firebase config
import { styles } from "./layout";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignUp = async () => {
    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      alert("Account created! Welcome " + userCredential.user.email);
      router.push("/login"); // navigate to login screen
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
      <Text style={styles.title}>Sign Up</Text>

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

      <TouchableOpacity style={styles.button} onPress={handleSignUp}>
        <Text style={styles.buttonText}>Sign Up</Text>
      </TouchableOpacity>
    </View>
  );
}