
import ast

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # 'operator' or 'operand'
        self.value = value  # the condition for operands (e.g., age > 30), and None for operators
        self.left = left  # left child for operators
        self.right = right  # right child for operators

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, left={self.left}, right={self.right})"

class RuleParser:
    operators = {
        ast.And: 'AND',
        ast.Or: 'OR',
        ast.Gt: '>',
        ast.Lt: '<',
        ast.Eq: '==',
    }

    def parse_expression(self, expression):
        tree = ast.parse(expression, mode='eval')
        return self.build_ast(tree.body)
    
    def build_ast(self, node):
        if isinstance(node, ast.BoolOp):
            operator_type = self.operators[type(node.op)]
            left = self.build_ast(node.values[0])
            right = self.build_ast(node.values[1])
            return Node(node_type='operator', value=operator_type, left=left, right=right)
        elif isinstance(node, ast.Compare):
            left = node.left.id  # e.g., 'age'
            op = self.operators[type(node.ops[0])]
            right = node.comparators[0].n  # e.g., 30
            return Node(node_type='operand', value=f"{left} {op} {right}")
        else:
            raise ValueError("Unsupported expression")

def combine_rules(rule_asts):
    if not rule_asts:
        return None
    
    combined_root = rule_asts[0]
    for rule_ast in rule_asts[1:]:
        combined_root = Node(node_type='operator', value='AND', left=combined_root, right=rule_ast)
    
    return combined_root

def evaluate_rule(json_data, node):
    if node.type == 'operand':
        field, op, value = node.value.split()
        if op == '>':
            return json_data[field] > int(value)
        elif op == '<':
            return json_data[field] < int(value)
        elif op == '==':
            return json_data[field] == value.strip("'")
        else:
            return False
    elif node.type == 'operator':
        left_result = evaluate_rule(json_data, node.left)
        right_result = evaluate_rule(json_data, node.right)
        if node.value == 'AND':
            return left_result and right_result
        elif node.value == 'OR':
            return left_result or right_result
    return False
