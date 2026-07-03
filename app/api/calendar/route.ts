import { generateIcsContent } from "@/lib/ics";

export async function GET() {
  const content = generateIcsContent();

  return new Response(content, {
    headers: {
      "Content-Type": "text/calendar; charset=utf-8",
      "Content-Disposition": 'attachment; filename="wedding.ics"',
    },
  });
}
