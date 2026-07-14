export const weddingConfig = {
  couple: {
    bride: "Анна",
    groom: "Пётр",
    hashtag: "#АннаИПётр2026",
  },
  families: {
    groomParents: "Елена и Михаил Петровы",
    brideParents: "Ольга и Андрей Смирновы",
  },
  date: {
    iso: "2026-08-15T16:00:00+03:00",
    display: "15 августа 2026",
    dayOfWeek: "суббота",
    time: "16:00",
    timezone: "Europe/Moscow",
  },
  venue: {
    name: "Ресторан «Белая Лилия»",
    address: "Москва, ул. Садовая, 12",
    coordinates: { lat: 55.7558, lng: 37.6173 },
    mapUrl: "https://yandex.ru/maps/?ll=37.617300%2C55.755800&z=16&pt=37.617300%2C55.755800%2Cpm2rdm",
    directions: "От метро «Садовая» — 5 минут пешком. Парковка доступна на территории ресторана.",
  },
  invitation: {
    greeting: "С большой радостью приглашаем вас",
    message: "разделить с нами день, когда две истории станут одной",
  },
  events: [
    {
      title: "Welcome-вечер",
      date: "Пятница, 14 августа",
      time: "19:00",
      location: "Веранда «Белой Лилии»",
      attire: "Cocktail",
      image: "/whimsical/5suou0FMJMkajEAwbnuSvyUyk8.png",
    },
    {
      title: "Церемония",
      date: "Суббота, 15 августа",
      time: "16:00",
      location: "Сад у главной террасы",
      attire: "Formal",
      image: "/whimsical/b6Th31NYMOJQv2Qdn9zyD7lSRE.png",
    },
    {
      title: "Праздничный ужин",
      date: "Суббота, 15 августа",
      time: "17:30",
      location: "Большой банкетный зал",
      attire: "Black tie optional",
      image: "/whimsical/LoSKPEWODa1GunmbO0EegZ6Nz3c.png",
    },
    {
      title: "Вечеринка",
      date: "Суббота, 15 августа",
      time: "20:30",
      location: "Зал под звёздами",
      attire: "Dance ready",
      image: "/whimsical/X560LnKi1To2JqXFBCn9fWH5n0.png",
    },
  ],
  coupleMessage: {
    title: "Жених и невеста",
    text: "Мы счастливы, что вы будете рядом в этот особенный день. Ваша любовь и поддержка значат для нас больше, чем можно выразить словами. До скорой встречи на нашем празднике!",
  },
  gallery: [
    { src: "/whimsical/Au6Fd8xhKZQHzSYz9pi4y994x0.png", alt: "Анна и Пётр" },
    { src: "/whimsical/5suou0FMJMkajEAwbnuSvyUyk8.png", alt: "Анна и Пётр танцуют" },
    { src: "/whimsical/X560LnKi1To2JqXFBCn9fWH5n0.png", alt: "Анна и Пётр под луной" },
    { src: "/whimsical/LoSKPEWODa1GunmbO0EegZ6Nz3c.png", alt: "Праздничный вечер" },
  ],
  details: [
    {
      title: "Фотографии",
      text: "Публикуя фотографии, отмечайте нас и используйте хэштег #АннаИПётр2026.",
    },
    {
      title: "Погода",
      text: "Ожидается тёплый день до +24°, но вечером пригодится лёгкая накидка.",
    },
    {
      title: "Дресс-код",
      text: "Пастельные и природные оттенки. Просим оставить белый цвет невесте.",
    },
    {
      title: "Парковка",
      text: "Для гостей будет доступна бесплатная парковка на территории ресторана.",
    },
  ],
  rsvp: {
    deadline: "1 июля 2026",
    menuOptions: ["Мясное", "Рыбное", "Вегетарианское"],
  },
  contacts: {
    bride: { name: "Анна", phone: "+7 (900) 123-45-67" },
    groom: { name: "Пётр", phone: "+7 (900) 765-43-21" },
  },
  site: {
    title: "Анна & Пётр — Приглашение на свадьбу",
    description: "Мы будем рады видеть вас на нашей свадьбе 15 августа 2026 года в Москве.",
    url: process.env.NEXT_PUBLIC_SITE_URL ?? "https://anna-i-petr.vercel.app",
  },
} as const;

export type WeddingConfig = typeof weddingConfig;
