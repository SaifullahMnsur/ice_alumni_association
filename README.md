# API Documentation

This document provides details of the available API endpoints for the events system.

## Base URL
All endpoints are prefixed with `https://saifullahmnsur.pythonanywhere.com/api/`.

---

## Event Endpoints

---

### 1. **List All Events**
- **URL**: `/api/events/`
- **Method**: `GET`
- **Description**: Retrieves a paginated list of all events.
- **Pagination**:
  - **Mandatory Query Parameters**:
    - `page`: The page number to fetch. This parameter is required.
    - `page_size`: The number of events per page. This parameter is required. The default value is `10` if not specified.
  - **Maximum Page Size**: 100 (Maximum page size allowed).

**Example Request**:
```plaintext
GET /api/events/?page=1&page_size=2
```
**Response**:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "event_id": "ICE-RU-Silver-Jubilee",
            "title": "ICE-RU-Silver-Jubilee",
            "description": "ICE-RU-Silver-Jubilee",
            "start_time": "2024-12-31T20:08:10Z",
            "end_time": "2025-01-01T20:08:14Z",
            "location": "Rajshahi, Bangladesh",
            "status": "upcoming",
            "created_at": "2024-12-31T20:08:29.781282Z",
            "updated_at": "2024-12-31T20:52:40.596782Z",
            "media_file": "http://localhost:8000/media/event_media/ICE-RU-Silver-Jubilee.jpg",
            "details": "http://localhost:8000/api/events/ICE-RU-Silver-Jubilee/?format=json"
        }
    ]
}
```

- `count`: Total number of events.
- `next`: URL for the next page of events (if available).
- `previous`: URL for the previous page of events (if available).
- `results`: List of events for the current page.

**Note**: 
- The `page` and `page_size` parameters are **mandatory**.
- By default, `page_size` is set to `10` if not provided.
- `page_size` can be customized by passing the query parameter `page_size` (up to a maximum of 100).

---

This ensures that the example request comes first, followed by the response with all the relevant details for the pagination API.

---

### 2. **Retrieve Event Details**
- **URL**: `/api/events/<str:event_id>/`
- **Method**: `GET`
- **Description**: Fetches details of a specific event using its `event_id`.
- **Response**:
  ```json
  {
    "event_id": "ICE-RU-Silver-Jubilee",
    "title": "ICE-RU-Silver-Jubilee",
    "description": "ICE-RU-Silver-Jubilee",
    "start_time": "2024-12-31T20:08:10Z",
    "end_time": "2025-01-01T20:08:14Z",
    "location": "Rajshahi, Bangladesh",
    "status": "upcoming",
    "created_at": "2024-12-31T20:08:29.781282Z",
    "updated_at": "2024-12-31T20:52:40.596782Z",
    "media_file": "http://localhost:8000/media/event_media/ICE-RU-Silver-Jubilee.jpg",
    "details": "http://localhost:8000/api/events/ICE-RU-Silver-Jubilee/?format=json"
  }
  ```
---


Here’s the updated documentation with tweaked values for the `/api/events/<slug:event_id>/register/` endpoint:

---

### 3. **Register for an Event**
- **URL**: `/api/events/<slug:event_id>/register/`
- **Method**: `POST`
- **Description**: Registers a participant for the specified event.

**Request Format**:
- Content-Type: `multipart/form-data`

**Request Parameters**:
| Field                | Type       | Required | Description                               |
|----------------------|------------|----------|-------------------------------------------|
| `student_id`         | `string`   | Yes      | Unique ID for the participant.            |
| `full_name`          | `string`   | Yes      | Full name of the participant.             |
| `date_of_birth`      | `date`     | Yes      | Participant's date of birth (YYYY-MM-DD). |
| `batch`              | `string`   | Yes      | Batch information of the participant.     |
| `session`            | `string`   | Yes      | Academic session of the participant.      |
| `email`              | `email`    | Yes      | Email address of the participant.         |
| `contact_number`     | `string`   | Yes      | Contact number of the participant.        |
| `whatsapp_number`    | `string`   | Yes      | WhatsApp number of the participant.       |
| `adult_guests`       | `integer`  | Yes      | Number of adult guests accompanying.      |
| `child_guests`       | `integer`  | Yes      | Number of child guests accompanying.      |
| `total_amount`       | `integer`  | No/Auto      | Total amount for the registration. total_amount will be auto calculated based on given data. Use the api to show total amount        |
| `payment_method`     | `string`   | Yes      | Payment method chosen (e.g., bkash, bank).|
| `transaction_id`     | `string`   | Yes      | Unique transaction ID for payment.        |
| `transaction_document` | `file`    | Yes      | File for the transaction document.        |
| `profile_picture`    | `file`     | Yes      | Profile picture of the participant.       |
| `password`           | `string`   | Yes      | Password for participant's account.       |

**Example Request**:
```plaintext
POST /api/events/ICE-RU-Silver-Jubilee/register/
```

**Example Form Data**:
```plaintext
student_id: 2110778000
full_name: John Doe
date_of_birth: 1995-10-15
batch: 22
session: 2020-2021
email: johndoe@gmail.com
contact_number: +8801234567890
whatsapp_number: +8809876543210
adult_guests: 3
child_guests: 1
total_amount: 12000.00
payment_method: bank
transaction_id: TX789123
transaction_document: <uploaded_file>
profile_picture: <uploaded_file>
password: example_password
```

**Response**:
```json
{
    "student_id": "2110778000",
    "full_name": "John Doe",
    "date_of_birth": "1995-10-15",
    "batch": "22",
    "session": "2020-2021",
    "email": "johndoe@gmail.com",
    "contact_number": "+8801234567890",
    "whatsapp_number": "+8809876543210",
    "adult_guests": 3,
    "child_guests": 1,
    "total_amount": "11000",
    "payment_method": "bank",
    "transaction_id": "TX789123",
    "transaction_document": "http://localhost:8000/media/transactions_documents/2110778000.jpg",
    "profile_picture": "http://localhost:8000/media/profile_picture/2110778000.jpg",
    "password": "pbkdf2_sha256$870000$5xybnh0HUIJgshgeG7fRLe$1hvkgWRkc3OSPYREn5xvQ7WJpYN65zddU6HQ4PhML0w=",
    "event": "ICE-RU-Silver-Jubilee"
}
```

**Note**:
- Ensure all required fields are provided.
- The `transaction_document` and `profile_picture` must be valid uploaded files.
- The `password` field is securely hashed before storage.


---

Here's how the updated documentation would look for the `calculate_total_amount` endpoint with the required `event_id` and optional query parameters `child_guests` and `adult_guests`:

---

### 4. **Calculate Total Amount for Event**

- **URL**: `/api/events/<event_id>/calculate_total_amount/`
- **Method**: `GET`
- **Description**: Calculates the total amount for an event based on the number of guests (adult and child).
- **Mandatory Query Parameters**:
  - `event_id`: The ID of the event for which the total amount is to be calculated. This is required.
  
- **Optional Query Parameters**:
  - `adult_guests`: The number of adult guests attending the event. Defaults to `0` if not provided.
  - `child_guests`: The number of child guests attending the event. Defaults to `0` if not provided.

**Example Request**:

```plaintext

GET /api/events/ICE-RU-Silver-Jubilee/calculate_total_amount/?event_id=ICE-RU-Silver-Jubilee&child_guests=3&adult_guests=4

```

**Response**:
```json
{
    "total_amount": 15000
}
```

**Note**: 
- `event_id` is **mandatory**.
- If `adult_guests` or `child_guests` are not provided, they default to `0`.
- The response contains the calculated total amount based on the provided guest numbers.

---
This ensures that the `event_id` is clearly mentioned as mandatory, and the `adult_guests` and `child_guests` parameters are optional with default values of `0`.

---

### 5. **Get Payment Methods**
- **URL**: `/api/events/<slug:event_id>/payment-methods/`
- **Method**: `GET`
- **Description**: Fetches the payment methods available for a specific event.
- **Response**:
  ```json
  {
      "bkash": {
          "account_number": "017XXXXXXXX",
          "payment_option": "make payment"
      },
      "nagad": {
          "account_number": "018XXXXXXXX",
          "payment_option": "send money"
      },
      "rocket": {
          "account_number": "019XXXXXXXX",
          "payment_option": "make payment"
      },
      "bank": {
          "account_name": "John Doe",
          "account_number": "1234567890",
          "bank_name": "Example Bank",
          "branch_name": "Main Branch",
          "swift_code": "EXAMPLE123",
          "routing_number": "123456",
          "city": "Dhaka",
          "country": "Bangladesh"
      }
  }
  ```

---

## Notes
1. **Error Responses**: If an error occurs (e.g., event not found, validation failure), the API returns an error message with the appropriate HTTP status code.
   ```json
   {
       "detail": "Event not found."
   }
   ```
2. **Authentication**: Add authentication details if applicable.
3. **Pagination**: Add pagination to list endpoints if needed.
```