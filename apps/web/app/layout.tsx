import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'Munesh AI',
  description: 'Autonomous operator for telecom execution, automation, and decision intelligence.',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
