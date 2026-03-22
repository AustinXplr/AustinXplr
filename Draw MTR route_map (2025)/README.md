# MTR Route Map (2025)

A Hong Kong MTR system map drawn with Python's `turtle` graphics library.  
Each line follows its official color and approximate real-world path.

## Requirements

- Python 3.x (3.7 or later recommended)
- No additional packages needed (`turtle` is part of the Python standard library)

## How to Run

1. Save the code as `Draw MTR route_map (2025).py`
2. Open a terminal and run:
   ```bash
   python "Draw MTR route_map (2025).py"
A window will open and the map will be drawn automatically.
Features

Uses official MTR line colors (e.g., Tsuen Wan Line red, East Rail Line light blue, Tuen Ma Line brown)
Includes Light Rail symbol, High Speed Rail, Disneyland Resort Line, and Airport Express
The northern section of the East Rail Line uses a dashed arc (implemented with dashed_arc())
Coordinates and angles are manually tuned to approximate the actual route layout
Code Structure

Section	Description
Imports	turtle for drawing, math for arc length calculation
Window setup	Title, background color, pen speed, pen size
Line drawing	Each line drawn separately with its own color and path
Dashed arc function	dashed_arc() creates the dashed effect for the East Rail Line
End	t.hideturtle() hides the cursor, t.done() keeps the window open
Notes

Coordinates and angles were manually adjusted. Changing them is not recommended — it may break the relative positions of the lines.
To change drawing speed, modify t.speed(0) (0 = fastest, 1–10 = slower).
The program ends when the drawing window is closed.
Author

Austin Li

License

For personal / educational use only.