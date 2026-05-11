from data_governance.data_quality import DataQualityChecker

# checker = DataQualityChecker("scores.db") # Hardcoding
checker = DataQualityChecker()
checker.load_rules_from_yaml("data_governance/quality_rules.yaml")  # Load rules from YAML instead
results = checker.run_all_checks()
print(f"✅ Ran {len(results)} quality checks")

for res in results:
    print(f"Rule: {res.rule_name}")
    print(f"Passed: {res.passed}")
    print(f"Score: {res.score:.2%}")
    print(f"Message: {res.message}\n")
