export type TaskStatus = 'pending' | 'running' | 'blocked' | 'complete';

export interface TaskCard {
  id: string;
  title: string;
  owner: 'research' | 'decision' | 'execution' | 'coding';
  status: TaskStatus;
  description: string;
}

export interface ActivityItem {
  id: string;
  agent: string;
  message: string;
  time: string;
}
