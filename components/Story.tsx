import { weddingConfig } from "@/config/wedding";
import { AnimatedSection } from "./AnimatedSection";

export function Story() {
  const { title, paragraphs } = weddingConfig.story;

  return (
    <AnimatedSection id="story" className="bg-white px-6 py-20">
      <div className="mx-auto max-w-2xl text-center">
        <p className="mb-2 text-sm uppercase tracking-[0.3em] text-[#C9A96E]">
          Любовь
        </p>
        <h2 className="font-serif text-3xl text-[#2C4A3E] sm:text-4xl">{title}</h2>
        <div className="mt-8 space-y-6 text-left text-[#2C4A3E]/80 leading-relaxed">
          {paragraphs.map((paragraph, i) => (
            <p key={i}>{paragraph}</p>
          ))}
        </div>
      </div>
    </AnimatedSection>
  );
}
