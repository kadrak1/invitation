import { weddingConfig } from "@/config/wedding";
import { AnimatedSection } from "./AnimatedSection";

export function Footer() {
  const { bride, groom, hashtag } = weddingConfig.couple;
  const { contacts } = weddingConfig;

  return (
    <AnimatedSection className="bg-[#2C4A3E] px-6 py-16 text-white">
      <div className="mx-auto max-w-2xl text-center">
        <h2 className="font-serif text-3xl">
          {bride} & {groom}
        </h2>
        <p className="mt-2 text-sm text-white/60">{hashtag}</p>

        <div className="mt-8 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <a
            href="/api/calendar"
            download="wedding.ics"
            className="inline-block rounded-full border border-[#C9A96E] px-6 py-3 text-sm uppercase tracking-[0.15em] text-[#C9A96E] transition hover:bg-[#C9A96E] hover:text-[#2C4A3E]"
          >
            Добавить в календарь
          </a>
        </div>

        <div className="mt-10 grid gap-4 text-sm sm:grid-cols-2">
          <div>
            <p className="text-white/50">Контакт невесты</p>
            <p className="mt-1">{contacts.bride.name}</p>
            <a
              href={`tel:${contacts.bride.phone.replace(/\s/g, "")}`}
              className="text-[#C9A96E] hover:underline"
            >
              {contacts.bride.phone}
            </a>
          </div>
          <div>
            <p className="text-white/50">Контакт жениха</p>
            <p className="mt-1">{contacts.groom.name}</p>
            <a
              href={`tel:${contacts.groom.phone.replace(/\s/g, "")}`}
              className="text-[#C9A96E] hover:underline"
            >
              {contacts.groom.phone}
            </a>
          </div>
        </div>

        <p className="mt-12 text-xs text-white/40">
          С любовью, {bride} и {groom} · {weddingConfig.date.display}
        </p>
      </div>
    </AnimatedSection>
  );
}
