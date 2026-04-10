#!/usr/bin/env python3
"""
Recupero codici sconto Zooplus da shopilo.it
Sursa: https://shopilo.it/negozi/zooplus.it
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

SHOPILO_URL = "https://shopilo.it/negozi/zooplus.it"
STORE_NAME = "Zooplus"


def fetch_coupons(url=SHOPILO_URL):
    """Restituisce la lista dei coupon attivi per Zooplus da shopilo.it"""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; coupon-fetcher/1.0; +https://github.com/shopilo-it/codice-sconto-zooplus)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Errore nel recupero: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    coupons = []

    for item in soup.select(".coupon-item, [data-coupon], .offer-card"):
        code_el     = item.select_one("[data-code], .coupon-code, .code")
        discount_el = item.select_one(".discount, .percent, .amount")
        desc_el     = item.select_one(".title, .description, h3")
        expires_el  = item.select_one(".expires, .expiry, [data-expires]")

        coupon = {
            "store":      STORE_NAME,
            "code":       code_el.get_text(strip=True)     if code_el     else None,
            "discount":   discount_el.get_text(strip=True) if discount_el else None,
            "description":desc_el.get_text(strip=True)     if desc_el     else None,
            "expires":    expires_el.get_text(strip=True)  if expires_el  else None,
            "source":     SHOPILO_URL,
            "fetched_at": datetime.now().isoformat()
        }

        if coupon["description"]:
            coupons.append(coupon)

    return coupons


if __name__ == "__main__":
    print(f"Recupero codici sconto {{STORE_NAME}} da shopilo.it...\n")
    coupons = fetch_coupons()

    if coupons:
        print(json.dumps(coupons, ensure_ascii=False, indent=2))
        print(f"\nTotale: {{len(coupons)}} coupon trovati")
    else:
        print(f"Nessun coupon trovato. Lista completa su: {SHOPILO_URL}")
