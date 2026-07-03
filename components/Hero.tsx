"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import { weddingConfig } from "@/config/wedding";

export function Hero() {
  const { bride, groom } = weddingConfig.couple;
  const { display, dayOfWeek } = weddingConfig.date;

  return (
    <section className="relative flex min-h-screen items-center justify-center overflow-hidden">
      <div className="absolute inset-0">
        <Image
          src="/photos/hero.jpg"
          alt={`${bride} и ${groom}`}
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-black/30 to-[#FAF7F2]" />
      </div>

      <div className="relative z-10 px-6 py-24 text-center text-white">
        <motion.p
          className="mb-4 text-sm uppercase tracking-[0.35em] text-[#C9A96E]"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          Приглашение на свадьбу
        </motion.p>

        <motion.h1
          className="font-serif text-5xl leading-tight sm:text-7xl md:text-8xl"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          {bride}
          <span className="mx-3 text-[#C9A96E]">&</span>
          {groom}
        </motion.h1>

        <motion.div
          className="mt-8 flex flex-col items-center gap-2"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          <p className="text-xl tracking-wide sm:text-2xl">{display}</p>
          <p className="text-sm uppercase tracking-[0.25em] text-white/80">
            {dayOfWeek}
          </p>
        </motion.div>

        <motion.a
          href="#rsvp"
          className="mt-12 inline-block rounded-full border border-[#C9A96E] bg-[#C9A96E]/20 px-8 py-3 text-sm uppercase tracking-[0.2em] backdrop-blur-sm transition hover:bg-[#C9A96E] hover:text-[#2C4A3E]"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.8 }}
        >
          Подтвердить присутствие
        </motion.a>
      </div>
    </section>
  );
}
