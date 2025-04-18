import React from 'react';
import { NavigationContainer, NavigationContainerProps } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { TestScreen } from '../screens/TestScreen';
import { WorkoutScreen } from '../screens/WorkoutScreen';
import { BaseBuilderScreen } from '../screens/BaseBuilderScreen';

export type RootStackParamList = {
  Test: undefined;
  Workout: undefined;
  BaseBuilder: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

export const AppNavigator: React.FC = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Test">
        <Stack.Screen 
          name="Test" 
          component={TestScreen}
          options={{ title: 'Test Screen' }}
        />
        <Stack.Screen 
          name="Workout" 
          component={WorkoutScreen}
          options={{ title: 'Workout' }}
        />
        <Stack.Screen 
          name="BaseBuilder" 
          component={BaseBuilderScreen}
          options={{ title: 'Base Builder' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}; 