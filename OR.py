# Transportation Problem Solver - Pure Logic with Terminal Output
# Uses tabulate library for clean tables

from typing import List, Tuple  # List and Tuple are "hints" telling us what data types to expect
from tabulate import tabulate  # Library that makes pretty tables in terminal

# These are "nicknames" for complex data types to make code easier to read
CostMatrix = List[List[float]]  # A list of lists containing numbers (costs)
Vector = List[int]              # A simple list of whole numbers (supply/demand)

class TransportationSolver:
    """
    MAIN CLASS: This is like a "smart calculator" that solves transportation problems
    It knows how to balance supply/demand and use 3 different methods
    """
    
    def __init__(
        self,
        cost_matrix: CostMatrix,  # 2D list: costs from each source to each destination
        supply: Vector,           # 1D list: how much each source has available
        demand: Vector            # 1D list: how much each destination needs
    ):
        """
        CONSTRUCTOR: This runs automatically when you create a solver
        Purpose: Store the input data safely and prepare everything
        """
        # self.cost_matrix = [row[:] for row in cost_matrix]
        # ?? EXPLANATION: Makes a DEEP COPY of the cost matrix
        # Why? So if we change costs later, original data stays safe
        # row[:] means "copy this row", [row[:] for row in...] means "copy every row"
        self.cost_matrix = [row[:] for row in cost_matrix]
        
        # self.supply = supply[:] and self.demand = demand[:]
        # Makes SHALLOW copies of supply and demand lists
        # [:] means "copy the entire list" - protects original data
        self.supply = supply[:]
        self.demand = demand[:]

        # Count number of sources (rows) and destinations (columns)
        self.m = len(self.supply)  # m = number of sources/supply points
        self.n = len(self.demand)  # n = number of destinations/demand points
        
        # Calculate totals for balancing check
        self.total_supply = sum(self.supply)   # Total available supply
        self.total_demand = sum(self.demand)   # Total required demand

        # Track if we added a dummy row/column later
        self.dummy_type = None  # Will be "supply" or "demand" if needed
        
        # Automatically balance the problem (add dummy if needed)
        self._balance_problem()

    def _balance_problem(self) -> None:
        """
        HELPER FUNCTION: Makes sure supply = demand by adding "dummy" rows/columns
        Purpose: Transportation math only works when total supply equals total demand
        Returns: Nothing (None) - just modifies the data in place
        """
        # Case 1: Too much supply (supply > demand)
        if self.total_supply > self.total_demand:
            diff = self.total_supply - self.total_demand  # How much extra supply?
            
            # Add dummy demand (fake destination that "absorbs" extra supply)
            self.demand.append(diff)  # Add extra demand value to demand list [1, 2 , 3, 4]
            
            # Add column of zeros to cost matrix (shipping to dummy = free)
            for row in self.cost_matrix:
                row.append(0)  # Each source gets a free route to dummy
            
            self.dummy_type = "demand"  # Remember we added dummy demand
            self.n += 1  # One more destination now #####
        
        # Case 2: Too much demand (demand > supply)
        elif self.total_supply < self.total_demand:
            diff = self.total_demand - self.total_supply  # How much extra demand?
            
            # Add dummy supply (fake source that provides extra supply)
            self.supply.append(diff)  # Add extra supply value
            
            # Add row of zeros to cost matrix (dummy source ships free)
            self.cost_matrix.append([0] * self.n)  # New row with n zeros #####
            
            self.dummy_type = "supply"  # Remember we added dummy supply
            self.m += 1  # One more source now

    def _make_headers(self) -> List[str]:
        """
        HELPER FUNCTION: Creates column headers for all tables
        Purpose: Makes consistent headers like "D1", "D2*", "Supply"
        Returns: List of strings (the headers)
        Note: * marks dummy columns
        """
        headers = [""]  # Empty first column for row labels (S1, S2, etc)
        
        # Create destination headers (D1, D2, D3, D4)
        for j in range(self.n):
            # Check if this is the dummy column (last column if dummy demand)
            is_dummy = (
                self.dummy_type == "demand" and j == self.n - 1
            )
            header = f"D{j+1}"  # "D1", "D2", etc
            if is_dummy:
                header += "*"     # Mark dummy with *
            headers.append(header)
        
        headers.append("Supply")  # Last column header
        return headers

    def _print_initial_table(self) -> None:
        """
        HELPER FUNCTION: Prints the starting problem with all costs
        Purpose: Shows the original problem setup clearly
        What it shows:
        - Costs from each source to each destination
        - Original supply and demand amounts
        """
        print("\n=== INITIAL PROBLEM TABLE (Costs) ===\n")
        
        headers = self._make_headers()  # Get headers (D1, D2, D3, D4, Supply)
        data = []  # List to hold all table rows
        
        # Add rows for each source (S1, S2, S3)
        for i in range(self.m):
            row = [f"S{i+1}"]  # Row label "S1", "S2", etc
            
            # Add cost for each destination ($12, $15, etc)
            for j in range(self.n):
                row.append(f"${int(self.cost_matrix[i][j])}")
            
            # Add supply amount for this source
            row.append(int(self.supply[i]))
            data.append(row)
        
        # Demand row (bottom row)
        dem_row = ["Demand"]  # Row label
        for mahoun in range(self.n):
            dem_row.append(int(self.demand[j]))  # Demand for each destination
        dem_row.append(int(self.total_supply))  # Total supply in last column
        data.append(dem_row)
        
        # Print beautiful table using tabulate library
        print(tabulate(data, headers=headers, tablefmt="grid"))
        
        # Show if we added dummy
        if self.dummy_type:
            msg = f"Dummy {self.dummy_type} added for balancing\n"
            print(msg)

    def _print_step_table(
        self,
        step_no: int,      # Current step number (1, 2, 3...)
        method: str,       # "NWC", "LCM", or "VAM"
        alloc: List[List[int]],  # Current allocation matrix (how much shipped where) #######
        s_left: Vector,    # ?? REMAINING supply after this step
        d_left: Vector,    # ?? REMAINING demand after this step
    ) -> None:
        """
        HELPER FUNCTION: Prints table showing current progress
        Purpose: Shows what we've allocated so far + remaining supply/demand
        Key feature: Shows "12×300" for allocated cells, "−" for empty cells
        """
        print(f"Step {step_no} - {method}\n")
        
        headers = self._make_headers()
        data = []
        
        # Source rows with current allocations
        for i in range(self.m):
            row = [f"S{i+1}"]
            for j in range(self.n):
                if alloc[i][j] > 0:  # If we've allocated something here ######
                    c = int(self.cost_matrix[i][j])  # Cost per unit
                    q = int(alloc[i][j])             # Quantity allocated
                    cell = f"{c}×{q}"                # "12×300" format
                else:
                    cell = "−"                       # Empty cell
                row.append(cell)
            row.append(int(s_left[i]))  # Remaining supply for this source
            data.append(row)
        
        # Demand row with remaining demand
        dem_row = ["Demand"]
        for j in range(self.n):
            dem_row.append(int(d_left[j]))  # Remaining demand
        dem_row.append("")  # Empty last column
        data.append(dem_row)
        
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print()

    def _print_final_allocation(
        self,
        alloc: List[List[int]]  # Final allocation matrix
    ) -> None:
        """
        HELPER FUNCTION: Prints FINAL results matrix (no supply column needed)
        Purpose: Clean final view of all allocations made
        Note: Removes "Supply" column since we're done allocating
        """
        print("=== Final Allocation Matrix ===\n")
        
        # Remove Supply column from headers
        headers = self._make_headers()[:-1]  
        data = []
        
        for i in range(self.m):
            row = [f"S{i+1}"]
            for j in range(self.n):
                if alloc[i][j] > 0:
                    c = int(self.cost_matrix[i][j])
                    q = int(alloc[i][j])
                    cell = f"{c}×{q}"
                else:
                    cell = "−"
                row.append(cell)
            data.append(row)
        
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print()

    def _print_cost_equation(
        self,
        alloc: List[List[int]]  # Allocation matrix to calculate from
    ) -> float:
        """
        HELPER FUNCTION: Creates and prints the final cost equation
        Purpose: Shows "total transportation cost = 12×300+15×1200...=106600"
        Returns: Total cost as a number
        Important: Ignores dummy allocations (they cost $0)
        """
        terms = []  # List to hold cost terms like "12×300"
        total = 0.0  # Running total cost
        
        # Check every possible source-destination pair
        for i in range(self.m):
            for j in range(self.n):
                q = alloc[i][j]  # Quantity allocated here
                
                # Skip dummy column allocations (cost = 0 anyway)
                is_dummy = (
                    self.dummy_type == "demand" and j == self.n - 1
                )
                if q > 0 and not is_dummy:  # Only real allocations
                    c = int(self.cost_matrix[i][j])
                    terms.append(f"{c}×{int(q)}")  # Add term like "12×300"
                    total += c * q                  # Add to running total
        
        # Build equation string
        equation = "total transportation cost = "
        equation += "+".join(terms)  # Join terms: "12×300+15×1200+..."
        equation += f"={int(total)}"
        
        print(equation)
        print()
        return total

    def solve_nwc(self) -> None:
        """
        MAIN METHOD 1: North-West Corner Method
        Algorithm: Start at top-left corner, allocate, move right/down
        Like reading a book: left-to-right, top-to-bottom
        """
        print("\n" + "=" * 70)
        print("METHOD: NORTH-WEST CORNER (NWC)")
        print("=" * 70)
        
        self._print_initial_table()  # Show starting problem
        
        # Create empty allocation matrix (all zeros initially)
        alloc = [[0] * self.n for _ in range(self.m)]
        
        # Working copies of supply/demand (these get modified)
        s = self.supply[:]
        d = self.demand[:]
        
        i = j = 0  # Start at top-left corner (row 0, column 0)
        step = 1   # Step counter

        # Continue until all supply or all demand is used
        while i < self.m and j < self.n:
            x = min(s[i], d[j])  # Allocate minimum of available supply/demand
            
            alloc[i][j] = x      # Record allocation
            s[i] -= x            # Reduce remaining supply
            d[j] -= x            # Reduce remaining demand
            
            cost = int(self.cost_matrix[i][j])
            print(
                f"Allocate {int(x)} units to S{i+1}→D{j+1} "
                f"(cost: ${cost}/unit)\n"
            )
            
            # Show current progress
            self._print_step_table(step, "NWC", alloc, s, d)
            step += 1

            # Decide where to move next:
            if s[i] == 0 and d[j] == 0:  # Both exhausted
                if j + 1 < self.n:
                    j += 1  # Move right
                else:
                    i += 1  # Move down
            elif s[i] == 0:              # Current row exhausted
                i += 1                    # Move down
            elif d[j] == 0:              # Current column exhausted
                j += 1                    # Move right

        # Show final results
        self._print_final_allocation(alloc)
        self._print_cost_equation(alloc)

    def _find_min_cost(
        self,
        s: Vector,           # Current remaining supply
        d: Vector,           # Current remaining demand
        exclude_col: int = -1  # Column to ignore (-1 = none)
    ) -> Tuple[int, int, float]:
        """
        HELPER FUNCTION: Finds cheapest available cell for Least Cost method
        Scans all cells, skips exhausted rows/columns and excluded columns
        Returns: (row_index, col_index, min_cost_value)
        """
        min_cost = float("inf")  # Start with impossibly high cost
        min_i = min_j = -1       # Track best row/column
        
        # Check every possible cell
        for i in range(self.m):
            if s[i] == 0:  # Skip exhausted rows
                continue
            for j in range(self.n):
                # Skip exhausted columns or excluded column
                if d[j] == 0 or j == exclude_col:
                    continue
                c = self.cost_matrix[i][j]
                if c < min_cost:  # Found cheaper cell!
                    min_cost, min_i, min_j = c, i, j
        
        return min_i, min_j, min_cost

    def solve_least_cost(self) -> None:
        """
        MAIN METHOD 2: Least Cost Method (Greedy approach)
        Algorithm: Always pick the cheapest available cell until done
        """
        print("\n" + "=" * 70)
        print("METHOD: LEAST COST METHOD (LCM)")
        print("=" * 70)
        
        self._print_initial_table()
        
        alloc = [[0] * self.n for _ in range(self.m)]
        s = self.supply[:]
        d = self.demand[:]
        step = 1

        # Identify dummy column if it exists
        dummy_col = (
            self.n - 1 if self.dummy_type == "demand" else -1
        )

        # Allocate to real destinations first (ignore dummy)
        while any(
            d[j] > 0
            for j in range(self.n - (1 if dummy_col >= 0 else 0))
        ):
            i, j, c = self._find_min_cost(s, d, exclude_col=dummy_col)
            if i == -1:  # No more real allocations possible
                break
            
            x = min(s[i], d[j])
            alloc[i][j] = x
            s[i] -= x
            d[j] -= x
            
            print(
                f"Min cost: S{i+1}→D{j+1} (${int(c)}), "
                f"allocate {int(x)} units\n"
            )
            self._print_step_table(step, "LCM", alloc, s, d)
            step += 1

        # Handle dummy column allocations (remaining supply)
        if dummy_col >= 0:
            for i in range(self.m):
                if s[i] > 0 and d[dummy_col] > 0:
                    x = min(s[i], d[dummy_col])
                    alloc[i][dummy_col] = x
                    s[i] -= x
                    d[dummy_col] -= x
                    
                    print(
                        f"Allocate remaining {int(x)} units "
                        f"from S{i+1} to dummy D{dummy_col+1}\n"
                    )
                    self._print_step_table(step, "LCM", alloc, s, d)
                    step += 1

        self._print_final_allocation(alloc)
        self._print_cost_equation(alloc)

    def solve_vam(self) -> None:
        """
        MAIN METHOD 3: Vogel's Approximation Method (Smartest method)
        Algorithm: 
        1. Calculate "penalties" (cost of NOT choosing best option)
        2. Pick row/column with highest penalty
        3. Allocate to cheapest cell in that row/column
        4. Repeat until done
        """
        print("\n" + "=" * 70)
        print("METHOD: VOGEL'S APPROXIMATION (VAM)")
        print("=" * 70)
        
        self._print_initial_table()
        
        alloc = [[0] * self.n for _ in range(self.m)]
        s = self.supply[:]
        d = self.demand[:]
        
        # Track which rows/columns still have supply/demand
        active_rows = [True] * self.m
        active_cols = [True] * self.n
        step = 1

        # Continue while both supply and demand remain
        while (
            any(s[i] > 0 and active_rows[i] for i in range(self.m))
            and
            any(d[j] > 0 and active_cols[j] for j in range(self.n))
        ):
            # === STEP 1: Calculate row penalties ===
            row_pen = [-1] * self.m  # Penalty scores for each row
            for i in range(self.m):
                if not active_rows[i] or s[i] == 0:
                    continue  # Skip exhausted rows
                costs = [
                    self.cost_matrix[i][j]
                    for j in range(self.n)
                    if active_cols[j] and d[j] > 0
                ]
                if len(costs) >= 2:
                    costs.sort()           # Sort costs: [8, 12, 20] -> smallest first
                    row_pen[i] = costs[1] - costs[0]  # Penalty = 2nd smallest - smallest
                elif len(costs) == 1:
                    row_pen[i] = 0         # Only 1 option = no penalty

            # === STEP 2: Calculate column penalties ===
            col_pen = [-1] * self.n
            for j in range(self.n):
                if not active_cols[j] or d[j] == 0:
                    continue
                costs = [
                    self.cost_matrix[i][j]
                    for i in range(self.m)
                    if active_rows[i] and s[i] > 0
                ]
                if len(costs) >= 2:
                    costs.sort()
                    col_pen[j] = costs[1] - costs[0]
                elif len(costs) == 1:
                    col_pen[j] = 0

            # === STEP 3: Find maximum penalty ===
            max_pen = -1
            is_row = True
            idx = -1
            
            # Check all row penalties
            for i in range(self.m):
                if row_pen[i] > max_pen:
                    max_pen, is_row, idx = row_pen[i], True, i
            
            # Check all column penalties (can override row)
            for j in range(self.n):
                if col_pen[j] > max_pen:
                    max_pen, is_row, idx = col_pen[j], False, j

            if idx == -1:  # No penalties found (problem solved)
                break

            # === STEP 4: Find minimum cost in selected row/column ===
            min_cost = float("inf")
            min_i = min_j = -1

            if is_row:  # Penalty was in a row
                i = idx
                for j in range(self.n):
                    if (
                        active_cols[j]
                        and d[j] > 0
                        and self.cost_matrix[i][j] < min_cost
                    ):
                        min_cost = self.cost_matrix[i][j]
                        min_i = i
                        min_j = j
            else:       # Penalty was in a column
                j = idx
                for i in range(self.m):
                    if (
                        active_rows[i]
                        and s[i] > 0
                        and self.cost_matrix[i][j] < min_cost
                    ):
                        min_cost = self.cost_matrix[i][j]
                        min_i = i
                        min_j = j

            if min_i == -1:  # No valid cell found
                break

            # === STEP 5: Make allocation ===
            x = min(s[min_i], d[min_j])
            alloc[min_i][min_j] = x
            s[min_i] -= x
            d[min_j] -= x

            # Mark exhausted rows/columns
            if s[min_i] == 0:
                active_rows[min_i] = False
            if d[min_j] == 0:
                active_cols[min_j] = False

            # Show progress
            which = "row" if is_row else "column"
            print(
                f"Max penalty {int(max_pen)} on {which} {idx+1}, "
                f"allocate {int(x)} to S{min_i+1}→D{min_j+1}\n"
            )
            self._print_step_table(step, "VAM", alloc, s, d)
            step += 1

        self._print_final_allocation(alloc)
        self._print_cost_equation(alloc)


# MAIN PROGRAM: This runs when you execute the file
if __name__ == "__main__":
    """
    ENTRY POINT: Creates example data and lets user choose method
    This is like the "start button" of the program
    """
    # Fixed example data (3 sources, 4 destinations)
    cost_matrix = [
        [12, 15, 18, 35],  # S1 costs to D1, D2, D3, D4
        [35, 48, 52, 28],  # S2 costs
        [8,  12, 20, 32],  # S3 costs
    ]
    supply = [2500, 1800, 1200]  # S1, S2, S3 available amounts
    demand = [1500, 1200, 1000, 800]  # D1, D2, D3, D4 required amounts

    # Create the solver with our data
    solver = TransportationSolver(cost_matrix, supply, demand)

    # Ask user which method to use
    print("\nChoose method:")
    print("  1) North-West Corner")
    print("  2) Least Cost Method")
    print("  3) Vogel Approximation")
    choice = input("\nEnter 1, 2, or 3: ").strip()  # .strip() removes spaces
    
    # Run selected method
    if choice == "1":
        solver.solve_nwc()
    elif choice == "2":
        solver.solve_least_cost()
    elif choice == "3":
        solver.solve_vam()
    else:
        print("Invalid choice")
