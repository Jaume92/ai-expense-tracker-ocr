import re


def parse_receipt(text: str):

    result = {
        "total": None,
        "date": None,
        "merchant": None
    }

    if not text or len(text) < 10:
        return result

    clean_text = text.replace(",", ".")
    lines = [l.strip() for l in clean_text.split("\n") if l.strip()]

    # ---------- FECHA ----------
    date_pattern = r'(\d{2}[./-]\d{2}[./-]\d{4})'
    dates = re.findall(date_pattern, clean_text)

    if dates:
        result["date"] = dates[0]

    # ---------- TOTAL ----------
    numbers = re.findall(r'\b\d{1,3}\.\d{2}\b', clean_text)

    filtered = []
    for n in numbers:
        if not any(n in d for d in dates):
            filtered.append(n)

    if filtered:
        result["total"] = max(filtered, key=lambda x: float(x))

    # ---------- MERCHANT ----------
    merchant_candidate = None

    # Header priority
    for line in lines[:8]:

        blacklist = ["fecha", "mesa", "atendido", "salon", "total", "iva"]

        if any(b in line.lower() for b in blacklist):
            continue

        digit_ratio = sum(c.isdigit() for c in line) / max(len(line), 1)

        if len(line) > 6 and digit_ratio < 0.2:
            merchant_candidate = line
            break

    # Fallback
    if merchant_candidate is None:
        for line in lines:
            digit_ratio = sum(c.isdigit() for c in line) / max(len(line), 1)

            if len(line) > 10 and digit_ratio < 0.15:
                merchant_candidate = line
                break

    result["merchant"] = merchant_candidate
        # ---------- LIMPIEZA FINAL ----------
    if result["merchant"]:
        result["merchant"] = result["merchant"].replace("'", "")
        result["merchant"] = result["merchant"].replace("“", "")
        result["merchant"] = result["merchant"].replace("”", "")
        result["merchant"] = result["merchant"].strip()

    # 🔥 DEVOLVER SIEMPRE
    return result
