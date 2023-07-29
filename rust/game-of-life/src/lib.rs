use std::borrow::Borrow;
use std::collections::HashSet;
use std::hash::Hash;
use std::iter::FromIterator;

/// A Coordinate in a 2D coordinate system.
#[derive(Eq, PartialEq, Hash, Debug)]
struct Coordinate {
    pub x: isize,
    pub y: isize,
}

/// A infinite Game Of Life universe
///
/// Attention:
/// The `Universe` at least needs the memory to keep track of all alive Cells and their Coordinates.
struct Universe {
    alive_cells: HashSet<Coordinate>,
}

impl Universe {
    pub fn new<I: Iterator<Item = Coordinate>>(alive_cells: I) -> Self {
        Universe {
            alive_cells: HashSet::from_iter(alive_cells),
        }
    }

    pub fn tick(&mut self) {
        let mut next_generation: Vec<Coordinate> = Vec::new();
        // 1. get set of cells which need to be considered in update
        // 2. for each affected coordinate/cell
        for position in self.affected_coordinates() {
            // 2.1 Get the state for the cell of the current position
            let cell = match self.alive_cells.contains(&position) {
                true => Cell {
                    is_alive: Liveliness::Alive,
                },
                false => Cell {
                    is_alive: Liveliness::Dead,
                },
            };
            // 2.2 Get all alive neighbours of for the cell of the current position
            let neighbours = self.alive_cells.iter().filter_map(|p| {
                let x_distance = (position.x - p.x).abs();
                let y_distance = (position.y - p.y).abs();
                if (x_distance <= 1) && (y_distance <= 1) {
                    Some(&Cell {
                        is_alive: Liveliness::Alive,
                    })
                } else {
                    None
                }
            });
            // 2.3 decide cell shall be alive or dead in the next generation
            if cell.next_generation_state(neighbours).into() {
                next_generation.push(position);
            }
        }
        // 3. update universe state
        self.alive_cells = HashSet::from_iter(next_generation.into_iter());
    }

    fn affected_coordinates(&self) -> impl Iterator<Item = Coordinate> + '_ {
        self.alive_cells
            .iter()
            .clone()
            .map(|position| {
                // for each alive cell all neighbours are relevant
                NeighboursIterator::new(Coordinate {
                    x: position.x,
                    y: position.y,
                })
            })
            .flatten()
    }
}

/// Iterator over all neighbours of a coordinate
struct NeighboursIterator {
    position: Coordinate,
    count: usize,
}

impl NeighboursIterator {
    pub fn new(position: Coordinate) -> Self {
        Self {
            position: Coordinate {
                x: position.x,
                y: position.y,
            },
            count: 0usize,
        }
    }
}

impl Iterator for NeighboursIterator {
    type Item = Coordinate;

    fn next(&mut self) -> Option<Self::Item> {
        let c = match self.count {
            // upper left
            0 => Some(Coordinate {
                x: self.position.x - 1,
                y: self.position.y + 1,
            }),
            // above
            1 => Some(Coordinate {
                x: self.position.x,
                y: self.position.y + 1,
            }),
            // upper right
            2 => Some(Coordinate {
                x: self.position.x + 1,
                y: self.position.y + 1,
            }),
            // to the right
            3 => Some(Coordinate {
                x: self.position.x + 1,
                y: self.position.y,
            }),
            // lower right
            4 => Some(Coordinate {
                x: self.position.x + 1,
                y: self.position.y - 1,
            }),
            // below
            5 => Some(Coordinate {
                x: self.position.x,
                y: self.position.y - 1,
            }),
            // lower left
            6 => Some(Coordinate {
                x: self.position.x - 1,
                y: self.position.y - 1,
            }),
            // to the left
            7 => Some(Coordinate {
                x: self.position.x - 1,
                y: self.position.y,
            }),
            _ => None,
        };
        self.count += 1;
        c
    }
}

/// A single cell in the universe it either can be alive or dead
#[derive(PartialOrd, PartialEq, Debug)]
struct Cell {
    is_alive: Liveliness,
}

impl Into<bool> for Cell {
    fn into(self) -> bool {
        self.is_alive.into()
    }
}

#[derive(PartialOrd, PartialEq, Debug, Copy, Clone)]
pub enum Liveliness {
    Dead,
    Alive,
}

impl Into<bool> for Liveliness {
    fn into(self) -> bool {
        match self {
            Liveliness::Alive => true,
            Liveliness::Dead => false,
        }
    }
}

impl<T: Borrow<bool>> From<T> for Liveliness {
    fn from(value: T) -> Self {
        match value.borrow() {
            true => Liveliness::Alive,
            false => Liveliness::Dead,
        }
    }
}

impl Cell {
    /// Rules:
    /// 1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
    /// 2. Any live cell with two or three live neighbours lives on to the next generation.
    /// 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    /// 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    pub fn next_generation_state<'a, I: Iterator<Item = &'a Cell>>(
        &self,
        neighbours: I,
    ) -> Liveliness {
        let alive_neighbours = neighbours.fold(0usize, |count, cell| {
            if cell.is_alive == Liveliness::Alive {
                count + 1
            } else {
                count
            }
        });
        match (&self.is_alive, alive_neighbours) {
            (Liveliness::Alive, alive_neighbours) if alive_neighbours < 2 => Liveliness::Dead,
            (Liveliness::Alive, 2..=3) => Liveliness::Alive,
            (Liveliness::Alive, alive_neighbours) if alive_neighbours > 3 => Liveliness::Dead,
            (Liveliness::Dead, 3) => Liveliness::Alive,
            _ => Liveliness::Dead,
        }
    }
}

#[cfg(test)]
mod tests {

    use crate::{Cell, Coordinate, Liveliness, NeighboursIterator};
    use std::collections::HashSet;

    #[test]
    fn test_create_new_neighbours_iterator() {
        let it = NeighboursIterator::new(Coordinate { x: 1, y: 1 });
        assert_eq!(Coordinate { x: 1, y: 1 }, it.position);
        assert_eq!(0, it.count);
    }

    #[test]
    fn test_a_neighbours_iterator() {
        let position = Coordinate { x: 0, y: 0 };
        let expected: HashSet<Coordinate> = vec![
            Coordinate { x: -1, y: 1 },  // upper left corner
            Coordinate { x: 0, y: 1 },   // above
            Coordinate { x: 1, y: 1 },   // upper right corner
            Coordinate { x: 1, y: 0 },   // to the right
            Coordinate { x: 1, y: -1 },  // lower right corner
            Coordinate { x: 0, y: -1 },  // below
            Coordinate { x: -1, y: -1 }, // lower left corner
            Coordinate { x: -1, y: 0 },  // to the left
        ]
        .into_iter()
        .collect();

        let actual: HashSet<Coordinate> = NeighboursIterator::new(position).collect();
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_from_for_liveliness() {
        assert_eq!(true, Liveliness::Alive.into());
        assert_eq!(Liveliness::Alive, Liveliness::from(true));
        assert_eq!(false, Liveliness::Dead.into());
        assert_eq!(Liveliness::Dead, Liveliness::from(false));
    }

    fn generate_neighbours(alive: usize) -> Vec<Cell> {
        const MAX_NEIGHBOURS: usize = 8;
        let mut neighbours: Vec<Cell> = Vec::new();
        (0..alive).into_iter().for_each(|_| {
            neighbours.push(Cell {
                is_alive: Liveliness::Alive,
            })
        });
        (alive..MAX_NEIGHBOURS).into_iter().for_each(|_| {
            neighbours.push(Cell {
                is_alive: Liveliness::Dead,
            })
        });
        neighbours
    }

    #[test]
    fn gol_rule_1_underpopulation() {
        let cell = Cell {
            is_alive: Liveliness::Alive,
        };
        let neighbours = generate_neighbours(1);

        assert_eq!(
            Liveliness::Dead,
            cell.next_generation_state(neighbours.as_slice().iter())
        );
    }

    #[test]
    fn gol_rule_2_survivor() {
        let cell = Cell {
            is_alive: Liveliness::Alive,
        };
        let two_alive_neighbours = generate_neighbours(2);
        let three_alive_neighbours = generate_neighbours(3);

        assert_eq!(
            Liveliness::Alive,
            cell.next_generation_state(two_alive_neighbours.as_slice().iter())
        );
        assert_eq!(
            Liveliness::Alive,
            cell.next_generation_state(three_alive_neighbours.as_slice().iter())
        );
    }

    #[test]
    fn gol_rule_3_overpopulation() {
        let cell = Cell {
            is_alive: Liveliness::Alive,
        };
        let four_alive_neighbours = generate_neighbours(4);
        let eight_alive_neighbours = generate_neighbours(8);

        assert_eq!(
            Liveliness::Dead,
            cell.next_generation_state(four_alive_neighbours.as_slice().iter())
        );
        assert_eq!(
            Liveliness::Dead,
            cell.next_generation_state(eight_alive_neighbours.as_slice().iter())
        );
    }

    #[test]
    fn gol_rule_4_dead_cell_comes_alive() {
        let cell = Cell {
            is_alive: Liveliness::Dead,
        };
        let three_alive_neighbours = generate_neighbours(3);

        assert_eq!(
            Liveliness::Alive,
            cell.next_generation_state(three_alive_neighbours.as_slice().iter())
        );
    }
}

