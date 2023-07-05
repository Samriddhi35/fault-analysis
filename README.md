# fault-analysis 
### Author : Samriddhi Sharma

Solution to the problem statement

 - The task is to design an algorithm and write its code to identify the input vector required to identify the fault at a
given node in a given circuit.
1. In the given solution  we mapped every node to its operation.
2. Identified the required value to validate the fault for stuck-at-fault node.
3. Traced back the node graph backwards to reach the inputs.
   Inshort, the solution uses depth-first search to solve the given problem statement in O(n)  time complexity .

### instructions to run the code

1. Paste the circuit in circuit.txt
2. Paste the fault in fault.txt
3. python3 code.py
