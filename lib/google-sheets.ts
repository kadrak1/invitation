import { google } from "googleapis";
import type { RsvpFormData } from "./rsvp-schema";

function getSheetsClient() {
  const email = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
  const key = process.env.GOOGLE_SERVICE_ACCOUNT_KEY?.replace(/\\n/g, "\n");
  const sheetId = process.env.GOOGLE_SHEETS_ID;

  if (!email || !key || !sheetId) {
    return null;
  }

  const auth = new google.auth.JWT({
    email,
    key,
    scopes: ["https://www.googleapis.com/auth/spreadsheets"],
  });

  return {
    sheets: google.sheets({ version: "v4", auth }),
    sheetId,
  };
}

export async function appendRsvpToSheet(data: RsvpFormData): Promise<boolean> {
  const client = getSheetsClient();
  if (!client) {
    console.warn("[RSVP] Google Sheets не настроен — ответ сохранён только в лог");
    console.info("[RSVP]", JSON.stringify({ ...data, timestamp: new Date().toISOString() }));
    return false;
  }

  const statusLabels: Record<RsvpFormData["status"], string> = {
    yes: "Приду",
    no: "Не смогу",
    maybe: "Пока не уверен(а)",
  };

  await client.sheets.spreadsheets.values.append({
    spreadsheetId: client.sheetId,
    range: "RSVP!A:G",
    valueInputOption: "USER_ENTERED",
    requestBody: {
      values: [
        [
          new Date().toISOString(),
          data.name,
          statusLabels[data.status],
          data.guestsCount,
          data.menu ?? "",
          data.allergies ?? "",
          data.message ?? "",
        ],
      ],
    },
  });

  return true;
}

export function isGoogleSheetsConfigured(): boolean {
  return Boolean(
    process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL &&
      process.env.GOOGLE_SERVICE_ACCOUNT_KEY &&
      process.env.GOOGLE_SHEETS_ID
  );
}
