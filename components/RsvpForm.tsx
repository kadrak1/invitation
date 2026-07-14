"use client";

import { useEffect, useState } from "react";
import { useForm, useWatch } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { weddingConfig } from "@/config/wedding";
import { rsvpSchema, type RsvpFormData } from "@/lib/rsvp-schema";

export function RsvpForm() {
  const searchParams = useSearchParams();
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    control,
    setValue,
    formState: { errors },
  } = useForm<RsvpFormData>({
    resolver: zodResolver(rsvpSchema),
    defaultValues: {
      guestsCount: 1,
      status: undefined,
    },
  });

  const status = useWatch({ control, name: "status" });

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
    <section id="rsvp" className="whim-rsvp">
      <div className="whim-rsvp-shell">
        <motion.div
          className="whim-rsvp-heading"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <p>Ждём вашего ответа</p>
          <h2>Будете с нами?</h2>
          <span>
            Пожалуйста, ответьте до {weddingConfig.rsvp.deadline}
          </span>
        </motion.div>

        <AnimatePresence mode="wait">
          {submitted ? (
            <motion.div
              key="success"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="whim-rsvp-success"
            >
              <span>✦</span>
              <h3>Спасибо!</h3>
              <p>
                Ваш ответ принят. Мы с нетерпением ждём встречи!
              </p>
            </motion.div>
          ) : (
            <motion.form
              key="form"
              onSubmit={handleSubmit(onSubmit)}
              className="whim-rsvp-form"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <div>
                <label>Имя и фамилия</label>
                <input
                  {...register("name")}
                  className="whim-field"
                  placeholder="Иван Иванов"
                />
                {errors.name && (
                  <p className="whim-form-error">{errors.name.message}</p>
                )}
              </div>

              <div>
                <label>Сможете ли вы прийти?</label>
                <div className="whim-status-grid">
                  {(
                    [
                      { value: "yes", label: "Приду" },
                      { value: "maybe", label: "Не уверен(а)" },
                      { value: "no", label: "Не смогу" },
                    ] as const
                  ).map(({ value, label }) => (
                    <label
                      key={value}
                      className={`whim-status ${status === value ? "whim-status-active" : ""}`}
                    >
                      <input
                        type="radio"
                        value={value}
                        {...register("status")}
                      />
                      {label}
                    </label>
                  ))}
                </div>
                {errors.status && (
                  <p className="whim-form-error">{errors.status.message}</p>
                )}
              </div>

              {status !== "no" && (
                <>
                  <div>
                    <label>Количество гостей (включая вас)</label>
                    <input
                      type="number"
                      min={1}
                      max={10}
                      {...register("guestsCount", { valueAsNumber: true })}
                      className="whim-field"
                    />
                    {errors.guestsCount && (
                      <p className="whim-form-error">
                        {errors.guestsCount.message}
                      </p>
                    )}
                  </div>

                  <div>
                    <label>Предпочтения по меню</label>
                    <select
                      {...register("menu")}
                      className="whim-field"
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
                    <label>Аллергии / особые пожелания</label>
                    <input
                      {...register("allergies")}
                      className="whim-field"
                      placeholder="Например: непереносимость орехов"
                    />
                  </div>
                </>
              )}

              <div>
                <label>Комментарий или поздравление</label>
                <textarea
                  {...register("message")}
                  rows={3}
                  className="whim-field"
                  placeholder="Будем рады вашим тёплым словам"
                />
              </div>

              {error && (
                <p className="whim-form-error whim-form-error-center">{error}</p>
              )}

              <button
                type="submit"
                disabled={loading}
                className="whim-submit"
              >
                {loading ? "Отправка..." : "Отправить ответ"}
              </button>
            </motion.form>
          )}
        </AnimatePresence>
      </div>
    </section>
  );
}
