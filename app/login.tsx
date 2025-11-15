import { Text, TextInput, TouchableOpacity, View } from "react-native";
import { styles } from "./_layout";

export default function Login() {
  return (
    <View style={styles.container}>
        <Text style={styles.title}>Sign in</Text>
        <TextInput 
            placeholder="Username" 
            placeholderTextColor="#777"
            style={styles.username}> 
        </TextInput>
        <TextInput 
            placeholder="Password" 
            placeholderTextColor="#777"
            style={styles.password}
            secureTextEntry={true}> 
        </TextInput>

      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Login</Text>
      </TouchableOpacity>
    </View>
  );
}