# NEXORA

**Operator deck** — a phosphor TUI multitool for public intel, network helpers, crypto, generators, and research links.

Educational / authorized use only. See [DISCLAIMER.md](DISCLAIMER.md).

```
  ███╗   ██╗███████╗██╗  ██╗ ██████╗ ██████╗  █████╗
  ████╗  ██║██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██╔══██╗
  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║██████╔╝███████║
  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║██╔══██╗██╔══██║
  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝██║  ██║██║  ██║
  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
```

## Windows (the Void-Tools-style path)

1. Install **Python 3.11+** (`python_installer.bat` opens python.org — tick **Add to PATH**).
2. Double-click `setup.bat` (confirms Python; no pip packages).
3. Double-click **`start.bat`**.

That launches `nexora.py` in your terminal: numbered modules, ANSI deck, public APIs only.

Linux / macOS:

```bash
python3 nexora.py
```

## Modules

| Deck | Tools |
| --- | --- |
| Intel | IP geolocation, DNS over HTTPS, RDAP, handle URL map, search-dork builder, email parse, MAC vendor |
| Net | HTTP probe (public URLs), session info, port atlas (reference, not a scanner), CIDR lab, weather, FX |
| Crypto | SHA hashes, HMAC-SHA256, JWT inspect (decode only), Base64, hex/bin |
| Gen | Password forge, UUID v4, lorem, color lab, QR link |
| Text | Case, wordstat, regex, URL codec, JSON, Morse, Caesar |
| Convert | Time, units, cron reader, HTTP status map |
| Links | Curated public research bookmarks |

Network helpers **refuse private / loopback targets**.

## License

MIT — [LICENSE](LICENSE)
