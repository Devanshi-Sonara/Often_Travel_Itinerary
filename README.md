# Often Travel Itinerary API 🌴✈️

A **FastAPI-powered** backend system for managing and recommending travel itineraries, designed as a solution for the SDE Intern assignment. Supports CRUD operations for itineraries (with day-wise accommodations, transfers, and activities) and provides intelligent recommendations via an MCP server.

---

## Features 🚀

### Core Functionality
- **Itinerary Management**:
  - Create itineraries with nested days, accommodations, transfers, and activities.
  - Fetch all itineraries or a specific itinerary by ID.
- **MCP Recommendation Engine**:
  - Get tailored itinerary recommendations based on desired trip duration (nights).
  - Falls back to closest matches if exact duration isn’t available.

### Technical Highlights
- **Relational Database Modeling**: PostgreSQL/SQLite with SQLAlchemy ORM.
- **RESTful API**: Fully documented with Swagger UI and ReDoc.
- **Data Validation**: Pydantic schemas for robust input/output modeling.
- **Seeding System**: Pre-populated with sample itineraries for Phuket/Krabi.

---

## Tech Stack 💻

| Category       | Technologies/Tools                         |
|----------------|--------------------------------------------|
| **Backend**    | FastAPI (Python 3.11+)                     |
| **Database**   | PostgreSQL (or SQLite for dev)             |
| **ORM**        | SQLAlchemy 2.0+                            |
| **Deployment** | Render/Vercel/Heroku (compatible)          |
| **Tools**      | Pydantic, Uvicorn, Alembic (for migrations)|

---

## Database Schema 🗄️

```plaintext
itineraries
├─ id
├─ name
├─ region (Phuket/Krabi)
├─ total_nights
└─ days (1-to-many)
   ├─ day_number
   ├─ accommodations (1-to-many)
   │  ├─ hotel
   │  ├─ city
   │  ├─ check_in/check_out
   ├─ transfers (1-to-many)
   │  ├─ from/to_loc
   │  ├─ mode (flight/ferry/taxi)
   │  ├─ depart/arrive
   └─ activities (1-to-many)
      ├─ name
      ├─ description
      ├─ start/end time
      ├─ price
```


## API Endpoints 📡

### Itineraries
| Method | Endpoint             | Description                          | Status Codes |
|--------|----------------------|--------------------------------------|--------------|
| `POST` | `/itineraries/`      | Create a new itinerary               | 201, 422     |
| `GET`  | `/itineraries/`      | List all itineraries (paginated)     | 200          |
| `GET`  | `/itineraries/{id}`  | Get details of a specific itinerary  | 200, 404     |

### Recommendations (MCP)
| Method | Endpoint             | Description                          | Query Param  |
|--------|----------------------|--------------------------------------|--------------|
| `GET`  | `/recommendations/`  | Get itineraries by night duration    | `nights=int` |

## Setup & Installation ⚙️

1. **Clone the Repository**
```bash
git clone https://github.com/Devanshi-Sonara/Often_Travel_Itinerary.git
```
2. **Configure Environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. **Install Dependencies**
```bash
pip install -r requirements.txt
```
4. **Database Setup**
PostgreSQL: Update DATABASE_URL in .env (or use SQLite default).

Auto-create tables (dev mode):

```bash
python main.py  # Triggers Base.metadata.create_all()
Seed sample data (Phuket/Krabi itineraries):
```
```bash
python seed.py
```
5. **Run the Server**
```bash
uvicorn main:app --reload
```

## Example Requests 🌐
**Create an Itinerary**
```bash
curl -X POST "http://127.0.0.1:8000/itineraries/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Phuket Adventure",
  "region": "Phuket",
  "total_nights": 3,
  "days": [
    {
      "day_number": 1,
      "accommodations": [{"hotel": "Beach Resort", "city": "Phuket", "check_in": "2025-06-01", "check_out": "2025-06-02"}],
      "transfers": [{"from_loc": "Airport", "to_loc": "Resort", "mode": "taxi", "depart": "08:00", "arrive": "08:45"}],
      "activities": [{"name": "Island Hopping", "start": "09:00", "end": "17:00"}]
    }
  ]
}'

```
**Get Recommendations**
```bash
curl "http://127.0.0.1:8000/recommendations/?nights=4"
```

