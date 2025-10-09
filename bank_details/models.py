from __future__ import annotations

import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# Credit Card Checker

def luhn_check(number: str) -> bool:
    """Luhn mod-10 for card numbers."""
    digits = [int(d) for d in number]
    checksum = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

def clabe_checksum_ok(clabe: str) -> bool:
    """
    Verifica CLABE de 18 dígitos usando ponderaciones 3,7,1 sobre los primeros 17.
    Dígito verificador = (10 - (suma % 10)) % 10 debe coincidir con el 18°.
    """
    if not re.fullmatch(r"\d{18}", clabe):
        return False
    weights = [3, 7, 1]
    total = 0
    for i in range(17):
        total += (int(clabe[i]) * weights[i % 3]) % 10
    check = (10 - (total % 10)) % 10
    return check == int(clabe[17])


def detect_card_brand(number: str) -> str:
    """
    Detecta marca básica sin APIs:
      - VISA: empieza con 4 (16 dígitos en este MVP)
      - MasterCard: 51–55 o 2221–2720
      - Si no coincide: OTHER
    """
    if len(number) != 16:
        return "Other"
    if number.startswith("4"):
        return "Visa"
    two = int(number[:2])
    four = int(number[:4])
    if 51 <= two <= 55 or 2221 <= four <= 2720:
        return "MasterCard"
    return "Other"


# Mapeo mínimo (extiende cuando quieras)
BANK_CODE_MAP = {
    "002": "Citibanamex",
    "012": "BBVA",
    "014": "Santander",
    "021": "HSBC",
    "072": "Banorte",
    "638": "Nu Bank",
    "722": "Mercado Pago"
    # TODO: añade más códigos si lo deseas
}

class BankDetails(models.Model):
    class Kind(models.TextChoices):
        CLABE = "CLABE", "CLABE"
        CARD = "CARD", "Card"
        ACCOUNT = "ACCOUNT", "Account"
    
    class Brand(models.TextChoices):
        VISA = "Visa", "Visa"
        MASTERCARD = "MasterCard", "MasterCard"
        OTHER = "Other", "Other"

    class BankNameSource(models.TextChoices):
        AUTO = "AUTO", "Auto-detected"
        MANUAL = "MANUAL", "Manual"
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bank_details",
    )

    kind = models.CharField(max_length=16, choices=Kind.choices)
    # Maximum length of numbers (CLABE=18, CARD=16, ACCOUNT flexible)
    value = models.CharField(max_length=32)

    bank_code = models.CharField(max_length=3, blank=True)
    bank_name = models.CharField(max_length=80, blank=True)
    bank_name_source = models.CharField(
        max_length=8, choices=BankNameSource.choices, default=BankNameSource.AUTO
    )

    brand = models.CharField(  # solo para CARD
        max_length=16, choices=Brand.choices, blank=True
    )

    alias = models.CharField(max_length=80, blank=True)
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ✅ Only 1 per (owner, kind)
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "kind"], name="uniq_bankdetail_owner_kind"
            )
        ]
        indexes = [
            models.Index(fields=["owner", "kind"]),
        ]
        ordering = ("owner", "kind", "-updated_at")
    
    def __str__(self) -> str:
        return f"{self.owner} · {self.kind} · {self.masked_value}"
    
    # Normalize and validations

    def clean(self):
        # Normaliza: quita espacios y guiones del value
        if self.value:
            self.value = re.sub(r"[\s\-]+", "", self.value)

        val = self.value or ""

        if self.kind == self.Kind.CLABE:
            if not re.fullmatch(r"\d{18}", val):
                raise ValidationError({"value": "CLABE must be exactly 18 digits."})
            if not clabe_checksum_ok(val):
                raise ValidationError({"value": "CLABE checksum is invalid."})

            self.bank_code = val[:3]
            # Autocompleta bank_name si está vacío o si está en modo AUTO
            suggestion = BANK_CODE_MAP.get(self.bank_code, "")
            if self.bank_name and self.bank_name.strip():
                self.bank_name_source = self.BankNameSource.MANUAL
            else:
                self.bank_name = suggestion
                self.bank_name_source = self.BankNameSource.AUTO

            # Marca no aplica
            self.brand = ""

        elif self.kind == self.Kind.CARD:
            if not re.fullmatch(r"\d{16}", val):
                raise ValidationError({"value": "Card number must be exactly 16 digits."})
            if not luhn_check(val):
                raise ValidationError({"value": "Card number failed Luhn checksum."})
            self.brand = detect_card_brand(val)
            # bank_code no aplica a tarjetas; limpia por si acaso
            self.bank_code = ""

        elif self.kind == self.Kind.ACCOUNT:
            if not re.fullmatch(r"\d{6,20}", val):
                raise ValidationError({"value": "Account number must be 6–20 digits."})
            # No hay autocompletado; respeta bank_name manual si existe
            self.bank_code = ""
            self.brand = ""

        else:
            raise ValidationError({"kind": "Unsupported kind."})

    def save(self, *args, **kwargs):
        # Garantiza que clean() se ejecute al guardar (incluye normalización)
        self.full_clean()
        return super().save(*args, **kwargs)

    # ---- Utilidades de presentación -----------------------------------------
    @property
    def masked_value(self) -> str:
        """Representación enmascarada (para admin/UI interna)."""
        v = self.value or ""
        if not v:
            return ""
        if self.kind == self.Kind.CARD:
            return f"{'*' * 12}{v[-4:]}"  # **** **** **** 1234
        if self.kind == self.Kind.CLABE:
            return f"{v[:3]}{'*' * 12}{v[-3:]}"  # 123 ************ 456
        # ACCOUNT: muestra últimos 4
        return f"{'*' * max(0, len(v) - 4)}{v[-4:]}"