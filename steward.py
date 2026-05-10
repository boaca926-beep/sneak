from data_governance.data_quality import DataQualityChecker

checker = DataQualityChecker("scores.db")
results = checker.run_all_checks()
print(f"✅ Ran {len(results)} quality checks")

result = results[0]
print(f"Rule: {result.rule_name}")
print(f"Passed: {result.passed}")
print(f"Score: {result.score:.2%}")
print(f"Message: {result.message}")
