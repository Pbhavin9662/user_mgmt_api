from app.db.session import SessionLocal
from app.services.user_service import get_by_email, create_user

def main():
    db = SessionLocal()
    try:
        email = "admin@example.com"
        existing = get_by_email(db, email)
        if existing:
            print("Admin already exists:", existing.email)
            return
        user = create_user(db, name="Admin", email=email, password="Admin@123", role="admin")
        print("Created admin:", user.email, user.id)
    finally:
        db.close()

if __name__ == "__main__":
    main()
