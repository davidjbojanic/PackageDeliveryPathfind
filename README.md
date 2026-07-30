# Salt Lake City Parcel Router

A command-line delivery routing simulator: it loads a day's worth of packages, assigns them across three trucks, calculates the most efficient delivery route for each truck using a nearest-neighbor algorithm, and lets you check the real-time status of any package (or the whole fleet) at any point in the day.

## The story

It's 7:45 a.m. at a small Salt Lake City parcel depot. Three trucks, two drivers, and forty packages that all need to be somewhere by end of day — some by 9:00 a.m., some by 10:30, a few whenever, and one with an address that's flat-out wrong until a corrected one comes in at 10:20.

The dispatcher's problem: figure out which packages go on which truck, in what order, so that every deadline is hit while the trucks collectively drive as few miles as possible. Do it wrong and a client's shipment shows up four hours late. Do it right and you've saved gas, driver hours, and a phone call from an angry customer.

This program is that dispatcher's solution — a self-contained routing engine (custom hash table, graph-based distance lookup, and a nearest-neighbor route builder) with a CLI dashboard that lets you rewind the day and see exactly where every package was, and every truck had driven, at any given minute.

## Features

- **Custom hash table** for package storage and lookup (no built-in dict used under the hood)
- **Graph-based distance model** loaded from a real distance matrix between delivery addresses
- **Nearest-neighbor routing** to minimize total miles driven per truck
- **Time-travel package lookup** — check the status of one package, or the entire fleet, as of any time of day
- **Live mileage totals**, correctly excluding miles not yet driven at the selected time
- **Clean terminal UI** — colored status badges, boxed tables, and package detail panels (no extra installs required)

## Requirements

- Python 3.9 or later
- No third-party packages — everything runs on the standard library

## Getting started

```bash
# Clone the repo
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# Run it — no pip install needed
python3 main.py
```

That's it. The program loads the package and distance data from the `data/` folder automatically and dispatches all three trucks the moment it starts.

> **Note:** Run it from the project's root folder (the one containing `main.py`), since it loads its CSV data using relative paths.

## How to use it

When you start the program, all three trucks are automatically loaded and dispatched:

```
╔══════════════════════════════════════════════════════════════╗
║                     WGUPS ROUTING SYSTEM                     ║
║             Salt Lake City Daily Local Delivery              ║
╚══════════════════════════════════════════════════════════════╝

Enter a time (e.g. 09:30) or q to quit:
```

**Step 1 — Enter a time.** Type any time in `HH:MM` (24-hour) format to "rewind" the day to that moment, e.g. `09:30`. Type `q` at any point to exit.

**Step 2 — Pick an action:**

```
  1  View all packages at selected time
  2  View one package at selected time
  3  Exit the program
```

### Option 1: View the whole fleet

Shows every package on every truck, its current status (`delivered`, `en route`, or `at the hub`), its deadline, and its drop-off time if delivered — followed by the combined mileage driven by all three trucks up to that point.

```
── Status of all packages at 09:30 ─────────────────────────────
Truck 1 — departure 8:00 AM
┌────┬────────────────────────────────────────┬─────────────┬──────────┬─────────┐
│ ID │ Address                                │ Status      │ Deadline │ Dropoff │
├────┼────────────────────────────────────────┼─────────────┼──────────┼─────────┤
│ 14 │ 4300 S 1300 E                          │ ● delivered │ 10:30 AM │ 8:06 AM │
│ 15 │ 4580 S 2300 E                          │ ● delivered │ 9:00 AM  │ 8:13 AM │
│ 37 │ 410 S State St                         │ ● en route  │ 10:30 AM │ NA      │
│ 11 │ 2600 Taylorsville Blvd                 │ ● en route  │ 5:00 PM  │ NA      │
└────┴────────────────────────────────────────┴─────────────┴──────────┴─────────┘

Truck 2 — departure 9:05 AM
┌────┬──────────────────────────┬─────────────┬──────────┬─────────┐
│ ID │ Address                  │ Status      │ Deadline │ Dropoff │
├────┼──────────────────────────┼─────────────┼──────────┼─────────┤
│ 25 │ 5383 South 900 East #104 │ ● delivered │ 10:30 AM │ 9:13 AM │
│ 28 │ 2835 Main St             │ ● en route  │ 5:00 PM  │ NA      │
└────┴──────────────────────────┴─────────────┴──────────┴─────────┘

Truck 3 — departure 10:40 AM
┌────┬─────────────────┬──────────────┬──────────┬─────────┐
│ ID │ Address         │ Status       │ Deadline │ Dropoff │
├────┼─────────────────┼──────────────┼──────────┼─────────┤
│ 9  │ 300 State St    │ ● at the hub │ 5:00 PM  │ NA      │
└────┴─────────────────┴──────────────┴──────────┴─────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Total mileage: 29.9 mi ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┛
```

*(Full output includes all packages per truck — trimmed here for readability.)*

### Option 2: Look up a single package

Enter a package ID (1–40) to see just that package's full detail card:

```
── Status of package ID#9 at 09:10 ─────────────────────────────
┌──────────────────────────┐
│ ID:       9              │
│ Address:  300 State St   │
│ City:     Salt Lake City │
│ Zip:      84103          │
│ Deadline: 5:00 PM        │
│ Weight:   2              │
│ Status:   ● at the hub   │
│ Dropoff:  None           │
└──────────────────────────┘
```

> Fun detail: try looking up package #9 before and after 10:20 a.m. — its address is intentionally wrong until a correction comes in mid-morning, exactly like a real dispatch correction would.

### Option 3: Exit

Ends the program.

## Project structure

```
.
├── main.py       # Entry point — loads data, dispatches trucks, runs the CLI loop
├── Truck.py      # Truck class: package loading, route calculation, status/mileage lookups
├── Hub.py        # Loads package data from CSV into the hash table
├── HashMap.py    # Custom hash table (chaining, auto-resize) used for package storage
├── Package.py    # Package data model
├── Distance.py   # Graph model + distance matrix loader
├── display.py    # Terminal UI helpers (colors, tables, panels) — presentation only
└── data/
    ├── WGUPS Package File.csv      # The day's package manifest
    ├── WGUPS Location list.csv     # Delivery addresses
    └── WGUPS Distance Table.csv    # Distance matrix between addresses
```

## How the routing works, briefly

1. **Load phase** — packages are read from CSV into a custom hash table (`HashMap.py`) keyed by package ID; delivery addresses are read into a graph (`Distance.py`) where edges are distances between locations.
2. **Assignment** — each truck is manually loaded with a subset of packages (grouped to respect deadlines, delivery constraints, and truck capacity).
3. **Routing** — each truck runs a nearest-neighbor algorithm: starting at the hub, it repeatedly travels to whichever remaining stop is closest, until all its packages are delivered.
4. **Timing** — delivery time for each stop is calculated from cumulative distance and a fixed truck speed, giving every package a computed drop-off time.
5. **Status lookup** — at any queried time, a package's status is derived by comparing that time against its computed drop-off time and its truck's departure time.

## License

Feel free to fork, adapt, or build on this for your own portfolio.