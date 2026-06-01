# Brza Dostava — Sustav narudžbi hrane

Sustav za naručivanje hrane iz restorana s upravljanjem narudžbama i dostavom.  
Projekt za kolegij **Razvoj web aplikacija** — SIT UNIZD.

---

## Tehnologije

| Sloj     | Stack                                          |
|----------|------------------------------------------------|
| Backend  | Python 3.11+, FastAPI, SQLAlchemy 2.0 (async) |
| Baza     | PostgreSQL 16 (Docker Compose)                 |
| Frontend | Vue 3, TypeScript, Pinia, Vue Router, Axios    |
| Auth     | JWT (access + refresh tokeni)                  |

---

## Preduvjeti

Prije pokretanja projekta trebate imati instalirano:

- **Python** ≥ 3.11 — [python.org/downloads](https://www.python.org/downloads/)
- **Docker Desktop** — [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
- **Node.js** ≥ 20 — [nodejs.org](https://nodejs.org/)
- **Git** — [git-scm.com](https://git-scm.com/)

---

## Brzo pokretanje

### 1. Kloniraj repo i kopiraj env varijable

```bash
git clone <url>
cd <repo>

# Linux/macOS:
cp .env.example .env

# Windows (PowerShell):
Copy-Item .env.example .env
```

### 2. Pokreni PostgreSQL bazu

```bash
docker compose up -d db
```

Provjera da baza radi:
```bash
docker compose ps
# Status treba biti "healthy"
```

> pgAdmin je dostupan na http://localhost:5050 (admin@admin.com / admin)

### 3. Pokreni backend (FastAPI)

```bash
cd api

# Kreiraj virtualno okruženje (jednom):
python -m venv .venv

# Aktiviraj ga:
# Linux/macOS:         source .venv/bin/activate
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# Windows cmd:         .venv\Scripts\activate.bat

# Instaliraj zavisnosti:
python -m pip install -r requirements.txt

# Primijeni migracije (kreira tablice):
python -m alembic upgrade head

# Umetni seed podatke:
python -m app.seed

# Pokreni dev server:
python -m uvicorn app.main:app --reload
```

### 4. Provjera backenda

- Health check: http://127.0.0.1:8000/health → `{"status": "ok"}`
- Swagger UI:   http://127.0.0.1:8000/docs

### 5. Pokreni frontend (Vue 3)

U **novom terminalu** (backend mora biti pokrenut):

```bash
cd web

# Instaliraj zavisnosti (jednom):
npm install

# Pokreni dev server:
npm run dev
```

Frontend se otvara na: http://localhost:5173

Za build (produkcija):

```bash
npm run build     # Generira web/dist/
npm run preview   # Lokalni pregled builda
```

> **Env varijabla:** Po defaultu frontend šalje zahtjeve na `http://localhost:8000`.
> Za produkcijski deploy dodaj `VITE_API_URL=https://tvoj-backend.url` u `.env` datoteku unutar `web/`.

---

## Korisnici za testiranje (seed)

| Uloga      | Korisničko ime  | Lozinka  | Opis                        |
|------------|-----------------|----------|-----------------------------|
| admin      | `admin`         | `admin123` | Administracija sustava    |
| restaurant | `pizza_owner`   | `rest123`  | Vlasnik Pizza Place-a     |
| restaurant | `burger_owner`  | `rest123`  | Vlasnik Burger House-a    |
| customer   | `customer1`     | `cust123`  | Kupac                     |
| courier    | `courier1`      | `cour123`  | Dostavljač                |

---

## Struktura projekta

```
repo/
├── api/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py           # App factory — sastavlja aplikaciju
│   │   ├── seed.py           # Seed podaci (admin, restorani, kupac, kurir)
│   │   ├── core/             # Infrastruktura (config, errors, logging)
│   │   │   ├── config.py     # Pydantic Settings — čita env varijable
│   │   │   ├── database.py   # SQLAlchemy engine, session, Base
│   │   │   ├── errors.py     # AppError + globalni exception handler
│   │   │   ├── phases.py     # OrderStatus enum (stanje narudžbe)
│   │   │   └── deps.py       # FastAPI dependencije (DB session, auth)
│   │   ├── routers/          # HTTP sloj — tanki routeri
│   │   ├── services/         # Poslovna logika (pravila, validacija)
│   │   ├── repositories/     # DB upiti (SQL, transakcije)
│   │   ├── models/           # SQLAlchemy ORM modeli (tablice)
│   │   └── schemas/          # Pydantic DTO-ovi (ulaz/izlaz API-ja)
│   ├── alembic/              # Alembic migracije
│   ├── alembic.ini
│   ├── tests/
│   ├── requirements.txt
│   └── pyproject.toml
├── web/                      # Vue 3 frontend
│   ├── src/
│   │   ├── main.ts           # Entry point (boot: dohvati /auth/me)
│   │   ├── App.vue           # Root — prebacuje layout (gost/aplikacija)
│   │   ├── router/           # Vue Router + role-based guardovi
│   │   ├── stores/           # Pinia: auth.ts, obavijesti.ts
│   │   ├── services/         # Axios API klijent + interceptor (auto-refresh)
│   │   ├── types/            # TypeScript interfacei za sve entitete
│   │   ├── components/       # Dijeljene komponente (Gumb, Modal, Tablica...)
│   │   ├── layouts/          # LayoutGost.vue, LayoutAplikacija.vue
│   │   ├── styles/           # CSS tokens, reset, globalne klase
│   │   └── views/
│   │       ├── admin/        # Restorani, Osoblje, Narudžbe (admin role)
│   │       ├── restoran/     # Jelovnik, Narudžbe (restaurant role)
│   │       ├── dostavljac/   # Dostave (courier role)
│   │       └── kupac/        # Restorani, Narudžbe (customer role)
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml        # PostgreSQL + pgAdmin
├── .env.example              # Primjer env varijabli (IDE U GIT)
├── .gitignore
└── README.md
```

---

## Slojevi backend arhitekture

Svaki sloj ima jednu odgovornost. Pravilo: **gornji sloj može zvati donji, ali nikad obrnuto**.

```
  HTTP request
       ↓
  ┌─────────┐
  │ Router   │  Parsira request, poziva service, vraća HTTP response.
  └────┬─────┘  NE sadrži poslovnu logiku.
       ↓
  ┌─────────┐
  │ Service  │  Provodi poslovna pravila (statusi, vlasništvo, validacija).
  └────┬─────┘  NE zna za HTTP status kodove.
       ↓
  ┌──────────────┐
  │ Repository   │  Izvršava SQL upite, vraća domenske objekte.
  └──────┬───────┘  NE zna za poslovnu logiku.
         ↓
  ┌─────────┐
  │   DB    │  PostgreSQL
  └─────────┘
```

| Sloj         | Odgovornost                              | Primjer datoteke              |
|--------------|------------------------------------------|-------------------------------|
| Router       | HTTP: parsiranje requesta, status kodovi | `routers/orders.py`           |
| Service      | Poslovna pravila, validacija, orkestra.  | `services/order_service.py`   |
| Repository   | SQL upiti, transakcije                   | `repositories/order_repo.py`  |
| Model        | ORM definicija tablica                   | `models/order.py`             |
| Schema (DTO) | Pydantic ulaz/izlaz modeli               | `schemas/order.py`            |

---

## Git konvencije

### Commit poruke

Format: `<tip>(<scope>): <opis>`

| Tip        | Značenje                             |
|------------|--------------------------------------|
| `feat`     | Nova funkcionalnost                  |
| `fix`      | Ispravka buga                        |
| `refactor` | Promjena bez nove funkcionalnosti    |
| `chore`    | Tooling, config, infrastruktura      |
| `docs`     | Dokumentacija                        |
| `test`     | Testovi                              |

Scope: `api`, `web`, ili prazan za root-level promjene.

### Env varijable

- Tajne (lozinke, JWT secret) **NIKAD** ne idu u git
- `.env.example` sadrži ključeve s demo vrijednostima — ide u git
- `.env` sadrži stvarne vrijednosti — **NE** ide u git (vidi `.gitignore`)
- U produkciji: env varovi dolaze iz platforme (Railway/Render)

---

## Baza podataka — workflow

### Modeli (ORM)

SQLAlchemy modeli žive u `api/app/models/`. Svaki model je Python klasa
koja odgovara jednoj tablici u bazi:

| Model        | Tablica       | Opis                                      |
|--------------|---------------|-------------------------------------------|
| `User`       | `users`       | Korisnik (admin, restaurant, courier, customer) |
| `Restaurant` | `restaurants` | Restoran s vlasnikom (owner_id → users)   |
| `MenuItem`   | `menu_items`  | Stavka jelovnika (restaurant_id → restaurants) |
| `Order`      | `orders`      | Narudžba s statusom i tijek isporuke      |
| `OrderItem`  | `order_items` | Stavke unutar narudžbe (snapshot cijene)  |

### Stanja narudžbe (OrderStatus)

```
pending → accepted → preparing → ready → on_the_way → delivered
                ↘                                        
              cancelled (samo pending, od strane kupca ili admina)
```

| Status       | Tko mijenja        |
|--------------|--------------------|
| → accepted   | restaurant         |
| → preparing  | restaurant         |
| → ready      | restaurant         |
| → on_the_way | courier            |
| → delivered  | courier            |
| → cancelled  | customer (pending) |

### Migracije (Alembic)

Alembic je "version control za bazu" — svaka promjena modela zahtijeva novu migraciju.

```bash
cd api

# Primijeni sve migracije (kreira tablice):
python -m alembic upgrade head

# Rollback zadnje migracije:
python -m alembic downgrade -1

# Generiraj novu migraciju nakon promjene modela:
python -m alembic revision --autogenerate -m "opis promjene"

# Prikaži povijest migracija:
python -m alembic history
```

> **Važno:** Uvijek pročitaj generiranu migraciju prije `upgrade`!
> Autogenerate može pogriješiti (npr. rename stupca → drop + create).

### Seed podaci

Seed skripta kreira inicijalne podatke za razvoj:

```bash
cd api
python -m app.seed
```

Kreira korisnike, 2 restorana s jelovnicima, kupca i dostavljača (vidi tablicu gore).

Skripta je **idempotentna** — sigurno je pokrenuti je više puta
(preskače zapise koji već postoje).

### Potpuni reset baze

Kad želiš krenuti ispočetka (briše SVE podatke):

```bash
docker compose down -v                        # Obriši kontejner + volume
docker compose up -d db                       # Pokreni svježu bazu
cd api
python -m alembic upgrade head               # Kreiraj tablice
python -m app.seed                           # Umetni seed podatke
```

### Direktan pristup bazi (psql)

```bash
docker exec -it mojprojekt1-db-1 psql -U fd_user -d food_delivery

# Korisni SQL upiti:
# \dt                              — lista tablica
# SELECT id, username, role FROM users;   — pregled korisnika
# SELECT * FROM restaurants;       — pregled restorana
# SELECT * FROM orders;            — pregled narudžbi
# \q                               — izlaz
```

---

## Korisne naredbe

```bash
# -- Baza --
docker compose up -d db          # Pokreni PostgreSQL
docker compose ps                # Status kontejnera
docker compose logs db           # Logovi baze
docker compose down              # Zaustavi sve
docker compose down -v           # Zaustavi + obriši podatke (reset)

# -- Backend (iz api/ direktorija, s aktiviranim venvom) --
python -m uvicorn app.main:app --reload    # Dev server s auto-reloadom
python -m pytest                           # Pokreni testove
python -m alembic upgrade head            # Primijeni sve migracije
python -m alembic downgrade -1            # Rollback zadnje migracije
python -m alembic revision --autogenerate -m "opis"  # Nova migracija
python -m app.seed                        # Seed podatke u bazu

# -- Frontend (iz web/ direktorija) --
npm run dev                      # Dev server (http://localhost:5173)
npm run build                    # Produkcijski build
npm run typecheck                # TypeScript provjera

# -- Git --
git log --oneline --decorate     # Kratki pregled povijesti
git diff <commit1>..<commit2>    # Usporedba dva commita
git show <commit>                # Detalji jednog commita
```
