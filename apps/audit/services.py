import requests
import pybreaker
from django.utils.timezone import now
from apps.audit.models import LoginAudit

# Circuit breaker: 3 failures, reset after 60 sec
breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=60)

@breaker
def get_country_from_ip(ip: str) -> str:
    """
    Call external service to map IP → country.
    If service fails, circuit breaker will open.
    """
    try:
        resp = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("country_name", "Unknown")
    except requests.RequestException:
        pass
    return "Unknown"

def log_login(user, request):
    """
    Store login attempt with IP, UserAgent, and country.
    """
    ip = get_client_ip(request)
    ua = request.META.get("HTTP_USER_AGENT", "")
    country = "Unknown"
    try:
        country = get_country_from_ip(ip)
    except pybreaker.CircuitBreakerError:
        # Circuit breaker open → skip external call
        country = "Unknown"

    LoginAudit.objects.create(
        user=user,
        ip_address=ip,
        user_agent=ua,
        country=country,
        timestamp=now()
    )

def get_client_ip(request):
    """
    Extract client IP from request headers.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
