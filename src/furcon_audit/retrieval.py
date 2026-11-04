"""Safe, provenance-preserving retrieval of public web pages.

Search results are candidates only. Retrieval records never constitute legal conclusions.
"""
from __future__ import annotations

import hashlib
import http.client
import ipaddress
import re
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Callable
from urllib.robotparser import RobotFileParser


USER_AGENT = "FurConComplianceAudit/2.0 (+read-only research)"
DEFAULT_MAX_BYTES = 2_000_000
MAX_RETRIEVAL_BYTES = 10_000_000
MAX_RETRIEVAL_TIMEOUT_SECONDS = 60


class RetrievalError(RuntimeError):
    def __init__(self, code: str, message: str, *, outcome: str = "failed") -> None:
        super().__init__(message)
        self.code = code
        self.outcome = outcome


@dataclass(frozen=True)
class FetchResponse:
    status: int
    headers: dict[str, str]
    body: bytes
    final_url: str


class _TextExtractor(HTMLParser):
    BLOCK_TAGS = {"p", "div", "section", "article", "main", "li", "h1", "h2",
                  "h3", "h4", "h5", "h6", "br", "tr"}
    IGNORED_TAGS = {"script", "style", "noscript", "iframe", "svg", "template"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.language: str | None = None
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.IGNORED_TAGS:
            self._ignored_depth += 1
            return
        if self._ignored_depth:
            return
        values = dict(attrs)
        if tag == "html":
            self.language = values.get("lang")
        if tag == "title":
            self.in_title = True
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.IGNORED_TAGS and self._ignored_depth:
            self._ignored_depth -= 1
            return
        if self._ignored_depth:
            return
        if tag == "title":
            self.in_title = False
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        if self.in_title:
            self.title_parts.append(data)
        if data.strip():
            self.parts.append(data)

    def result(self) -> tuple[str, str | None, str | None]:
        text = re.sub(r"[ \t\r\f\v]+", " ", "".join(self.parts))
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        title = " ".join("".join(self.title_parts).split()) or None
        return text, title, self.language


def _validate_public_url(url: str, resolver: Callable = socket.getaddrinfo) -> str:
    if not isinstance(url, str) or not url or any(ord(char) < 32 or ord(char) == 127 for char in url):
        raise RetrievalError("invalid_url", "URL must be a non-empty string without control characters.",
                             outcome="blocked")
    try:
        parsed = urllib.parse.urlsplit(url)
        explicit_port = parsed.port
    except ValueError as exc:
        raise RetrievalError("invalid_url", "URL contains an invalid host or port.",
                             outcome="blocked") from exc
    if parsed.scheme not in {"http", "https"}:
        raise RetrievalError("unsupported_scheme", "Only HTTP and HTTPS URLs are allowed.",
                             outcome="blocked")
    if not parsed.hostname or parsed.username or parsed.password:
        raise RetrievalError("invalid_url", "URL must have a host and no embedded credentials.",
                             outcome="blocked")
    expected_port = 443 if parsed.scheme == "https" else 80
    if explicit_port not in {None, expected_port}:
        raise RetrievalError("nonstandard_port", "Only the scheme's standard port is allowed.",
                             outcome="blocked")
    host = parsed.hostname.rstrip(".").lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".localhost"):
        raise RetrievalError("private_host", "Local hostnames are blocked.", outcome="blocked")
    try:
        literal = ipaddress.ip_address(host)
        addresses = [literal]
    except ValueError:
        try:
            records = resolver(host, parsed.port or (443 if parsed.scheme == "https" else 80),
                               type=socket.SOCK_STREAM)
            addresses = [ipaddress.ip_address(row[4][0].split("%", 1)[0]) for row in records]
        except (OSError, ValueError, IndexError) as exc:
            raise RetrievalError("dns_failure", "Hostname could not be resolved.") from exc
    if not addresses or any(not address.is_global for address in addresses):
        raise RetrievalError("private_network_target", "Private or non-public network targets are blocked.",
                             outcome="blocked")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path or "/",
                                   parsed.query, ""))


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _validate_public_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _validate_redirect_url(current_url: str, location: str,
                           resolver: Callable = socket.getaddrinfo) -> str:
    """Validate a redirect target and forbid HTTPS downgrade before connecting."""
    target = urllib.parse.urljoin(current_url, location)
    validated = _validate_public_url(target, resolver=resolver)
    if (urllib.parse.urlsplit(current_url).scheme == "https"
            and urllib.parse.urlsplit(validated).scheme != "https"):
        raise RetrievalError("https_downgrade", "HTTPS redirects cannot downgrade to HTTP.",
                             outcome="blocked")
    return validated


def _resolve_public_addresses(host: str, port: int) -> list[str]:
    try:
        literal = ipaddress.ip_address(host)
        addresses = [str(literal)]
    except ValueError:
        try:
            records = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
            addresses = list(dict.fromkeys(row[4][0].split("%", 1)[0] for row in records))
        except (OSError, ValueError, IndexError) as exc:
            raise RetrievalError("dns_failure", "Hostname could not be resolved.") from exc
    parsed = [ipaddress.ip_address(value) for value in addresses]
    if not parsed or any(not address.is_global for address in parsed):
        raise RetrievalError("private_network_target",
                             "Private or non-public network targets are blocked.",
                             outcome="blocked")
    return addresses


class _PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, host: str, port: int, ip: str, timeout: int):
        super().__init__(host, port, timeout=timeout)
        self._pinned_ip = ip

    def connect(self):
        self.sock = socket.create_connection((self._pinned_ip, self.port), self.timeout)


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host: str, port: int, ip: str, timeout: int):
        super().__init__(host, port, timeout=timeout, context=ssl.create_default_context())
        self._pinned_ip = ip

    def connect(self):
        raw = socket.create_connection((self._pinned_ip, self.port), self.timeout)
        self.sock = self._context.wrap_socket(raw, server_hostname=self.host)


def _stdlib_fetch(url: str, timeout: int, max_bytes: int) -> FetchResponse:
    current = _validate_public_url(url)
    for redirect_count in range(6):
        parsed = urllib.parse.urlsplit(current)
        host = parsed.hostname or ""
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        addresses = _resolve_public_addresses(host, port)
        path = urllib.parse.urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
        response = None
        last_error = None
        for address in addresses:
            connection = (_PinnedHTTPSConnection(host, port, address, timeout)
                          if parsed.scheme == "https"
                          else _PinnedHTTPConnection(host, port, address, timeout))
            try:
                connection.request("GET", path, headers={
                    "Host": parsed.netloc, "User-Agent": USER_AGENT,
                    "Accept": "text/html,text/plain,application/xhtml+xml;q=0.9,*/*;q=0.1"
                })
                response = connection.getresponse()
                headers = dict(response.getheaders())
                location = response.getheader("Location")
                if response.status in {301, 302, 303, 307, 308} and location:
                    response.read(max_bytes + 1)
                    connection.close()
                    if redirect_count >= 5:
                        raise RetrievalError("too_many_redirects", "Redirect limit exceeded.",
                                             outcome="blocked")
                    current = _validate_redirect_url(current, location)
                    break
                body = response.read(max_bytes + 1)
                if len(body) > max_bytes:
                    raise RetrievalError("payload_too_large",
                                         "Response exceeded the configured size limit.",
                                         outcome="blocked")
                final_url = current
                response.close()
                connection.close()
                return FetchResponse(response.status, headers, body, final_url)
            except RetrievalError:
                connection.close()
                raise
            except (OSError, http.client.HTTPException) as exc:
                last_error = exc
                connection.close()
        else:
            raise RetrievalError("network_error", "The source could not be retrieved.") from last_error
        if response is None:
            continue
    raise RetrievalError("too_many_redirects", "Redirect limit exceeded.", outcome="blocked")

def _robots_allowed(url: str, user_agent: str, fetch: Callable) -> bool:
    parsed = urllib.parse.urlsplit(url)
    robots_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "/robots.txt", "", ""))
    try:
        response = fetch(robots_url)
    except RetrievalError:
        raise RetrievalError("robots_unavailable", "Could not verify robots.txt policy.",
                             outcome="blocked")
    if (not isinstance(response, FetchResponse) or not isinstance(response.status, int)
            or isinstance(response.status, bool) or not isinstance(response.body, bytes)):
        raise RetrievalError("robots_unavailable", "Robots response was malformed.",
                             outcome="blocked")
    if len(response.body) > DEFAULT_MAX_BYTES:
        raise RetrievalError("robots_too_large", "robots.txt exceeded the configured size limit.",
                             outcome="blocked")
    if response.status == 404:
        return True
    if response.status in {401, 403}:
        return False
    if response.status < 200 or response.status >= 300:
        raise RetrievalError("robots_unavailable", "Could not verify robots.txt policy.",
                             outcome="blocked")
    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.parse(response.body.decode("utf-8", errors="replace").splitlines())
    return parser.can_fetch(user_agent, url)


def retrieve_page(
    url: str,
    *,
    attempt_id: str | None = None,
    timeout: int = 20,
    max_bytes: int = DEFAULT_MAX_BYTES,
    fetcher: Callable[[str, int, int], FetchResponse] = _stdlib_fetch,
    robots_checker: Callable[[str, str, Callable], bool] = _robots_allowed,
    resolver: Callable = socket.getaddrinfo,
) -> dict:
    """Retrieve one public page and return source/retrieval records plus preserved content.

    Raw decoded content and extracted text remain separate from Evidence. Callers must
    deliberately select excerpts and create Evidence records after source review.
    """
    if (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)
            or not 1 <= timeout <= MAX_RETRIEVAL_TIMEOUT_SECONDS):
        raise ValueError(f"timeout must be between 1 and {MAX_RETRIEVAL_TIMEOUT_SECONDS} seconds")
    if (not isinstance(max_bytes, int) or isinstance(max_bytes, bool)
            or not 1 <= max_bytes <= MAX_RETRIEVAL_BYTES):
        raise ValueError(f"max_bytes must be an integer between 1 and {MAX_RETRIEVAL_BYTES}")
    if attempt_id is not None and not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", attempt_id):
        raise ValueError("attempt_id must be a valid opaque ID")
    canonical_url = _validate_public_url(url, resolver=resolver)
    retrieval_id = "retrieval_" + uuid.uuid4().hex[:20]
    source_id = "source_" + hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()[:20]
    now = datetime.now(timezone.utc).isoformat()
    base = {
        "source": {
            "schema_version": "1.0.0", "source_id": source_id,
            "canonical_url": canonical_url, "title": None,
            "source_type": "unverified", "verification_status": "unverified"
        },
        "retrieval": {
            "schema_version": "1.0.0", "retrieval_id": retrieval_id,
            "source_id": source_id, "retrieved_at": now, "method": "http_fetch",
            "outcome": "failed", "content_hash": None, "error_code": None,
            "attempt_id": attempt_id
        },
        "content": None
    }
    try:
        def bounded_fetch(target: str) -> FetchResponse:
            return fetcher(target, timeout, max_bytes)
        if not robots_checker(canonical_url, USER_AGENT, bounded_fetch):
            raise RetrievalError("robots_disallowed", "robots.txt disallows this retrieval.",
                                 outcome="blocked")
        response = bounded_fetch(canonical_url)
        if (not isinstance(response, FetchResponse) or not isinstance(response.body, bytes)
                or not isinstance(response.status, int) or isinstance(response.status, bool)
                or not isinstance(response.headers, dict)
                or not isinstance(response.final_url, str)):
            raise RetrievalError("invalid_fetch_response", "Retriever returned an invalid response.")
        if len(response.body) > max_bytes:
            raise RetrievalError("payload_too_large",
                                 "Response exceeded the configured size limit.", outcome="blocked")
        if response.status in {401, 403, 407, 451}:
            raise RetrievalError("access_restricted", f"Source returned HTTP {response.status}.",
                                 outcome="blocked")
        if response.status < 200 or response.status >= 300:
            raise RetrievalError("http_error", f"Source returned HTTP {response.status}.")
        final_url = _validate_public_url(response.final_url, resolver=resolver)
        if urllib.parse.urlsplit(canonical_url).scheme == "https" and urllib.parse.urlsplit(final_url).scheme != "https":
            raise RetrievalError("https_downgrade", "HTTPS retrieval cannot redirect to HTTP.",
                                 outcome="blocked")
        content_type = response.headers.get("Content-Type", response.headers.get("content-type", ""))
        if not isinstance(content_type, str):
            raise RetrievalError("invalid_content_type", "Content-Type header must be text.")
        media_type = content_type.split(";", 1)[0].strip().lower()
        if media_type not in {"text/html", "application/xhtml+xml", "text/plain"}:
            raise RetrievalError("unsupported_media_type", f"Unsupported content type: {media_type or 'unknown'}.",
                                 outcome="blocked")
        raw = response.body
        charset_match = re.search(r"charset=([^; ]+)", content_type, re.I)
        charset = charset_match.group(1).strip('"\'') if charset_match else "utf-8"
        try:
            decoded = raw.decode(charset, errors="replace")
        except LookupError:
            decoded = raw.decode("utf-8", errors="replace")
            charset = "utf-8-fallback"
        if media_type in {"text/html", "application/xhtml+xml"}:
            extractor = _TextExtractor()
            extractor.feed(decoded)
            text, title, language = extractor.result()
        else:
            text, title, language = decoded.strip(), None, None
        final_source_id = "source_" + hashlib.sha256(final_url.encode("utf-8")).hexdigest()[:20]
        base["source"]["source_id"] = final_source_id
        base["retrieval"]["source_id"] = final_source_id
        base["source"]["canonical_url"] = final_url
        base["source"]["title"] = title
        base["retrieval"].update({
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "outcome": "success",
            "content_hash": hashlib.sha256(raw).hexdigest()
        })
        base["content"] = {
            "raw_text": decoded, "extracted_text": text, "content_type": media_type,
            "charset": charset, "language": language, "final_url": final_url,
            "byte_length": len(raw)
        }
        return base
    except RetrievalError as exc:
        base["retrieval"]["outcome"] = exc.outcome
        base["retrieval"]["error_code"] = exc.code
        base["retrieval"]["retrieved_at"] = datetime.now(timezone.utc).isoformat()
        base["error"] = {"code": exc.code, "message": str(exc)}
        return base
