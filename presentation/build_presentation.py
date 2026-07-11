#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор презентации «Gardenscapes vs Royal Match» (тестовое задание Junior Game Designer).
Собирает .pptx, совместимый с импортом в Google Slides.
Запуск: python3 build_presentation.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------------------------------------------------------------- палитра
BG        = RGBColor(0xF7, 0xF5, 0xF0)   # тёплый светлый фон
INK       = RGBColor(0x1F, 0x2A, 0x44)   # тёмно-синий текст
MUT       = RGBColor(0x5A, 0x64, 0x78)   # приглушённый текст
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
GS_GREEN  = RGBColor(0x2F, 0x8F, 0x4E)   # Gardenscapes
GS_DARK   = RGBColor(0x1E, 0x6B, 0x38)
GS_LIGHT  = RGBColor(0xE3, 0xF1, 0xE6)
RM_BLUE   = RGBColor(0x2D, 0x5F, 0xC1)   # Royal Match
RM_DARK   = RGBColor(0x1F, 0x46, 0x94)
RM_LIGHT  = RGBColor(0xE6, 0xED, 0xFA)
GOLD      = RGBColor(0xE0, 0xA2, 0x38)
GOLD_LT   = RGBColor(0xFA, 0xF0, 0xDC)
RED       = RGBColor(0xBE, 0x4F, 0x45)
RED_LIGHT = RGBColor(0xF8, 0xE7, 0xE4)
LINE_GRAY = RGBColor(0xDE, 0xDA, 0xD2)

FONT = "Arial"

SW, SH = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH
BLANK = prs.slide_layouts[6]

PAGE_TOTAL = 15
_page = 0


# ---------------------------------------------------------------- helpers
def new_slide(bg=BG):
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    r.fill.solid(); r.fill.fore_color.rgb = bg
    r.line.fill.background()
    r.shadow.inherit = False
    return s


def rect(s, x, y, w, h, fill=None, line=None, line_w=0.75, rounded=False, adj=0.10):
    shp = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE, x, y, w, h)
    if rounded:
        try:
            shp.adjustments[0] = adj
        except Exception:
            pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp


def txt(s, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        space_after=4, line_spacing=1.0):
    """paras: список абзацев; абзац = список ранов (text, size, color, bold, italic)."""
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        p.line_spacing = line_spacing
        for (t, size, color, bold, italic) in runs:
            r = p.add_run()
            r.text = t
            r.font.name = FONT
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.italic = italic
    return tb


def R(t, size=13, color=INK, bold=False, italic=False):
    return (t, size, color, bold, italic)


def chip(s, x, y, w, h, text, bg, fg=WHITE, size=11, bold=True):
    c = rect(s, x, y, w, h, fill=bg, rounded=True, adj=0.5)
    tf = c.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.name = FONT; r.font.size = Pt(size); r.font.bold = bold
    r.font.color.rgb = fg
    return c


def header(s, kicker, title, accent=GOLD, kicker_fg=WHITE, title_size=27):
    global _page
    kw = Inches(min(0.45 + 0.093 * len(kicker), 4.2))
    chip(s, Inches(0.55), Inches(0.42), kw, Inches(0.34), kicker, accent, kicker_fg, size=11)
    txt(s, Inches(0.55), Inches(0.88), Inches(12.2), Inches(0.75),
        [[R(title, title_size, INK, True)]])
    rect(s, Inches(0.57), Inches(1.62), Inches(1.35), Pt(3), fill=accent)


def footer(s, label="Gardenscapes × Royal Match — сравнительный анализ"):
    global _page
    _page += 1
    if _page == 1:
        return
    txt(s, Inches(0.55), Inches(7.08), Inches(9.0), Inches(0.3),
        [[R(label, 9, MUT)]])
    txt(s, Inches(12.35), Inches(7.08), Inches(0.45), Inches(0.3),
        [[R(f"{_page:02d}", 9, MUT, True)]], align=PP_ALIGN.RIGHT)


def bullets(s, x, y, w, h, items, size=13, gap=8, marker_color=GOLD,
            head_color=INK, body_color=INK, line_spacing=1.04):
    """items: список ('заголовок', 'текст') или просто 'текст'."""
    paras = []
    for it in items:
        if isinstance(it, tuple):
            head, body = it
            runs = [R("▪  ", size, marker_color, True),
                    R(head, size, head_color, True)]
            if body:
                runs.append(R(" — " + body, size, body_color))
            paras.append(runs)
        else:
            paras.append([R("▪  ", size, marker_color, True), R(it, size, body_color)])
    return txt(s, x, y, w, h, paras, space_after=gap, line_spacing=line_spacing)


def card(s, x, y, w, h, title, items, accent, fill=WHITE, title_size=15,
         body_size=12.5, gap=7, badge=None):
    rect(s, x, y, w, h, fill=fill, line=LINE_GRAY, rounded=True, adj=0.045)
    rect(s, x, y, Inches(0.09), h, fill=accent, rounded=False)
    tx = x + Inches(0.28)
    txt(s, tx, y + Inches(0.17), w - Inches(0.5), Inches(0.4),
        [[R(title, title_size, accent, True)]])
    if badge:
        chip(s, x + w - Inches(1.75), y + Inches(0.18), Inches(1.5), Inches(0.3),
             badge, accent, WHITE, size=9.5)
    bullets(s, tx, y + Inches(0.62), w - Inches(0.55), h - Inches(0.8),
            items, size=body_size, gap=gap, marker_color=accent)


def set_cell(cell, paras, align=PP_ALIGN.LEFT, fill=None, anchor=MSO_ANCHOR.MIDDLE):
    if fill is not None:
        cell.fill.solid(); cell.fill.fore_color.rgb = fill
    cell.vertical_anchor = anchor
    cell.margin_left = Inches(0.1); cell.margin_right = Inches(0.1)
    cell.margin_top = Inches(0.045); cell.margin_bottom = Inches(0.045)
    tf = cell.text_frame
    tf.word_wrap = True
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = 1.0
        for (t, size, color, bold, italic) in runs:
            r = p.add_run(); r.text = t
            r.font.name = FONT; r.font.size = Pt(size)
            r.font.color.rgb = color; r.font.bold = bold; r.font.italic = italic


def table(s, x, y, w, data, col_w, row_h=Inches(0.52), header_fills=None,
          header_fg=None, body_size=11.5, head_size=11.5, col_aligns=None,
          row_fills=None):
    """data[0] — шапка; data[r][c] — str или список ранов."""
    rows, cols = len(data), len(data[0])
    gf = s.shapes.add_table(rows, cols, x, y, w, Emu(int(row_h) * rows))
    tbl = gf.table
    tbl.first_row = False
    tbl.horz_banding = False
    # убрать дефолтный стиль pptx (синие полосы)
    tblPr = tbl._tbl.find(qn('a:tblPr'))
    if tblPr is not None:
        for st in tblPr.findall(qn('a:tableStyleId')):
            tblPr.remove(st)
    for c, cw in enumerate(col_w):
        tbl.columns[c].width = cw
    for r_i in range(rows):
        tbl.rows[r_i].height = row_h
    for r_i, row in enumerate(data):
        for c_i, val in enumerate(row):
            cell = tbl.cell(r_i, c_i)
            is_head = (r_i == 0)
            if is_head:
                fill = header_fills[c_i] if header_fills else INK
                fg = (header_fg[c_i] if isinstance(header_fg, list) else header_fg) or WHITE
                paras = [[R(str(val), head_size, fg, True)]] if isinstance(val, str) else val
                set_cell(cell, paras, align=PP_ALIGN.CENTER, fill=fill)
            else:
                fill = None
                if row_fills is not None:
                    fill = row_fills[r_i - 1][c_i] if isinstance(row_fills[r_i - 1], (list, tuple)) else row_fills[r_i - 1]
                if fill is None:
                    fill = WHITE if r_i % 2 == 1 else RGBColor(0xF1, 0xEE, 0xE7)
                align = col_aligns[c_i] if col_aligns else PP_ALIGN.LEFT
                paras = [[R(str(val), body_size, INK)]] if isinstance(val, str) else val
                set_cell(cell, paras, align=align, fill=fill)
    return tbl


def insight(s, x, y, w, h, text_runs, accent=GOLD, fill=GOLD_LT, icon="→"):
    rect(s, x, y, w, h, fill=fill, rounded=True, adj=0.14)
    rect(s, x, y, Inches(0.09), h, fill=accent)
    txt(s, x + Inches(0.28), y, w - Inches(0.5), h,
        [[R(icon + "  ", 13, accent, True)] + text_runs],
        anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)


# ================================================================ 1. ТИТУЛ
s = new_slide(INK)
# декоративные фигуры
rect(s, Inches(-1.2), Inches(5.9), Inches(16), Inches(2.4), fill=RGBColor(0x27, 0x33, 0x52))
c1 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.6), Inches(-1.4), Inches(4.4), Inches(4.4))
c1.fill.solid(); c1.fill.fore_color.rgb = RGBColor(0x27, 0x33, 0x52); c1.line.fill.background(); c1.shadow.inherit = False
c2 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(11.7), Inches(-0.5), Inches(2.4), Inches(2.4))
c2.fill.solid(); c2.fill.fore_color.rgb = GOLD; c2.line.fill.background(); c2.shadow.inherit = False

chip(s, Inches(0.85), Inches(1.05), Inches(4.35), Inches(0.42),
     "ТЕСТОВОЕ ЗАДАНИЕ · JUNIOR GAME DESIGNER", GOLD, INK, size=12)
txt(s, Inches(0.85), Inches(1.85), Inches(11.6), Inches(2.3), [
    [R("Gardenscapes ", 48, RGBColor(0x8F, 0xD6, 0xA4), True),
     R("vs ", 48, RGBColor(0xB9, 0xC3, 0xD9), False),
     R("Royal Match", 48, RGBColor(0x9D, 0xBC, 0xF5), True)],
    [R("Сравнительный анализ дизайн-решений вовлечения и удержания игроков", 20, RGBColor(0xD8, 0xDD, 0xE9))],
])
txt(s, Inches(0.85), Inches(4.35), Inches(11.0), Inches(1.2), [
    [R("Дизайн-решения удержания  ·  Сравнение механик  ·  Проблемы Gardenscapes  ·  Предложения по улучшению",
       14, RGBColor(0x9A, 0xA5, 0xC0))],
])
rect(s, Inches(0.87), Inches(4.22), Inches(2.2), Pt(3), fill=GOLD)
txt(s, Inches(0.85), Inches(6.35), Inches(11.0), Inches(0.6), [
    [R("Кандидат: [Ваше имя]      ·      Playrix      ·      июль 2026", 13, RGBColor(0x8E, 0x99, 0xB5))],
])
footer(s)

# ================================================================ 2. СОДЕРЖАНИЕ
s = new_slide()
header(s, "СТРУКТУРА", "Пять вопросов — пять блоков ответа", GOLD)
items = [
    ("01", "Дизайн-решения вовлечения и удержания", "Какие приёмы используют обе игры: core, мета, live-ops, социальные и психологические механики", GS_GREEN),
    ("02", "Наиболее удачные решения", "Что работает лучше всего в каждой игре и почему — с позиции ретеншена и монетизации", GOLD),
    ("03", "Сравнительный анализ механик", "Пауэр-апы и core-геймплей · жизни и монетизация · мета-слой и live-ops", RM_BLUE),
    ("04", "Проблемы Gardenscapes", "Пейсинг меты, доверие к маркетингу, пики сложности, перегруженный UX", RED),
    ("05", "Что и как можно улучшить", "Конкретные решения с ожидаемым эффектом и метриками, приоритизация по impact / effort", GS_GREEN),
]
y = Inches(1.95)
for num, t, d, ac in items:
    rect(s, Inches(0.55), y, Inches(12.25), Inches(0.88), fill=WHITE, line=LINE_GRAY, rounded=True, adj=0.10)
    chip(s, Inches(0.75), y + Inches(0.22), Inches(0.62), Inches(0.44), num, ac, WHITE, size=14)
    txt(s, Inches(1.62), y + Inches(0.10), Inches(11.0), Inches(0.4),
        [[R(t, 15.5, INK, True)]])
    txt(s, Inches(1.62), y + Inches(0.47), Inches(11.0), Inches(0.35),
        [[R(d, 11.5, MUT)]])
    y += Inches(0.99)
footer(s)

# ================================================================ 3. ОБЗОР ИГР
s = new_slide()
header(s, "КОНТЕКСТ", "Две философии одного жанра", GOLD)
card(s, Inches(0.55), Inches(1.9), Inches(6.0), Inches(4.35),
     "Gardenscapes — «мета прежде всего»", [
        ("Playrix, 2016", "пионер формата match-3 + реновация"),
        ("Фантазия «своего сада»", "звёзды за уровни тратятся на восстановление сада по задачам"),
        ("Сюжет и персонажи", "дворецкий Остин, «сериальная» подача: игровой день = эпизод"),
        ("Глубокая прогрессия", "тысячи уровней, сезонные события, коллекции, команды"),
        ("Ставка на эмоциональную привязанность", "сад — «дом», который жалко бросить"),
     ], GS_GREEN, fill=GS_LIGHT, badge="MATCH-3 + META")
card(s, Inches(6.8), Inches(1.9), Inches(6.0), Inches(4.35),
     "Royal Match — «core прежде всего»", [
        ("Dream Games, 2021", "лидер жанра по выручке от IAP"),
        ("Максимально отполированный match-3", "быстрые анимации, высокая читаемость поля"),
        ("Минималистичная мета", "лёгкий декор замка короля Роберта — выбрана после A/B-тестов против «без меты» и «эпизодной меты»"),
        ("Плотный live-ops календарь", "6+ параллельных событий, пики — по выходным"),
        ("«Уважение к игроку»", "без принудительной рекламы, бесплатный шаффл, щедрый старт"),
     ], RM_BLUE, fill=RM_LIGHT, badge="CORE-FIRST")
insight(s, Inches(0.55), Inches(6.42), Inches(12.25), Inches(0.52),
        [R("Обе игры удерживают игрока, но разными «крючками»: Gardenscapes — привязанностью к прогрессу меты, Royal Match — азартом и темпом самого core-геймплея.", 12.5, INK)])
footer(s)

# ================================================================ 4. Q1 — GS
s = new_slide()
header(s, "ВОПРОС 1 · ВОВЛЕЧЕНИЕ И УДЕРЖАНИЕ", "Дизайн-решения Gardenscapes", GS_GREEN)
card(s, Inches(0.55), Inches(1.9), Inches(6.0), Inches(2.6),
     "Мета и нарратив", [
        ("Незавершённый сад (эффект Зейгарник)", "всегда есть начатая, но не законченная зона — она «тянет» вернуться"),
        ("Звёзды как валюта прогресса", "уровень → звезда → задача в саду: каждый уровень осмыслен"),
        ("Остин и сюжет", "персонаж-компаньон реагирует на прогресс, создаёт эмоциональный контекст"),
     ], GS_GREEN)
card(s, Inches(6.8), Inches(1.9), Inches(6.0), Inches(2.6),
     "Ритм возвращений", [
        ("Игровой день = эпизод", "естественная точка выхода и повод вернуться завтра"),
        ("Ежедневные награды и колесо удачи", "привычка ежедневного захода"),
        ("Сезонные события и декор", "ограниченные по времени украшения — FOMO"),
     ], GS_GREEN)
card(s, Inches(0.55), Inches(4.68), Inches(6.0), Inches(1.75),
     "Социальный слой", [
        ("Команды", "обмен жизнями, чат — социальное обязательство"),
        ("Турниры и лидерборды", "соревнование как причина «ещё одного уровня»"),
     ], GS_GREEN)
card(s, Inches(6.8), Inches(4.68), Inches(6.0), Inches(1.75),
     "Экономика удержания", [
        ("Жизни (5 шт.)", "пауза при проигрышах → «вернись позже» и защита от выгорания"),
        ("Бустеры и монеты", "накопление ресурсов привязывает к аккаунту"),
     ], GS_GREEN)
footer(s)

# ================================================================ 5. Q1 — RM
s = new_slide()
header(s, "ВОПРОС 1 · ВОВЛЕЧЕНИЕ И УДЕРЖАНИЕ", "Дизайн-решения Royal Match", RM_BLUE)
card(s, Inches(0.55), Inches(1.9), Inches(6.0), Inches(2.6),
     "Азарт и темп core-игры", [
        ("Win-streak → Super Light Ball", "серия побед даёт мощный бонус на старте; проигрыш сбрасывает серию — сильнейший стимул «не проиграть»"),
        ("Осцилляция сложности", "чередование лёгких и сложных уровней: пики напряжения + «отдых» → эмоциональные качели"),
        ("King's Nightmare", "milestone-уровни-испытания с возможностью пропуска — ощущение выбора"),
     ], RM_BLUE)
card(s, Inches(6.8), Inches(1.9), Inches(6.0), Inches(2.6),
     "Доверие как механика удержания", [
        ("Бесплатный шаффл", "нет ходов — поле перемешивается бесплатно, а не за бустер"),
        ("Только IAP, ноль принудительной рекламы", "session flow не прерывается"),
        ("Щедрый онбординг", "много наград на старте → доверие → конверсия позже"),
     ], RM_BLUE)
card(s, Inches(0.55), Inches(4.68), Inches(6.0), Inches(1.75),
     "Live-ops календарь", [
        ("6+ параллельных событий", "Team Battle, Weekly Contest, альбомы-коллекции, кооп «поезд»"),
        ("Пики по выходным", "выручка растёт за счёт событий, а не роста DAU"),
     ], RM_BLUE)
card(s, Inches(6.8), Inches(4.68), Inches(6.0), Inches(1.75),
     "Эндгейм и лёгкая мета", [
        ("Royal League", "турнир на 20 игроков для «доигравших контент»"),
        ("Декор областей", "мета в один тап — прогресс без когнитивной нагрузки"),
     ], RM_BLUE)
footer(s)

# ================================================================ 6. ПСИХОЛОГИЯ
s = new_slide()
header(s, "ВОПРОС 1 · ОБЩИЙ ФУНДАМЕНТ", "Психологические приёмы: одна база — разные акценты", GOLD)
data = [
    ["Приём", "Gardenscapes", "Royal Match"],
    [[[R("Loss aversion (страх потери)", 11, INK, True)]],
     "Потеря жизни, сгорающие награды событий",
     "Проигрыш сбрасывает win-streak — главный денежный рычаг"],
    [[[R("Near-miss («почти прошёл»)", 11, INK, True)]],
     "«Не хватило 2 ходов» → оффер +5 ходов",
     "То же ядро; уровни строятся под near-miss"],
    [[[R("Эффект Зейгарник", 11, INK, True)]],
     "Сад всегда «в ремонте», задачи дня открыты",
     "Недостроенная область, неполный альбом"],
    [[[R("Переменные награды", 11, INK, True)]],
     "Сундуки, колесо удачи, мини-игры",
     "Пропеллер, карточные паки, мини-игры"],
    [[[R("Социальное обязательство", 11, INK, True)]],
     "Команды, обмен жизнями",
     "Кооп-события: главный приз — общий на команду"],
]
table(s, Inches(0.55), Inches(1.9), Inches(12.25), data,
      [Inches(3.0), Inches(4.6), Inches(4.65)],
      row_h=Inches(0.6), body_size=11,
      header_fills=[INK, GS_GREEN, RM_BLUE])
insight(s, Inches(0.55), Inches(6.15), Inches(12.25), Inches(0.72),
        [R("Ключевая разница: Gardenscapes мотивирует «строй и возвращайся», Royal Match — «не прерывай серию». Второй приём короче по циклу и сильнее давит на сессионную активность.", 12, INK)])
footer(s)

# ================================================================ 7. Q2 — УДАЧНЫЕ РЕШЕНИЯ
s = new_slide()
header(s, "ВОПРОС 2", "Наиболее удачные решения", GOLD)
card(s, Inches(0.55), Inches(1.9), Inches(6.0), Inches(2.45),
     "Gardenscapes: мета + сюжет", [
        ("Долгосрочная эмоциональная привязка", "игрок «инвестировал» в сад месяцы — уйти психологически дорого"),
        ("Каждый уровень осмыслен", "звезда → видимое изменение мира, а не абстрактный счётчик"),
     ], GS_GREEN, fill=GS_LIGHT, badge="LTV / D30+")
card(s, Inches(6.8), Inches(1.9), Inches(6.0), Inches(2.45),
     "Royal Match: win-streak", [
        ("«Не проиграть» сильнее, чем «выиграть»", "серия превращает каждый уровень в ставку — растут и сессии, и конверсия в покупку ходов"),
        ("Монетизирует успех, а не только неудачу", "редкий случай в жанре"),
     ], RM_BLUE, fill=RM_LIGHT, badge="СЕССИИ / ARPDAU")
card(s, Inches(0.55), Inches(4.5), Inches(6.0), Inches(2.45),
     "Royal Match: дизайн доверия", [
        ("Бесплатный шаффл + отказ от рекламы", "воспринимается как «игра уважает моё время и ресурсы»"),
        ("Щедрый старт → покупки позже", "доверие конвертируется в LTV, а не в ранний отток"),
     ], RM_BLUE, fill=RM_LIGHT, badge="ДОВЕРИЕ / RETENTION")
card(s, Inches(6.8), Inches(4.5), Inches(6.0), Inches(2.45),
     "Общее: near-miss + live-ops", [
        ("Покупка +5 ходов в момент «почти прошёл»", "главный источник выручки жанра: высокая воспринимаемая ценность в точке фрустрации"),
        ("Событийный календарь", "постоянные краткосрочные цели поверх core-петли"),
     ], GOLD, fill=GOLD_LT, badge="МОНЕТИЗАЦИЯ")
footer(s)

# ================================================================ 8. Q3 — CORE / ПАУЭР-АПЫ
s = new_slide()
header(s, "ВОПРОС 3 · МЕХАНИКА 1", "Core-геймплей и пауэр-апы", RM_BLUE)
data = [
    ["Критерий", "Gardenscapes", "Royal Match"],
    ["Принцип создания",
     "От количества фишек: 4 → петарда, 5 → бомба, 6 → динамит, 7+ → TNT",
     "От формы матча: 4 в линию → ракета, 4 квадратом → пропеллер, 5 L/T → TNT, 5 в линию → световой шар"],
    ["Глубина решений",
     "Проще: «собирай больше» — одна ось мышления",
     "Глубже: игрок выбирает форму матча под задачу уровня"],
    ["Элемент случайности",
     "Rainbow Blast — заряжается взрывами пауэр-апов",
     "Пропеллер — «умная случайность», летит в полезную цель"],
    ["Темп и читаемость",
     "Анимации медленнее, поле визуально плотнее",
     "Быстрые анимации, высокий контраст → короткие бодрые сессии"],
]
table(s, Inches(0.55), Inches(1.95), Inches(12.25), data,
      [Inches(2.5), Inches(4.85), Inches(4.9)],
      row_h=Inches(0.83),
      header_fills=[INK, GS_GREEN, RM_BLUE], body_size=11.5)
insight(s, Inches(0.55), Inches(6.35), Inches(12.25), Inches(0.62),
        [R("Вывод: система «форма матча = тип пауэр-апа» даёт больше осознанных решений за ход и выше skill ceiling — core Royal Match интереснее сам по себе, без опоры на мету.", 12.5, INK)],
        accent=RM_BLUE, fill=RM_LIGHT)
footer(s)

# ================================================================ 9. Q3 — ЖИЗНИ И МОНЕТИЗАЦИЯ
s = new_slide()
header(s, "ВОПРОС 3 · МЕХАНИКА 2", "Жизни, экономика и монетизация", RM_BLUE)
data = [
    ["Критерий", "Gardenscapes", "Royal Match"],
    ["Система жизней",
     "5 жизней, регенерация по таймеру; жизни можно просить у команды",
     "5 жизней + частые подарки «безлимитных жизней» за события и командные награды"],
    ["Модель выручки",
     "IAP (монеты, бустеры, пропуска) + офферы; много параллельных валют",
     "Только IAP, одна валюта — монеты; ноль рекламы"],
    ["Точка покупки",
     "+5 ходов при near-miss, бустеры перед уровнем, пакеты в попапах",
     "+5 ходов при near-miss + защита win-streak — покупка «страхует» серию"],
    ["Давление на игрока",
     "Растёт с прогрессом: чаще пики сложности, больше попапов офферов",
     "Сдержанное в онбординге; давление концентрируется в событийных пиках"],
]
table(s, Inches(0.55), Inches(1.95), Inches(12.25), data,
      [Inches(2.5), Inches(4.85), Inches(4.9)],
      row_h=Inches(0.83),
      header_fills=[INK, GS_GREEN, RM_BLUE], body_size=11.5)
insight(s, Inches(0.55), Inches(6.35), Inches(12.25), Inches(0.62),
        [R("Вывод: Royal Match монетизирует меньшую долю игрового времени, но в более сильных эмоциональных точках (серия под угрозой) — выше конверсия при меньшем раздражении.", 12.5, INK)],
        accent=RM_BLUE, fill=RM_LIGHT)
footer(s)

# ================================================================ 10. Q3 — МЕТА И LIVE-OPS
s = new_slide()
header(s, "ВОПРОС 3 · МЕХАНИКА 3", "Мета-слой и live-ops", RM_BLUE)
data = [
    ["Критерий", "Gardenscapes", "Royal Match"],
    ["Мета-слой",
     "Тяжёлый: звёзды → задачи → сюжет; сад из многих зон, выбор вариантов декора",
     "Лёгкий: декор области в один тап; фон для core, а не отдельная игра"],
    ["Цена мета-прогресса",
     "1–2 звезды за уровень, задачи по 1–3 звезды → часы на один «эпизод»",
     "Ключи капают быстро, область закрывается за игровую сессию-две"],
    ["Live-ops",
     "Сезонные события, растянутые на недели; отдельные механики под событие",
     "6+ коротких параллельных событий с недельным ритмом и пиками в выходные"],
    ["Роль меты в удержании",
     "Главный крючок: ради сада терпят сложные уровни",
     "Вспомогательная: главный крючок — сам core и серия побед"],
]
table(s, Inches(0.55), Inches(1.95), Inches(12.25), data,
      [Inches(2.5), Inches(4.85), Inches(4.9)],
      row_h=Inches(0.83),
      header_fills=[INK, GS_GREEN, RM_BLUE], body_size=11.5)
insight(s, Inches(0.55), Inches(6.35), Inches(12.25), Inches(0.62),
        [R("Вывод: это не «лучше/хуже», а разные ставки. Но пейсинг меты Gardenscapes — самое уязвимое место: именно здесь копится усталость игрока (см. вопрос 4).", 12.5, INK)],
        accent=GOLD, fill=GOLD_LT)
footer(s)

# ================================================================ 11. Q4 — ПРОБЛЕМЫ GS
s = new_slide()
header(s, "ВОПРОС 4", "Проблемы Gardenscapes", RED)
probs = [
    ("1. Мета превращается в гринд",
     "Звёзды капают медленно, а задачи часто «бытовые» («полить клумбу»). Уровни начинают ощущаться работой ради валюты, связь «уровень → награда» обесценивается."),
    ("2. Разрыв между рекламой и игрой",
     "Креативы с pull-the-pin не соответствуют core-геймплею (запрет ASA, 2020). Обманутые ожидания → отток новичков, урон доверию и рейтингу в сторах."),
    ("3. Пики сложности + давление монетизации",
     "На средних и поздних уровнях сложность резко растёт синхронно с ростом офферов — читается игроками как «pay-to-win», источник негативных отзывов."),
    ("4. Перегруженный UX",
     "Каскад попапов с офферами на входе, много параллельных валют и событий — высокая когнитивная нагрузка до первого хода."),
    ("5. Темп core ниже конкурентов",
     "Медленные анимации и «количественные» пауэр-апы делают сессию менее динамичной на фоне Royal Match."),
    ("6. Эрозия доверия в мелочах",
     "Нет бесплатного шаффла и подобных «жестов уважения», которые стали новым стандартом жанра."),
]
y = Inches(1.85)
xs = [Inches(0.55), Inches(6.8)]
for i, (t, d) in enumerate(probs):
    x = xs[i % 2]
    rect(s, x, y, Inches(6.0), Inches(1.38), fill=WHITE, line=LINE_GRAY, rounded=True, adj=0.07)
    rect(s, x, y, Inches(0.09), Inches(1.38), fill=RED)
    txt(s, x + Inches(0.26), y + Inches(0.1), Inches(5.6), Inches(0.35),
        [[R(t, 12.5, RED, True)]])
    txt(s, x + Inches(0.26), y + Inches(0.42), Inches(5.6), Inches(0.92),
        [[R(d, 10.5, INK)]], line_spacing=1.02)
    if i % 2 == 1:
        y += Inches(1.52)
insight(s, Inches(0.55), Inches(6.45), Inches(12.25), Inches(0.5),
        [R("Общий корень: игра давит на игрока там, где Royal Match инвестирует в доверие.", 12.5, INK)],
        accent=RED, fill=RED_LIGHT, icon="!")
footer(s)

# ================================================================ 12. Q5 — УЛУЧШЕНИЯ
s = new_slide()
header(s, "ВОПРОС 5", "Что и как улучшить", GS_GREEN)
data = [
    ["Проблема", "Решение", "Ожидаемый эффект"],
    ["Мета-гринд",
     "Сжать стоимость задач в начале «эпизода»; добавить milestone-задачи и значимые развилки декора и сюжета",
     "D7 / D30 retention, время до дропа меты"],
    ["Разрыв рекламы и игры",
     "Встроить механики из креативов (pull-the-pin) как регулярный мини-режим; выровнять креативы с геймплеем",
     "Конверсия install → D1, рейтинг в сторах"],
    ["Пики сложности",
     "Осцилляция сложности по модели RM; win-streak с бонусом на старте уровня как награда за серию",
     "Длина сессии, конверсия near-miss без роста churn"],
    ["Перегруженный UX",
     "Контекстные офферы вместо каскада попапов; единый хаб событий",
     "Отказы в первые 60 сек сессии"],
    ["Темп core",
     "Ускорить анимации; бесплатный шаффл при отсутствии ходов",
     "Уровней за сессию, тон отзывов"],
]
table(s, Inches(0.55), Inches(1.9), Inches(12.25), data,
      [Inches(2.3), Inches(6.35), Inches(3.6)],
      row_h=Inches(0.68), body_size=11,
      header_fills=[RED, GS_GREEN, INK])
insight(s, Inches(0.55), Inches(6.35), Inches(12.25), Inches(0.62),
        [R("Принцип: не копировать Royal Match, а вернуть Gardenscapes его силу — осмысленную мету, убрав источники фрустрации вокруг неё.", 12, INK)],
        accent=GS_GREEN, fill=GS_LIGHT)
footer(s)

# ================================================================ 13. ПРИОРИТИЗАЦИЯ
s = new_slide()
header(s, "ВОПРОС 5 · ПЛАН ВНЕДРЕНИЯ", "Приоритизация: impact / effort", GS_GREEN)
cols = [
    ("QUICK WINS", GS_GREEN, GS_LIGHT, [
        ("Бесплатный шаффл", "маленькая фича — большой сигнал доверия"),
        ("Ускорение анимаций core", "конфиг + полировка, без изменения баланса"),
        ("Контекстные офферы", "правила показа вместо каскада попапов"),
    ]),
    ("СРЕДНИЙ ГОРИЗОНТ", GOLD, GOLD_LT, [
        ("Win-streak с наградой на старте", "требует баланса экономики и A/B-теста"),
        ("Единый хаб событий", "UX-редизайн главного экрана"),
        ("Пересборка кривой сложности", "данные по churn-уровням уже есть"),
    ]),
    ("СТРАТЕГИЧЕСКИЕ", RM_BLUE, RM_LIGHT, [
        ("Пейсинг меты и развилки сюжета", "затрагивает контент-пайплайн"),
        ("Выравнивание маркетинга и геймплея", "мини-режимы из креативов + новые креативы; долгий возврат доверия"),
    ]),
]
x = Inches(0.55)
for title, ac, fl, items in cols:
    rect(s, x, Inches(1.95), Inches(3.95), Inches(4.35), fill=fl, line=LINE_GRAY, rounded=True, adj=0.05)
    chip(s, x + Inches(0.25), Inches(2.18), Inches(2.3), Inches(0.36), title, ac, WHITE, size=11)
    bullets(s, x + Inches(0.28), Inches(2.75), Inches(3.45), Inches(3.4),
            items, size=11.5, gap=10, marker_color=ac)
    x += Inches(4.15)
insight(s, Inches(0.55), Inches(6.5), Inches(12.25), Inches(0.55),
        [R("Каждое изменение — через A/B-тест: подход самих Dream Games, доказавший, что даже «лёгкая мета» должна быть проверена данными, а не вкусом.", 12.5, INK)])
footer(s)

# ================================================================ 14. ВЫВОДЫ
s = new_slide()
header(s, "ИТОГ", "Выводы и метрики контроля", GOLD)
bullets(s, Inches(0.55), Inches(1.95), Inches(12.2), Inches(2.9), [
    ("Royal Match выигрывает «здесь и сейчас»", "темп core, win-streak и дизайн доверия дают лучшую сессионную динамику и конверсию."),
    ("Gardenscapes сильнее в эмоциональной привязке", "мета и сюжет — уникальный актив, который Royal Match сознательно не стал копировать."),
    ("Главные точки роста Gardenscapes", "пейсинг меты, честность к игроку (маркетинг, шаффл, офферы) и темп core-геймплея."),
    ("Философия изменений", "не догонять конкурента по фичам, а убрать фрустрацию вокруг своей главной силы — сада."),
], size=14, gap=12)
rect(s, Inches(0.55), Inches(4.85), Inches(12.25), Inches(1.55), fill=INK, rounded=True, adj=0.07)
txt(s, Inches(0.85), Inches(5.05), Inches(11.6), Inches(0.35),
    [[R("KPI ДЛЯ МОНИТОРИНГА ИЗМЕНЕНИЙ", 12, GOLD, True)]])
kpis = ["D1 / D7 / D30 retention", "Длина и частота сессий", "Конверсия near-miss", "ARPDAU", "Рейтинг в сторах"]
x = Inches(0.85)
for k in kpis:
    w = Inches(0.55 + 0.082 * len(k))
    chip(s, x, Inches(5.5), w, Inches(0.55), k, RGBColor(0x2C, 0x3A, 0x5E), WHITE, size=10.5, bold=False)
    x += w + Inches(0.15)
footer(s)

# ================================================================ 15. ФИНАЛ
s = new_slide(INK)
rect(s, Inches(-1.2), Inches(5.7), Inches(16), Inches(2.6), fill=RGBColor(0x27, 0x33, 0x52))
c1 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.9), Inches(-1.2), Inches(3.8), Inches(3.8))
c1.fill.solid(); c1.fill.fore_color.rgb = RGBColor(0x27, 0x33, 0x52); c1.line.fill.background(); c1.shadow.inherit = False
txt(s, Inches(0.85), Inches(1.7), Inches(11.6), Inches(1.6), [
    [R("Спасибо за внимание!", 44, WHITE, True)],
    [R("Готов(а) обсудить любой из разделов подробнее.", 18, RGBColor(0xB9, 0xC3, 0xD9))],
])
rect(s, Inches(0.87), Inches(3.35), Inches(2.2), Pt(3), fill=GOLD)
txt(s, Inches(0.85), Inches(3.7), Inches(11.6), Inches(2.6), [
    [R("ИСТОЧНИКИ И МАТЕРИАЛЫ", 12, GOLD, True)],
    [R("Собственные игровые сессии в обеих играх · справочные центры Playrix и Dream Games (механики пауэр-апов)", 11.5, RGBColor(0x9A, 0xA5, 0xC0))],
    [R("Naavik — разборы Royal Match и стратегии Dream Games · Sensor Tower — live-ops календарь Royal Match", 11.5, RGBColor(0x9A, 0xA5, 0xC0))],
    [R("ASA / BBC — решение по рекламе Gardenscapes и Homescapes (2020) · агрегаторы отзывов игроков", 11.5, RGBColor(0x9A, 0xA5, 0xC0))],
], space_after=6)
txt(s, Inches(0.85), Inches(6.4), Inches(11.6), Inches(0.5), [
    [R("Кандидат: [Ваше имя]  ·  [email / telegram]  ·  тестовое задание Junior Game Designer, Playrix", 12, RGBColor(0x8E, 0x99, 0xB5))],
])
footer(s)

# ---------------------------------------------------------------- сохранение
OUT = "gardenscapes_vs_royal_match.pptx"
prs.save(OUT)
print(f"OK: {OUT}, слайдов: {len(prs.slides.__iter__.__self__._sldIdLst)}")
