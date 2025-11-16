import { router } from "expo-router";
import { sendPasswordResetEmail } from "firebase/auth";
import { useState } from "react";
import { Text, TextInput, TouchableOpacity, View } from "react-native";
import { auth } from "../config/firebaseConfig";
import { styles } from "./layout";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");

  const resetPassword = async () => {
    try {
      await sendPasswordResetEmail(auth, email);
      alert("Password reset email sent!");
      router.push("/login");
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
      <Text style={styles.title}>Password Reset</Text>

        <TextInput
            placeholder="Username@gmail.com"
            placeholderTextColor="#777"
            style={styles.username}
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address" 
            autoCapitalize="none"          // prevents capital letters in email
        />

        <TouchableOpacity style={styles.button} onPress={resetPassword} disabled={!email}>
            <Text style={styles.buttonText}>Reset Password</Text>
        </TouchableOpacity>
    </View>
  );
}