import { weddingConfig } from "@/config/wedding";

export function generateIcsContent(): string {
  const start = new Date(weddingConfig.date.iso);
  const end = new Date(start.getTime() + 6 * 60 * 60 * 1000);

  const formatDate = (date: Date) =>
    date.toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";

  const uid = `wedding-${weddingConfig.couple.bride}-${weddingConfig.couple.groom}@invitation`;

  return [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Wedding Invitation//RU",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "BEGIN:VEVENT",
    `UID:${uid}`,
    `DTSTAMP:${formatDate(new Date())}`,
    `DTSTART:${formatDate(start)}`,
    `DTEND:${formatDate(end)}`,
    `SUMMARY:Свадьба ${weddingConfig.couple.bride} и ${weddingConfig.couple.groom}`,
    `DESCRIPTION:${weddingConfig.site.description}`,
    `LOCATION:${weddingConfig.venue.address}`,
    "END:VEVENT",
    "END:VCALENDAR",
  ].join("\r\n");
}
