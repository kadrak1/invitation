import { weddingConfig } from "@/config/wedding";
import { AnimatedSection } from "./AnimatedSection";

export function DressCode() {
  const { title, description, colors, suggestions } = weddingConfig.dressCode;

  return (
    <AnimatedSection id="dresscode" className="bg-white px-6 py-20">
      <div className="mx-auto max-w-2xl text-center">
        <p className="mb-2 text-sm uppercase tracking-[0.3em] text-[#C9A96E]">
          Стиль
        </p>
        <h2 className="font-serif text-3xl text-[#2C4A3E] sm:text-4xl">{title}</h2>
        <p className="mt-6 text-[#2C4A3E]/80 leading-relaxed">{description}</p>

        <div className="mt-8 flex justify-center gap-3">
          {colors.map((color) => (
            <div
              key={color}
              className="h-10 w-10 rounded-full border border-[#2C4A3E]/10 shadow-sm"
              style={{ backgroundColor: color }}
              title={color}
            />
          ))}
        </div>

        <ul className="mt-8 space-y-3 text-left text-sm text-[#2C4A3E]/70">
          {suggestions.map((item, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className="mt-0.5 text-[#C9A96E]">✦</span>
              {item}
            </li>
          ))}
        </ul>
      </div>
    </AnimatedSection>
  );
}
