# TradeSense AI - SaaS Platform

## Prerequisites
- Python 3.9+
- Node.js 18+ (for Frontend)
- PostgreSQL (Production) / SQLite (Dev)

## Quick Start Scope

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

pip install -r requirements.txt

# Initialize Database
python init_db.py

# Run Server
python app.py
```
Backend will run on `http://localhost:5000`

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend will run on `http://localhost:3000`

## Architecture Highlights
- **Multi-tenant**: Database schema supports `tenant_id` segregation.
- **Market Data**: Interface `IMarketDataProvider` supports `YFinance`, `Polygon`, and `DefeatBeta`.
- **Prop Firm Logic**: `ChallengeService` enforces Daily Loss and Drawdown limits.
- **Frontend**: Next.js 14 App Router, TailwindCSS.

## API Documentation
- `POST /api/v1/<tenant>/auth/login`
- `GET /api/v1/<tenant>/market-data/last?symbol=EURUSD`
- `POST /api/v1/<tenant>/trades/`

## Troubleshooting

### Frontend Setup Issues / "npx not found"
If you encounter errors running `npx` or `npm`:
1. **Install Node.js**: Download and install the LTS version from [nodejs.org](https://nodejs.org/).
2. **Verify Installation**: Open a new terminal and run `node -v` and `npm -v`.
3. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```
4. **Run Dev Server**:
   ```bash
   npm run dev
   ```

### Missing Types
If you see "Cannot find module 'react'" errors in your editor, run `npm install` in the frontend directory to download the necessary type definitions.
