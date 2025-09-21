# Insurance Premium Policy Service

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/buromlangshylla/policy-service.git
   cd policy-service
   ```

2. **Create and activate a virtual environment:**
   ```
   python -m venv venv-policy
   venv-policy\Scripts\activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```
   python manage.py migrate
   ```

5. **Run the development server:**
   ```
   python manage.py runserver
   ```

## API Endpoints

All endpoints are prefixed with `/policies/`.

### List Policies (with filters, pagination, ordering, and search)

**GET** `/policies/`

**Query Parameters:**
- `status`: string
- `start_date`: `YYYY-MM-DD`
- `end_date`: `YYYY-MM-DD`
- `grace_period_end_date`: `YYYY-MM-DD`
- `agent_id`: integer (must be a valid user ID from auth service)
- `ordering`: field name (e.g., `start_date`, `-end_date`)
- `search`: string (searches relevant fields)
- `page`: integer (for pagination)
- `page_size`: integer (items per page)

**Example:**
```
GET /policies/?status=active&agent_id=123&page=1&page_size=10&ordering=-start_date
```

### Policy Detail

**GET** `/policies/{id}/`

**Example:**
```
GET /policies/1/
```

### Create Policy

**POST** `/policies/`

**Request Body (JSON):**
- `policy_number`: string
- `status`: string (e.g., `active`, `inactive`)
- `start_date`: `YYYY-MM-DD` (must be greater than `end_date`)
- `end_date`: `YYYY-MM-DD`
- `grace_period_end_date`: `YYYY-MM-DD`
- `agent_id`: integer (must be a valid user ID from auth service)
- other required fields as per your model

**Example:**
```
POST /policies/
Content-Type: application/json
{
  "policy_number": "POL123456",
  "status": "active",
  "start_date": "2025-10-01",
  "end_date": "2025-09-30",
  "grace_period_end_date": "2025-10-15",
  "agent_id": 123
}
```

Returns the created policy object or validation errors.

## Data Types

- `status`: string (e.g., `active`, `inactive`)
- `start_date`, `end_date`, `grace_period_end_date`: `YYYY-MM-DD`
- `agent_id`: integer

## Postman Collection

The Postman collection for this API is included in the repository as `insurance.postman_collection.json`.

**To use:**
1. Open Postman.
2. Click `Import`.
3. Select the file `insurance.postman_collection.json` from the project root.
4. Access all example requests and documentation for the API.

---

For more details, see the source code and API documentation in the Postman workspace.
