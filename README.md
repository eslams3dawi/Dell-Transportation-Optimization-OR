# 📦 Dell Transportation Optimization (Operation Research)

## 📌 Overview
This project applies **Operation Research transportation models** to optimize the distribution of **Dell electronics products** from manufacturing plants to regional distribution centers.  
The objective is to **minimize total transportation cost** while satisfying supply and demand constraints.

The project demonstrates and compares three classical transportation approaches:
- **North-West Corner Method**
- **Least Cost Method**
- **Vogel’s Approximation Method (VAM)**

---

## 🏭 Case Study: Dell Electronics Supply Chain

### 🔹 Sources (Manufacturing Plants)
- Lodz, Poland  
- Penang, Malaysia  
- Turkey Factory  

### 🔹 Destinations (Distribution Centers)
- Germany DC  
- Spain DC  
- Scandinavia DC  
- Dubai DC  

Each source has a fixed **supply capacity**, and each destination has a specific **demand requirement**.

---

## 🎯 Objective
- Minimize the **total transportation cost**
- Satisfy all supply and demand constraints
- Compare solution quality across different transportation methods

---

## 🚛 Transportation Methods Used

### 1️⃣ North-West Corner Method
- Simple initial feasible solution
- Does not consider transportation costs
- Used as a baseline for comparison

### 2️⃣ Least Cost Method
- Allocates shipments starting from the lowest transportation cost
- Produces better results than North-West Corner

### 3️⃣ Vogel’s Approximation Method (VAM)
- Uses penalty costs to guide allocation
- Produces solutions close to the optimal solution

---

## 📊 Comparison Criteria
- Total transportation cost  
- Solution efficiency  
- Method complexity  

| Method | Cost Quality | Complexity |
|------|-------------|------------|
| North-West Corner | High Cost | Very Low |
| Least Cost | Medium Cost | Low |
| Vogel’s Approximation | Lowest Cost | Medium |

---

## 🧮 Mathematical Model

### Decision Variable
\[
x_{ij} = \text{Units transported from source } i \text{ to destination } j
\]

### Objective Function
\[
\min Z = \sum_i \sum_j c_{ij} x_{ij}
\]

### Constraints
- Supply constraints  
- Demand constraints  
- Non-negativity constraints  

---

## 🖥️ Implementation
- Programming Language: **Python**
- Transportation algorithms implemented programmatically
- Results printed and compared for all methods

---
