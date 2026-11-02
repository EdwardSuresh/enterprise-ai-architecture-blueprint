# Contributing

Thank you for improving the kit.

1. **Open an issue first** for anything larger than a typo, so the change fits the blueprint's structure.
2. **Keep the core cloud-neutral.** Cloud SDK code goes only in `platform/adapters/`.
3. **Keep sector detail in `domain-packs/`.** Use the six-step overlay method in `domain-packs/README.md`.
4. **Every rule change needs a test.** Policy gate rules go in `tests/test_policy_gate.py`.
5. **Run the gates locally** before a pull request: `pytest -q && kit-evals --suite evals/suites/quality.yaml && kit-policy-gate`.
6. **Label examples honestly.** Organization stories are "Illustrative example" unless they are client-approved case studies.
7. **No confidential information.** Never include real client names, data or internal documents.
8. **Update `CHANGELOG.md`** under an "Unreleased" heading.

By contributing, you agree that code is licensed under MIT and content under CC BY 4.0.
