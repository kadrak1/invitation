import { weddingConfig } from "@/config/wedding";
import { AnimatedSection } from "./AnimatedSection";

export function Schedule() {
  const { schedule } = weddingConfig;

  return (
    <AnimatedSection id="schedule" className="bg-[#FAF7F2] px-6 py-20">
      <div className="mx-auto max-w-2xl">
        <div className="text-center">
          <p className="mb-2 text-sm uppercase tracking-[0.3em] text-[#C9A96E]">
            Программа
          </p>
          <h2 className="font-serif text-3xl text-[#2C4A3E] sm:text-4xl">
            Расписание дня
          </h2>
        </div>

        <div className="relative mt-12">
          <div className="absolute left-4 top-0 h-full w-px bg-[#C9A96E]/40 sm:left-1/2" />

          {schedule.map((item, i) => (
            <div
              key={i}
              className={`relative mb-8 flex items-start gap-6 sm:gap-0 ${
                i % 2 === 0 ? "sm:flex-row" : "sm:flex-row-reverse"
              }`}
            >
              <div className="hidden w-1/2 sm:block" />
              <div
                className={`w-full sm:w-1/2 ${
                  i % 2 === 0 ? "sm:pr-12 sm:text-right" : "sm:pl-12"
                }`}
              >
                <div className="rounded-2xl border border-[#C9A96E]/20 bg-white p-6">
                  <span className="font-serif text-lg text-[#C9A96E]">{item.time}</span>
                  <h3 className="mt-1 font-serif text-xl text-[#2C4A3E]">{item.title}</h3>
                  <p className="mt-2 text-sm text-[#2C4A3E]/70">{item.description}</p>
                </div>
              </div>
              <div className="absolute left-4 top-6 h-3 w-3 -translate-x-1/2 rounded-full border-2 border-[#C9A96E] bg-white sm:left-1/2" />
            </div>
          ))}
        </div>
      </div>
    </AnimatedSection>
  );
}
