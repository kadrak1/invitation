"use client";

import Image from "next/image";
import { Suspense, useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { weddingConfig } from "@/config/wedding";
import { Countdown } from "./Countdown";
import { RsvpForm } from "./RsvpForm";

const assets = {
  stars: "/whimsical/B9rNrlRBfXrORwzfHvYWhPDX1Y.png",
  mansion: "/whimsical/wKiH01QNP8DMVItVBJyF9tbg.png",
  balloon: "/whimsical/zBBH7icAYR0OpqziDnEQFIFyRE.png",
  leftTree: "/whimsical/rEehKhdtkygCYWwZsEWl6rkOY.png",
  rightTree: "/whimsical/ZSJY7eumK7S41MjYYufhtN01IRg.png",
  leftAngel: "/whimsical/6rQfdQWBH6ylEsj5Cvtu32ESw.png",
  rightAngel: "/whimsical/jCuNHP5Ac6wXitZpW034izWL8.png",
  leftFlowers: "/whimsical/nANJUUA3JunmZmLf3Peu7TbmMU.png",
  rightFlowers: "/whimsical/zGRmbM0Kc7cI5GZh2XKWu9xP920.png",
  topStars: "/whimsical/mkfwcRjo0Q4e0yChswkKfBTFN7I.png",
  paperLeft: "/whimsical/EdEFe6n6lZU38I3Q3QjTMt9iEY.png",
  paperRight: "/whimsical/LjMVHbCtoHm46EvfNtJa0PczbLw.png",
  paperTop: "/whimsical/FZrF0IYCyry5YbaC0YGwqR4xmrU.png",
  hearts: "/whimsical/NmVSVg1aTrcYbgmRoP9eOE9gpw.png",
  weather: "/whimsical/LAJ3Nftw1I9tvsShsVZHFUHMx0.png",
  question: "/whimsical/BS00HRHT5NWobvzo4WjW9UA763g.png",
  route: "/whimsical/FMx33N0QNZEN9o98413jFSazlw.png",
  floral: "/whimsical/nv75Gi2nlNnvSJBzV4dt8hZ8FWU.png",
  proposal: "/whimsical/HhPRLnuLh4pdr7VqoNmbDtngx28.png",
};

const reveal = {
  hidden: { opacity: 0, y: 48 },
  visible: { opacity: 1, y: 0 },
};

function RsvpFallback() {
  return <div className="rsvp-fallback" />;
}

function Hero() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });
  const skyY = useTransform(scrollYProgress, [0, 1], [0, 160]);
  const balloonY = useTransform(scrollYProgress, [0, 1], [0, -120]);
  const mansionY = useTransform(scrollYProgress, [0, 1], [0, 80]);

  return (
    <section ref={ref} className="whim-hero">
      <motion.div className="whim-hero-stars" style={{ y: skyY }}>
        <Image src={assets.stars} alt="" fill priority sizes="100vw" />
      </motion.div>

      <motion.div
        className="whim-balloon"
        style={{ y: balloonY }}
        initial={{ opacity: 0, x: 60, rotate: 8 }}
        animate={{ opacity: 1, x: 0, rotate: 0 }}
        transition={{ duration: 1.8, delay: 0.8, ease: "easeOut" }}
      >
        <Image src={assets.balloon} alt="" fill priority sizes="180px" />
      </motion.div>

      <div className="whim-crescent" aria-hidden="true">
        <span />
      </div>

      <motion.div
        className="whim-title"
        initial="hidden"
        animate="visible"
        transition={{ staggerChildren: 0.28, delayChildren: 0.35 }}
      >
        <motion.p variants={reveal} className="whim-kicker">
          Мы женимся
        </motion.p>
        <motion.h1 variants={reveal}>
          <span>{weddingConfig.couple.groom}</span>
          <small>и</small>
          <span>{weddingConfig.couple.bride}</span>
        </motion.h1>
        <motion.p variants={reveal} className="whim-date">
          {weddingConfig.date.display}
        </motion.p>
      </motion.div>

      <motion.div className="whim-mansion" style={{ y: mansionY }}>
        <Image src={assets.mansion} alt="" fill priority sizes="900px" />
      </motion.div>

      <motion.div
        className="whim-tree whim-tree-left"
        initial={{ opacity: 0, x: -120 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 1.6, delay: 0.2 }}
      >
        <Image src={assets.leftTree} alt="" fill priority sizes="420px" />
      </motion.div>
      <motion.div
        className="whim-tree whim-tree-right"
        initial={{ opacity: 0, x: 120 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 1.6, delay: 0.2 }}
      >
        <Image src={assets.rightTree} alt="" fill priority sizes="420px" />
      </motion.div>

      <motion.div
        className="whim-angel whim-angel-left"
        animate={{ y: [0, -13, 0], rotate: [-2, 2, -2] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
      >
        <Image src={assets.leftAngel} alt="" fill sizes="140px" />
      </motion.div>
      <motion.div
        className="whim-angel whim-angel-right"
        animate={{ y: [0, 13, 0], rotate: [2, -2, 2] }}
        transition={{ duration: 5.5, repeat: Infinity, ease: "easeInOut" }}
      >
        <Image src={assets.rightAngel} alt="" fill sizes="140px" />
      </motion.div>

      <div className="whim-flowers whim-flowers-left">
        <Image src={assets.leftFlowers} alt="" fill sizes="360px" />
      </div>
      <div className="whim-flowers whim-flowers-right">
        <Image src={assets.rightFlowers} alt="" fill sizes="360px" />
      </div>

      <a href="#invitation" className="whim-scroll">
        <span>Листайте вниз</span>
        <i />
      </a>
    </section>
  );
}

function Invitation() {
  return (
    <section id="invitation" className="whim-invitation">
      <div className="whim-paper-top">
        <Image src={assets.paperTop} alt="" fill sizes="100vw" />
      </div>
      <div className="whim-paper-side whim-paper-left">
        <Image src={assets.paperLeft} alt="" fill sizes="120px" />
      </div>
      <div className="whim-paper-side whim-paper-right">
        <Image src={assets.paperRight} alt="" fill sizes="120px" />
      </div>

      <motion.div
        className="whim-invite-copy"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.25 }}
        transition={{ staggerChildren: 0.15 }}
      >
        <motion.p variants={reveal} className="whim-kicker whim-kicker-dark">
          {weddingConfig.invitation.greeting}
        </motion.p>
        <motion.p variants={reveal} className="whim-parents">
          {weddingConfig.families.groomParents}
          <span>и</span>
          {weddingConfig.families.brideParents}
        </motion.p>
        <motion.p variants={reveal} className="whim-invite-message">
          {weddingConfig.invitation.message}
        </motion.p>
        <motion.h2 variants={reveal}>
          {weddingConfig.couple.groom}
          <small>&</small>
          {weddingConfig.couple.bride}
        </motion.h2>
        <motion.div variants={reveal} className="whim-date-lockup">
          <span>{weddingConfig.date.dayOfWeek}</span>
          <strong>15</strong>
          <span>августа · 2026</span>
        </motion.div>
      </motion.div>

      <Events />
    </section>
  );
}

function Events() {
  return (
    <div className="whim-events">
      <motion.div
        className="whim-events-heading"
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
      >
        <p>Программа праздника</p>
        <h2>В этот особенный день</h2>
      </motion.div>

      <div className="whim-event-grid">
        {weddingConfig.events.map((event, index) => (
          <motion.article
            key={event.title}
            className="whim-event-card"
            initial={{ opacity: 0, y: 80, rotate: index % 2 ? 2 : -2 }}
            whileInView={{ opacity: 1, y: 0, rotate: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.8, delay: index * 0.08 }}
          >
            <div className="whim-event-image">
              <Image
                src={event.image}
                alt={event.title}
                fill
                sizes="(max-width: 768px) 82vw, 280px"
              />
            </div>
            <div className="whim-event-details">
              <span>0{index + 1}</span>
              <h3>{event.title}</h3>
              <p>{event.date}</p>
              <p>{event.time} · {event.attire}</p>
              <p>{event.location}</p>
              <a href={weddingConfig.venue.mapUrl} target="_blank" rel="noreferrer">
                Показать маршрут
              </a>
            </div>
          </motion.article>
        ))}
      </div>
    </div>
  );
}

function RouteBanner() {
  return (
    <section className="whim-route">
      <motion.div
        className="whim-route-mark"
        animate={{ y: [0, -10, 0] }}
        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
      >
        <Image src={assets.route} alt="" fill sizes="180px" />
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
      >
        <p>Место встречи</p>
        <h2>{weddingConfig.venue.name}</h2>
        <span>{weddingConfig.venue.address}</span>
        <a href={weddingConfig.venue.mapUrl} target="_blank" rel="noreferrer">
          Посмотреть маршрут
        </a>
      </motion.div>
    </section>
  );
}

function Couple() {
  const gallery = [...weddingConfig.gallery, ...weddingConfig.gallery];

  return (
    <section className="whim-couple">
      <motion.div
        className="whim-couple-title"
        initial={{ opacity: 0, scale: 0.9 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true }}
      >
        <div className="whim-hearts">
          <Image src={assets.hearts} alt="" fill sizes="90px" />
        </div>
        <p>Давайте знакомиться</p>
        <h2>{weddingConfig.coupleMessage.title}</h2>
      </motion.div>

      <motion.p
        className="whim-couple-message"
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
      >
        {weddingConfig.coupleMessage.text}
      </motion.p>

      <div className="whim-gallery-window">
        <div className="whim-gallery-track">
          {gallery.map((photo, index) => (
            <div className="whim-gallery-card" key={`${photo.src}-${index}`}>
              <Image src={photo.src} alt={photo.alt} fill sizes="320px" />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Details() {
  const icons = [assets.hearts, assets.weather, assets.floral, assets.question];

  return (
    <section className="whim-details">
      <motion.div
        className="whim-details-heading"
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
      >
        <p>?</p>
        <h2>Полезно знать</h2>
        <span>Несколько деталей, чтобы вы чувствовали себя комфортно и наслаждались каждым моментом.</span>
      </motion.div>

      <div className="whim-detail-list">
        {weddingConfig.details.map((item, index) => (
          <motion.article
            key={item.title}
            initial={{ opacity: 0, x: index % 2 ? 80 : -80 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.75 }}
          >
            <div className="whim-detail-icon">
              <Image src={icons[index]} alt="" fill sizes="100px" />
            </div>
            <div>
              <span>0{index + 1}</span>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </div>
          </motion.article>
        ))}
      </div>
    </section>
  );
}

function Ending() {
  return (
    <footer className="whim-ending">
      <div className="whim-ending-stars">
        <Image src={assets.topStars} alt="" fill sizes="100vw" />
      </div>
      <motion.div
        className="whim-proposal"
        initial={{ opacity: 0, scale: 0.85 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 1 }}
      >
        <Image src={assets.proposal} alt="Предложение руки и сердца" fill sizes="700px" />
      </motion.div>
      <Countdown />
      <p className="whim-ending-message">
        Наши семьи счастливы разделить с вами один из самых важных дней нашей жизни.
      </p>
      <a href="/api/calendar" className="whim-calendar">
        Добавить в календарь
      </a>
      <p className="whim-signature">
        {weddingConfig.couple.groom} & {weddingConfig.couple.bride}
      </p>
    </footer>
  );
}

export function WhimsicalInvitation() {
  return (
    <main className="whimsical-site">
      <Hero />
      <Invitation />
      <RouteBanner />
      <Couple />
      <Suspense fallback={<RsvpFallback />}>
        <RsvpForm />
      </Suspense>
      <Details />
      <Ending />
    </main>
  );
}
