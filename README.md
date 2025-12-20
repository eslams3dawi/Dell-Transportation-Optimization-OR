# 📦 Dell Transportation Optimization (Operation Research)

## 📌 Overview
This project applies **Operation Research transportation models** to optimize the distribution of **Dell electronics products** from manufacturing plants to regional distribution centers across the **EMEA (Europe, Middle East, and Africa) region**. The objective is to **minimize total transportation cost** while satisfying supply and demand constraints.

The project demonstrates and compares three classical transportation approaches:
- **North-West Corner Method**
- **Least Cost Method**
- **Vogel's Approximation Method (VAM)**

---

## 🏢 Business Context

**Dell Technologies** is a Fortune 500 company with annual revenue exceeding $94 billion. The company manufactures computers, servers, storage systems, and networking equipment at 10 global manufacturing facilities serving 180+ countries worldwide.

### Real-World Problem
Dell faces a critical operational challenge in optimizing its European, Middle Eastern, and African (EMEA) distribution network. The current distribution strategy is based on historical patterns and manual decisions, resulting in inefficiencies.

---

## 🏭 Case Study: Dell EMEA Supply Chain

### 🔹 Sources (Manufacturing Plants)

| Manufacturing Facility | Monthly Capacity |
|------------------------|------------------|
| **Dell Łódź, Poland** | 2,500 units/month |
| **Dell Penang, Malaysia** | 1,800 units/month |
| **Contract Partner in Turkey** | 1,200 units/month |
| **Total Available Supply** | **5,500 units/month** |

### 🔹 Destinations (Distribution Centers)

| Distribution Center | Monthly Demand |
|---------------------|----------------|
| **Central European DC (Germany)** | 1,500 units/month |
| **Southern European DC (Spain)** | 1,200 units/month |
| **Northern European DC (Scandinavia)** | 1,000 units/month |
| **Middle East/Africa DC (Dubai)** | 800 units/month |
| **Total Demand** | **4,500 units/month** |

### 💰 Transportation Cost Matrix ($ per unit)

| From / To | Germany DC | Spain DC | Scandinavia DC | Dubai DC |
|-----------|------------|----------|----------------|----------|
| **Łódź, Poland** | $12 | $15 | $18 | $35 |
| **Penang, Malaysia** | $45 | $48 | $52 | $28 |
| **Turkey Factory** | $8 | $12 | $20 | $32 |

**Key Characteristics:**
- Varying transportation costs based on distance, mode, and logistics networks
- Production capacity constraints at each facility
- Specific demand requirements at each distribution center
- Products: Desktop computers, laptops, and components

---

## 🎯 Objective
- **Minimize the total transportation cost**
- Satisfy all supply and demand constraints
- Compare solution quality across different transportation methods

---

## 🚛 Transportation Methods Used

### 1️⃣ North-West Corner Method
- Simple initial feasible solution
- Does not consider transportation costs
- Used as a baseline for comparison
- **Complexity:** Very Low
- **Cost Quality:** High Cost

### 2️⃣ Least Cost Method
- Allocates shipments starting from the lowest transportation cost
- Produces better results than North-West Corner
- **Complexity:** Low
- **Cost Quality:** Medium Cost

### 3️⃣ Vogel's Approximation Method (VAM)
- Uses penalty costs to guide allocation
- Produces solutions close to the optimal solution
- **Complexity:** Medium
- **Cost Quality:** Lowest Cost (Best)

---

## 📊 Comparison Criteria

| Method | Cost Quality | Complexity | Description |
|--------|-------------|------------|-------------|
| **North-West Corner** | High Cost | Very Low | Baseline method, ignores costs |
| **Least Cost** | Medium Cost | Low | Cost-aware allocation |
| **Vogel's Approximation** | Lowest Cost | Medium | Penalty-based optimization |

**Conclusion:** The Vogel Approximation Method typically provides the best cost solution for Dell's EMEA distribution network, achieving substantial savings through optimized allocation of resources.

---

## 🧮 Mathematical Model

### Decision Variables

Let $x_{ij}$ = Units shipped from source $i$ to destination $j$

**Specific Variables:**
- $x_{11}$ = Units shipped from Łódź to Germany DC
- $x_{12}$ = Units shipped from Łódź to Spain DC
- $x_{13}$ = Units shipped from Łódź to Scandinavia DC
- $x_{14}$ = Units shipped from Łódź to Dubai DC
- $x_{21}$ = Units shipped from Penang to Germany DC
- $x_{22}$ = Units shipped from Penang to Spain DC
- $x_{23}$ = Units shipped from Penang to Scandinavia DC
- $x_{24}$ = Units shipped from Penang to Dubai DC
- $x_{31}$ = Units shipped from Turkey to Germany DC
- $x_{32}$ = Units shipped from Turkey to Spain DC
- $x_{33}$ = Units shipped from Turkey to Scandinavia DC
- $x_{34}$ = Units shipped from Turkey to Dubai DC

### Objective Function

**Minimize Total Transportation Cost:**

$$\min Z = 12x_{11} + 15x_{12} + 18x_{13} + 35x_{14} + 45x_{21} + 48x_{22} + 52x_{23} + 28x_{24} + 8x_{31} + 12x_{32} + 20x_{33} + 32x_{34}$$

### Constraints

**Supply Constraints:**
- Łódź Facility: $x_{11} + x_{12} + x_{13} + x_{14} \leq 2500$
- Penang Facility: $x_{21} + x_{22} + x_{23} + x_{24} \leq 1800$
- Turkey Factory: $x_{31} + x_{32} + x_{33} + x_{34} \leq 1200$

**Demand Constraints:**
- Germany DC: $x_{11} + x_{21} + x_{31} = 1500$
- Spain DC: $x_{12} + x_{22} + x_{32} = 1200$
- Scandinavia DC: $x_{13} + x_{23} + x_{33} = 1000$
- Dubai DC: $x_{14} + x_{24} + x_{34} = 800$

**Non-negativity Constraints:**
$$x_{ij} \geq 0 \quad \forall i, j$$

---

## 🖥️ Implementation

- **Programming Language:** Python
- Transportation algorithms implemented programmatically
- Results printed and compared for all methods
- Both code implementation and website verification used for validation

---

## 📈 Key Findings

The transportation problem is one of the most practical applications of operations research. By comparing three different solution methods (North-West Corner, Least Cost, and Vogel's Approximation Method) using both Python implementation and website verification, the project demonstrates that **algorithmic choice matters significantly**. The **Vogel Approximation Method** provides the best cost solution for Dell's EMEA distribution network, achieving substantial savings through optimized allocation of resources.

---
