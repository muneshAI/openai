import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Munesh AI Dashboard",
  description: "Observe autonomous multi-agent workflows",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
