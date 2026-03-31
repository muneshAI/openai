import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';
import { api } from '../api/client';
import { useAppStore } from '../store/useAppStore';

export default function DashboardScreen() {
  const dashboard = useAppStore((s) => s.dashboard);
  const setDashboard = useAppStore((s) => s.setDashboard);

  const fetchDashboard = async () => {
    const { data } = await api.get('/score/dashboard');
    setDashboard(data);
  };

  useEffect(() => {
    fetchDashboard().catch(() => null);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Today</Text>
      <Text>Status: {dashboard?.workout_done_today ? 'Done' : 'Not Done'}</Text>
      <Text>Fitness Score: {dashboard?.fitness_score ?? 0}/100</Text>
      <Text>Streak: {dashboard?.current_streak ?? 0} days</Text>
      <Text>Weekly Completed: {dashboard?.weekly_completed ?? 0}</Text>
      <Button title="Refresh" onPress={fetchDashboard} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, gap: 12 },
  title: { fontSize: 28, fontWeight: '700' },
});
