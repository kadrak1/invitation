import { ImageResponse } from "next/og";
import { weddingConfig } from "@/config/wedding";

export const runtime = "edge";
export const alt = weddingConfig.site.title;
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OgImage() {
  const { bride, groom } = weddingConfig.couple;
  const { display } = weddingConfig.date;

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          background: "linear-gradient(135deg, #2C4A3E 0%, #1e3329 100%)",
          color: "#FAF7F2",
        }}
      >
        <div
          style={{
            fontSize: 28,
            letterSpacing: "0.3em",
            textTransform: "uppercase",
            color: "#C9A96E",
            marginBottom: 24,
          }}
        >
          Приглашение на свадьбу
        </div>
        <div
          style={{
            fontSize: 72,
            fontFamily: "serif",
            display: "flex",
            alignItems: "center",
            gap: 24,
          }}
        >
          {bride}
          <span style={{ color: "#C9A96E" }}>&</span>
          {groom}
        </div>
        <div
          style={{
            fontSize: 32,
            marginTop: 32,
            color: "#FAF7F2",
            opacity: 0.9,
          }}
        >
          {display}
        </div>
      </div>
    ),
    { ...size }
  );
}
