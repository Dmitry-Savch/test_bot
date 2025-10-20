"""
Interactive Coordinate Measurement Tool for Bybit FD Templates

This script allows you to precisely measure text coordinates by clicking on the template image.
Results are automatically saved to bybit_fd_config.py

Usage:
1. Run: python measure_coordinates_interactive.py
2. Click on positions where text should be placed
3. Press Enter to move to next measurement
4. Script updates bybit_fd_config.py automatically
"""

import cv2
import numpy as np
from PIL import Image
from typing import List, Tuple, Dict

class CoordinateMeasurer:
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.img = cv2.imread(template_path)
        if self.img is None:
            raise FileNotFoundError(f"Cannot load template: {template_path}")

        self.img_height, self.img_width = self.img.shape[:2]
        self.current_point = None
        self.window_name = "Coordinate Measurement Tool"

        # Collected coordinates
        self.y_positions: List[int] = []
        self.column_x: Dict[str, int] = {}

    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events."""
        if event == cv2.EVENT_MOUSEMOVE:
            self.current_point = (x, y)
            self.update_display()
        elif event == cv2.EVENT_LBUTTONDOWN:
            self.clicked_point = (x, y)
            print(f"✓ Зафіксовано координату: X={x}, Y={y}")

    def update_display(self):
        """Update display with current mouse position and coordinates."""
        display = self.img.copy()

        # Draw crosshair at mouse position
        if self.current_point:
            x, y = self.current_point
            cv2.line(display, (x, 0), (x, self.img_height), (0, 255, 0), 1)
            cv2.line(display, (0, y), (self.img_width, y), (0, 255, 0), 1)

            # Show coordinates
            text = f"X: {x}, Y: {y}"
            cv2.putText(display, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                       1, (0, 255, 0), 2)

        # Show collected points
        for idx, y_pos in enumerate(self.y_positions):
            cv2.line(display, (0, y_pos), (self.img_width, y_pos), (255, 0, 0), 1)
            cv2.putText(display, f"Row {idx+1}", (10, y_pos-5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        for col_name, x_pos in self.column_x.items():
            cv2.line(display, (x_pos, 0), (x_pos, self.img_height), (0, 0, 255), 1)
            cv2.putText(display, col_name, (x_pos+5, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        cv2.imshow(self.window_name, display)

    def measure_rows(self, num_rows: int = 11) -> List[int]:
        """Measure Y positions for table rows."""
        print(f"\n📏 Вимірювання Y-координат для {num_rows} рядків")
        print("=" * 60)
        print("Інструкції:")
        print("  1. Наведіть курсор на БАЗОВУ ЛІНІЮ тексту першого рядка")
        print("  2. Клікніть лівою кнопкою миші")
        print("  3. Натисніть ENTER для переходу до наступного рядка")
        print("  4. Натисніть 'q' для завершення вимірювання рядків")
        print("=" * 60)

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        self.update_display()

        for row_idx in range(num_rows):
            self.clicked_point = None
            print(f"\n➤ Вимірювання рядка {row_idx + 1}/{num_rows}")
            print("  Клікніть на базову лінію тексту, потім натисніть ENTER...")

            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == 13:  # Enter
                    if self.clicked_point:
                        y_coord = self.clicked_point[1]
                        self.y_positions.append(y_coord)
                        print(f"  ✓ Рядок {row_idx + 1}: Y = {y_coord}")
                        break
                    else:
                        print("  ⚠ Спочатку клікніть на позицію!")
                elif key == ord('q'):
                    print("\n⏹ Вимірювання рядків завершено достроково")
                    return self.y_positions

        print(f"\n✅ Всі {len(self.y_positions)} рядків виміряно!")
        return self.y_positions

    def measure_columns(self) -> Dict[str, int]:
        """Measure X positions for table columns."""
        columns = [
            ("MONEDA_X", "Moneda (Currency)"),
            ("BANCO_X", "Banco (Bank)"),
            ("TIEMPO_X", "Tiempo (Time)"),
            ("ESTADO_X", "Estado (Status)"),
            ("MONTO_X", "Monto (Amount)"),
            ("NUMERO_CUENTA_X", "Numero de cuenta (Account)")
        ]

        print(f"\n📏 Вимірювання X-координат для {len(columns)} колонок")
        print("=" * 60)
        print("Інструкції:")
        print("  1. Наведіть курсор на ЦЕНТР колонки (для center alignment)")
        print("  2. Клікніть лівою кнопкою миші")
        print("  3. Натисніть ENTER для переходу до наступної колонки")
        print("  4. Натисніть 'q' для завершення вимірювання колонок")
        print("=" * 60)

        for col_name, col_description in columns:
            self.clicked_point = None
            print(f"\n➤ Вимірювання колонки: {col_description}")
            print("  Клікніть на центр колонки, потім натисніть ENTER...")

            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == 13:  # Enter
                    if self.clicked_point:
                        x_coord = self.clicked_point[0]
                        self.column_x[col_name] = x_coord
                        print(f"  ✓ {col_name}: X = {x_coord}")
                        self.update_display()
                        break
                    else:
                        print("  ⚠ Спочатку клікніть на позицію!")
                elif key == ord('q'):
                    print("\n⏹ Вимірювання колонок завершено достроково")
                    return self.column_x

        print(f"\n✅ Всі {len(self.column_x)} колонок виміряно!")
        return self.column_x

    def save_to_config(self, config_path: str = "_utils/bybit_fd_config.py"):
        """Save measured coordinates to config file."""
        print(f"\n💾 Збереження координат у {config_path}...")

        # Read current config
        with open(config_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Prepare new content
        new_lines = []
        in_y_positions = False
        in_x_positions = False
        skip_until_bracket = False

        for line in lines:
            # Handle Y_POSITIONS section
            if 'Y_POSITIONS = [' in line:
                in_y_positions = True
                new_lines.append('Y_POSITIONS = [\n')
                for idx, y_pos in enumerate(self.y_positions):
                    new_lines.append(f'    {y_pos},   # Row {idx + 1}\n')
                new_lines.append(']\n')
                skip_until_bracket = True
                continue

            if skip_until_bracket and ']' in line and in_y_positions:
                in_y_positions = False
                skip_until_bracket = False
                continue

            if in_y_positions:
                continue

            # Handle X positions
            if 'MONEDA_X' in line:
                in_x_positions = True

            if in_x_positions:
                if 'MONEDA_X' in line:
                    new_lines.append(f'MONEDA_X = {self.column_x.get("MONEDA_X", 680)}                    # "Moneda" (Currency) column\n')
                elif 'BANCO_X' in line:
                    new_lines.append(f'BANCO_X = {self.column_x.get("BANCO_X", 860)}                     # "Banco" (Bank) column\n')
                elif 'TIEMPO_X' in line:
                    new_lines.append(f'TIEMPO_X = {self.column_x.get("TIEMPO_X", 1080)}                   # "Tiempo" column\n')
                elif 'ESTADO_X' in line:
                    new_lines.append(f'ESTADO_X = {self.column_x.get("ESTADO_X", 1350)}                   # "Estado" column\n')
                elif 'MONTO_X' in line:
                    new_lines.append(f'MONTO_X = {self.column_x.get("MONTO_X", 1800)}                    # "Monto" column\n')
                elif 'NUMERO_CUENTA_X' in line:
                    new_lines.append(f'NUMERO_CUENTA_X = {self.column_x.get("NUMERO_CUENTA_X", 2150)}            # "Numero de cuenta" column\n')
                    in_x_positions = False
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # Write updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"✅ Координати успішно збережено у {config_path}")

    def run(self):
        """Run the interactive measurement tool."""
        print("\n" + "=" * 60)
        print("🎯 ІНТЕРАКТИВНИЙ ІНСТРУМЕНТ ВИМІРЮВАННЯ КООРДИНАТ")
        print("=" * 60)
        print(f"Шаблон: {self.template_path}")
        print(f"Розмір: {self.img_width} × {self.img_height} px")
        print("=" * 60)

        # Measure rows first
        self.measure_rows(num_rows=11)

        # Then measure columns
        self.measure_columns()

        # Show summary
        print("\n" + "=" * 60)
        print("📊 ПІДСУМОК ВИМІРЮВАНЬ")
        print("=" * 60)
        print(f"\nY-координати ({len(self.y_positions)} рядків):")
        for idx, y_pos in enumerate(self.y_positions):
            print(f"  Row {idx + 1}: Y = {y_pos}")

        print(f"\nX-координати ({len(self.column_x)} колонок):")
        for col_name, x_pos in self.column_x.items():
            print(f"  {col_name}: X = {x_pos}")

        # Ask to save
        print("\n" + "=" * 60)
        response = input("\n💾 Зберегти координати у bybit_fd_config.py? (y/n): ")
        if response.lower() == 'y':
            self.save_to_config()
            print("\n✅ Готово! Координати оновлено.")
        else:
            print("\n⏹ Координати не збережено.")

        cv2.destroyAllWindows()


def main():
    template_path = "templates/Group 1312320191.png"

    try:
        measurer = CoordinateMeasurer(template_path)
        measurer.run()
    except FileNotFoundError as e:
        print(f"\n❌ Помилка: {e}")
        print("Переконайтеся, що файл templates/Group 1312320191.png існує.")
    except Exception as e:
        print(f"\n❌ Несподівана помилка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
