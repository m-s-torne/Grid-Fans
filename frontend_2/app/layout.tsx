import type { Metadata } from "next";
import { Open_Sans } from "next/font/google";
import { Providers } from "./providers";
import "./globals.css";

const openSans = Open_Sans({
  variable: "--font-open",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Grid Fans",
  description: "Fantasy F1 league manager",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${openSans.variable} antialiased`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
