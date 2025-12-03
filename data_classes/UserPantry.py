from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Tuple, Iterable

@dataclass
class PantryEntry():
    name: str 
    qty: float
    unit: str
    expires_on: Optional[datetime] = None


class Pantry():
    _CANON = {
        "white rice":"rice",
        "brown rice":"rice",
        "brocolli":"broccoli",
        "garbanzo beans":"chickpeas"
    }
    
    @staticmethod
    def norm(s: str) -> str:
        s = s.strip().lower()
        return Pantry._CANON.get(s, s)

    def __init__(self, user_id: str = "default", items: Optional[List[str]] = None):
        self.user_id = user_id
        self.items: Dict[str, PantryEntry] = {}
        
        if items:
            for item_name in items:
                normalized = self.norm(item_name)
                self.items[normalized] = PantryEntry(name=normalized, qty=1.0, unit="unit")