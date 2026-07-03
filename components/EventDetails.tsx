import { weddingConfig } from "@/config/wedding";
import { AnimatedSection } from "./AnimatedSection";

export function EventDetails() {
  const { date, venue, ceremony, reception } = weddingConfig;

  return (
    <AnimatedSection id="details" className="bg-[#FAF7F2] px-6 py-20">
      <div className="mx-auto max-w-4xl">
        <div className="text-center">
          <p className="mb-2 text-sm uppercase tracking-[0.3em] text-[#C9A96E]">
            Когда и где
          </p>
          <h2 className="font-serif text-3xl text-[#2C4A3E] sm:text-4xl">
            Детали мероприятия
          </h2>
        </div>

        <div className="mt-12 grid gap-6 sm:grid-cols-2">
          <div className="rounded-2xl border border-[#C9A96E]/20 bg-white p-8 text-center">
            <span className="text-3xl">📅</span>
            <h3 className="mt-4 font-serif text-xl text-[#2C4A3E]">Дата</h3>
            <p className="mt-2 text-[#2C4A3E]/80">{date.display}</p>
            <p className="text-sm text-[#2C4A3E]/60">{date.dayOfWeek}, {date.time}</p>
          </div>

          <div className="rounded-2xl border border-[#C9A96E]/20 bg-white p-8 text-center">
            <span className="text-3xl">📍</span>
            <h3 className="mt-4 font-serif text-xl text-[#2C4A3E]">Место</h3>
            <p className="mt-2 font-medium text-[#2C4A3E]">{venue.name}</p>
            <p className="text-sm text-[#2C4A3E]/60">{venue.address}</p>
          </div>

          <div className="rounded-2xl border border-[#C9A96E]/20 bg-white p-8 text-center">
            <span className="text-3xl">💍</span>
            <h3 className="mt-4 font-serif text-xl text-[#2C4A3E]">{ceremony.title}</h3>
            <p className="mt-2 text-[#2C4A3E]/80">{ceremony.time}</p>
            <p className="text-sm text-[#2C4A3E]/60">{ceremony.location}</p>
          </div>

          <div className="rounded-2xl border border-[#C9A96E]/20 bg-white p-8 text-center">
            <span className="text-3xl">🥂</span>
            <h3 className="mt-4 font-serif text-xl text-[#2C4A3E]">{reception.title}</h3>
            <p className="mt-2 text-[#2C4A3E]/80">{reception.time}</p>
            <p className="text-sm text-[#2C4A3E]/60">{reception.location}</p>
          </div>
        </div>
      </div>
    </AnimatedSection>
  );
}
