"""
theme.py
Definisi konstanta warna, font, dan style modern untuk seluruh aplikasi.
Mendukung mode Light dan Dark.
"""


class Theme:
    """Menyimpan palet warna & font aktif. Dapat diubah lewat toggle dark/light mode."""

    FONT_FAMILY = "Segoe UI"

    LIGHT = {
        "bg_primary": "#F4F6F9",
        "bg_secondary": "#FFFFFF",
        "bg_sidebar": "#1E3A5F",
        "bg_sidebar_hover": "#28496F",
        "bg_sidebar_active": "#2F5A8C",
        "text_primary": "#1F2937",
        "text_secondary": "#6B7280",
        "text_on_sidebar": "#E5EAF1",
        "accent": "#2F6FED",
        "accent_hover": "#255BC4",
        "border": "#E2E5EA",
        "card_bg": "#FFFFFF",
        "success": "#22A06B",
        "warning": "#F0A93A",
        "danger": "#E5484D",
        "table_row_odd": "#FFFFFF",
        "table_row_even": "#F6F8FB",
        "table_header": "#1E3A5F",
        "table_header_text": "#FFFFFF",
    }

    DARK = {
        "bg_primary": "#151B23",
        "bg_secondary": "#1D242E",
        "bg_sidebar": "#0F151C",
        "bg_sidebar_hover": "#1B2733",
        "bg_sidebar_active": "#25384A",
        "text_primary": "#E7ECF3",
        "text_secondary": "#9AA5B1",
        "text_on_sidebar": "#DCE3EC",
        "accent": "#4C8DFF",
        "accent_hover": "#3F76D6",
        "border": "#2B333D",
        "card_bg": "#1D242E",
        "success": "#3DBE85",
        "warning": "#F0B54D",
        "danger": "#F0696D",
        "table_row_odd": "#1D242E",
        "table_row_even": "#232C38",
        "table_header": "#0F151C",
        "table_header_text": "#E7ECF3",
    }

    _mode = "light"
    _colors = LIGHT

    @classmethod
    def set_mode(cls, mode):
        cls._mode = mode
        cls._colors = cls.LIGHT if mode == "light" else cls.DARK

    @classmethod
    def get_mode(cls):
        return cls._mode

    @classmethod
    def color(cls, key):
        return cls._colors.get(key, "#000000")

    @classmethod
    def font(cls, size=10, weight="normal"):
        return (cls.FONT_FAMILY, size, weight)
