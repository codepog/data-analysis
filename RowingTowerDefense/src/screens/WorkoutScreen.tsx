import React, { useEffect, useState } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { Text, Button, ProgressBar } from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import { startWorkout, updateWorkoutData, endWorkout } from '../store/workoutSlice';
import { bluetoothService } from '../services/BluetoothService';

export const WorkoutScreen: React.FC = () => {
  const dispatch = useDispatch();
  const { currentWorkout, isWorkoutActive } = useSelector((state: RootState) => state.workout);
  const [isConnecting, setIsConnecting] = useState(false);

  useEffect(() => {
    return () => {
      if (isWorkoutActive) {
        bluetoothService.disconnect();
      }
    };
  }, [isWorkoutActive]);

  const handleConnect = async () => {
    try {
      setIsConnecting(true);
      await bluetoothService.startScanning();
      const connected = await bluetoothService.connect();
      
      if (connected) {
        dispatch(startWorkout());
        await bluetoothService.startWorkout();
      } else {
        Alert.alert('Connection Error', 'Failed to connect to rowing machine');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to connect to rowing machine');
    } finally {
      setIsConnecting(false);
    }
  };

  const handleEndWorkout = async () => {
    try {
      await bluetoothService.disconnect();
      dispatch(endWorkout());
    } catch (error) {
      Alert.alert('Error', 'Failed to end workout');
    }
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatSplit = (split: number): string => {
    const mins = Math.floor(split / 60);
    const secs = split % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Rowing Workout</Text>
      
      {!isWorkoutActive ? (
        <Button
          mode="contained"
          onPress={handleConnect}
          loading={isConnecting}
          disabled={isConnecting}
          style={styles.button}
        >
          Connect to Rowing Machine
        </Button>
      ) : (
        <View style={styles.workoutContainer}>
          <View style={styles.metricContainer}>
            <Text style={styles.metricLabel}>Distance</Text>
            <Text style={styles.metricValue}>
              {currentWorkout?.distance.toFixed(0)}m
            </Text>
          </View>

          <View style={styles.metricContainer}>
            <Text style={styles.metricLabel}>Time</Text>
            <Text style={styles.metricValue}>
              {formatTime(currentWorkout?.duration || 0)}
            </Text>
          </View>

          <View style={styles.metricContainer}>
            <Text style={styles.metricLabel}>Split</Text>
            <Text style={styles.metricValue}>
              {formatSplit(currentWorkout?.split || 0)}/500m
            </Text>
          </View>

          {currentWorkout?.heartRate && (
            <View style={styles.metricContainer}>
              <Text style={styles.metricLabel}>Heart Rate</Text>
              <Text style={styles.metricValue}>
                {currentWorkout.heartRate} BPM
              </Text>
            </View>
          )}

          <Button
            mode="contained"
            onPress={handleEndWorkout}
            style={styles.endButton}
          >
            End Workout
          </Button>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  button: {
    marginTop: 20,
  },
  workoutContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  metricContainer: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 10,
    marginVertical: 10,
    width: '100%',
    alignItems: 'center',
    elevation: 2,
  },
  metricLabel: {
    fontSize: 16,
    color: '#666',
  },
  metricValue: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 5,
  },
  endButton: {
    marginTop: 30,
    backgroundColor: '#ff4444',
  },
}); 