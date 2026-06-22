import os
import sys

print("="*50)
print("  CIRAS — Cybercrime Investigation & Record Analysis System")
print("  Running Full Analysis Pipeline")
print("="*50)

steps = [
    ("Generating mock data",        "python3 data/mock_data_generator.py"),
    ("CDR Analysis",                "python3 analysis/cdr_analysis.py"),
    ("IMEI Analysis",               "python3 analysis/imei_analysis.py"),
    ("Tower Analysis",              "python3 analysis/tower_analysis.py"),
    ("Graph Builder",               "python3 analysis/graph_builder.py"),
    ("Risk Scoring",                "python3 analysis/risk_scorer.py --with-complaints"),
    ("Network Graph",               "python3 analysis/network_graph.py"),
]

use_mock = '--mock' in sys.argv or len(sys.argv) == 1

if use_mock:
    print("\nMode: Demo (mock data)")
    run_steps = steps
else:
    print("\nMode: Real data (skipping mock data generation)")
    run_steps = steps[1:]

print()
for name, cmd in run_steps:
    print(f">>> {name}...")
    result = os.system(cmd)
    if result != 0:
        print(f"ERROR in {name}. Stopping.")
        sys.exit(1)
    print(f"✓ {name} complete\n")

print("="*50)
print("  Pipeline complete.")
print("  Run: streamlit run dashboard/app.py")
print("="*50)
