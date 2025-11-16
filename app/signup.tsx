import { router } from "expo-router";
import { Text, TextInput, TouchableOpacity, View } from "react-native";
import { styles } from "./layout";

export default function Signup() {
    return (
    <View style={styles.container}>
        <Text style={styles.title}>Sign up</Text>
        <Text style={styles.email}>Email</Text>
        <TextInput 
            placeholder="Someone@gmail.com" 
            placeholderTextColor="#777"
            style={styles.username}> 
        </TextInput>
        <Text style={styles.passwordtext}>Password</Text>
        <TextInput 
            placeholder="Password1234" 
            placeholderTextColor="#777"
            style={styles.password}
            secureTextEntry={true}> 
        </TextInput>
        <TouchableOpacity 
            style={styles.button}
            onPress={() => router.push("/")}>
        <Text style={styles.buttonText}>Sign Up</Text>
        </TouchableOpacity>
    </View>
    );
}