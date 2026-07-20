# -*- coding: utf-8 -*-
"""
Architecture OS - Core Engine
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml
from dataclasses import dataclass


@dataclass
class EngineInfo:
    id: str
    name: str
    version: str
    owner: str
    purpose: str
    classification: str
    maturity: str
    stage: str
    allowed_failures: int
    path: Path

    def has_engine_yaml(self) -> bool:
        return (self.path / "engine.yaml").exists()

    def load_engine_yaml(self) -> Dict:
        path = self.path / "engine.yaml"
        if path.exists():
            with open(path) as f:
                return yaml.safe_load(f)
        return {}


class ArchitectureOS:
    """The Architecture Operating System - orchestrates all compilers"""

    def __init__(self, engines_path: str = "engines"):
        self.engines_path = Path(engines_path)
        self.compilers = {}
        self.engines: List[EngineInfo] = []

    def register_compiler(self, name: str, compiler) -> None:
        """Register a compiler with the OS"""
        self.compilers[name] = compiler

    def discover_engines(self) -> List[EngineInfo]:
        """Discover all engines in the engines directory"""
        engines = []
        if not self.engines_path.exists():
            return engines
        for engine_dir in self.engines_path.iterdir():
            if engine_dir.is_dir():
                engine_yaml = engine_dir / "engine.yaml"
                if engine_yaml.exists():
                    try:
                        with open(engine_yaml) as f:
                            data = yaml.safe_load(f)
                        engine = EngineInfo(
                            id=data.get("id", engine_dir.name),
                            name=data.get("name", engine_dir.name),
                            version=data.get("version", "0.0.0"),
                            owner=data.get("owner", "Unknown"),
                            purpose=data.get("purpose", ""),
                            classification=data.get("classification", "Unknown"),
                            maturity=data.get("maturity", "Development"),
                            stage=data.get("stage", "Development"),
                            allowed_failures=data.get("allowed_failures", 0),
                            path=engine_dir,
                        )
                        engines.append(engine)
                    except Exception as e:
                        print(f"⚠️ Error reading {engine_yaml}: {e}")
        self.engines = engines
        return engines

    def compile(
        self, engine_id: Optional[str] = None, verbose: bool = False, fix: bool = False
    ) -> Dict[str, Any]:
        """Run the compilation process"""

        engines = self.discover_engines()
        if not engines:
            return {
                "error": "No engines found",
                "build_decision": {"blocked": True, "reason": "No engines discovered"},
            }

        if engine_id:
            engines = [e for e in engines if e.id == engine_id]
            if not engines:
                return {
                    "error": f"Engine {engine_id} not found",
                    "build_decision": {
                        "blocked": True,
                        "reason": f"Engine {engine_id} not found",
                    },
                }

        results = {
            "timestamp": "2026-07-19",
            "engines": [],
            "platform_score": {},
            "repair_plan": [],
            "build_decision": {"blocked": False, "reason": "All checks passed"},
        }

        for engine in engines:
            engine_result = {
                "id": engine.id,
                "name": engine.name,
                "layers": {},
                "overall_score": 0,
                "status": "Healthy",
            }

            for compiler_name, compiler in self.compilers.items():
                result = compiler.compile(engine, verbose=verbose, fix=fix)
                engine_result["layers"][compiler_name] = result

                if result.get("status") == "Critical":
                    engine_result["status"] = "Broken"
                    results["build_decision"]["blocked"] = True
                    results["build_decision"]["reason"] = (
                        f"Critical failures in {engine.id}"
                    )

            # Calculate score
            scores = [r.get("score", 0) for r in engine_result["layers"].values()]
            engine_result["overall_score"] = (
                int(sum(scores) / len(scores)) if scores else 0
            )

            if engine_result["overall_score"] >= 90:
                engine_result["status"] = "Healthy"
            elif engine_result["overall_score"] >= 60:
                engine_result["status"] = "Warning"
            else:
                engine_result["status"] = "Broken"
                results["build_decision"]["blocked"] = True

            results["engines"].append(engine_result)

        # Calculate platform score
        layers = ["identity", "architecture", "dependency", "runtime", "platform"]
        scores = {layer: [] for layer in layers}
        for engine in results["engines"]:
            for layer in layers:
                if layer in engine.get("layers", {}):
                    scores[layer].append(engine["layers"][layer].get("score", 0))

        for layer, values in scores.items():
            results["platform_score"][layer] = (
                int(sum(values) / len(values)) if values else 0
            )
        results["platform_score"]["overall"] = int(
            sum(results["platform_score"].values()) / len(results["platform_score"])
        )

        # Generate repair plan
        for engine in results["engines"]:
            if engine["status"] in ["Broken", "Warning"]:
                for layer, layer_result in engine.get("layers", {}).items():
                    if layer_result.get("status") in ["Critical", "Warning"]:
                        results["repair_plan"].append(
                            {
                                "priority": "Critical"
                                if layer_result["status"] == "Critical"
                                else "Warning",
                                "engine": engine["id"],
                                "layer": layer,
                                "issue": layer_result.get("issue", "Unknown"),
                                "fix": layer_result.get("fix", "Unknown"),
                                "estimated_effort": layer_result.get(
                                    "estimated_effort", "Unknown"
                                ),
                            }
                        )

        return results
