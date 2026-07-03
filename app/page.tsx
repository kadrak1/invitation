import { Suspense } from "react";
import { Hero } from "@/components/Hero";
import { Countdown } from "@/components/Countdown";
import { Story } from "@/components/Story";
import { EventDetails } from "@/components/EventDetails";
import { Map } from "@/components/Map";
import { Schedule } from "@/components/Schedule";
import { DressCode } from "@/components/DressCode";
import { Gallery } from "@/components/Gallery";
import { RsvpForm } from "@/components/RsvpForm";
import { Footer } from "@/components/Footer";

function RsvpFormFallback() {
  return (
    <section className="bg-white px-6 py-20">
      <div className="mx-auto max-w-lg text-center">
        <div className="h-8 w-48 mx-auto animate-pulse rounded bg-[#FAF7F2]" />
      </div>
    </section>
  );
}

export default function Home() {
  return (
    <main>
      <Hero />
      <Countdown />
      <Story />
      <EventDetails />
      <Map />
      <Schedule />
      <DressCode />
      <Gallery />
      <Suspense fallback={<RsvpFormFallback />}>
        <RsvpForm />
      </Suspense>
      <Footer />
    </main>
  );
}
