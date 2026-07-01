# 📚 Online Kutubxona Bot

Aiogram 2.x asosida qurilgan, minglab elektron kitob, audiokitob, darslik va lug'atlarni foydalanuvchilarga yetkazib beruvchi to'liq funksional Telegram bot. Bot production muhitida ishlab, real foydalanuvchilarga xizmat ko'rsatgan (`@E_KitobXazinasi_Bot`).

## Imkoniyatlari

### Foydalanuvchilar uchun
- Kategoriya bo'yicha kitob qidirish (o'zbek/jahon/mumtoz adabiyoti, bolalar adabiyoti, diniy kitoblar, she'riyat va h.k.)
- 1–11-sinf darsliklari (o'zbek va rus tillarida, fanlar va sinflar bo'yicha filtrlash)
- Audiokitoblar katalogi
- Wikipedia integratsiyasi — botdan chiqmasdan maqola qidirish (FSM holatlari orqali boshqariladi)
- Botni baholash tizimi — foydalanuvchi baho qoldirsa, admin darhol xabar oladi
- Guruhga qo'shilganda avtomatik tanishtiruv xabari

### Admin uchun
- **Statistika paneli** — foydalanuvchilar va guruhlar sonini real vaqtda ko'rish
- **Broadcast (reklama) tizimi** — istalgan turdagi kontent (matn/rasm/video/post) barcha foydalanuvchi va guruhlarga inline tasdiqlash bosqichi bilan yuboriladi
- Xatolarni kuzatish — yuborilmagan (bloklangan) xabarlar soni alohida hisoblanadi

## Arxitektura

```
kutubxona_bot/
├── config/              # Bot sozlamalari, ADMINS ro'yxati
├── filters/             # Custom filterlar: IsPrivate, IsGroup, AdminFilter
├── handlers/
│   ├── users/           # start, help, echo, admin (asosiy logika)
│   ├── groups/          # guruhga qo'shilganda ishlaydigan handler
│   └── errors/          # xatoliklarni ushlash
├── keyboards/
│   └── default/         # ReplyKeyboardMarkup'lar (dinamik menyu)
├── middlewares/         # DB middleware, throttling (spam himoyasi)
├── states/              # FSM holatlari (AdminReklama, WikiState)
├── utils/
│   ├── db.py            # SQLite ustida custom Database klassi
│   └── misc/            # logging, throttling yordamchi funksiyalari
├── app.py               # Kirish nuqtasi
└── loader.py            # dp, bot, storage obyektlari
```

## Texnik yechimlar

- **FSM (Finite State Machine)** — admin broadcast jarayoni ikki bosqichda: kontent qabul qilish → inline tugmalar orqali tasdiqlash/bekor qilish
- **Middleware** — har bir so'rovda foydalanuvchi/guruh avtomatik bazaga yoziladi; throttling middleware spam so'rovlarning oldini oladi
- **Filter-based routing** — `IsPrivate`, `IsGroup`, `AdminFilter` orqali handler'lar kontekstga qarab ajratiladi
- **SQLite** — `utils/db.py`dagi custom `Database` klassi orqali foydalanuvchi/guruh ma'lumotlari saqlanadi

## O'rnatish

```bash
git clone https://github.com/sobirturdiev006-lang/kutubxona_bot.git
cd kutubxona_bot

python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# .env-shablon asosida .env yarating va quyidagilarni to'ldiring:
# BOT_TOKEN=
# ADMINS=

python app.py
```

## Ma'lum cheklov

Kitoblar katalogi hozircha handler kodiga bevosita yozilgan (`file_id` orqali). Bu yondashuvning sababi — Telegramning `file_id` qiymatlari **faqat shu aniq bot tokeniga bog'liq** bo'lib, boshqa bot orqali qayta ishlatib bo'lmaydi.

**Kelajakdagi rejalar:**
- [ ] Kitoblar katalogini PostgreSQL/SQLite jadvaliga ko'chirish (hardcoded ro'yxat o'rniga)
- [ ] Admin uchun kitob qo'shish/o'chirish CRUD paneli
- [ ] Qidiruv funksiyasi (kategoriya bo'yicha emas, nom bo'yicha qidirish)
- [ ] Pagination — katalogni sahifalab ko'rsatish

## Texnologiyalar

- Python 3.11
- Aiogram 2.x
- SQLite
- Wikipedia API (`wikipedia` kutubxonasi)

## Muallif

Junior Backend Developer — Aiogram va bot arxitekturasini mustahkamlash maqsadida qurilgan, real foydalanuvchilarga xizmat ko'rsatgan loyiha.