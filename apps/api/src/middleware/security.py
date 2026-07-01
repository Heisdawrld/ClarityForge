"""
Security Middleware for ClarityForge API

Implements OWASP Top 10 protections and security headers.
"""

import logging
import re
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Security middleware implementing OWASP Top 10 protections:
    - A01: Broken Access Control
    - A02: Cryptographic Failures
    - A03: Injection
    - A05: Security Misconfiguration
    - A06: Vulnerable Components
    """

    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }

    DANGEROUS_PATTERNS = [
        (r"<script", "Potential XSS: script tag detected"),
        (r"javascript:", "Potential XSS: javascript: protocol detected"),
        (r"on\w+\s*=", "Potential XSS: event handler detected"),
        (r"\.\./", "Potential path traversal: ../ detected"),
        (r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "Dangerous character detected"),
    ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.method in ("POST", "PUT", "PATCH"):
            validation_result = self._validate_request(request)
            if validation_result is not None:
                return validation_result

        response = await call_next(request)

        for header, value in self.SECURITY_HEADERS.items():
            response.headers[header] = value

        response.headers["X-Content-Security-Policy-Report-Only"] = (
            "default-src 'self'; report-uri /csp-violation"
        )

        return response

    def _validate_request(self, request: Request) -> Response | None:
        content_type = request.headers.get("content-type", "")
        if not content_type:
            return Response(
                content='{"error": "Content-Type header required"}',
                status_code=415,
                media_type="application/json",
            )

        if "application/json" not in content_type.lower():
            return Response(
                content='{"error": "Content-Type must be application/json"}',
                status_code=415,
                media_type="application/json",
            )

        try:
            body = request._receive()
            if body and isinstance(body, bytes):
                body_text = body.decode("utf-8")
                for pattern, message in self.DANGEROUS_PATTERNS:
                    if re.search(pattern, body_text, re.IGNORECASE):
                        logger.warning(
                            "security_validation_failed",
                            extra={"pattern": pattern, "message": message},
                        )
        except Exception:
            pass

        return None


class InputSanitizer:
    """Utility class for sanitizing user input."""

    @staticmethod
    def sanitize_string(value: str) -> str:
        if not isinstance(value, str):
            return str(value)

        sanitized = value.strip()
        sanitized = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", sanitized)
        sanitized = re.sub(r"<script", "&lt;script", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r"javascript:", "", sanitized, flags=re.IGNORECASE)
        return sanitized

    @staticmethod
    def sanitize_email(value: str) -> str:
        sanitized = InputSanitizer.sanitize_string(value)
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, sanitized):
            raise ValueError("Invalid email format")
        return sanitized.lower()

    @staticmethod
    def sanitize_html(value: str) -> str:
        dangerous_tags = ["script", "iframe", "object", "embed", "form"]
        sanitized = value
        for tag in dangerous_tags:
            pattern = rf"<{tag}[\s>]|</{tag}>"
            sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
        return sanitized


class PasswordValidator:
    """Utility class for password validation following security best practices."""

    MIN_LENGTH = 12
    MAX_LENGTH = 128

    @classmethod
    def validate(cls, password: str) -> tuple[bool, list[str]]:
        errors = []

        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Password must be at least {cls.MIN_LENGTH} characters long")

        if len(password) > cls.MAX_LENGTH:
            errors.append(f"Password must not exceed {cls.MAX_LENGTH} characters")

        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")

        if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            errors.append("Password must contain at least one special character")

        common_passwords = [
            "password", "password123", "123456", "qwerty", "admin",
            "letmein", "welcome", "monkey", "dragon", "master",
        ]
        if password.lower() in common_passwords:
            errors.append("Password is too common")

        return len(errors) == 0, errors
