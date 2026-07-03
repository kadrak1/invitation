import { z } from "zod";

export const rsvpSchema = z.object({
  name: z.string().min(2, "Введите имя и фамилию"),
  status: z.enum(["yes", "no", "maybe"], {
    message: "Выберите вариант ответа",
  }),
  guestsCount: z.number().min(1).max(10),
  menu: z.string().optional(),
  allergies: z.string().optional(),
  message: z.string().max(500).optional(),
});

export type RsvpFormData = z.infer<typeof rsvpSchema>;
