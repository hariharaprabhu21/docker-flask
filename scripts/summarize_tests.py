import os
import xml.etree.ElementTree as ET

root = ET.parse("test-results/junit.xml").getroot()
suite = root.find("testsuite") if root.tag == "testsuites" else root

total = int(suite.get("tests"))
failed = int(suite.get("failures")) + int(suite.get("errors"))
skipped = int(suite.get("skipped"))
passed = total - failed - skipped

with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
    f.write("## Test results\n\n")
    f.write("| Total | Passed | Failed | Skipped |\n")
    f.write("|---|---|---|---|\n")
    f.write(f"| {total} | {passed} | {failed} | {skipped} |\n")

print(f"{passed}/{total} tests passed")