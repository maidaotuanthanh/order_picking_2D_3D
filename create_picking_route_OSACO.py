from distance_picking import DistanceCalculator
from next_location import LocationSelector
import random


class RouteCalculator:
    def __init__(self, y_low, y_high, num_ants=50, max_iterations=300):
        self.location_selector = LocationSelector(y_low, y_high)
        self.distance_calculator = DistanceCalculator(y_low, y_high)
        self.num_ants = num_ants
        self.max_iterations = max_iterations
        # Initialize parameters for OSACO (these can be tuned or optimized)
        self.alpha = 2.0  # Influence of pheromone
        self.beta = 5.0  # Influence of heuristic value (1/distan ce)
        self.rho = 0.1  # Pheromone evaporation rate
        self.Q = 100  # Pheromone deposit factor

    def initialize_ants(self, num_nodes):
        """Initialize ants and pheromone matrix."""
        ants = [random.randint(0, num_nodes - 1) for _ in range(self.num_ants)]
        pheromone = [[1 for _ in range(num_nodes)] for _ in range(num_nodes)]
        return ants, pheromone

    def probability(self, pheromone, visibility, alpha, beta):
        """Calculate the probability of moving to a node."""
        return (pheromone ** alpha) * (visibility ** beta)

    def update_pheromones(self, pheromone, best_path):
        """Update pheromones globally with reward mechanism."""
        # Evaporation
        for i in range(len(pheromone)):
            for j in range(len(pheromone[i])):
                pheromone[i][j] *= (1 - self.rho)

        # Global pheromone update (only reward the best path)
        for i in range(len(best_path) - 1):
            # best_path[i] and best_path[i + 1] are now indices, not tuples
            pheromone[best_path[i]][best_path[i + 1]] += self.Q / self.calculate_total_distance(
                [self.all_locs[idx] for idx in best_path]
            )

    def ant_colony_optimization(self, origin_loc, list_locs):
        """Implement the Optimal Sequential Ant Colony Optimization (OSACO) algorithm."""
        # Include origin location in the list of all locations
        self.all_locs = [origin_loc] + list_locs  # Ensure origin_loc and list_locs are tuples/lists
        num_nodes = len(self.all_locs)  # Number of nodes including origin
        ants, pheromone = self.initialize_ants(num_nodes)
        best_path = None
        best_distance = float('inf')

        for iteration in range(self.max_iterations):
            ants_paths = []
            for ant in ants:
                # Construct a solution for each ant
                unvisited = list(range(num_nodes))
                unvisited.remove(ant)
                path = [ant]

                while unvisited:
                    current_node_index = path[-1]  # This is an index
                    current_node = self.all_locs[current_node_index]  # Convert index to coordinate

                    # Prepare visibility list using actual coordinates
                    visibility = [
                        1 / self.distance_calculator.distance_picking(
                            current_node, self.all_locs[next_node_index]  # Convert index to coordinate
                        )
                        for next_node_index in unvisited
                    ]

                    # Calculate probabilities for the next move
                    probabilities = [
                        self.probability(pheromone[current_node_index][next_node_index], visibility[idx], self.alpha,
                                         self.beta)
                        for idx, next_node_index in enumerate(unvisited)
                    ]
                    total_prob = sum(probabilities)
                    probabilities = [p / total_prob for p in probabilities]

                    # Choose next node based on calculated probabilities
                    next_node_index = random.choices(unvisited, weights=probabilities)[0]
                    path.append(next_node_index)
                    unvisited.remove(next_node_index)

                # Complete the route back to the start
                path.append(ant)
                ants_paths.append(path)

                # Evaluate the solution using actual coordinates
                current_distance = self.calculate_total_distance([self.all_locs[idx] for idx in path])
                if current_distance < best_distance:
                    best_distance = current_distance
                    best_path = path  # Store the path as indices

            # Update pheromones with best path
            self.update_pheromones(pheromone, best_path)

        # Return results with coordinates instead of indices
        optimized_route = [self.all_locs[idx] for idx in best_path]
        return best_distance, optimized_route

    def calculate_total_distance(self, route):
        total_distance = 0
        for i in range(len(route) - 1):
            # Use route directly, as it already contains coordinates
            total_distance += self.distance_calculator.distance_picking(route[i], route[i + 1])
        return total_distance

    def create_picking_route(self, origin_loc, list_locs):
        total_distance, optimized_route = self.ant_colony_optimization(origin_loc, list_locs)
        return total_distance, optimized_route
