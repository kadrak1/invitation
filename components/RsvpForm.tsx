"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { weddingConfig } from "@/config/wedding";
import { rsvpSchema, type RsvpFormData } from "@/lib/rsvp-schema";
import { AnimatedSection } from "./AnimatedSection";

export function RsvpForm() {
  const searchParams = useSearchParams();
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<RsvpFormData>({
    resolver: zodResolver(rsvpSchema),
    defaultValues: {
      guestsCount: 1,
      status: undefined,
    },
  });

  const status = watch("status");

  useEffect(() => {
    const guest = searchParams.get("guest");
    if (guest) {
      setValue("name", decodeURIComponent(guest));
    }
  }, [searchParams, setValue]);

  async function onSubmit(data: RsvpFormData) {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/rsvp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.error ?? "Не удалось отправить ответ");
      }

      setSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Произошла ошибка");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AnimatedSection id="rsvp" className="bg-white px-6 py-20">
      <div className="mx-auto max-w-lg">
        <div className="text-center">
          <p className="mb-2 text-sm uppercase tracking-[0.3em] text-[#C9A96E]">
            RSVP
          </p>
          <h2 className="font-serif text-3xl text-[#2C4A3E] sm:text-4xl">
            Подтвердите присутствие
          </h2>
          <p className="mt-4 text-sm text-[#2C4A3E]/70">
            Пожалуйста, ответьте до {weddingConfig.rsvp.deadline}
          </p>
        </div>

        <AnimatePresence mode="wait">
          {submitted ? (
            <motion.div
              key="success"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="mt-10 rounded-2xl border border-[#C9A96E]/30 bg-[#FAF7F2] p-8 text-center"
            >
              <span className="text-4xl">💌</span>
              <h3 className="mt-4 font-serif text-2xl text-[#2C4A3E]">Спасибо!</h3>
              <p className="mt-2 text-[#2C4A3E]/70">
                Ваш ответ принят. Мы с нетерпением ждём встречи!
              </p>
            </motion.div>
          ) : (
            <motion.form
              key="form"
              onSubmit={handleSubmit(onSubmit)}
              className="mt-10 space-y-6"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <div>
                <label className="mb-1 block text-sm text-[#2C4A3E]/80">
                  Имя и фамилия
                </label>
                <input
                  {...register("name")}
                  className="w-full rounded-xl border border-[#2C4A3E]/20 bg-[#FAF7F2] px-4 py-3 text-[#2C4A3E] outline-none transition focus:border-[#C9A96E]"
                  placeholder="Иван Иванов"
                />
                {errors.name && (
                  <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                )}
              </div>

              <div>
                <label className="mb-2 block text-sm text-[#2C4A3E]/80">
                  Сможете ли вы прийти?
                </label>
                <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
                  {(
                    [
                      { value: "yes", label: "Приду" },
                      { value: "maybe", label: "Не уверен(а)" },
                      { value: "no", label: "Не смогу" },
                    ] as const
                  ).map(({ value, label }) => (
                    <label
                      key={value}
                      className={`cursor-pointer rounded-xl border px-4 py-3 text-center text-sm transition ${
                        status === value
                          ? "border-[#C9A96E] bg-[#C9A96E]/10 text-[#2C4A3E]"
                          : "border-[#2C4A3E]/20 text-[#2C4A3E]/70 hover:border-[#C9A96E]/50"
                      }`}
                    >
                      <input
                        type="radio"
                        value={value}
                        {...register("status")}
                        className="sr-only"
                      />
                      {label}
                    </label>
                  ))}
                </div>
                {errors.status && (
                  <p className="mt-1 text-sm text-red-600">{errors.status.message}</p>
                )}
              </div>

              {status !== "no" && (
                <>
                  <div>
                    <label className="mb-1 block text-sm text-[#2C4A3E]/80">
                      Количество гостей (включая вас)
                    </label>
                    <input
                      type="number"
                      min={1}
                      max={10}
                      {...register("guestsCount", { valueAsNumber: true })}
                      className="w-full rounded-xl border border-[#2C4A3E]/20 bg-[#FAF7F2] px-4 py-3 text-[#2C4A3E] outline-none transition focus:border-[#C9A96E]"
                    />
                    {errors.guestsCount && (
                      <p className="mt-1 text-sm text-red-600">
                        {errors.guestsCount.message}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="mb-1 block text-sm text-[#2C4A3E]/80">
                      Предпочтения по меню
                    </label>
                    <select
                      {...register("menu")}
                      className="w-full rounded-xl border border-[#2C4A3E]/20 bg-[#FAF7F2] px-4 py-3 text-[#2C4A3E] outline-none transition focus:border-[#C9A96E]"
                    >
                      <option value="">Выберите вариант</option>
                      {weddingConfig.rsvp.menuOptions.map((option) => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="mb-1 block text-sm text-[#2C4A3E]/80">
                      Аллергии / особые пожелания
                    </label>
                    <input
                      {...register("allergies")}
                      className="w-full rounded-xl border border-[#2C4A3E]/20 bg-[#FAF7F2] px-4 py-3 text-[#2C4A3E] outline-none transition focus:border-[#C9A96E]"
                      placeholder="Например: непереносимость орехов"
                    />
                  </div>
                </>
              )}

              <div>
                <label className="mb-1 block text-sm text-[#2C4A3E]/80">
                  Комментарий или поздравление
                </label>
                <textarea
                  {...register("message")}
                  rows={3}
                  className="w-full resize-none rounded-xl border border-[#2C4A3E]/20 bg-[#FAF7F2] px-4 py-3 text-[#2C4A3E] outline-none transition focus:border-[#C9A96E]"
                  placeholder="Будем рады вашим тёплым словам"
                />
              </div>

              {error && (
                <p className="text-center text-sm text-red-600">{error}</p>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-full bg-[#2C4A3E] px-8 py-4 text-sm uppercase tracking-[0.2em] text-white transition hover:bg-[#1e3329] disabled:opacity-60"
              >
                {loading ? "Отправка..." : "Отправить ответ"}
              </button>
            </motion.form>
          )}
        </AnimatePresence>
      </div>
    </AnimatedSection>
  );
}
