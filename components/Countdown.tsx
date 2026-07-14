"use client";

import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { weddingConfig } from "@/config/wedding";

type TimeLeft = {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
};

function calculateTimeLeft(target: Date): TimeLeft | null {
  const diff = target.getTime() - Date.now();
  if (diff <= 0) return null;

  return {
    days: Math.floor(diff / (1000 * 60 * 60 * 24)),
    hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
    minutes: Math.floor((diff / (1000 * 60)) % 60),
    seconds: Math.floor((diff / 1000) % 60),
  };
}

const units: { key: keyof TimeLeft; label: string }[] = [
  { key: "days", label: "дней" },
  { key: "hours", label: "часов" },
  { key: "minutes", label: "минут" },
  { key: "seconds", label: "секунд" },
];

export function Countdown() {
  const target = useMemo(() => new Date(weddingConfig.date.iso), []);
  const [timeLeft, setTimeLeft] = useState<TimeLeft | null>(() =>
    calculateTimeLeft(target)
  );

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(calculateTimeLeft(target));
    }, 1000);
    return () => clearInterval(timer);
  }, [target]);

  return (
    <section className="whim-countdown">
      <motion.p
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
      >
        Обратный отсчёт начался
      </motion.p>
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
      >
        {timeLeft ? "До нашей встречи" : "Этот день настал"}
      </motion.h2>

      {timeLeft && (
        <div className="whim-time-grid">
          {units.map(({ key, label }, i) => (
            <motion.div
              key={key}
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
            >
              <strong>{String(timeLeft[key]).padStart(2, "0")}</strong>
              <span>{label}</span>
            </motion.div>
          ))}
        </div>
      )}
    </section>
  );
}
