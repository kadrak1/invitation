import type { RsvpFormData } from "./rsvp-schema";

const statusLabels: Record<RsvpFormData["status"], string> = {
  yes: "✅ Приду",
  no: "❌ Не смогу",
  maybe: "🤔 Пока не уверен(а)",
};

export async function notifyTelegram(data: RsvpFormData): Promise<void> {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;

  if (!token || !chatId) return;

  const text = [
    "💌 Новый RSVP",
    "",
    `👤 ${data.name}`,
    `📋 ${statusLabels[data.status]}`,
    `👥 Гостей: ${data.guestsCount}`,
    data.menu ? `🍽 Меню: ${data.menu}` : null,
    data.allergies ? `⚠️ Аллергии: ${data.allergies}` : null,
    data.message ? `💬 ${data.message}` : null,
  ]
    .filter(Boolean)
    .join("\n");

  await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text }),
  });
}
