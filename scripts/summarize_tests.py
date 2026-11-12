import glob
import os
import xml.etree.ElementTree as ET

rows = []
for path in sorted(glob.glob("test-results/*/juniy.xml")):
    version = path.split("/")[1].replace("test-results-", "")
    root = ET.parse(path).getroot() 
    suite = root.find("testsuite") if root.tag == "testsuites" else root

    total = int(suite.get("tests"))
    failed = int(suite.get("failures")) + int(suite.get("errors"))
    skipped = int(suite.get("skipped"))
    passed = total - failed - skipped
    rows.append(f"| {version} | {total} | {passed} | {failed} | {skipped} |")

with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
    f.write("## Test results\n\n")
    f.write("| Total | Passed | Failed | Skipped |\n")
    f.write("|---|---|---|---|\n")
    f.write("\n".join(rows) + "\n")

print(f"summarized {len(rows)} test reports")