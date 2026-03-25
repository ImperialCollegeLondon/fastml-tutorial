import ndjson                    
import os
import sys

# Load report json
PROJECT_NAME = sys.argv[1]
print("Project name:", PROJECT_NAME)

report_file = os.path.join(
    PROJECT_NAME,
    'build',
    'myproject.report.prj',
    'reports',
    'resources',
    'json',
    'summary.ndjson'
)

with open(report_file, "r") as f:
    summary = ndjson.load(f)

# -------------------------
# Summarise report contents
# -------------------------
resource_names = list(filter(lambda x: x["name"] == "Estimated Resource Usage", summary))[0]['columns'][1:-1]
available = list(filter(lambda x: x["name"] == "Available", summary))[0]['data'][:-1]
estimated_resources = list(filter(lambda x: x["name"] == "Total", summary))[0]['data'][:-1]

print("~~~~~~~~~~~~~~ Resource usage ~~~~~~~~~~~~~~")
for i, resource in enumerate(resource_names):
    print(f"--> {resource}:")
    print(f"      * Available resource: {available[i]}")
    print(f"      * Used resource (estimated): {estimated_resources[i]}")
    print(f"      * Percentage of used resource (estimated): {100*float(estimated_resources[i])/float(available[i]):.2f}%")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
