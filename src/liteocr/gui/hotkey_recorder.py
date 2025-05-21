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
        self.has_pressed_char_key = False

    def start_recording(self):
        """Start listening for hotkey combination."""
        if self.recording:
            return

        self.recording = True
        self.recorded_keys = set()
        self.has_pressed_char_key = False
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

        key_processed_for_hotkey_string = False
        current_key_str = None

        try:
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.recorded_keys.add("<ctrl>")
                key_processed_for_hotkey_string = True
            elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.recorded_keys.add("<alt>")
                key_processed_for_hotkey_string = True
            elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
                self.recorded_keys.add("<shift>")
                key_processed_for_hotkey_string = True
            elif (
                key == keyboard.Key.cmd_l
                or key == keyboard.Key.cmd_r
                or key == keyboard.Key.cmd
            ):  # cmd for mac
                self.recorded_keys.add("<cmd>")
                key_processed_for_hotkey_string = True
            elif key == keyboard.Key.esc:
                self.stop_recording(cancelled=True)
                return  # Stop further processing for Esc

            # Try to get a character representation
            elif isinstance(key, keyboard.KeyCode):
                # Check if char is a printable character and not a control character
                if (
                    key.char
                    and len(key.char) == 1
                    and key.char.isprintable()
                    and not (0 <= ord(key.char) <= 31)
                ):
                    current_key_str = key.char.lower()
                # Fallback for Windows: Use vk for A-Z and 0-9 if char is None or control char
                # (e.g. when Ctrl is pressed, key.char might be \x01 for 'a')
                elif hasattr(key, "vk"):
                    vk = key.vk
                    if 0x41 <= vk <= 0x5A:  # A-Z
                        current_key_str = chr(vk).lower()
                    elif 0x30 <= vk <= 0x39:  # 0-9
                        current_key_str = chr(vk)
                    elif 0x60 <= vk <= 0x69:  # Numpad 0-9
                        current_key_str = str(vk - 0x60)

                if current_key_str:
                    self.recorded_keys.add(current_key_str)
                    self.has_pressed_char_key = True
                    key_processed_for_hotkey_string = True

            elif isinstance(key, keyboard.Key):  # Special keys like F1, Space, Enter
                # Map common special keys to a more readable format
                key_name_map = {
                    keyboard.Key.space: "<space>",
                    keyboard.Key.enter: "<enter>",
                    keyboard.Key.tab: "<tab>",
                    keyboard.Key.backspace: "<backspace>",
                    keyboard.Key.delete: "<delete>",
                    keyboard.Key.up: "<up>",
                    keyboard.Key.down: "<down>",
                    keyboard.Key.left: "<left>",
                    keyboard.Key.right: "<right>",
                    keyboard.Key.home: "<home>",
                    keyboard.Key.end: "<end>",
                    keyboard.Key.page_up: "<page_up>",
                    keyboard.Key.page_down: "<page_down>",
                    # Add F keys
                    **{getattr(keyboard.Key, f"f{i}"): f"<f{i}>" for i in range(1, 13)},
                }
                if key in key_name_map:
                    current_key_str = key_name_map[key]
                else:  # For other unmapped special keys, use their default name
                    current_key_str = f"<{key.name}>"

                if current_key_str:
                    self.recorded_keys.add(current_key_str)
                    self.has_pressed_char_key = True
                    key_processed_for_hotkey_string = True

            if key_processed_for_hotkey_string:
                # Emit the currently formed hotkey string for live update
                self.key_pressed.emit(self._format_hotkey_string())

        except AttributeError:
            logging.warning(
                f"AttributeError for key: {key}. This key might not have 'char' or 'vk'."
            )
        except Exception as e:
            logging.error(f"Error during hotkey key press: {e}")
            self.stop_recording(cancelled=True)

    def _on_key_release(self, key):
        """Handle key release events during recording."""
        if not self.recording:
            return

        # Determine if the released key is a modifier
        is_modifier = key in [
            keyboard.Key.ctrl_l,
            keyboard.Key.ctrl_r,
            keyboard.Key.alt_l,
            keyboard.Key.alt_r,
            keyboard.Key.shift_l,
            keyboard.Key.shift_r,
            keyboard.Key.cmd_l,
            keyboard.Key.cmd_r,
            keyboard.Key.cmd,
        ]

        if not is_modifier and self.has_pressed_char_key:
            has_actual_keys = any(
                k not in ["<ctrl>", "<alt>", "<shift>", "<cmd>"]
                for k in self.recorded_keys
            )
            if has_actual_keys:
                self.stop_recording()

    def _format_hotkey_string(self):
        """Format the recorded keys into a standardized hotkey string."""
        if not self.recorded_keys:
            return ""

        modifiers_order = ["<ctrl>", "<shift>", "<alt>", "<cmd>"]

        present_modifiers = [m for m in modifiers_order if m in self.recorded_keys]

        action_keys = sorted(list(self.recorded_keys - set(modifiers_order)))

        if not action_keys:
            return ""

        final_keys = present_modifiers + action_keys

        return "+".join(final_keys)
