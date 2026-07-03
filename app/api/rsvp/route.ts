import { NextResponse } from "next/server";
import { ZodError } from "zod";
import { rsvpSchema } from "@/lib/rsvp-schema";
import { appendRsvpToSheet } from "@/lib/google-sheets";
import { notifyTelegram } from "@/lib/telegram";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const data = rsvpSchema.parse(body);

    await appendRsvpToSheet(data);
    await notifyTelegram(data).catch(() => {});

    return NextResponse.json({ success: true });
  } catch (error) {
    if (error instanceof ZodError) {
      return NextResponse.json({ error: "Некорректные данные формы" }, { status: 400 });
    }
    console.error("[RSVP]", error);
    return NextResponse.json({ error: "Ошибка сервера" }, { status: 500 });
  }
}
