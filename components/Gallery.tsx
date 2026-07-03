"use client";

import Image from "next/image";
import { useState } from "react";
import { weddingConfig } from "@/config/wedding";
import { AnimatedSection } from "./AnimatedSection";

export function Gallery() {
  const { gallery } = weddingConfig;
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <AnimatedSection id="gallery" className="bg-[#FAF7F2] px-6 py-20">
      <div className="mx-auto max-w-4xl">
        <div className="text-center">
          <p className="mb-2 text-sm uppercase tracking-[0.3em] text-[#C9A96E]">
            Моменты
          </p>
          <h2 className="font-serif text-3xl text-[#2C4A3E] sm:text-4xl">
            Наши фотографии
          </h2>
        </div>

        <div className="relative mt-10 aspect-[4/3] overflow-hidden rounded-2xl">
          <Image
            src={gallery[activeIndex].src}
            alt={gallery[activeIndex].alt}
            fill
            className="object-cover transition-opacity duration-500"
            sizes="(max-width: 768px) 100vw, 896px"
          />
        </div>

        <div className="mt-4 flex justify-center gap-3">
          {gallery.map((photo, i) => (
            <button
              key={i}
              type="button"
              onClick={() => setActiveIndex(i)}
              className={`relative h-16 w-16 overflow-hidden rounded-lg border-2 transition ${
                i === activeIndex
                  ? "border-[#C9A96E]"
                  : "border-transparent opacity-60 hover:opacity-100"
              }`}
              aria-label={photo.alt}
            >
              <Image src={photo.src} alt={photo.alt} fill className="object-cover" sizes="64px" />
            </button>
          ))}
        </div>
      </div>
    </AnimatedSection>
  );
}
