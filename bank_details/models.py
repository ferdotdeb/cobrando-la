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

class BankDetails(models.Model):
    class Kind(models.TextChoices):
        CLABE = "CLABE", "CLABE"
        CARD = "CARD", "Card"
        ACCOUNT = "ACCOUNT", "Account"
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bank_details",
    )

    kind = models.CharField(max_length=16, choices=Kind.choices)
    # Maximum length of numbers (CLABE=18, CARD=16, ACCOUNT flexible)
    value = models.CharField(max_length=32)

    bank_name = models.CharField(max_length=80, blank=True)
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
        # Normalize: quit spaces and dashes from value
        if self.value:
            self.value = re.sub(r"[\s-]", "", self.value)

        val = self.value or ""

        if self.kind == self.Kind.CLABE:
            # CLABE: exactly 18 digits (checksum real opcional; MVP = len check)
            if not re.fullmatch(r"\d{18}", val):
                raise ValidationError({"value": "CLABE must be exactly 18 digits."})

        elif self.kind == self.Kind.CARD:
            # Card: 16 digits + Luhn
            if not re.fullmatch(r"\d{16}", val):
                raise ValidationError({"value": "Card number must be exactly 16 digits."})
            if not luhn_check(val):
                raise ValidationError({"value": "Card number failed Luhn checksum."})
            
        elif self.kind == self.Kind.ACCOUNT:
            # Account: flexible 6–20 digits (varies by bank)
            if not re.fullmatch(r"\d{6,20}", val):
                raise ValidationError({"value": "Account number must be 6–20 digits."})
            
        else:
            raise ValidationError({"kind": "Invalid kind of bank detail."})

    def save(self, *args, **kwargs):
        # Guarantee clean is called
        self.full_clean()
        return super().save(*args, **kwargs)

     
    @property
    def masked_value(self) -> str:
        """Shows an obfuscated value."""
        v = self.value or ""
        if not v:
            return ""
        if self.kind == self.Kind.CARD:
            # **** **** **** 1234
            return f"{'*' * 12}{v[-4:]}"
        if self.kind == self.Kind.CLABE:
            # 123 ************ 456 (keep first 3 and last 3)
            return f"{v[:3]}{'*' * 12}{v[-3:]}"
        # ACCOUNT: keep last 4
        return f"{'*' * max(0, len(v) - 4)}{v[-4:]}"       