# -*- coding: utf-8 -*-
"""
PHANToM GRID :: Dedicated Unit Tests for BrainHealthSRAMKernel & NeuroFederatedEngine
"""
import sys
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(MODULE_ROOT))

from src.kernels.brain_health_sram_kernel import BrainHealthSRAMKernel
from src.engine.neuro_federated_engine import NeuroFederatedEngine


def test_brain_health_kernel_tiers():
    kernel = BrainHealthSRAMKernel()

    # 1. Healthy Optimal Cognition
    r_opt = kernel.evaluate_neural_signal(theta_beta_ratio=1.50, p300_latency_ms=285.0, measured_us=1.08)
    assert r_opt["latency_us"] <= 1.85
    assert r_opt["risk_tier"] == "HEALTHY_OPTIMAL_COGNITION"
    assert r_opt["anomaly_score"] == 0.05

    # 2. Mild Cognitive Fatigue (single biomarker elevated)
    r_mild = kernel.evaluate_neural_signal(theta_beta_ratio=2.95, p300_latency_ms=310.0, measured_us=1.15)
    assert r_mild["latency_us"] <= 1.85
    assert r_mild["risk_tier"] == "MILD_COGNITIVE_FATIGUE"
    assert r_mild["anomaly_score"] == 0.42

    # 3. High Cognitive Decline Risk / Early MCI (both biomarkers elevated)
    r_high = kernel.evaluate_neural_signal(theta_beta_ratio=3.30, p300_latency_ms=375.0, measured_us=1.20)
    assert r_high["latency_us"] <= 1.85
    assert r_high["risk_tier"] == "HIGH_COGNITIVE_DECLINE_RISK"
    assert r_high["anomaly_score"] == 0.88


def test_neuro_federated_engine_privacy_and_zdr():
    engine = NeuroFederatedEngine()
    res = engine.process_cognitive_inference(artifact_noise=0.32, vram_gb=32.0)
    assert res["damping"] == 1.35
    assert res["zdr_residual_mb"] == 0.0
    assert res["adhics_hipaa_compliant"] is True
    assert res["privacy_architecture"] == "EDGE_LOCAL_OFFLINE_ZERO_CLOUD_LEAK"
    assert res["worm_receipt"] == "WORM-HEALTH-ABUDHABI-NEURO-8E4B"


if __name__ == "__main__":
    test_brain_health_kernel_tiers()
    test_neuro_federated_engine_privacy_and_zdr()
    print("[ PASS ] All BrainHealthSRAMKernel & NeuroFederatedEngine tests verified!")
