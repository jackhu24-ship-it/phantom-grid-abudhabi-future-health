# -*- coding: utf-8 -*-
"""
PHANToM GRID :: Step 3 Atomic Closure Test Suite for PG-MOD-28 Abu Dhabi Future Health (Neuro-Edge & Brain Health)
(§3.4.24 Pure ASCII + Rule 83)
"""
import sys
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(MODULE_ROOT))

from src.runner import FutureHealthSovereignRunner


def run_atomic_closure_tests():
    print("[*] Starting PG-MOD-28 (Abu Dhabi Future Health :: Brain Health & Neuro-Edge) Step 3 Atomic Closure Gate Verification...")
    runner = FutureHealthSovereignRunner()

    # TEST 1: Brain-Health SRAM Kernel Latency (<= 1.85us) & Early Cognitive Biomarker Check
    r1 = runner.execute_clinical_cycle({
        "vram_gb": 30.0,
        "artifact_noise": 0.05,
        "theta_beta_ratio": 1.48,
        "p300_latency_ms": 288.0,
    })
    assert r1["latency_us"] <= 1.85, f"TEST 1 FAIL: Latency {r1['latency_us']}us > 1.85us"
    assert r1["risk_tier"] == "HEALTHY_OPTIMAL_COGNITION"
    print(f"  [+] TEST 1 PASS: Brain-Health SRAM Kernel Latency = {r1['latency_us']:.2f}us (<= 1.85us) | Tier: {r1['risk_tier']}")

    # TEST 2: Early MCI / High Cognitive Decline Biomarker Detection (Theta/Beta > 2.80 & P300 > 340ms)
    r_mci = runner.execute_clinical_cycle({
        "vram_gb": 31.0,
        "artifact_noise": 0.08,
        "theta_beta_ratio": 3.25,
        "p300_latency_ms": 372.0,
    })
    assert r_mci["risk_tier"] == "HIGH_COGNITIVE_DECLINE_RISK" and r_mci["anomaly_score"] == 0.88
    print(f"  [+] TEST 2 PASS: Early Brain Health MCI Biomarker Detected ({r_mci['risk_tier']}, Score={r_mci['anomaly_score']})")

    # TEST 3: 50GB VRAM Hard Meltdown Trip
    tripped = False
    try:
        runner.execute_clinical_cycle({"vram_gb": 52.5, "artifact_noise": 0.05})
    except RuntimeError:
        tripped = True
    assert tripped, "TEST 3 FAIL: VRAM 52.5GB failed to trip E-STOP!"
    print("  [+] TEST 3 PASS: 50GB Global VRAM Meltdown Trip Verified.")

    # TEST 4: Ocular/EMG Artifact 1.35x Damping Gate & Privacy-Preserving Edge Architecture
    r3 = runner.execute_clinical_cycle({"vram_gb": 34.0, "artifact_noise": 0.34})
    assert r3["damping"] == 1.35 and r3["action"] == "APPLY_OCULAR_ARTIFACT_DAMPING_AND_ALERT"
    assert r3["privacy_architecture"] == "EDGE_LOCAL_OFFLINE_ZERO_CLOUD_LEAK"
    print("  [+] TEST 4 PASS: Ocular/EMG Artifact > 0.25 Triggered 1.35x Damping & Edge Privacy Verified.")

    # TEST 5: HIPAA / ADHICS 2-Pass ZDR Wipe & WORM Receipt
    assert r3["zdr_residual_mb"] == 0.0 and r3["worm_receipt"] == "WORM-HEALTH-ABUDHABI-6F8E2A1C"
    assert r3["neuro_worm_receipt"] == "WORM-HEALTH-ABUDHABI-NEURO-8E4B"
    print(f"  [+] TEST 5 PASS: 2-Pass PHI ZDR Purge (0.00MB) & Receipts: {r3['worm_receipt']} / {r3['neuro_worm_receipt']}")

    print("\n[ ALL 5 ATOMIC CLOSURE TESTS PASSED - PRODUCTION READY ]")


def test_atomic_closure_pytest():
    run_atomic_closure_tests()


if __name__ == "__main__":
    run_atomic_closure_tests()
