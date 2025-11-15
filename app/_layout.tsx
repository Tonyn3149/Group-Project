import { Stack } from "expo-router";
import { StyleSheet } from "react-native";

export default function RootLayout() {
  return <Stack />;
}
export const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#4b0000',
    padding: 20,
  },
  title: {
    fontSize: 22,
    color: "white",
    marginBottom: 10,
    marginTop: -40,
  },
  bar: {
    width: '80%',
    height: 5,
    backgroundColor: "white",
    marginVertical: 20,
    borderRadius: 2,
  },
  button: {
    width: '70%',
    paddingVertical: 12,
    backgroundColor: '#333',
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 20,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
  }
});
