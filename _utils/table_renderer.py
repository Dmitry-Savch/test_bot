"""
Table Renderer for Bybit Withdrawal History Screenshots

Optimized rendering engine that reduces image copying and provides
a clean API for rendering tabular data on images.
Uses text_draw module for all text rendering operations.
"""
from typing import List, Tuple, Literal
from PIL import Image
from dataclasses import dataclass
from _utils import bybit_config
from _utils import text_draw


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
    """Optimized table renderer for withdrawal history screenshots using text_draw module."""

    def __init__(self, config: TableConfig):
        """
        Initialize table renderer with configuration.

        Args:
            config: Table rendering configuration
        """
        self.config = config

    def render_table(
        self,
        base_image: Image.Image,
        rows: List[dict[str, str]]
    ) -> Image.Image:
        """
        Render table data onto base image using text_draw module.

        Args:
            base_image: Template image to render on
            rows: List of row data, each row is a dict mapping column names to text

        Returns:
            New image with rendered table
        """
        result = base_image.copy()

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

                # Use text_draw.execute to render text with proper alignment
                result = text_draw.execute(
                    base_image=result,
                    font_sz=self.config.font_size,
                    text=text,
                    position=(col_config.x_position, y_pos),
                    alignment=col_config.alignment,
                    font_family=self.config.font_family,
                    text_color=self.config.text_color,
                    kerning=self.config.kerning
                )

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
            'account': ColumnConfig(x_position=bybit_config.NUMERO_CUENTA_X, alignment='center'),
            'bank': ColumnConfig(x_position=bybit_config.BANCO_X, alignment='center'),
            'amount': ColumnConfig(x_position=bybit_config.MONTO_X, alignment='center'),
        }
    )


def create_bybit_fd_table_config() -> TableConfig:
    """
    Create Bybit FD (Successful) table configuration.

    Uses shared configuration from bybit_fd_config.py to ensure consistency.
    Template size: 3840 x 2712 px

    Returns:
        TableConfig for Bybit FD tables
    """
    from _utils import bybit_fd_config

    return TableConfig(
        font_family=bybit_fd_config.FONT_FAMILY,
        font_size=bybit_fd_config.FONT_SIZE,
        text_color=bybit_fd_config.TEXT_COLOR,
        kerning=bybit_fd_config.KERNING,
        y_positions=bybit_fd_config.Y_POSITIONS,
        columns={
            'currency': ColumnConfig(x_position=bybit_fd_config.MONEDA_X, alignment='center'),
            'bank': ColumnConfig(x_position=bybit_fd_config.BANCO_X, alignment='center'),
            'time': ColumnConfig(x_position=bybit_fd_config.TIEMPO_X, alignment='center'),
            'status': ColumnConfig(x_position=bybit_fd_config.ESTADO_X, alignment='center'),
            'amount': ColumnConfig(x_position=bybit_fd_config.MONTO_X, alignment='center'),
            'account': ColumnConfig(x_position=bybit_fd_config.NUMERO_CUENTA_X, alignment='center'),
        }
    )
