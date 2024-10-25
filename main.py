
from flask import Flask, request, jsonify
from app.core.rule_engine import RuleParser, combine_rules, evaluate_rule

app = Flask(__name__)
rule_parser = RuleParser()

rules = {}

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_str = request.json.get('rule')
    rule_name = request.json.get('name')
    ast_rule = rule_parser.parse_expression(rule_str)
    rules[rule_name] = ast_rule
    return jsonify({"message": "Rule created successfully", "rule": str(ast_rule)})

@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    rule_names = request.json.get('rules')
    rule_asts = [rules[name] for name in rule_names]
    combined_rule = combine_rules(rule_asts)
    return jsonify({"message": "Rules combined", "rule": str(combined_rule)})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate():
    data = request.json.get('data')
    rule_name = request.json.get('rule')
    ast_rule = rules[rule_name]
    result = evaluate_rule(data, ast_rule)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
