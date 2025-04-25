# 📊 SalesPath API Documentation

This document provides an overview of the RESTful APIs exposed by the SalesPath backend (Flask + SQLAlchemy), for managing sales activities, client tracking, revenue analysis, and prospect logging.

---

## ⚖️ General

### `GET /`

**Test database connection**

- Response: ✅ Connected or ❌ Failed message

---

## 💼 Salesman

### `GET /api/salesmen`

**Get all salesmen**

- Returns: List of salesmen with basic info

---

## 📈 Client

### `GET /api/clients`

**Get all clients**

- Returns: List of clients

### `GET /api/clients-per-salesman`

**Get total and visited clients per salesman (optional date range)**

- Query Params:
  - `from`: Start datetime
  - `to`: End datetime
- Returns: List of salesmen with `TotalClients` and `VisitedClients`

---

## 📆 Visits

### `GET /api/visits`

**Fetch visits with optional filters and revenue data**

- Query Params (all optional):
  - `from`: Start datetime
  - `to`: End datetime
  - `sales`: Filter by SalesName
  - `region`: Filter by ClientReg
  - `activity`: Filter by Visit.Activity (e.g., "Sale", "Problem")
  - `resolved`: 0 or 1 (filter resolved status)
- Returns: List of visits with associated invoice revenue

### `POST /api/visits`

**Create a new visit record**

- Body:

```json
{
  "SalesName": "Alex",
  "ClientId": "CL001",
  "Activity": "Problem",
  "Notes": "Note here",
  "ProblemNotes": "Issue observed",
  "Resolved": 0,
  "VisitDateTime": "2024-04-22T10:00:00"
}
```

- Returns: Created visit object

### `PUT /api/visit/<visit_id>/resolve`

**Update resolved status of a specific visit**

- Body:

```json
{ "Resolved": 1 }
```

- Returns: Confirmation message with updated resolved status

---

## 💰 Revenue

### `GET /api/revenue`

**Get total revenue per salesman in a time range**

- Query Params:
  - `from`, `to`: Date range
  - `region`: Optional region filter
- Returns: List of `{ SalesName, TotalRevenue }`

---

## 📅 Prospects

### `GET /api/prospects`

**Get prospects with optional filters**

- Query Params:
  - `sales`: SalesName
  - `region`: ProspectReg
- Returns: List of prospects

### `POST /api/prospects`

**Add a new prospect**

- Body:

```json
{
  "ProspectReg": "Chiang Mai",
  "ProspectSubReg": "Hang Dong",
  "SalesName": "Joe"
}
```

- Returns: Created prospect object

---

## ⚡ Problem Reports

### `GET /api/problems`

**Fetch visits with Activity = "Problem"**

- Optional Filters:
  - `sales`: SalesName
  - `region`: ClientReg
  - `from`: Start datetime
  - `to`: End datetime
- Returns: List of problem-related visits with:
  - ClientId
  - ClientReg
  - ClientSubReg
  - ClientType
  - VisitDateTime
  - ProblemNotes
