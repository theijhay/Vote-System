## Project Documentation

The Student Voter System is a backend system built with Django and Django Rest Framework (DRF) to process CSV/Excel files containing student voter data. The system asynchronously processes large files using Celery and RabbitMQ to ensure performance and scalability. After processing, the system saves the data to a database and notifies the admin via email upon successful completion.

#### Setup and Installation

- Python 3.x
- RabbitMQ (for Celery)
- RabbitMQ for message brokering in production

**Steps:**
- Clone the repository:
```json
git clone https://github.com/your-username/student-voter-system.git
```
```
cd student-voter-system
```

- Set up a virtual environment:
```
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

- Install dependencies:
```
pip install -r requirements.txt
```

- Install and configure RabbitMQ:

Install RabbitMQ by following the instructions for your OS: [RabbitMQ Installation Guide](https://www.rabbitmq.com/docs/download)

Ensure RabbitMQ is running:
```
sudo service rabbitmq-server start
```

- Apply database migrations:
```
python manage.py migrate
```

- Create a superuser for admin access:
```
python manage.py createsuperuser
```
### Environment Variables
Create a .env file in the root directory to configure the environment variables:
```json
# Django settings
SECRET_KEY="your-secret-key"
DEBUG=True  # Change to False in production
ALLOWED_HOSTS="*"


# Email settings (for Gmail)
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-email-password"
DEFAULT_FROM_EMAIL="your-email@gmail.com"
ADMIN_EMAIL="admin@example.com"


# Celery settings
CELERY_BROKER_URL="amqp://localhost"
Make sure to update the credentials according to your setup (e.g., email credentials, database URL).
```

### Running the Application
To run the backend application, follow these steps:

- Run the Django development server:
```
python manage.py runserver
```

- Start the Celery worker:
```
celery -A student_election worker --loglevel=info
```

### API Endpoints

- **File Upload Endpoint:**
- **URL:** `/api/upload/`
- **Method:** `POST`
- **Description:** Upload a CSV or Excel file for asynchronous processing.
- **Request Body:**
file (multipart/form-data): The file to be processed.
- **Response:**

- **Status:** `202 Accepted`
- **Body:**
```json
{
  "message": "File uploaded and processing started",
  "task_id": "string"
}
```
- Task Status Endpoint:

- **URL:** `/api/task-status/<task_id>/`
- **Method:** GET
- **Description:** Get the status of the processing task.
- **Response:**
- **Status:** `200 OK`

- **Body:**

```json
{
  "state": "SUCCESS",
  "status": "Task is processing",
  "result": "File processing completed successfully"
}
```

### Asynchronous Processing with Celery

The file processing is handled asynchronously using Celery and RabbitMQ. The system reads large files in chunks to prevent memory overload and processes each row, saving the data into the database.


### Database Design

The StudentVoter model represents the structure for student voter information. The model contains the following fields:
```json
student_id: Unique ID for each student.
first_name: Student's first name.
last_name: Student's last name.
email: Student's email address.
department: Department the student belongs to.
year: Year of study.
is_eligible: Boolean indicating whether the student is eligible to vote.
```

### Handling File Uploads

- The system accepts CSV or Excel files for processing. 
- Uploaded files are validated for format, and each row is processed asynchronously. 
- The processed data is stored in the StudentVoter model.
- File validation ensures that only CSV or Excel files are accepted.
- Chunked processing is used to handle large files efficiently.

### Email Notification System

- Once the file processing is complete, the system sends an email to the admin notifying them of the success or failure of the operation.

The email contains details about:
- Number of records processed and saved.
- Any missing fields in the file.


### Testing

You can run tests using Django’s built-in test framework:
```
python manage.py test voters
```

Ensure that the file upload, data saving, and email notifications work as expected.

### Deployment Instructions

For deployment, you can use Railway, Render, or any other PaaS provider. Make sure to:

- Set environment variables correctly for production (`DEBUG=False`, `ALLOWED_HOSTS`, etc.).
- Configure the database and email settings for your production environment.
- Ensure your deployment supports asynchronous processing with Celery and RabbitMQ.

### Thought Process and Problem-Solving Approach

- Scalability: The use of Celery and chunked file processing ensures that the system can handle large files without performance issues.
- Asynchronous Processing: The system leverages Celery to process files asynchronously, ensuring that the application remains responsive even when dealing with large datasets.
- Email Notifications: After processing, the system notifies the admin of the results, providing transparency into the system’s operations.
- Data Integrity: Only rows with valid data (like `student_id` and `email`) are saved to the database, ensuring data integrity.

**Challenges:**
- Handling large file uploads without overwhelming the server.
- Ensuring that email notifications work reliably across different environments (development vs. production).

### Conclusion
This project provides a scalable and efficient system for processing student voter data, ensuring that the election process is seamless and data replication is handled effectively. The use of asynchronous tasks, combined with clear notifications and error handling, ensures that admins are always informed of the system’s status.