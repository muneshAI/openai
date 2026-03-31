import React from 'react';
import { NavigationContainer, DefaultTheme, DarkTheme } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar } from 'expo-status-bar';
import DashboardScreen from './src/screens/DashboardScreen';
import WorkoutScreen from './src/screens/WorkoutScreen';
import ProgressScreen from './src/screens/ProgressScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import { useAppStore } from './src/store/useAppStore';

const Tab = createBottomTabNavigator();

export default function App() {
  const darkMode = useAppStore((s) => s.darkMode);

  return (
    <NavigationContainer theme={darkMode ? DarkTheme : DefaultTheme}>
      <StatusBar style={darkMode ? 'light' : 'dark'} />
      <Tab.Navigator>
        <Tab.Screen name="Dashboard" component={DashboardScreen} />
        <Tab.Screen name="Workout" component={WorkoutScreen} />
        <Tab.Screen name="Progress" component={ProgressScreen} />
        <Tab.Screen name="Settings" component={SettingsScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
