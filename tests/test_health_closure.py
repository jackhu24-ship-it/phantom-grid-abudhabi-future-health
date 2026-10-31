# -*- coding: utf-8 -*-
"""
PHANToM GRID :: Step 3 Atomic Closure Test Suite for PG-MOD-28 Abu Dhabi Future Health (§3.4.24 Pure ASCII + Rule 83)
"""
import sys
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(MODULE_ROOT))

from src.runner import FutureHealthSovereignRunner


def run_atomic_closure_tests():
    print("[*] Starting PG-MOD-28 (Abu Dhabi Future Health) Step 3 Atomic Closure Gate Verification...")
    runner = FutureHealthSovereignRunner()

    # TEST 1: Bio-Telemetry SRAM Kernel Latency (<= 1.85us)
    r1 = runner.execute_clinical_cycle({"vram_gb": 30.0, "drift_error": 0.05})
    assert r1["latency_us"] <= 1.85, f"TEST 1 FAIL: Latency {r1['latency_us']}us > 1.85us"
    print(f"  [+] TEST 1 PASS: Bio-Telemetry SRAM Kernel Latency = {r1['latency_us']:.2f}us (<= 1.85us)")

    # TEST 2: 50GB VRAM Hard Meltdown Trip
    tripped = False
    try:
        runner.execute_clinical_cycle({"vram_gb": 52.5, "drift_error": 0.05})
    except RuntimeError:
        tripped = True
    assert tripped, "TEST 2 FAIL: VRAM 52.5GB failed to trip E-STOP!"
    print("  [+] TEST 2 PASS: 50GB Global VRAM Meltdown Trip Verified.")

    # TEST 3: Physiological Artifact 1.35x Damping Gate
    r3 = runner.execute_clinical_cycle({"vram_gb": 34.0, "drift_error": 0.34})
    assert r3["damping"] == 1.35 and r3["action"] == "APPLY_ARTIFACT_DAMPING_AND_ALERT"
    print("  [+] TEST 3 PASS: Sensor Drift > 0.25 Triggered 1.35x Damping & Clinical Alert.")

    # TEST 4: HIPAA / ADHICS 2-Pass ZDR Wipe & WORM Receipt
    assert r3["zdr_residual_mb"] == 0.0 and r3["worm_receipt"] == "WORM-HEALTH-ABUDHABI-6F8E2A1C"
    print(f"  [+] TEST 4 PASS: 2-Pass PHI ZDR Purge (0.00MB) & Receipt: {r3['worm_receipt']}")

    print("\n[ ALL 4 ATOMIC CLOSURE TESTS PASSED - PRODUCTION READY ]")


if __name__ == "__main__":
    run_atomic_closure_tests()
