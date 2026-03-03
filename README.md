# AddressBook

A minimal REST API to create, update, delete, and query addresses. Addresses are stored with coordinates and can be retrieved by location (within a given distance of a point). Uses FastAPI, SQLAlchemy (SQLite), and geopy for geodesic distance.

## Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd AddressBook
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   cd backend\src
   pip install -r requirements.txt
   ```

4. **Configure environment**:

   From `backend\src`, copy the example env file into `backend`:

   ```bash
   copy ..\.env.example ..\.env
   ```

   Tables are created automatically on first run.

5. **Run the application**:

   From `backend\src`:

   ```bash
   uvicorn app:app --reload --port 8080
   ```

   The API will be available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/addresses` | Create an address (body: `latitude`, `longitude`, optional `label`) |
| GET | `/api/v1/addresses` | List all addresses, or filter by `latitude`, `longitude`, `radius_km` (all three required for distance filter) |
| GET | `/api/v1/addresses/{id}` | Get one address by ID |
| PATCH | `/api/v1/addresses/{id}` | Update an address (partial: `latitude`, `longitude`, `label`) |
| DELETE | `/api/v1/addresses/{id}` | Delete an address |

- **Coordinates**: `latitude` in [-90, 90], `longitude` in [-180, 180].
- **Distance query**: For `GET /api/v1/addresses`, pass query parameters `latitude`, `longitude`, and `radius_km` (positive) to get only addresses within that radius (km) of the point. Omit them to list all addresses.
