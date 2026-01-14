"""Control state management for manual overrides and system modes."""

from dataclasses import dataclass
from enum import Enum
import threading
from typing import Callable, Optional


class SystemMode(Enum):
    """Operating modes for the detection system."""
    AUTO = "auto"
    MANUAL = "manual"
    PAUSED = "paused"
    DEGRADED = "degraded"


@dataclass
class ControlState:
    """
    Represents the current control state of the system.
    Allows for manual overrides and emergency stops.
    """
    mode: SystemMode = SystemMode.AUTO
    manual_override: bool = False
    emergency_stop: bool = False
    confidence_threshold: float = 0.5
    enable_llm: bool = True
    enable_tracking: bool = True
    request_quit: bool = False
    paused: bool = False
    
    def is_active(self) -> bool:
        """Check if the system is actively processing."""
        return not self.emergency_stop and self.mode != SystemMode.PAUSED and not self.paused
    
    def is_auto_mode(self) -> bool:
        """Check if system is in automatic mode."""
        return self.mode == SystemMode.AUTO and not self.manual_override
    
    def set_manual_override(self, enabled: bool):
        """Enable or disable manual override mode."""
        self.manual_override = enabled
        if enabled:
            self.mode = SystemMode.MANUAL
        elif self.mode == SystemMode.MANUAL:
            self.mode = SystemMode.AUTO
    
    def toggle_emergency_stop(self):
        """Toggle emergency stop state."""
        self.emergency_stop = not self.emergency_stop
    
    def toggle_pause(self):
        """Toggle pause state."""
        self.paused = not self.paused
        if self.paused:
            self.mode = SystemMode.PAUSED
        elif self.mode == SystemMode.PAUSED:
            self.mode = SystemMode.AUTO
    
    def set_quit(self):
        """Request to quit the application."""
        self.request_quit = True
    
    def set_degraded_mode(self, enabled: bool):
        """Switch to degraded mode (reduced functionality)."""
        if enabled:
            self.mode = SystemMode.DEGRADED
        elif self.mode == SystemMode.DEGRADED:
            self.mode = SystemMode.AUTO


class ControlListener:
    """
    Listens for control inputs (keyboard/events) to update ControlState.
    Runs in a separate thread to handle user input asynchronously.
    """
    
    def __init__(self, control_state: ControlState):
        """
        Initialize the control listener.
        
        Args:
            control_state: The ControlState instance to update
        """
        self.control_state = control_state
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._callbacks = {}
    
    def start(self):
        """Start listening for control inputs in a background thread."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """Stop listening for control inputs."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
    
    def register_callback(self, key: str, callback: Callable):
        """Register a callback for a specific key press."""
        self._callbacks[key] = callback
    
    def _listen_loop(self):
        """Main loop for listening to control inputs (stub implementation)."""
        # This is a stub - in a real implementation, you'd listen for keyboard
        # events or other control inputs here
        while self._running:
            threading.Event().wait(0.1)
    
    def handle_key(self, key: str):
        """
        Handle a key press event.
        
        Args:
            key: The key that was pressed
        """
        # Common key mappings
        if key == 'p':
            # Toggle pause
            self.control_state.toggle_pause()
        elif key == 'm':
            # Toggle manual override
            self.control_state.set_manual_override(not self.control_state.manual_override)
        elif key == 'e':
            # Toggle emergency stop
            self.control_state.toggle_emergency_stop()
        elif key == 'l':
            # Toggle LLM
            self.control_state.enable_llm = not self.control_state.enable_llm
        elif key == 'q':
            # Quit application
            self.control_state.set_quit()
        
        # Call registered callback if exists
        if key in self._callbacks:
            self._callbacks[key]()
