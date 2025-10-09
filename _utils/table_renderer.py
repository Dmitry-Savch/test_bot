"""
Table Renderer for Bybit Withdrawal History Screenshots

Optimized rendering engine that reduces image copying and provides
a clean API for rendering tabular data on images.
"""
from typing import List, Tuple, Literal
from PIL import Image
from PIL import ImageDraw, ImageFont
from dataclasses import dataclass


@dataclass
class ColumnConfig:
    """Configuration for a table column."""
    x_position: int
    alignment: Literal['left', 'right'] = 'left'


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

        # Get font metrics for baseline alignment
        ascent, descent = self._font.getmetrics()

        # Render each row
        for row_idx, row_data in enumerate(rows):
            if row_idx >= len(self.config.y_positions):
                break

            y_base = self.config.y_positions[row_idx]

            # Render each column in the row
            for col_name, text in row_data.items():
                if col_name not in self.config.columns:
                    continue

                col_config = self.config.columns[col_name]

                # Calculate x position based on alignment
                if col_config.alignment == 'right':
                    text_width = self._get_text_width(text)
                    x_pos = col_config.x_position - text_width
                else:
                    x_pos = col_config.x_position

                # Y position using baseline alignment
                y_pos = y_base - ascent

                # Draw text
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

    Coordinates are calibrated for 70% scaled template.
    Original template size: 6720 x 4200 px
    After 70% resize: 4704 x 2940 px
    Images are resized BEFORE text rendering for accurate positioning.

    Returns:
        TableConfig for Bybit tables
    """
    return TableConfig(
        font_family="fonts/OpenSans-Semibold.ttf",
        font_size=77,  # Scaled for high-res template (70% of ~110px)
        text_color=(255, 255, 255),
        kerning=2.0,  # Adjusted for large text
        # Y positions for 6 rows (measured from reference screenshot, scaled to 70%)
        y_positions=[930, 1169, 1407, 1645, 1882, 2121],
        columns={
            'time': ColumnConfig(x_position=700, alignment='left'),
            'account': ColumnConfig(x_position=1624, alignment='left'),
            'bank': ColumnConfig(x_position=2674, alignment='left'),
            'amount': ColumnConfig(x_position=3850, alignment='right'),
        }
    )
