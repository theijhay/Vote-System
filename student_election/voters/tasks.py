from celery import shared_task
import pandas as pd
from io import StringIO
from django.core.mail import send_mail
from django.conf import settings
from .models import StudentVoter

@shared_task
def process_file_task(file_content):
    try:
        missing_fields = set()
        saved_records = 0  # Track the number of successfully saved records

        """Read the CSV file in chunks for memory efficiency"""
        for chunk in pd.read_csv(StringIO(file_content), chunksize=100):
            available_fields = list(chunk.columns)

            for _, row in chunk.iterrows():
                """Map the row data to fields"""
                student_data = {
                    'student_id': row.get('student_id', None),
                    'first_name': row.get('first_name', ''),
                    'last_name': row.get('last_name', ''),
                    'email': row.get('email', None),
                    'department': row.get('department', ''),
                    'year': row.get('year', 1),  # Default year to 1 if missing
                    'is_eligible': row.get('is_eligible', False),
                }

                """Check for missing critical fields like 'student_id' and 'email'"""
                if not student_data['student_id']:
                    missing_fields.add('student_id')
                if not student_data['email']:
                    missing_fields.add('email')

                """Save the student data if both student_id and email are present"""
                if student_data['student_id'] and student_data['email']:
                    StudentVoter.objects.create(**student_data)
                    saved_records += 1  # Increment count for successfully saved records

        """Prepare the email content"""
        email_subject = "File Processing Completed"
        email_message = f"The file has been processed successfully.\n\n{saved_records} records were saved."
        if missing_fields:
            email_message += f"\n\nHowever, the following fields were missing in some rows: {', '.join(missing_fields)}"

        """Try sending the email"""
        try:
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as email_error:
            """Handle email sending failure"""
            print(f"Failed to send email: {email_error}")
            return f"File processing completed successfully. However, email failed to send due to: {email_error}"

        """Return success message to the frontend with the number of saved records"""
        return f"File processing completed successfully. {saved_records} records were saved."
    
    except Exception as e:
        """Handle unexpected errors during file processing"""
        try:
            send_mail(
                'File Processing Failed',
                f"Unexpected error during file processing: {e}",
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as email_error:
            print(f"Failed to send error email: {email_error}")
        print(f"Unexpected error during file processing: {e}")
        return f"File processing failed due to: {e}"
