import sqlite3

with sqlite3.connect('concrete.db') as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("ALL TESTS")
    cursor.execute("""
        SELECT project_name, actual_strength, passed
        FROM concrete_tests
        ORDER BY test_id
    """)
    for test in cursor:
        status = "PASS" if test["passed"] else "FAIL"
        print(f"{test['project_name']}: {test['actual_strength']} PSI - {status}")

    print("\nFAILED TESTS")
    cursor.execute("""
        SELECT project_name, test_date, required_strength, actual_strength
        FROM concrete_tests
        WHERE passed = 0
        ORDER BY test_id
    """)
    for test in cursor:
        print(f"{test['project_name']} on {test['test_date']}")
        print(f"  Required: {test['required_strength']} PSI")
        print(f"  Actual: {test['actual_strength']} PSI")
        print()

    print("TESTS PER PROJECT")
    cursor.execute("""
        SELECT project_name, SUM(passed) AS passing_tests, COUNT(*) AS total_tests
        FROM concrete_tests
        GROUP BY project_name
        ORDER BY project_name
    """)
    for project in cursor:
        print(f"{project['project_name']}: {project['passing_tests']}/{project['total_tests']} passed")
