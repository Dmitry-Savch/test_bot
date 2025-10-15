"""
Table Renderer for Bybit Withdrawal History Screenshots

Optimized rendering engine that reduces image copying and provides
a clean API for rendering tabular data on images.
"""
from typing import List, Tuple, Literal
from PIL import Image
from PIL import ImageDraw, ImageFont
from dataclasses import dataclass
from _utils import bybit_config


@dataclass
class ColumnConfig:
    """Configuration for a table column."""
    x_position: int
    alignment: Literal['left', 'right', 'center'] = 'left'


@dataclass
class TableConfig:
    """Configuration for table rendering."""
    font_family: str
    font_size: int
    text_color: Tuple[int, int, int]
    kerning: float
    y_positions: List[int]
    columns: dict[str, ColumnConfig]


class TableRenderer:
    """Optimized table renderer for withdrawal history screenshots."""

    def __init__(self, config: TableConfig):
        """
        Initialize table renderer with configuration.

        Args:
            config: Table rendering configuration
        """
        self.config = config
        self._font = None
        self._load_font()

    def _load_font(self):
        """Load font once during initialization."""
        try:
            self._font = ImageFont.truetype(
                self.config.font_family,
                self.config.font_size
            )
        except Exception:
            self._font = ImageFont.load_default()

    def _get_text_width(self, text: str) -> int:
        """Calculate text width with kerning."""
        if hasattr(self._font, 'getlength'):
            base_width = self._font.getlength(text)
        else:
            bbox = self._font.getbbox(text)
            base_width = bbox[2] - bbox[0]

        # Add kerning for all characters except the last one
        extra_tracking = max(0, len(text) - 1) * self.config.kerning
        return int(round(base_width + extra_tracking))

    def _draw_text_with_kerning(
        self,
        draw: ImageDraw.ImageDraw,
        position: Tuple[int, int],
        text: str,
        fill: Tuple[int, int, int, int]
    ):
        """Draw text with custom kerning."""
        x, y = position

        if self.config.kerning == 0:
            # Fast path: no extra kerning
            draw.text((x, y), text, font=self._font, fill=fill)
            return

        # Draw each character with kerning
        for char in text:
            draw.text((x, y), char, font=self._font, fill=fill)
            if hasattr(self._font, 'getlength'):
                char_width = self._font.getlength(char)
            else:
                bbox = self._font.getbbox(char)
                char_width = bbox[2] - bbox[0]
            x += int(round(char_width + self.config.kerning))

    def render_table(
        self,
        base_image: Image.Image,
        rows: List[dict[str, str]]
    ) -> Image.Image:
        """
        Render table data onto base image.

        Args:
            base_image: Template image to render on
            rows: List of row data, each row is a dict mapping column names to text

        Returns:
            New image with rendered table
        """
        # Work on RGBA for transparency support
        result = base_image.convert("RGBA")
        overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Prepare color
        r, g, b = self.config.text_color
        fill = (r, g, b, 255)

        # Render each row
        for row_idx, row_data in enumerate(rows):
            if row_idx >= len(self.config.y_positions):
                break

            y_pos = self.config.y_positions[row_idx]

            # Render each column in the row
            for col_name, text in row_data.items():
                if col_name not in self.config.columns:
                    continue

                col_config = self.config.columns[col_name]

                # Calculate x position based on alignment
                text_width = self._get_text_width(text)

                if col_config.alignment == 'right':
                    x_pos = col_config.x_position - text_width
                elif col_config.alignment == 'center':
                    x_pos = col_config.x_position - (text_width // 2)
                else:  # left
                    x_pos = col_config.x_position

                # Draw text (y_pos is the top of the text bounding box)
                self._draw_text_with_kerning(
                    draw,
                    (x_pos, y_pos),
                    text,
                    fill
                )

        # Composite overlay onto result
        result.alpha_composite(overlay)
        return result


def create_bybit_table_config() -> TableConfig:
    """
    Create standard Bybit withdrawal history table configuration.

    Uses shared configuration from bybit_config.py to ensure consistency
    across all rendering methods.

    Coordinates are calibrated for 50% scaled template.
    Original template size: 6720 x 4200 px
    After 50% resize: 3360 x 2100 px
    Images are resized BEFORE text rendering for accurate positioning.

    Returns:
        TableConfig for Bybit tables
    """
    return TableConfig(
        font_family=bybit_config.FONT_FAMILY,
        font_size=bybit_config.FONT_SIZE,
        text_color=bybit_config.TEXT_COLOR,
        kerning=bybit_config.KERNING,
        y_positions=bybit_config.Y_POSITIONS,
        columns={
            'time': ColumnConfig(x_position=bybit_config.TIEMPO_X, alignment='left'),
            'account': ColumnConfig(x_position=bybit_config.NUMERO_CUENTA_X, alignment='left'),
            'bank': ColumnConfig(x_position=bybit_config.BANCO_X, alignment='left'),
            'amount': ColumnConfig(x_position=bybit_config.MONTO_X, alignment='center'),
        }
    )
