import React, { useState } from 'react';
import { View, Text, StyleSheet, Switch, TextInput, Button } from 'react-native';
import { api } from '../api/client';
import { useAppStore } from '../store/useAppStore';

export default function SettingsScreen() {
  const darkMode = useAppStore((s) => s.darkMode);
  const setDarkMode = useAppStore((s) => s.setDarkMode);
  const [enabled, setEnabled] = useState(true);
  const [time, setTime] = useState('06:00:00');
  const [timezone, setTimezone] = useState('UTC');

  const save = async () => {
    await api.put('/reminders/settings', {
      reminders_enabled: enabled,
      reminder_time: time,
      timezone,
    });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Settings</Text>
      <View style={styles.row}>
        <Text>Dark mode</Text>
        <Switch value={darkMode} onValueChange={setDarkMode} />
      </View>
      <View style={styles.row}>
        <Text>Reminders</Text>
        <Switch value={enabled} onValueChange={setEnabled} />
      </View>
      <TextInput style={styles.input} value={time} onChangeText={setTime} placeholder="Reminder time HH:MM:SS" />
      <TextInput style={styles.input} value={timezone} onChangeText={setTimezone} placeholder="Timezone" />
      <Button title="Save Settings" onPress={save} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, gap: 12 },
  title: { fontSize: 24, fontWeight: '700' },
  row: { flexDirection: 'row', justifyContent: 'space-between' },
  input: { borderWidth: 1, borderColor: '#888', padding: 8, borderRadius: 8 },
});
