import { weddingConfig } from "@/config/wedding";
import { AnimatedSection } from "./AnimatedSection";

export function Map() {
  const { venue } = weddingConfig;
  const { lat, lng } = venue.coordinates;

  return (
    <AnimatedSection id="map" className="bg-white px-6 py-20">
      <div className="mx-auto max-w-4xl">
        <div className="text-center">
          <p className="mb-2 text-sm uppercase tracking-[0.3em] text-[#C9A96E]">
            Как добраться
          </p>
          <h2 className="font-serif text-3xl text-[#2C4A3E] sm:text-4xl">
            {venue.name}
          </h2>
          <p className="mt-2 text-[#2C4A3E]/70">{venue.address}</p>
        </div>

        <div className="mt-8 overflow-hidden rounded-2xl border border-[#C9A96E]/20 shadow-sm">
          <iframe
            title="Карта места проведения"
            src={`https://yandex.ru/map-widget/v1/?ll=${lng}%2C${lat}&z=15&pt=${lng}%2C${lat}%2Cpm2rdm`}
            width="100%"
            height="400"
            allowFullScreen
            className="block w-full"
          />
        </div>

        <p className="mt-6 text-center text-sm leading-relaxed text-[#2C4A3E]/70">
          {venue.directions}
        </p>

        <div className="mt-4 text-center">
          <a
            href={venue.mapUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block text-sm text-[#C9A96E] underline underline-offset-4 transition hover:text-[#2C4A3E]"
          >
            Открыть в Яндекс.Картах
          </a>
        </div>
      </div>
    </AnimatedSection>
  );
}
