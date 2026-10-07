"""Bake the self-hosted server address and public key into the client at build time.

Reads RENDEZVOUS_SERVER and RS_PUB_KEY from the environment (GitHub Secrets),
so they never appear in the public source tree.
"""
import os
import sys

CONFIG = "libs/hbb_common/src/config.rs"
OLD_SERVERS = 'pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];'
OLD_KEY = 'pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";'

server = os.environ.get("RENDEZVOUS_SERVER", "").strip()
key = os.environ.get("RS_PUB_KEY", "").strip()
if not server or not key:
    sys.exit("RENDEZVOUS_SERVER and RS_PUB_KEY must be set")

with open(CONFIG, encoding="utf-8") as f:
    src = f.read()

for old in (OLD_SERVERS, OLD_KEY):
    if src.count(old) != 1:
        sys.exit(f"expected exactly one match in {CONFIG}: {old.split('=')[0].strip()}")

src = src.replace(OLD_SERVERS, f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{server}"];')
src = src.replace(OLD_KEY, f'pub const RS_PUB_KEY: &str = "{key}";')

with open(CONFIG, "w", encoding="utf-8", newline="\n") as f:
    f.write(src)
print("Server config injected")
