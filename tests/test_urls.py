import re
import socket
import ipaddress
from urllib.parse import urlparse

import validators


class URLValidationError(Exception):
    pass


def validate_url(long_url: str, blacklist_domains: list[str]) -> bool:
    """
    Validates a long URL against security constraints.
    Raises URLValidationError if invalid.
    """

    # 1️⃣ Basic format validation
    if not validators.url(long_url):
        raise URLValidationError("Invalid URL format.")

    parsed = urlparse(long_url)

    # 2️⃣ Enforce HTTPS
    if parsed.scheme != "https":
        raise URLValidationError("Only HTTPS URLs are allowed.")

    hostname = parsed.hostname

    if not hostname:
        raise URLValidationError("Invalid hostname.")

    # 3️⃣ Block localhost explicitly
    if hostname.lower() in ["localhost", "127.0.0.1"]:
        raise URLValidationError("Localhost URLs are not allowed.")

    # 4️⃣ Check if hostname is an IP
    try:
        ip_obj = ipaddress.ip_address(hostname)

        # Block private, loopback, reserved IPs
        if (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_reserved
            or ip_obj.is_link_local
        ):
            raise URLValidationError("Private or restricted IP addresses are not allowed.")

    except ValueError:
        # Not an IP, try resolving domain
        try:
            resolved_ip = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(resolved_ip)

            if (
                ip_obj.is_private
                or ip_obj.is_loopback
                or ip_obj.is_reserved
                or ip_obj.is_link_local
            ):
                raise URLValidationError("Domain resolves to restricted IP address.")

        except socket.gaierror:
            raise URLValidationError("Domain cannot be resolved.")

    # 5️⃣ Check malware blacklist (DB domains)
    domain = hostname.lower()

    if domain in blacklist_domains:
        raise URLValidationError("Domain is blacklisted (malware).")

    # 6️⃣ Optional: Length constraint
    if len(long_url) > 2048:
        raise URLValidationError("URL exceeds maximum allowed length.")

    return True
