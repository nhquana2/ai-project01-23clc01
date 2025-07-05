# Project 1: Rush Hour Puzzle Solver - Class of Introduction to Artificial Intelligence

> A visual, interactive solver for the classic "Rush Hour" traffic-jam puzzle.  
> Experiment with state-space search techniques such as **BFS**, **DFS**, **UCS**, and **A\*** – all animated in real-time via Pygame.

---

## 📂 Project structure

```
ai-project01-23clc01/
├── assets/              # Images, buttons and bitmap font
├── definition/          # Core game & state representation (Board, Vehicle)
├── gui/                 # Menu, controller and drawing utilities
├── solvers/             # Search algorithms & heuristics
├── maps/                # JSON maps describing each puzzle
├── main.py              # Entry-point that launches the GUI
└── README.md            # You are here
```

### Map format
Each map is a JSON array where every element describes one vehicle:
```json
{
  "id": 0,              // integer – vehicle identifier (0 is the red car)
  "length": 2,          // 2 or 3 cells long
  "orientation": "H",   // "H" for horizontal, "V" for vertical
  "row": 2,
  "col": 1
}
```
The board is a 6×6 grid with the exit on the right edge of row 2.

#### Key modules & classes (high-level)

* `definition/board.py` – `Board` class that models a 6 × 6 puzzle state and exposes move generation & goal-test helpers.
* `definition/vehicle.py` – `Vehicle` data container (length, orientation, position).
* `solvers/` – search strategies implementing the `Solver` *protocol* (DFS, BFS, UCS, AStar) and reusable heuristics.
* `gui/menu.py` & `gui/controller.py` – Pygame menu, board renderer, animation loop and metrics display.
* `assets/` – PNG sprites & bitmap font used by the interface.

---

## Installation & Running

> Requires **Python ≥ 3.9**

1. Clone the repository:
   ```bash
   git clone https://github.com/nhquana2/ai-project01-23clc01.git
   cd ai-project01-23clc01
   ```
2. (Optional) create a virtual environment with python venv or conda:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

   ```bash
   conda create -n rush_hour python==3.9
   conda activate rush_hour
   select rush_hour interpreter
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the GUI:
   ```bash
   python main.py
   ```


