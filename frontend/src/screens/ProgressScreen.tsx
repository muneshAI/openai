import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { VictoryBar, VictoryChart, VictoryTheme } from 'victory-native';
import { api } from '../api/client';

export default function ProgressScreen() {
  const [weekly, setWeekly] = useState<{ day: string; completed: number }[]>([]);
  const [monthlyCompleted, setMonthlyCompleted] = useState(0);

  useEffect(() => {
    api.get('/progress').then(({ data }) => {
      setWeekly(data.weekly);
      setMonthlyCompleted(data.monthly_completed);
    });
  }, []);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Analytics</Text>
      <Text>Monthly Completed Workouts: {monthlyCompleted}</Text>
      <VictoryChart theme={VictoryTheme.material} domainPadding={16}>
        <VictoryBar data={weekly} x="day" y="completed" />
      </VictoryChart>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: '700', marginBottom: 12 },
});
