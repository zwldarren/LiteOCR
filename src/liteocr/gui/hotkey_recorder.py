from PySide6.QtCore import QObject, Signal
from pynput import keyboard
import logging


class HotkeyRecorder(QObject):
    """Handles recording keyboard shortcuts and emits the result as a formatted string."""

    recording_started = Signal()
    recording_stopped = Signal(str)  # Emits the recorded hotkey string
    recording_cancelled = Signal()
    key_pressed = Signal(str)  # Emits each key press as a string

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listener = None
        self.recording = False
        self.recorded_keys = set()

    def start_recording(self):
        """Start listening for hotkey combination."""
        if self.recording:
            return

        self.recording = True
        self.recorded_keys = set()
        self.recording_started.emit()

        # Stop any existing listener
        if self.listener:
            self.listener.stop()

        self.listener = keyboard.Listener(
            on_press=self._on_key_press, on_release=self._on_key_release
        )
        self.listener.start()

    def stop_recording(self, cancelled=False):
        """Stop recording and clean up resources."""
        if self.listener:
            self.listener.stop()
            self.listener = None

        self.recording = False

        if cancelled:
            self.recording_cancelled.emit()
        elif self.recorded_keys:
            hotkey_str = self._format_hotkey_string()
            self.recording_stopped.emit(hotkey_str)
        else:
            self.recording_cancelled.emit()

    def _on_key_press(self, key):
        """Handle key press events during recording."""
        if not self.recording:
            return

        try:
            # Handle special keys
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.recorded_keys.add("<ctrl>")
            elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.recorded_keys.add("<alt>")
            elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
                self.recorded_keys.add("<shift>")
            elif key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
                self.recorded_keys.add("<cmd>")
            elif key == keyboard.Key.esc:
                self.stop_recording(cancelled=True)
                return
            elif hasattr(key, "char") and key.char is not None:
                key_str = key.char.lower()
                self.recorded_keys.add(key_str)
                self.key_pressed.emit(key_str)
            else:
                # Handle other special keys (F1-F12, etc.)
                key_str = str(key).replace("Key.", "<") + ">"
                self.recorded_keys.add(key_str)
                self.key_pressed.emit(key_str)

        except Exception as e:
            logging.error(f"Error during hotkey key press: {e}")
            self.stop_recording(cancelled=True)

    def _on_key_release(self, key):
        """Handle key release events during recording."""
        if not self.recording:
            return

        # Stop recording when a non-modifier key is released
        is_modifier = (
            key == keyboard.Key.ctrl_l
            or key == keyboard.Key.ctrl_r
            or key == keyboard.Key.alt_l
            or key == keyboard.Key.alt_r
            or key == keyboard.Key.shift_l
            or key == keyboard.Key.shift_r
            or key == keyboard.Key.cmd_l
            or key == keyboard.Key.cmd_r
        )

        if not is_modifier and self.recorded_keys:
            self.stop_recording()
        elif is_modifier and not any(
            k.startswith("<") and k.endswith(">")
            for k in self.recorded_keys
            if k not in ["<ctrl>", "<alt>", "<shift>", "<cmd>"]
        ):
            self.stop_recording()

    def _format_hotkey_string(self):
        """Format the recorded keys into a standardized hotkey string."""
        sorted_keys = []

        # Add modifiers in consistent order
        if "<ctrl>" in self.recorded_keys:
            sorted_keys.append("<ctrl>")
        if "<shift>" in self.recorded_keys:
            sorted_keys.append("<shift>")
        if "<alt>" in self.recorded_keys:
            sorted_keys.append("<alt>")
        if "<cmd>" in self.recorded_keys:
            sorted_keys.append("<cmd>")

        # Add non-modifier keys
        non_modifiers = sorted(
            k
            for k in self.recorded_keys
            if not k.startswith("<") or k in [f"<f{i}>" for i in range(1, 13)]
        )
        sorted_keys.extend(non_modifiers)

        return "+".join(sorted_keys)
