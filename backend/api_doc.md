# 🧾 SalesPath API Handbook

## 📍 Base URL

```
http://your_ip:5000 -> get the ip when "python run.py"
```

---

## 🔌 Test Connection

### `GET /`

Test database connectivity.

**Response:**

- `✅ Connected to MySQL successfully!`
- or error message if DB fails

---

## 👤 Salesmen

### `GET /api/salesmen`

Returns all salesmen.

**Response:**

```json
[{ "SalesName": "Alice" }, { "SalesName": "Bob" }]
```

---

## 🧾 Clients

### `GET /api/clients`

Returns all clients.

**Response:**

```json
[
  {
    "ClientId": "CL001",
    "ClientReg": "Bangkok",
    "ClientSubReg": "Pathumwan",
    "ClientType": "Retail",
    "SalesName": "Alice"
  },
  ...
]
```

---

## 📅 Visits

### `GET /api/visits`

Returns all visits, with optional filters and invoice matching.

**Query Parameters (optional):**

- `from`: ISO date (e.g. `2024-01-01`)
- `to`: ISO date (e.g. `2024-12-31`)
- `sales`: SalesName to filter by
- `region`: Client region

**Response:**

```json
[
  {
    "VisitId": 1,
    "SalesName": "Alice",
    "ClientId": "CL001",
    "VisitDateTime": "2024-04-18T10:00:00",
    "Activity": "Sale",
    "Notes": "Followed up with client",
    "ProblemNotes": null,
    "Resolved": true,
    "InvoiceAmount": 5000.00
  },
  ...
]
```

---

### `POST /api/visits`

Create a new visit record.

**Request Body:**

```json
{
  "SalesName": "Alice",
  "ClientId": "CL001",
  "Activity": "Problem",
  "Notes": "Issue reported",
  "ProblemNotes": "Incorrect delivery",
  "Resolved": false
}
```

**Optional field:** `VisitDateTime` (ISO format)

**Response:**

```json
{
  "message": "Visit created successfully",
  "visit": {
    "VisitId": 2,
    ...
  }
}
```

---

## 🔍 Prospects

### `GET /api/prospects`

Returns all prospects with optional filters.

**Query Parameters (optional):**

- `sales`: SalesName
- `region`: ProspectReg

**Response:**

```json
[
  {
    "ProspectId": 1,
    "ProspectReg": "Bangkok",
    "ProspectSubReg": "Pathumwan",
    "SalesName": "Alice"
  }
]
```

---

### `POST /api/prospects`

Create a new prospect.

**Request Body:**

```json
{
  "ProspectReg": "Bangkok",
  "ProspectSubReg": "Pathumwan",
  "SalesName": "Alice"
}
```

**Response:**

```json
{
  "message": "Prospect created successfully",
  "prospect": {
    "ProspectId": 1,
    ...
  }
}
```

---

## 🧪 Sample Error Response

```json
{
  "error": "Missing required fields"
}
```
