# SMAC BT-Agent
SMAC BT-Agent is an agent framework based on the behaviour tree in the SMAC environment.

## Features
- [x] Moving after meeting walls optimization
- [x] Evading direction optimization
- [x] Attacking during evading policy oprimization
- [x] Attacking policy optimization

- [ ] Coordinate moving
- [ ] exploration policy

## Installation

## SMAC environment rule instruction
### Map Coordination
Coordinate origin is at the `left-down` corner.

### Action
Action list
```
[no-op, stop, move, attack]
```
Move list
```
[
    north - 2
    south - 3
    east - 4
    west - 5
]
```
Attack list contains enemy id.

Kite
