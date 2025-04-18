import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export const TestScreen: React.FC = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Rowing Tower Defense</Text>
      <Text style={styles.subtitle}>Test Screen</Text>
      <Text style={styles.text}>
        If you can see this screen, the app is running correctly!
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    marginBottom: 20,
  },
  text: {
    fontSize: 16,
    textAlign: 'center',
  },
}); 