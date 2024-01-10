# Grade Planner Backend

The Grade Planner Backend serves as the backbone for the Grade Planner application, enabling data extraction from the relevant student academic documents. This repository houses the backend written in Python and built using FastAPI.

## Features

### Endpoints

#### API Endpoints

- `/api/v1/result`: Extracts result data from a student's uploaded result document.

`Sample Response`:

```json
{
	...
    "courses": [
      {
        "course_code": "EDS211",
        "title": "Entrepreneurial Development Studies III",
        "unit": 1
      },
      {
        "course_code": "GEC210",
        "title": "Engineering Mathematics I",
        "unit": 3
      },
      {
        "course_code": "GEC212",
        "title": "Engineering Graphics",
        "unit": 2
      },
      {
        "course_code": "GEC213",
        "title": "Materials Science & Engineering",
        "unit": 2
      },
	...
}
```

- `/api/v1/course_reg`: Extracts a student's course data from the uploaded course registration document.

`Sample Response`:

```json
{
	...
    "semesters": [
      {
        "courses": [
          {
            "course_code": "CHM111",
            "title": "General Physical Chemistry",
            "unit": 3,
            "grade": "A",
            "grade_point": 15
          },
          {
            "course_code": "CHM119",
            "title": "General Chemistry Practical I",
            "unit": 1,
            "grade": "A",
            "grade_point": 5
          },
          {
            "course_code": "CIT111",
            "title": "Microsoft Office Specialist on Microsoft Office 20",
            "unit": 0,
            "grade": "A",
            "grade_point": 0
          },
		...
}
```

### Documentation

The API documentation is available at `/docs` endpoint.

### File Upload Format

The backend accepts file uploads in PDF format for result and course registration documents.

## Implementation Details

### Technologies Used

- Written in Python
- Server built with FastAPI

### PDF Parsing

- The backend leverages PDF parsing capabilities to extract relevant data from uploaded documents.

- **Limitations:** The PDF parsing functionality is specifically tailored to Covenant University documents. While it may work with other institutions' documents, compatibility is not guaranteed.

## Setup

To run the Grade Planner Backend locally:

1. Clone this repository.
2. Install the necessary dependencies.
3. Run the server.

### Local Development

1. Clone the repository:

   ```bash
   git clone https://github.com/gradeplanner-backend.git
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt

   ```

3. Start the server

   ```bash
   uvicorn main:app --reload
   ```

## Contributing

Contributions to enhance compatibility with other institution documents or to improve the backend's functionality are welcome!
