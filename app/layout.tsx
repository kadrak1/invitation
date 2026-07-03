import type { Metadata } from "next";
import { Cormorant_Garamond, Inter } from "next/font/google";
import { weddingConfig } from "@/config/wedding";
import "./globals.css";

const cormorant = Cormorant_Garamond({
  variable: "--font-cormorant",
  subsets: ["latin", "cyrillic"],
  weight: ["400", "500", "600", "700"],
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin", "cyrillic"],
});

export const metadata: Metadata = {
  metadataBase: new URL(weddingConfig.site.url),
  title: weddingConfig.site.title,
  description: weddingConfig.site.description,
  openGraph: {
    title: weddingConfig.site.title,
    description: weddingConfig.site.description,
    url: weddingConfig.site.url,
    siteName: weddingConfig.site.title,
    locale: "ru_RU",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: weddingConfig.site.title,
    description: weddingConfig.site.description,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru" className={`${cormorant.variable} ${inter.variable} scroll-smooth`}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
