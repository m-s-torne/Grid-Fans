"""Lineup slot value object"""
from dataclasses import dataclass
from enum import Enum


class SlotPosition(str, Enum):
    """Valid lineup positions for drivers"""
    MAIN_1 = "main_1"
    MAIN_2 = "main_2"
    MAIN_3 = "main_3"
    RESERVE = "reserve"


@dataclass(frozen=True)
class LineupSlot:
    """
    Immutable value object representing a lineup position.
    
    Each user team has 3 main drivers and 1 reserve driver.
    Main drivers score full points, reserve scores partial points.
    """
    
    position: SlotPosition
    
    def __post_init__(self):
        """Validate slot position"""
        if not isinstance(self.position, SlotPosition):
            raise ValueError(f"Invalid lineup position: {self.position}")
    
    @property
    def is_main_slot(self) -> bool:
        """Check if this is a main driver slot"""
        return self.position in (
            SlotPosition.MAIN_1,
            SlotPosition.MAIN_2,
            SlotPosition.MAIN_3,
        )
    
    @property
    def is_reserve_slot(self) -> bool:
        """Check if this is the reserve slot"""
        return self.position == SlotPosition.RESERVE
    
    @property
    def points_multiplier(self) -> float:
        """
        Get points multiplier for this slot.
        
        Returns:
            1.0 for main drivers, 0.5 for reserve
        """
        return 1.0 if self.is_main_slot else 0.5
    
    @property
    def display_name(self) -> str:
        """Get human-readable slot name"""
        names = {
            SlotPosition.MAIN_1: "Main Driver 1",
            SlotPosition.MAIN_2: "Main Driver 2",
            SlotPosition.MAIN_3: "Main Driver 3",
            SlotPosition.RESERVE: "Reserve Driver",
        }
        return names[self.position]
    
    @property
    def slot_index(self) -> int:
        """Get zero-based index (0-3)"""
        indices = {
            SlotPosition.MAIN_1: 0,
            SlotPosition.MAIN_2: 1,
            SlotPosition.MAIN_3: 2,
            SlotPosition.RESERVE: 3,
        }
        return indices[self.position]
    
    @property
    def is_required(self) -> bool:
        """
        Check if this slot must be filled.
        
        Returns:
            True for main slots, False for reserve
        """
        return self.is_main_slot
    
    def can_swap_with(self, other: "LineupSlot") -> bool:
        """
        Check if this slot can be swapped with another.
        
        Args:
            other: Another lineup slot
            
        Returns:
            True if slots can be swapped (both main or one is reserve)
        """
        # Can always swap within main slots
        if self.is_main_slot and other.is_main_slot:
            return True
        
        # Can swap main with reserve
        if (self.is_main_slot and other.is_reserve_slot) or \
           (self.is_reserve_slot and other.is_main_slot):
            return True
        
        return False
    
    @classmethod
    def from_string(cls, slot_str: str) -> "LineupSlot":
        """Create slot from string (case-insensitive)"""
        try:
            position = SlotPosition(slot_str.lower())
            return cls(position)
        except ValueError:
            raise ValueError(
                f"Invalid slot string: {slot_str}. "
                f"Must be main_1, main_2, main_3, or reserve"
            )
    
    @classmethod
    def from_index(cls, index: int) -> "LineupSlot":
        """Create slot from index (0-3)"""
        positions = [
            SlotPosition.MAIN_1,
            SlotPosition.MAIN_2,
            SlotPosition.MAIN_3,
            SlotPosition.RESERVE,
        ]
        
        if not 0 <= index < len(positions):
            raise ValueError(f"Invalid slot index: {index}. Must be 0-3")
        
        return cls(positions[index])
    
    @classmethod
    def all_main_slots(cls) -> list["LineupSlot"]:
        """Get all main driver slots"""
        return [
            cls(SlotPosition.MAIN_1),
            cls(SlotPosition.MAIN_2),
            cls(SlotPosition.MAIN_3),
        ]
    
    @classmethod
    def all_slots(cls) -> list["LineupSlot"]:
        """Get all lineup slots"""
        return [cls(pos) for pos in SlotPosition]
    
    def __str__(self) -> str:
        return self.display_name
    
    def __repr__(self) -> str:
        return f"LineupSlot({self.position.value})"
