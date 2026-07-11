#!/usr/bin/env python3
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

BG = RGBColor(0xF7, 0xF5, 0xF0)
INK = RGBColor(0x1F, 0x2A, 0x44)
MUT = RGBColor(0x5A, 0x64, 0x78)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GS = RGBColor(0x2F, 0x8F, 0x4E)
GS_LT = RGBColor(0xE3, 0xF1, 0xE6)
RM = RGBColor(0x2D, 0x5F, 0xC1)
RM_LT = RGBColor(0xE6, 0xED, 0xFA)
GOLD = RGBColor(0xE0, 0xA2, 0x38)
GOLD_LT = RGBColor(0xFA, 0xF0, 0xDC)
RED = RGBColor(0xBE, 0x4F, 0x45)
RED_LT = RGBColor(0xF8, 0xE7, 0xE4)
LINE = RGBColor(0xDE, 0xDA, 0xD2)
FONT = "Arial"
SW = Inches(13.333)
SH = Inches(7.5)

prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH
BLANK = prs.slide_layouts[6]


def run(text, size=12, color=INK, bold=False, italic=False):
    return text, size, color, bold, italic


def slide(bg=BG):
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    r.fill.solid()
    r.fill.fore_color.rgb = bg
    r.line.fill.background()
    r.shadow.inherit = False
    return s


def box(s, x, y, w, h, fill=WHITE, line=None, rounded=False, radius=0.08):
    shape = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        x, y, w, h
    )
    if rounded:
        shape.adjustments[0] = radius
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(0.7)
    shape.shadow.inherit = False
    return shape


def text(s, x, y, w, h, paragraphs, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, gap=3, spacing=1.0):
    shape = s.shapes.add_textbox(x, y, w, h)
    frame = shape.text_frame
    frame.word_wrap = True
    frame.vertical_anchor = anchor
    frame.margin_left = 0
    frame.margin_right = 0
    frame.margin_top = 0
    frame.margin_bottom = 0
    for index, runs in enumerate(paragraphs):
        p = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        p.alignment = align
        p.space_after = Pt(gap)
        p.line_spacing = spacing
        for value, size, color, bold, italic in runs:
            r = p.add_run()
            r.text = value
            r.font.name = FONT
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.italic = italic
    return shape


def chip(s, x, y, w, label, color, fg=WHITE, size=10.5):
    shape = box(s, x, y, w, Inches(0.34), color, rounded=True, radius=0.5)
    frame = shape.text_frame
    frame.margin_left = Inches(0.05)
    frame.margin_right = Inches(0.05)
    frame.margin_top = 0
    frame.margin_bottom = 0
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.name = FONT
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = fg


def header(s, kicker, title, color=GOLD, size=27):
    width = Inches(min(0.48 + len(kicker) * 0.094, 4.3))
    chip(s, Inches(0.55), Inches(0.34), width, kicker, color)
    text(s, Inches(0.55), Inches(0.78), Inches(12.2), Inches(0.62),
         [[run(title, size, INK, True)]])
    box(s, Inches(0.57), Inches(1.43), Inches(1.35), Pt(3), color)


def footer(s):
    number = len(prs.slides)
    if number == 1:
        return
    text(s, Inches(0.55), Inches(7.13), Inches(9), Inches(0.18),
         [[run("Gardenscapes × Royal Match — сравнительный анализ", 8, MUT)]])
    text(s, Inches(12.4), Inches(7.13), Inches(0.35), Inches(0.18),
         [[run(f"{number:02d}", 8, MUT, True)]], align=PP_ALIGN.RIGHT)


def bullet_list(s, x, y, w, h, items, color=GOLD, size=11,
                gap=5, spacing=1.0):
    paragraphs = []
    for item in items:
        if isinstance(item, tuple):
            title, body = item
            paragraphs.append([
                run("▪  ", size, color, True),
                run(title, size, INK, True),
                run(" — " + body, size, INK)
            ])
        else:
            paragraphs.append([
                run("▪  ", size, color, True),
                run(item, size, INK)
            ])
    text(s, x, y, w, h, paragraphs, gap=gap, spacing=spacing)


def card(s, x, y, w, h, title, items, color, fill=WHITE,
         title_size=14, body_size=10.5, gap=5):
    box(s, x, y, w, h, fill, LINE, True, 0.05)
    box(s, x, y, Inches(0.08), h, color)
    text(s, x + Inches(0.25), y + Inches(0.13),
         w - Inches(0.42), Inches(0.38),
         [[run(title, title_size, color, True)]])
    bullet_list(s, x + Inches(0.25), y + Inches(0.55),
                w - Inches(0.45), h - Inches(0.68),
                items, color, body_size, gap, 1.0)


def mini_card(s, x, y, w, h, title, body, color=RED, fill=WHITE):
    box(s, x, y, w, h, fill, LINE, True, 0.06)
    box(s, x, y, Inches(0.07), h, color)
    text(s, x + Inches(0.2), y + Inches(0.08),
         w - Inches(0.34), Inches(0.27),
         [[run(title, 10.5, color, True)]])
    text(s, x + Inches(0.2), y + Inches(0.36),
         w - Inches(0.34), h - Inches(0.41),
         [[run(body, 8.7, INK)]], spacing=0.95)


def set_cell(cell, paragraphs, fill, align=PP_ALIGN.LEFT):
    cell.fill.solid()
    cell.fill.fore_color.rgb = fill
    cell.margin_left = Inches(0.08)
    cell.margin_right = Inches(0.08)
    cell.margin_top = Inches(0.035)
    cell.margin_bottom = Inches(0.035)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    frame = cell.text_frame
    frame.word_wrap = True
    for index, runs in enumerate(paragraphs):
        p = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        p.alignment = align
        p.space_after = 0
        p.line_spacing = 0.95
        for value, size, color, bold, italic in runs:
            r = p.add_run()
            r.text = value
            r.font.name = FONT
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.italic = italic


def data_table(s, x, y, w, rows, widths, row_h, header_fills,
               body_size=9.5):
    shape = s.shapes.add_table(
        len(rows), len(rows[0]), x, y, w, Emu(int(row_h) * len(rows))
    )
    table = shape.table
    table.first_row = False
    table.horz_banding = False
    props = table._tbl.find(qn("a:tblPr"))
    if props is not None:
        for style in props.findall(qn("a:tableStyleId")):
            props.remove(style)
    for index, width in enumerate(widths):
        table.columns[index].width = width
    for index in range(len(rows)):
        table.rows[index].height = row_h
    for r_index, row in enumerate(rows):
        for c_index, value in enumerate(row):
            if r_index == 0:
                paragraphs = [[run(value, 10.5, WHITE, True)]]
                set_cell(table.cell(r_index, c_index), paragraphs,
                         header_fills[c_index], PP_ALIGN.CENTER)
            else:
                fill = WHITE if r_index % 2 else RGBColor(0xF0, 0xED, 0xE7)
                paragraphs = value if isinstance(value, list) else [
                    [run(value, body_size, INK)]
                ]
                set_cell(table.cell(r_index, c_index), paragraphs, fill)


def insight(s, y, message, color=GOLD, fill=GOLD_LT, size=11.5):
    box(s, Inches(0.55), y, Inches(12.25), Inches(0.48),
        fill, LINE, True, 0.15)
    box(s, Inches(0.55), y, Inches(0.08), Inches(0.48), color)
    text(s, Inches(0.82), y, Inches(11.7), Inches(0.48),
         [[run("→  ", size, color, True),
           run(message, size, INK)]],
         anchor=MSO_ANCHOR.MIDDLE)


s = slide(INK)
box(s, Inches(-1), Inches(5.9), Inches(15.5), Inches(2), RGBColor(0x2A, 0x36, 0x56))
circle = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.7), Inches(-1.1),
                            Inches(4.1), Inches(4.1))
circle.fill.solid()
circle.fill.fore_color.rgb = RGBColor(0x2A, 0x36, 0x56)
circle.line.fill.background()
circle.shadow.inherit = False
gold_circle = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(11.9), Inches(-0.35),
                                 Inches(2.1), Inches(2.1))
gold_circle.fill.solid()
gold_circle.fill.fore_color.rgb = GOLD
gold_circle.line.fill.background()
gold_circle.shadow.inherit = False
chip(s, Inches(0.85), Inches(0.95), Inches(4.25),
     "ТЕСТОВОЕ ЗАДАНИЕ · JUNIOR GAME DESIGNER", GOLD, INK, 11.5)
text(s, Inches(0.85), Inches(1.72), Inches(11.7), Inches(1.45), [[
    run("Gardenscapes ", 46, RGBColor(0x8F, 0xD6, 0xA4), True),
    run("vs ", 46, RGBColor(0xB9, 0xC3, 0xD9)),
    run("Royal Match", 46, RGBColor(0x9D, 0xBC, 0xF5), True)
]])
text(s, Inches(0.85), Inches(3.15), Inches(10.9), Inches(0.75), [[
    run("Сравнительный анализ дизайн-решений, механик и точек роста",
        20, RGBColor(0xD8, 0xDD, 0xE9))
]])
box(s, Inches(0.87), Inches(4.17), Inches(2.2), Pt(3), GOLD)
text(s, Inches(0.85), Inches(4.38), Inches(11.2), Inches(0.8), [[
    run("Фокус: личный игровой опыт, удержание, основной цикл, live-ops и монетизация",
        13, RGBColor(0x9A, 0xA5, 0xC0))
]])
text(s, Inches(0.85), Inches(6.45), Inches(11), Inches(0.35), [[
    run("Кандидат: [Ваше имя]   ·   Playrix   ·   июль 2026",
        12, RGBColor(0x8E, 0x99, 0xB5))
]])
footer(s)

s = slide()
header(s, "1 · УДЕРЖАНИЕ И ВОВЛЕЧЕНИЕ",
       "Сильнейшие крючки Gardenscapes", GS)
card(s, Inches(0.55), Inches(1.7), Inches(6.05), Inches(4.95),
     "Почему игрок возвращается", [
         ("Восстановление, а не постройка",
          "контраст «до/после» усиливает ценность труда; 3 варианта оформления дают самовыражение и чувство собственности"),
         ("Сюжет и жизнь персонажей",
          "эмоциональная привязанность; клиффхэнгер в конце дня создаёт следующую цель"),
         ("Постоянное разнообразие",
          "новые механики → затем ивенты, коллекции, социальные активности и мини-игры"),
         ("Лимиты и таймеры",
          "жизни и энергия возвращают по таймеру; ограниченные события ускоряют прохождение"),
         ("Социальный слой",
          "помощь = взаимность, кооп = долг, профили = статус, PvP = азарт"),
         ("Сниженный донатный прессинг",
          "награды за сюжет, ивенты и помощь клана поддерживают лояльность")
     ], GS, GS_LT, 14, 10.4, 6)
card(s, Inches(6.8), Inches(1.7), Inches(6.0), Inches(4.95),
     "Наиболее удачные решения", [
         ("Винстрик престартовых бустеров",
          "страх потери мотивирует тратить монеты и инвентарь; моё самое сильное наблюдение"),
         ("Накопленный труд в саду",
          "чем больше вложено, тем дороже психологически бросить игру — долгосрочный retention"),
         ("Временные жизни, бустеры и множители",
          "«поиграю, пока не закончилось» удлиняет сессию"),
         ("PvP и активности на скорость",
          "эмоции и спешка повышают ошибки, расход ходов и сокращают жизнь винстрика"),
         ("Соревнование на выбывание",
          "«Болотное испытание» держит напряжение лучше одиночного аналога; Royal Match усилил формулу в «Лавовом приключении»")
     ], GOLD, GOLD_LT, 14, 10.4, 6)
footer(s)

s = slide()
header(s, "2 · СРАВНЕНИЕ МЕХАНИК",
       "Основной цикл, комбо и интеграция мини-игр", RM)
rows = [
    ["Аспект", "Gardenscapes", "Royal Match"],
    ["Комбо",
     "Взрывы заряжают «ульт» — молнию. Прогресс копится пошагово.",
     "Бустеры объединяют эффекты: больше решений, выше предсказуемость исхода."],
    ["Молния / световой шар",
     "Молния комбинируется только с молнией, зато не исчезает от других взрывов: можно сначала раскрыть цветы, затем собрать их.",
     "Световой шар раскрывается в разных комбинациях и сильнее по вариативности."],
    ["Пауэр-апы",
     "Количество фишек определяет радиус. Петарда слаба и редко стоит хода.",
     "Форма матча определяет эффект; пропеллер легко собрать, он полезен сам и в комбо."],
    ["Стартовые бустеры",
     "Дополнительные ходы полезны всегда; другие бустеры хотя бы заряжают молнию.",
     "Тесные поля часто не дают разместить стартовые бустеры — их ценность девальвируется."],
    ["Разделение поля",
     "Порталы и стенки: визуально сложнее, но добавляют игровые механики.",
     "Отдельные плашки фона: проще и чище, но менее системно."],
    ["Мини-игры",
     "Редкие, почти не развиваются, слабо награждают и ощущаются чужеродно.",
     "«Кошмар Короля» органичнее: знакомые механики, эмоциональный накал и перебивка ритма."]
]
data_table(s, Inches(0.55), Inches(1.72), Inches(12.25), rows,
           [Inches(2.0), Inches(5.1), Inches(5.15)], Inches(0.67),
           [INK, GS, RM], 9.3)
insight(s, Inches(6.53),
        "Комбо Royal Match интереснее и предсказуемее; похожее решение уже есть у Playrix в Mystery Matters.",
        RM, RM_LT, 11)
footer(s)

s = slide()
header(s, "3 · СРАВНЕНИЕ МЕТА-СИСТЕМ",
       "Сессия, социал, события и монетизация", RM)
rows = [
    ["Аспект", "Gardenscapes", "Royal Match"],
    ["Продолжительность сессии",
     "Временные подарки реже, но удерживает разнообразие дополнительных активностей.",
     "Безлимитные жизни, бустеры и x2 чередуются: постоянный крючок «пока не закончится»."],
    ["Множитель x2",
     "Таймеры наград сильнее подталкивают продолжать прямо сейчас.",
     "Бонус x2 не ограничен временем и хуже ускоряет сессию, зато продаётся отдельно."],
    ["Социальные активности",
     "Кооп, помощь и PvP есть, но вклад и матчмейкинг ощущаются менее конкурентными.",
     "Больше турниров и PvP; весомый вклад в командные события лучше совпадает с аудиторией."],
    ["Предсказуемость «почти победы»",
     "Неясно, сколько ходов не хватает; покупка продолжения рискованнее.",
     "Часто не хватает 1–2 ходов: игрок понимает, что покупка почти гарантирует победу."],
    ["Платные паки",
     "Офферы менее соблазнительны и хуже показывают будущую ценность.",
     "Цепочка «бесплатный бонус → покупка → ещё бесплатные подарки» и второй оффер как боевой пропуск со скидкой."],
    ["PvP-эмоция",
     "Лидеры часто недосягаемы — возможная проблема матчмейкинга.",
     "Соперники идут рядом; частые первые места дают понятную порцию дофамина."]
]
data_table(s, Inches(0.55), Inches(1.72), Inches(12.25), rows,
           [Inches(2.0), Inches(5.1), Inches(5.15)], Inches(0.68),
           [INK, GS, RM], 9.3)
insight(s, Inches(6.55),
        "Royal Match лучше продаёт продолжение: игрок видит достижимый результат и ценность оффера.",
        GOLD, GOLD_LT, 11)
footer(s)

s = slide()
header(s, "4 · ПРОБЛЕМЫ GARDENSCAPES",
       "Точки трения, замеченные в игровой сессии", RED)
problems = [
    ("Маркетинг ≠ основной цикл",
     "Иконка и первые скриншоты обещают pull-the-pin, который почти не встречается."),
    ("Головоломки",
     "Мало уровней, слабая оптимизация, нет роста сложности, награды ничтожны."),
    ("Чужеродные мини-игры",
     "Не развиваются и не награждают: непонятно, зачем они существуют."),
    ("Слабый онбординг",
     "Динамит и TNT изучаются опытным путём; поиск гномов объяснён неясно."),
    ("Бесполезная петарда",
     "Редко оправдывает ход; пропеллер Royal Match собирается проще и полезнее."),
    ("«Магическая шляпа» поздно",
     "До открытия игра пугает будущим paywall; после — темп резко улучшается."),
    ("Маленькие отступы от края",
     "На mini-девайсах жесты у края вызывают шторку или смену приложения."),
    ("Непредсказуемый проигрыш",
     "В отличие от Royal Match, неясно, спасут ли дополнительные ходы."),
    ("Скрытая сложность",
     "Некоторые трудные уровни не отмечены — расход бустера ощущается ловушкой."),
    ("PvP-матчмейкинг",
     "До лидера невозможно приблизиться; соревнование перестаёт мотивировать."),
    ("Потеря незаконченного уровня",
     "Разрядка телефона засчитывается как поражение — сильное чувство несправедливости."),
    ("Эрозия доверия",
     "Сумма мелких проблем создаёт больше давления, чем лояльности.")
]
for index, (title_value, body) in enumerate(problems):
    col = index % 3
    row = index // 3
    mini_card(s,
              Inches(0.55 + col * 4.12),
              Inches(1.7 + row * 1.25),
              Inches(3.88), Inches(1.1),
              title_value, body, RED,
              RED_LT if index in (0, 5, 7) else WHITE)
insight(s, Inches(6.62),
        "Главный риск — игрок уходит до того, как «Магическая шляпа» раскроет быстрый и увлекающий темп.",
        RED, RED_LT, 10.7)
footer(s)

s = slide()
header(s, "5 · ЧТО УЛУЧШИТЬ СНАЧАЛА",
       "Основной цикл, онбординг, честность и монетизация", GS)
improvements = [
    ("1. Раньше открыть «Шляпу»",
     "Сбалансировать первые уровни; дать временный бесплатный бустер. Проверять по D1/D7 и уровню раннего оттока.",
     GS, GS_LT),
    ("2. Углубить головоломки",
     "Больше уровней, рост сложности и заметные награды — реальная связка рекламы с продуктом.",
     GS, GS_LT),
    ("3. Обучать через зрелище",
     "Начинать обучающие уровни с активации бустера и каскада анимаций; отдельно объяснить TNT, динамит и гномов.",
     RM, RM_LT),
    ("4. Добавить бонусные уровни",
     "После сложных уровней давать расслабляющую сессию с большим количеством монет, как в Royal Match.",
     RM, RM_LT),
    ("5. Сохранить незаконченный уровень",
     "После сворачивания или разрядки восстанавливать состояние; минимум — предупреждать о низком заряде.",
     RED, RED_LT),
    ("6. Починить честность сложности",
     "Маркировать сложные уровни, улучшить прогноз «почти победы» и матчмейкинг PvP; увеличить отступы от края.",
     RED, RED_LT),
    ("7. Развить винстрик",
     "Сделать бустеры временными; добавить «заморозку» или восстановление за монеты — референс Duolingo.",
     GOLD, GOLD_LT),
    ("8. Пересобрать офферы",
     "Заимствовать цепочку Royal Match: бесплатный вход → понятный пакет → видимая будущая награда.",
     GOLD, GOLD_LT)
]
for index, (title_value, body, color, fill) in enumerate(improvements):
    col = index % 2
    row = index // 2
    mini_card(s,
              Inches(0.55 + col * 6.25),
              Inches(1.7 + row * 1.25),
              Inches(6.0), Inches(1.1),
              title_value, body, color, fill)
insight(s, Inches(6.62),
        "Порядок: сначала снизить ранний отток и несправедливость, затем усиливать монетизацию.",
        GS, GS_LT, 11)
footer(s)

s = slide()
header(s, "6 · БЭКЛОГ ИДЕЙ",
       "События, социальный слой и мета", GOLD)
rows = [
    ["Идея", "Как работает", "Зачем"],
    ["Экспедиция 2.0",
     "Больше крафта и сбора; факелы и открытие клеток; выборы в диалогах и загадки с повтором за энергию.",
     "Глубина вместо простой расчистки прохода."],
    ["Рогалик",
     "Череда карт с новым расположением элементов и гномов; мета-прокачка запаса бустеров или упрощения карт.",
     "Реиграбельность и вариативные сессии."],
    ["Раскраска-коллекция",
     "За уровни выпадают краски; обмен с друзьями или рецепт 3 ненужных → 1 нужная.",
     "Коллекционирование + социальная торговля."],
    ["Соревнование на эффективность",
     "Побеждает игрок, закончивший уровень за меньшее количество ходов.",
     "Состязание мастерства вместо одной гонки по времени."],
    ["Статус и достижения",
     "Показывать % прохождения с первого раза; ачивки и просмотр достижений других игроков.",
     "Мастерство, статусность, темы для профиля."],
    ["Кастомизация",
     "Дополнительный декор за монеты, платные скины персонажей.",
     "Новые точки расхода валюты и косметическая монетизация."],
    ["Личная локация + соцсвязь",
     "Личная локация с предметами, помощью и ресурсами; визиты, публикация участков и голосование за лучший декор.",
     "Чувство собственности должно пересекаться с геймплеем."]
]
data_table(s, Inches(0.55), Inches(1.68), Inches(12.25), rows,
           [Inches(2.45), Inches(6.2), Inches(3.6)], Inches(0.63),
           [INK, GS, RM], 9.1)
footer(s)

s = slide(INK)
box(s, Inches(-1), Inches(5.75), Inches(15.5), Inches(2), RGBColor(0x2A, 0x36, 0x56))
text(s, Inches(0.85), Inches(0.8), Inches(11.7), Inches(0.8),
     [[run("Главный вывод", 38, WHITE, True)]])
box(s, Inches(0.87), Inches(1.72), Inches(2.2), Pt(3), GOLD)
text(s, Inches(0.85), Inches(2.05), Inches(11.5), Inches(2.6), [
    [run("Gardenscapes уже сильнее в главном: ", 20, RGBColor(0x8F, 0xD6, 0xA4), True),
     run("восстановление сада создаёт чувство собственности и долгосрочную привязанность.", 20, WHITE)],
    [run("Точка роста — дать игроку раньше почувствовать эту силу: ", 20, RGBColor(0x9D, 0xBC, 0xF5), True),
     run("ускорить ранний основной цикл, честно объяснить механики и сделать результат хода предсказуемее.", 20, WHITE)]
], gap=16, spacing=1.05)
text(s, Inches(0.85), Inches(4.85), Inches(11.5), Inches(0.6), [[
    run("Приоритет проверки: ранняя «Магическая шляпа» → честные «почти победы» и сложность → улучшенные головоломки → новые социальные события.",
        13, RGBColor(0xB9, 0xC3, 0xD9))
]])
text(s, Inches(0.85), Inches(6.35), Inches(11.4), Inches(0.5), [[
    run("Основа анализа: личные игровые сессии и заметки кандидата   ·   [Ваше имя]   ·   [email / telegram]",
        11, RGBColor(0x8E, 0x99, 0xB5))
]])
footer(s)

prs.save("gardenscapes_vs_royal_match.pptx")
print(f"OK: gardenscapes_vs_royal_match.pptx, слайдов: {len(prs.slides)}")
