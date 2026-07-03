"use client";

import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { weddingConfig } from "@/config/wedding";
import { AnimatedSection } from "./AnimatedSection";

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
    <AnimatedSection className="bg-[#FAF7F2] px-6 py-20">
      <div className="mx-auto max-w-3xl text-center">
        <p className="mb-2 text-sm uppercase tracking-[0.3em] text-[#C9A96E]">
          До торжества осталось
        </p>
        <h2 className="font-serif text-3xl text-[#2C4A3E] sm:text-4xl">
          {timeLeft ? "Считаем дни..." : "Этот день настал!"}
        </h2>

        {timeLeft && (
          <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-4">
            {units.map(({ key, label }, i) => (
              <motion.div
                key={key}
                className="rounded-2xl border border-[#C9A96E]/30 bg-white px-4 py-6"
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
              >
                <span className="block font-serif text-4xl text-[#2C4A3E] sm:text-5xl">
                  {String(timeLeft[key]).padStart(2, "0")}
                </span>
                <span className="mt-1 block text-xs uppercase tracking-wider text-[#2C4A3E]/60">
                  {label}
                </span>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </AnimatedSection>
  );
}
