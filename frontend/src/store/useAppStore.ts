import { create } from 'zustand';

interface Dashboard {
  workout_done_today: boolean;
  fitness_score: number;
  current_streak: number;
  longest_streak: number;
  weekly_completed: number;
}

interface AppState {
  token: string | null;
  darkMode: boolean;
  dashboard: Dashboard | null;
  setToken: (token: string | null) => void;
  setDarkMode: (value: boolean) => void;
  setDashboard: (dashboard: Dashboard) => void;
}

export const useAppStore = create<AppState>((set) => ({
  token: null,
  darkMode: false,
  dashboard: null,
  setToken: (token) => set({ token }),
  setDarkMode: (darkMode) => set({ darkMode }),
  setDashboard: (dashboard) => set({ dashboard }),
}));
