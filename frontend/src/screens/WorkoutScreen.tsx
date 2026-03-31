import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, Button } from 'react-native';
import { api } from '../api/client';

export default function WorkoutScreen() {
  const [type, setType] = useState('P90X');
  const [duration, setDuration] = useState('30');
  const [status, setStatus] = useState('');

  const submit = async () => {
    await api.post('/workouts', {
      date: new Date().toISOString().slice(0, 10),
      type,
      duration: Number(duration),
      intensity: 3,
      calories: Number(duration) * 8,
      completed: true,
    });
    setStatus('Workout logged successfully');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Log Workout</Text>
      <TextInput value={type} onChangeText={setType} style={styles.input} placeholder="Workout Type" />
      <TextInput
        value={duration}
        onChangeText={setDuration}
        style={styles.input}
        placeholder="Duration"
        keyboardType="numeric"
      />
      <Button title="Mark Completed" onPress={submit} />
      <Text>{status}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, gap: 12 },
  title: { fontSize: 24, fontWeight: '700' },
  input: { borderWidth: 1, borderColor: '#777', padding: 10, borderRadius: 8 },
});
