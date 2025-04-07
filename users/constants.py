# User roles
ROLE_USER = "user"
ROLE_ADMIN = "admin"
ROLE_SUPER_ADMIN = "super_admin"

USER_ROLES = [
    (ROLE_USER, "User"),
    (ROLE_ADMIN, "Admin"),
    (ROLE_SUPER_ADMIN, "Super Admin"),
]

ALLOWED_SIGNUP_ROLES = [
    (ROLE_USER, "User"),
    (ROLE_ADMIN, "Admin"),
]

# Verification status
VERIFICATION_STATUS_PENDING = "pending"
VERIFICATION_STATUS_VERIFIED = "verified"

VERIFICATION_STATUSES = [
    (VERIFICATION_STATUS_PENDING, "Pending"),
    (VERIFICATION_STATUS_VERIFIED, "Verified"),
]

# Email verification token expiration (in seconds)
EMAIL_VERIFICATION_TOKEN_EXPIRATION = 86400  # 24 hours
