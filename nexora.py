#!/usr/bin/env python3
"""NEXORA operator deck — stdlib only. Educational / authorized use."""
from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import os
import platform
import re
import secrets
import socket
import string
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone

GREEN = "\033[92m"
DIM = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"
CYAN = "\033[96m"

if os.name == "nt":
    os.system("")  # enable ANSI on Windows 10+

BANNER = r"""
  ███╗   ██╗███████╗██╗  ██╗ ██████╗ ██████╗  █████╗
  ████╗  ██║██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██╔══██╗
  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║██████╔╝███████║
  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║██╔══██╗██╔══██║
  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝██║  ██║██║  ██║
  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
"""

PRIVATE = re.compile(
    r"^(localhost|127\.|10\.|0\.|192\.168\.|169\.254\.|172\.(1[6-9]|2\d|3[0-1])\.|::1)$",
    re.I,
)


def c(text: str, color: str = GREEN) -> str:
    return f"{color}{text}{RESET}"


def pause() -> None:
    input(c("\n  [enter] return to deck", DIM))


def ask(label: str, default: str = "") -> str:
    extra = f" [{default}]" if default else ""
    val = input(c(f"  {label}{extra}: ", CYAN)).strip()
    return val or default


def get_json(url: str, headers: dict | None = None) -> object:
    req = urllib.request.Request(url, headers={"Accept": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=12) as res:
        raw = res.read().decode("utf-8", "replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw[:8000]}


def assert_public(target: str) -> str:
    host = target
    if "://" in target:
        host = urllib.parse.urlparse(target).hostname or target
    host = host.split("/")[0]
    if PRIVATE.match(host) or host in {"0.0.0.0"}:
        raise ValueError("Private / loopback targets are blocked.")
    return target


def dump(data: object) -> None:
    print(c(json.dumps(data, indent=2, default=str)))


def tool_ip() -> None:
    ip = ask("IP (blank = this host via ipwho.is)")
    if ip:
        assert_public(ip)
    path = urllib.parse.quote(ip) if ip else ""
    dump(get_json(f"https://ipwho.is/{path}"))


def tool_dns() -> None:
    name = assert_public(ask("Host", "example.com").replace("https://", "").replace("http://", "").split("/")[0])
    rtype = ask("Type", "A").upper()
    url = f"https://cloudflare-dns.com/dns-query?name={urllib.parse.quote(name)}&type={urllib.parse.quote(rtype)}"
    dump(get_json(url, {"Accept": "application/dns-json"}))


def tool_rdap() -> None:
    domain = assert_public(ask("Domain", "example.com").split("/")[0])
    dump(get_json(f"https://rdap.org/domain/{urllib.parse.quote(domain)}"))


def tool_http() -> None:
    raw = ask("URL", "https://example.com")
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    assert_public(raw)
    t0 = time.time()
    req = urllib.request.Request(raw, method="GET")
    with urllib.request.urlopen(req, timeout=12) as res:
        body = res.read()
        headers = dict(res.headers.items())
        dump(
            {
                "status": res.status,
                "final": res.geturl(),
                "ms": int((time.time() - t0) * 1000),
                "bytes": len(body),
                "headers": headers,
            }
        )


def tool_mac() -> None:
    mac = ask("MAC", "00:1A:2B:3C:4D:5E")
    req = urllib.request.Request(f"https://api.macvendors.com/{urllib.parse.quote(mac)}")
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            print(c(res.read().decode()))
    except urllib.error.HTTPError as e:
        print(c(e.read().decode() if e.fp else str(e)))


def tool_weather() -> None:
    city = ask("City", "Berlin")
    geo = get_json(f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1")
    results = geo.get("results") if isinstance(geo, dict) else None
    if not results:
        print("No match.")
        return
    g = results[0]
    wx = get_json(
        f"https://api.open-meteo.com/v1/forecast?latitude={g['latitude']}&longitude={g['longitude']}&current=temperature_2m,wind_speed_10m"
    )
    dump({"place": g, "weather": wx})


def tool_hash() -> None:
    text = ask("Input").encode()
    dump(
        {
            "md5": hashlib.md5(text).hexdigest(),
            "sha1": hashlib.sha1(text).hexdigest(),
            "sha256": hashlib.sha256(text).hexdigest(),
            "sha512": hashlib.sha512(text).hexdigest(),
        }
    )


def tool_hmac() -> None:
    msg = ask("Message").encode()
    key = ask("Key").encode()
    print(c(hmac.new(key, msg, hashlib.sha256).hexdigest()))


def tool_pass() -> None:
    n = int(ask("Length", "20") or "20")
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    print(c("".join(secrets.choice(alphabet) for _ in range(max(4, min(n, 128))))))


def tool_uuid() -> None:
    n = int(ask("Count", "5") or "5")
    for _ in range(max(1, min(n, 50))):
        print(c(str(uuid.uuid4())))


def tool_b64() -> None:
    import base64

    mode = ask("Mode encode|decode", "encode")
    text = ask("Text")
    if mode.startswith("d"):
        print(c(base64.b64decode(text.encode()).decode("utf-8", "replace")))
    else:
        print(c(base64.b64encode(text.encode()).decode()))


def tool_jwt() -> None:
    import base64

    token = ask("JWT")
    parts = token.split(".")
    if len(parts) < 2:
        print("Not a JWT.")
        return

    def dec(p: str) -> object:
        pad = p + "=" * (-len(p) % 4)
        raw = base64.urlsafe_b64decode(pad.encode())
        return json.loads(raw.decode())

    dump({"header": dec(parts[0]), "payload": dec(parts[1]), "segments": len(parts)})


def tool_cidr() -> None:
    raw = ask("CIDR", "192.168.1.0/24")
    net = ipaddress.ip_network(raw, strict=False)
    dump(
        {
            "network": str(net.network_address),
            "broadcast": str(net.broadcast_address),
            "netmask": str(net.netmask),
            "hosts": net.num_addresses,
        }
    )


def tool_ports() -> None:
    q = ask("Filter (optional)").lower()
    ports = [
        (22, "SSH"),
        (53, "DNS"),
        (80, "HTTP"),
        (443, "HTTPS"),
        (25, "SMTP"),
        (587, "Submission"),
        (993, "IMAPS"),
        (3306, "MySQL"),
        (5432, "PostgreSQL"),
        (6379, "Redis"),
        (3389, "RDP"),
        (27017, "MongoDB"),
    ]
    for p, name in ports:
        if not q or q in str(p) or q in name.lower():
            print(f"  {p:>5}  {name}")


def tool_handles() -> None:
    h = urllib.parse.quote(ask("Username").lstrip("@"))
    for u in [
        f"https://github.com/{h}",
        f"https://gitlab.com/{h}",
        f"https://x.com/{h}",
        f"https://reddit.com/user/{h}",
        f"https://keybase.io/{h}",
    ]:
        print(" ", u)


def tool_links() -> None:
    for name, url in [
        ("OSINT Framework", "https://osintframework.com/"),
        ("Have I Been Pwned", "https://haveibeenpwned.com/"),
        ("crt.sh", "https://crt.sh/"),
        ("urlscan.io", "https://urlscan.io/"),
        ("VirusTotal", "https://www.virustotal.com/"),
        ("Wayback Machine", "https://web.archive.org/"),
        ("Cloudflare Radar", "https://radar.cloudflare.com/"),
    ]:
        print(f"  {name:22} {url}")


def tool_time() -> None:
    dump(
        {
            "iso": datetime.now(timezone.utc).isoformat(),
            "unix": int(time.time()),
            "host": platform.platform(),
            "python": sys.version.split()[0],
            "hostname": socket.gethostname(),
        }
    )


def tool_dorks() -> None:
    t = ask("Site or term", "example.com")
    print(f"  site:{t}")
    print(f"  site:{t} filetype:pdf")
    print(f"  https://www.google.com/search?q={urllib.parse.quote('site:' + t)}")
    print(f"  https://web.archive.org/web/*/{t}")
    print(f"  https://crt.sh/?q={urllib.parse.quote(t)}")


MENU = [
    ("01", "IP INTEL", tool_ip),
    ("02", "DNS QUERY", tool_dns),
    ("03", "DOMAIN RDAP", tool_rdap),
    ("04", "HTTP PROBE", tool_http),
    ("05", "MAC VENDOR", tool_mac),
    ("06", "WX BRIEF", tool_weather),
    ("07", "HASH BENCH", tool_hash),
    ("08", "HMAC-SHA256", tool_hmac),
    ("09", "PASSFORGE", tool_pass),
    ("10", "UUID v4", tool_uuid),
    ("11", "BASE64", tool_b64),
    ("12", "JWT INSPECT", tool_jwt),
    ("13", "CIDR LAB", tool_cidr),
    ("14", "PORT ATLAS", tool_ports),
    ("15", "HANDLE MAP", tool_handles),
    ("16", "SEARCH DORKS", tool_dorks),
    ("17", "LINK HUB", tool_links),
    ("18", "TIMECORE", tool_time),
]


def screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    print(c(BANNER))
    print(c("  NEXORA  //  operator deck  //  lawful use only", BOLD + GREEN))
    print(c("  stdlib Python · public APIs · private ranges blocked\n", DIM))
    for i, (code, name, _) in enumerate(MENU):
        end = "\n" if i % 2 else "    "
        print(c(f"  [{code}] {name:<14}", GREEN), end=end)
    if len(MENU) % 2:
        print()
    print(c("\n  [Q]  quit\n", DIM))


def main() -> None:
    while True:
        screen()
        choice = input(c("  select > ", CYAN)).strip().lower()
        if choice in {"q", "quit", "exit"}:
            print(c("  deck closed."))
            return
        match = next((m for m in MENU if m[0] == choice.zfill(2) or m[0] == choice), None)
        if not match:
            print("  unknown module")
            time.sleep(0.7)
            continue
        print(c(f"\n  :: {match[1]}\n", BOLD + GREEN))
        try:
            match[2]()
        except Exception as exc:  # noqa: BLE001 — CLI boundary
            print(c(f"  error: {exc}"))
        pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(c("\n  interrupted."))
