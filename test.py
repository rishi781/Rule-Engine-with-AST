import requests

BASE_URL = "http://127.0.0.1:5000"


def test_create_rule():
    rule_data = {
        "rule": "age > 30 and department == 'Sales'",
        "name": "rule1"
    }
    response = requests.post(f"{BASE_URL}/create_rule", json=rule_data)
    print("Create Rule Response:", response.json())


def test_combine_rules():
    rule_data1 = {
        "rule": "age > 30 and department == 'Sales'",
        "name": "rule1"
    }
    rule_data2 = {
        "rule": "age < 25 and department == 'Marketing'",
        "name": "rule2"
    }

    requests.post(f"{BASE_URL}/create_rule", json=rule_data1)
    requests.post(f"{BASE_URL}/create_rule", json=rule_data2)

    combine_data = {
        "rules": ["rule1", "rule2"]
    }
    response = requests.post(f"{BASE_URL}/combine_rules", json=combine_data)
    print("Combine Rules Response:", response.json())


def test_evaluate_rule():
    test_data = {
        "rule": "rule1",
        "data": {
            "age": 35,
            "department": "Sales",
            "salary": 60000,
            "experience": 3
        }
    }
    response = requests.post(f"{BASE_URL}/evaluate_rule", json=test_data)
    print("Evaluate Rule Response:", response.json())


if __name__ == "__main__":
    test_create_rule()
    test_combine_rules()
    test_evaluate_rule()
