def find_inputs(node, value, node_map, node_values):
    if node in ['A', 'B', 'C', 'D']:
        node_values[node] = value
        return
    if node_map[node][0] == 'NOT':
        find_inputs(node_map[node][1][0], value^1, node_map, node_values)
    elif node_map[node][0] == '&':
        # If AND gate output required is '1', all inputs should be '1'
        input_val = [value] * len(node_map[node][1])
        # If '0', any one input can be '0'
        if value == 0:
            input_val[0] = 0
        for n, val in zip(node_map[node][1], input_val):
            find_inputs(n, val, node_map, node_values)
    elif node_map[node][0] == '|':
        input_val = [value] * len(node_map[node][1])
        if value == 1:
            input_val[0] = 1  # any input can be '1' to get OR output as '1'
        for n, val in zip(node_map[node][1], input_val):
            find_inputs(n, val, node_map, node_values)
    elif node_map[node][0] == '^':
        if value == 1:  # Any one input can be '1' for XOR output as '1'
            find_inputs(node_map[node][1][0], 1, node_map, node_values)
            find_inputs(node_map[node][1][1], 0, node_map, node_values)
        else:
            find_inputs(node_map[node][1][0], 1, node_map, node_values)
            find_inputs(node_map[node][1][1], 1, node_map, node_values)


def process_circuit_file(file_name):
    node_map = {}
    with open(file_name, 'r') as f:
        for line in f:
            node, operation = line.strip().split(" = ")
            operation_parts = operation.split()
            if len(operation_parts) == 2:
                node_map[node] = ["NOT", [operation_parts[1]]]
            else:
                node_map[node] = [operation_parts[1], [operation_parts[0], operation_parts[2]]]
    return node_map


def process_fault_file(file_name):
    fault_data = {}
    with open(file_name, 'r') as f:
        for line in f:
            key, value = line.strip().split(" = ")
            fault_data[key] = value
    return fault_data


def test_faults(circuit_file, fault_file, output_file):
    node_map = process_circuit_file(circuit_file)
    fault_data = process_fault_file(fault_file)
    fault_node = fault_data['FAULT_AT']
    st_type = fault_data['FAULT_TYPE']
    node_values = {}
    # For the stuck-at-fault node, find the required value to validate the fault
    required_value = 0 if st_type == 'SA0' else 1
    find_inputs(fault_node, required_value, node_map, node_values)
    # Output node 'Z' is added last to evaluate the complete behavior
    find_inputs('Z', required_value, node_map, node_values)
    node_values['Z'] = required_value
    ans = f"[A, B, C, D] = [{node_values['A']}, {node_values['B']}, {node_values['C']}, {node_values['D']}], Z = {required_value}"
    with open(output_file, 'w') as output:
        output.write(ans)
    output.close()

circuit_file = 'circuit.txt'
fault_file = 'fault.txt'
output_file = 'output.txt'
test_faults(circuit_file, fault_file, output_file)