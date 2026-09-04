#!/usr/bin/env python3
"""
ShramAI Production Deployment Pre-Flight Verification Script.
Validates environment prerequisites, knowledge base datasets, Docker configurations,
and API connectivity.
"""
import os
import sys
import json
from pathlib import Path

# Set UTF-8 encoding for standard output if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ANSI Color Codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def check_mark(status: bool) -> str:
    return f"{GREEN}[PASS]{RESET}" if status else f"{RED}[FAIL]{RESET}"


def run_checks():
    root_dir = Path(__file__).resolve().parent.parent
    os.chdir(root_dir)

    print(f"\n{BOLD}{CYAN}==============================================================={RESET}")
    print(f"{BOLD}{CYAN}      ShramAI Production Deployment Verification Engine         {RESET}")
    print(f"{BOLD}{CYAN}==============================================================={RESET}\n")

    checks_passed = 0
    total_checks = 0

    # Check 1: Python Version
    total_checks += 1
    py_ver = sys.version_info
    py_ok = py_ver.major == 3 and py_ver.minor >= 10
    print(f"{check_mark(py_ok)} Python Version: {py_ver.major}.{py_ver.minor}.{py_ver.micro} (Requires Python >= 3.10)")
    if py_ok: checks_passed += 1

    # Check 2: Core Project Directories
    total_checks += 1
    dirs_to_check = ["backend/app", "frontend/src", "data/knowledge_base", "models"]
    dirs_ok = all((root_dir / d).exists() for d in dirs_to_check)
    print(f"{check_mark(dirs_ok)} Project Structure: All core directories verified")
    if dirs_ok: checks_passed += 1

    # Check 3: Four Labour Codes Datasets
    total_checks += 1
    codes = [
        "code_on_wages_2019.json",
        "industrial_relations_code_2020.json",
        "social_security_code_2020.json",
        "oshwc_code_2020.json",
    ]
    kb_dir = root_dir / "data" / "knowledge_base"
    codes_ok = all((kb_dir / c).exists() for c in codes)
    print(f"{check_mark(codes_ok)} Statutory Knowledge Base: All 4 Indian Labour Codes present")
    if codes_ok: checks_passed += 1

    # Check 4: Deterministic Rule Catalog
    total_checks += 1
    rules_file = root_dir / "backend" / "app" / "compliance" / "rules" / "statutory_rules.json"
    rules_ok = rules_file.exists()
    print(f"{check_mark(rules_ok)} Deterministic Rules: Statutory rules catalog present ({rules_file.name})")
    if rules_ok: checks_passed += 1

    # Check 5: Container Packaging
    total_checks += 1
    docker_files = [
        root_dir / "docker-compose.yml",
        root_dir / "docker-compose.prod.yml",
        root_dir / "backend" / "Dockerfile",
        root_dir / "frontend" / "Dockerfile",
        root_dir / "frontend" / "nginx.conf",
    ]
    docker_ok = all(f.exists() for f in docker_files)
    print(f"{check_mark(docker_ok)} Docker Packaging: Production Dockerfiles & Compose profiles verified")
    if docker_ok: checks_passed += 1

    # Check 6: CI/CD Workflows
    total_checks += 1
    ci_file = root_dir / ".github" / "workflows" / "ci-cd.yml"
    ci_ok = ci_file.exists()
    print(f"{check_mark(ci_ok)} CI/CD Automation: GitHub Actions workflow verified")
    if ci_ok: checks_passed += 1

    # Check 7: Cloud PaaS Blueprints
    total_checks += 1
    cloud_files = [root_dir / "render.yaml", root_dir / "railway.json"]
    cloud_ok = all(f.exists() for f in cloud_files)
    print(f"{check_mark(cloud_ok)} Cloud Blueprints: Render & Railway manifests verified")
    if cloud_ok: checks_passed += 1

    # Check 8: Fast-API Application Import Test
    total_checks += 1
    api_import_ok = False
    try:
        sys.path.insert(0, str(root_dir / "backend"))
        from app.main import app
        from app.services.deployment_service import DeploymentService
        readiness = DeploymentService.check_readiness()
        api_import_ok = readiness.all_healthy
    except Exception as e:
        print(f"  {YELLOW}Warning during internal import: {str(e)}{RESET}")
    print(f"{check_mark(api_import_ok)} Backend Architecture: App factory & DeploymentService verified")
    if api_import_ok: checks_passed += 1

    # Summary
    print(f"\n{BOLD}---------------------------------------------------------------{RESET}")
    print(f"Verification Results: {BOLD}{checks_passed}/{total_checks}{RESET} pre-flight checks passed.")
    if checks_passed == total_checks:
        print(f"{BOLD}{GREEN}[OK] ShramAI is 100% READY FOR PRODUCTION DEPLOYMENT.{RESET}\n")
        return 0
    else:
        print(f"{BOLD}{RED}[FAILED] Some pre-flight deployment checks failed. Review output above.{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_checks())
