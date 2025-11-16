import { Stack } from "expo-router";
import { StyleSheet } from "react-native";

export default function _layout() {
  return <Stack />;
}
export const styles = StyleSheet.create({
  // all page styles
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
  },
  username: {
    backgroundColor: "#e8e8e8",
    padding: 12,
    borderRadius: 8,
    marginBottom: 20,
  },
  password: {
    backgroundColor: "#e8e8e8",
    padding: 12,
    borderRadius: 8,
    marginBottom: 30,
  },
  email: {
    color: "black",
    alignSelf: "flex-start",
    marginLeft: '41%',
    marginBottom: 5,
    padding: 20,
  },
  passwordtext: {
    color: "black",
    alignSelf: "flex-start",
    marginLeft: '41%',
    marginBottom: 5,
    padding: 20,
  },
  backButton: {
    position: 'absolute',
    top: 50,
    left: 20,
  },
  backText: {
    color: 'white',
    fontSize: 16,
  },
});
