# Vibe Coding as a Software Engineering Methodology for Production Systems: A Critical Evaluation

## Abstract

This document evaluates the claim that "vibe coding is a valid software engineering methodology for production systems." Drawing on practitioner literature, emerging empirical research, industry surveys, and documented production failure cases from 2025–2026, it finds the claim invalid in its strong form but partially defensible when appropriately scoped. Pure vibe coding—AI-assisted code generation with minimal human review, testing, or architectural oversight—fails to satisfy the reliability, security, maintainability, and governance requirements that define production-grade software. A corrected position recognises AI-assisted code generation as a legitimate accelerator within a disciplined engineering framework, not as a standalone production methodology. Conclusions rest primarily on industry observation and practitioner analysis; the evidence base is characterised by a notable absence of longitudinal controlled studies, which Section 7 identifies as the field's most pressing research need.

---

## Evidence Base and Scope

This document draws on primary standards documents, empirical studies where available, industry surveys, practitioner analyses, and documented production incident reports published between February 2025 and April 2026. Vendor blog posts and opinion pieces are used for discourse mapping and terminology, not as evidentiary anchors for quantitative claims. Where specific figures are cited, their provenance and limitations are noted inline. Absence of peer-reviewed longitudinal evidence is itself a substantive finding, not merely a limitation to be disclaimed.

---

## 1. Definition and Origins

"Vibe coding" was coined by Andrej Karpathy on 2 February 2025 in a widely circulated post on X, describing a development style in which the programmer communicates intent through natural language prompts to large language models (LLMs) such as Claude or GPT-4, accepts generated output with minimal review, and iterates rapidly based on observable behaviour rather than structural understanding of the code ([https://x.com/karpathy/status/1886192184808149383](https://x.com/karpathy/status/1886192184808149383)). Karpathy explicitly framed it as appropriate for "throwaway weekend projects" and rapid prototyping, not for systems requiring long-term maintenance or operational reliability.

By early 2026, the term had entered mainstream discourse. Wikipedia's entry characterises it as prioritising speed and iterative experimentation over code comprehension ([https://en.wikipedia.org/wiki/Vibe_coding](https://en.wikipedia.org/wiki/Vibe_coding)). IBM's technical overview similarly positions it as a tool for MVPs, learning, and low-stakes exploration ([https://www.ibm.com/think/topics/vibe-coding](https://www.ibm.com/think/topics/vibe-coding)). Replit's platform blog describes it as well-suited to rapid experimentation but explicitly distinguishes it from professional software engineering ([https://blog.replit.com/what-is-vibe-coding](https://blog.replit.com/what-is-vibe-coding)).

A critical source of confusion in public discourse is the conflation of four related but non-identical practices. The claim under evaluation concerns only the first:

| Term | Defining Characteristic |
|---|---|
| **Pure vibe coding** | Prompt-and-accept; no review, no tests, no architectural intent |
| **AI-assisted coding** | LLM used as a tool within a conventional engineering workflow |
| **Agentic engineering** | AI as primary implementation agent with enforced human review and automated testing |
| **Production deployment with guardrails** | Any of the above, gated by SAST/DAST scanning, CI quality gates, and governance controls |

Karpathy subsequently signalled a pivot away from pure vibe coding toward structured agentic workflows, a shift reported by The New Stack as his characterisation of the original framing as increasingly passé ([https://thenewstack.io/vibe-coding-is-passe-karpathy-has-a-new-name-for-the-future/](https://thenewstack.io/vibe-coding-is-passe-karpathy-has-a-new-name-for-the-future/)).

---

## 2. What Production Systems Require

A production software system is held to standards formalised in ISO/IEC 25010, which specifies quality characteristics including functional correctness, reliability, performance efficiency, security, maintainability, and portability ([https://www.iso.org/standard/35733.html](https://www.iso.org/standard/35733.html)). Operational production systems additionally require:

- **Security assurance**: threat modelling, vulnerability scanning, and adherence to frameworks such as the OWASP Top 10 ([https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/));
- **Test coverage**: unit, integration, regression, and end-to-end testing with documented coverage targets;
- **Code review and auditability**: traceable change history, peer review, and compliance documentation;
- **Observability**: logging, monitoring, alerting, and incident response procedures;
- **Dependency governance**: licence compliance, supply-chain security, and version management;
- **Maintainability**: readable, documented code that engineers not present at creation can understand and modify.

The critical question is whether pure vibe coding satisfies these requirements. The evidence surveyed here consistently indicates it does not.

---

## 3. Identified Failures Against Production Standards

### 3.1 Security Vulnerabilities

One industry analysis examining AI-authored pull requests found that AI-generated code produced approximately 2.74 times more security vulnerabilities than human-written code, alongside a 1.7 times higher rate of general code quality issues ([https://coderabbit.ai/blog/ai-generated-code-security-vulnerabilities](https://coderabbit.ai/blog/ai-generated-code-security-vulnerabilities); reported in Forbes: [https://www.forbes.com/sites/jodiecook/2026/03/20/vibe-coding-has-a-massive-security-problem](https://www.forbes.com/sites/jodiecook/2026/03/20/vibe-coding-has-a-massive-security-problem)). Common failure modes include OWASP Top 10 issues such as SQL injection, insecure direct object references, and exposed API credentials. Snyk's analysis of vibe-coded applications similarly identified elevated rates of critical vulnerabilities in AI-generated codebases ([https://snyk.io/articles/the-highs-and-lows-of-vibe-coding](https://snyk.io/articles/the-highs-and-lows-of-vibe-coding)).

An important qualification applies to these figures: datasets were drawn primarily from open-source projects using zero-shot prompting. Context-aware agentic workflows—where the LLM indexes a private codebase via retrieval-augmented generation (RAG)—demonstrably reduce this risk surface. The 2.74× figure should therefore be understood as an upper bound for uncontrolled vibe coding, not as a universal property of all AI-assisted development. The implication is that the security gap is partially addressable by engineering controls, but that pure vibe coding, which applies no such controls, operates at or near that upper bound.

A compounding problem is that these vulnerabilities frequently pass conventional static analysis because the code is syntactically and functionally plausible while being architecturally insecure ([https://retool.com/blog/vibe-coding-risks](https://retool.com/blog/vibe-coding-risks); [https://www.kognitos.com/blog/why-vibe-coding-breaks-in-production](https://www.kognitos.com/blog/why-vibe-coding-breaks-in-production)).

### 3.2 Documented Production Failures

The theoretical risk surface described above has materialised in documented incidents. A technical audit of a vibe-coded SaaS product identified nine critical issues including exposed API keys, absent database transaction handling, and missing input validation—flaws that passed functional testing but would be exploitable in production ([https://lasoft.org/blog/we-audited-a-vibe-coded-saas-product-and-found-9-critical-issues](https://lasoft.org/blog/we-audited-a-vibe-coded-saas-product-and-found-9-critical-issues)). A separate analysis documented seven production failure cases attributed to vibe-coded systems, including credential leakage affecting over 1.5 million records and database destruction events ([https://www.getautonoma.com/blog/vibe-coding-failures](https://www.getautonoma.com/blog/vibe-coding-failures)). Practitioner reports document systems that appeared functional during development collapsing under modest user loads, with one case describing failure at approximately 50 concurrent users ([https://www.reddit.com/r/microsaas/comments/1rgxqe5/](https://www.reddit.com/r/microsaas/comments/1rgxqe5/)). Azati's analysis reported a 180% increase in production incidents in projects developed without code review, a condition characteristic of pure vibe coding ([https://azati.ai/blog/vibe-coding-hidden-cost-without-code-review](https://azati.ai/blog/vibe-coding-hidden-cost-without-code-review)).

These cases are drawn from practitioner reports rather than controlled studies and should not be treated as representative samples. They are nonetheless significant as documented instances, not merely theoretical predictions, of production failure attributable to the absence of engineering controls.

### 3.3 Cognitive and Maintenance Debt

A production methodology must be reproducible and transferable across engineering teams over time. Pure vibe coding frequently produces "black-box" codebases in which no human engineer possesses a working understanding of the system's logic or architectural decisions. Research published on arXiv examining vibe coding in practice warns that this pattern makes long-term maintenance substantially more difficult once the original prompting context is lost ([https://arxiv.org/html/2510.00328v1](https://arxiv.org/html/2510.00328v1)). A peer-reviewed study presented at ICSE 2026 provides additional empirical grounding for the maintenance challenges introduced by AI-generated codebases ([https://kblincoe.github.io/publications/2026_ICSE_SEIP_vibe-coding.pdf](https://kblincoe.github.io/publications/2026_ICSE_SEIP_vibe-coding.pdf)).

The result is not merely technical debt but cognitive debt: systems that cannot be safely modified, extended, or debugged by engineers who were not present at the original AI session. This is structurally analogous to an accelerated interest rate on deferred quality costs—the longer the system operates without human comprehension, the more expensive any subsequent intervention becomes.

Addy Osmani's November 2025 analysis draws a sharp distinction between vibe coding and AI-assisted engineering: the former involves accepting AI output with minimal scrutiny, while the latter uses AI as a tool within a disciplined process that includes review, testing, and human accountability ([https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98](https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98)).

### 3.4 The Productivity Paradox

The productivity case for vibe coding is more ambiguous than its advocates claim. IBM's analysis of internal tooling projects reported development time reductions of approximately 60% during initial build phases ([https://www.ibm.com/think/topics/vibe-coding](https://www.ibm.com/think/topics/vibe-coding)). Stack Overflow's 2025 Developer Survey, however, found that only approximately 3% of developers report high trust in AI-generated code without review, suggesting that the majority of developers who use these tools invest significant verification time ([https://survey.stackoverflow.co/2025/](https://survey.stackoverflow.co/2025/)). Builder.io's analysis of the prototype-to-production transition documents a consistent pattern in which vibe-coded prototypes that appear complete require substantial rework before production deployment ([https://www.builder.io/m/explainers/vibe-coding-limitations](https://www.builder.io/m/explainers/vibe-coding-limitations)).

A plausible interpretation of these data points is that vibe coding creates a velocity trap: initial development speed is real and measurable, but downstream debugging, security remediation, and maintainability costs erode or eliminate the net gain when measured over a full development and operational lifecycle. This dynamic is consistent with established models of technical debt accumulation, where deferred quality costs compound over time. A total cost of ownership (TCO) analysis—comparing initial build speed against defect remediation, security patching, and maintainability costs over a 12–24 month horizon—is conspicuously absent from current literature and represents a critical research gap. The velocity trap interpretation should be treated as a well-motivated inference pending such evidence, not as a settled conclusion.

### 3.5 Exception Handling and Operational Brittleness

Multiple practitioner analyses document that vibe-coded systems exhibit poor exception handling, inadequate edge-case coverage, and failure modes that emerge only at production scale. Charter Global concludes that "pure vibe coding falls short" of production requirements because AI systems optimise for demonstrable functionality in the prompt context rather than for the full operational surface area ([https://www.charterglobal.com/can-vibe-coding-produce-production-grade-software](https://www.charterglobal.com/can-vibe-coding-produce-production-grade-software)). Thoughtworks reaches a similar conclusion, noting that such systems routinely fail when confronted with adversarial inputs, load conditions, or dependency failures absent from the original prompt ([https://www.thoughtworks.com/en-us/insights/blog/generative-ai/can-vibe-coding-produce-production-grade-software](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/can-vibe-coding-produce-production-grade-software)).

METR's controlled research on AI-assisted development tasks provides an important empirical counterpoint to marketing-led productivity narratives. On complex real-world software tasks, AI-assisted developers were on average slower than unassisted developers, with output exhibiting more security-relevant defects ([https://metr.org/blog/2025-07-22-vibe-coding-study/](https://metr.org/blog/2025-07-22-vibe-coding-study/)). This finding challenges the assumption that AI assistance uniformly accelerates development across all task types and complexity levels.

### 3.6 Governance and Compliance Gaps

Enterprise production environments are subject to regulatory requirements—GDPR, SOC 2, HIPAA, PCI-DSS, and others—that demand documented development processes, traceable decision-making, and auditable change management. Pure vibe coding produces none of these artefacts by design. Retool's enterprise risk analysis identifies this as a categorical barrier to regulated-sector adoption, not merely a tooling maturity gap ([https://retool.com/blog/vibe-coding-risks](https://retool.com/blog/vibe-coding-risks)). The governance gap is not primarily a technical problem solvable by better LLMs; it is a process problem requiring human accountability structures that pure vibe coding structurally precludes.

---

## 4. Logical Flaws in the Original Claim

The claim as stated contains several compounding errors.

**Conflation of tool with production methodology.** A production methodology is a structured, repeatable system of practices that specifies the controls necessary to achieve production-grade assurance—defined phases, quality gates, verification procedures, and accountability structures. Pure vibe coding is a prompt-and-accept interaction pattern. The critical point is not that it is "too informal to be a methodology" but that it does not specify the controls required for production assurance and therefore cannot constitute a valid production methodology regardless of how it is formalised ([https://hexaware.com/blogs/vibe-coding-vs-traditional-software-development-a-complete-comparison](https://hexaware.com/blogs/vibe-coding-vs-traditional-software-development-a-complete-comparison)). Comparing it to Agile, Scrum, or XP reveals a category difference: those methodologies specify how quality and accountability are maintained; vibe coding specifies neither.

**Prototype performance does not predict production performance.** The claim implicitly extrapolates from vibe coding's demonstrated utility in prototyping contexts to production suitability. The conditions that make it effective for prototypes—tolerance for defects, low security requirements, controlled environments, short operational lifetimes—are precisely the conditions absent in production ([https://trickle.so/blog/vibe-coding-vs-traditional-development](https://trickle.so/blog/vibe-coding-vs-traditional-development)). The documented failure cases in Section 3.2 illustrate what happens when this extrapolation is acted upon.

**Absence of supporting evidence.** The literature surveyed here does not establish any convincing documented case in which a pure vibe-coded system—with no post-generation human review, testing, or refactoring—sustained a production environment over a meaningful period. Anecdotal cases cited as successes consistently involve iterative human review and correction, which by definition introduces engineering controls and disqualifies them as instances of pure vibe coding ([https://cloud.google.com/discover/what-is-vibe-coding](https://cloud.google.com/discover/what-is-vibe-coding)). An absolute claim that no such case exists anywhere would be epistemically overreaching; the accurate and defensible claim is that none have been documented with sufficient rigour to serve as evidence for the original thesis.

---

## 5. The Emerging Synthesis: AI-Augmented Engineering

The industry has not rejected AI-assisted code generation; it has refined the conditions under which it can be deployed responsibly. By 2026, a clear distinction had emerged between pure vibe coding and "agentic engineering"—a workflow in which AI functions as the primary implementation agent but human engineers enforce review cycles, automated test suites, and architectural governance.

Simon Willison's concept of "vibe engineering" argues that the value of LLMs in development is fully realisable only when paired with human epistemic responsibility over the output ([https://simonwillison.net/2025/Oct/7/vibe-engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering)). Superblocks' enterprise framework describes a guardrailed variant in which LLM-generated code is automatically scanned for vulnerabilities, subjected to deterministic test execution, and gated behind human approval before deployment ([https://www.superblocks.com/blog/what-is-enterprise-vibe-coding](https://www.superblocks.com/blog/what-is-enterprise-vibe-coding)). OpenAI's Codex documentation frames agentic coding tools as production-relevant specifically when operating within sandboxed, permissioned environments with test execution and human review loops integrated into CI/CD pipelines ([https://openai.com/index/introducing-codex/](https://openai.com/index/introducing-codex/)).

The consistent pattern across these accounts is that AI-assisted code generation contributes measurable value to production workflows when embedded in—not substituted for—conventional software engineering discipline. This is not a weakened or hedged version of the original claim; it is a fundamentally different claim about a fundamentally different practice.

---

## 6. Corrected and More Defensible Claim

The original claim should be replaced with the following:

> **Pure vibe coding is not a valid standalone production methodology. It does not specify the controls necessary for production-grade assurance and has not been documented successfully sustaining production systems without the addition of conventional engineering practices. AI-assisted code generation becomes production-appropriate only when embedded within a disciplined software engineering framework that includes human review, automated testing, security scanning, and governance controls. Within such a framework, it is a potentially powerful acceleration technique—not a replacement for engineering rigour.**

---

## 7. Empirical Next Steps

The following research directions would sharpen the evidence base and establish more precise boundary conditions for practitioners and policymakers.

1. **Total cost of ownership studies.** Controlled comparisons of AI-augmented versus traditionally engineered systems, tracked over 12–24 months for defect rates, security incidents, maintenance costs, and developer comprehension, would resolve the productivity paradox identified in Section 3.4 and provide the longitudinal grounding entirely absent from current literature. This is the single highest-priority research need in this field.

2. **Security benchmark replication and stratification.** The existing vulnerability differential findings should be replicated across larger and more diverse codebases, stratified by prompting approach (zero-shot versus RAG-enhanced agentic), application domain, and level of human review intervention. This would establish whether the elevated vulnerability rate is a property of AI code generation per se or of uncontrolled zero-shot prompting specifically—a distinction with significant practical implications.

3. **Cognitive load and comprehension studies.** Controlled experiments measuring how quickly engineers unfamiliar with a codebase can understand, modify, and safely extend vibe-coded versus traditionally engineered systems would quantify the cognitive debt problem with the precision needed for engineering management decisions.

4. **Governance framework piloting.** Structured pilots in regulated industries—healthcare, finance, critical infrastructure—applying AI-augmented engineering processes to production workloads would test whether current governance gaps are fundamental barriers or addressable through tooling and process design. Outcome measures should include regulatory audit outcomes, not merely technical metrics.

5. **Trust calibration studies.** Research examining the conditions under which developer trust in AI output is well-calibrated—neither over-trusting nor counterproductively sceptical—would inform both training programme design and tooling development for production contexts.

6. **Tipping-point analysis.** Empirical work identifying the codebase scale, user count, dependency depth, or operational complexity threshold at which vibe-coded projects must transition to agentic engineering discipline to avoid failure would give practitioners actionable guidance that current literature entirely lacks. A mathematically grounded threshold—even a rough one—would have substantial practical value for engineering managers deciding when informal AI-assisted workflows require formalisation.

---

## 8. Conclusion

The claim that pure vibe coding is a valid software engineering methodology for production systems is not supported by available evidence. In its canonical form, it lacks the structural characteristics of a production methodology, fails to specify the controls required for production assurance, and has not been documented sustaining production systems over time without supplementation by conventional engineering practices. The elevated security vulnerability differential in zero-shot AI-generated code, the cognitive debt problem documented in empirical literature, the governance compliance gap, the documented production failure cases, and the unresolved productivity paradox collectively constitute a substantial and multi-dimensional evidentiary burden against the claim.

The more defensible and practically grounded position is that AI-assisted code generation—particularly in its more disciplined agentic forms—is a powerful accelerator that becomes production-appropriate when treated as one rigorously governed component of a software engineering process. The field's most pressing need is not further commentary elaborating this conclusion but the longitudinal empirical studies, production incident analyses, and tipping-point threshold research that would allow its boundary conditions to be defined with the precision practitioners require.

---

## References

- Karpathy, A. (2025). Original vibe coding post. [https://x.com/karpathy/status/1886192184808149383](https://x.com/karpathy/status/1886192184808149383)
- Wikipedia. Vibe coding. [https://en.wikipedia.org/wiki/Vibe_coding](https://en.wikipedia.org/wiki/Vibe_coding)
- IBM Think. What is vibe coding? [https://www.ibm.com/think/topics/vibe-coding](https://www.ibm.com/think/topics/vibe-coding)
- Replit Blog. What is vibe coding? [https://blog.replit.com/what-is-vibe-coding](https://blog.replit.com/what-is-vibe-coding)
- The New Stack. Vibe coding is passé: Karpathy has a new name for the future. [https://thenewstack.io/vibe-coding-is-passe-karpathy-has-a-new-name-for-the-future/](https://thenewstack.io/vibe-coding-is-passe-karpathy-has-a-new-name-for-the-future/)
- ISO/IEC 25010:2011. Systems and software quality requirements and evaluation. [https://www.iso.org/standard/35733.html](https://www.iso.org/standard/35733.html)
- OWASP. Top Ten. [https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/)
- CodeRabbit. AI-generated code security vulnerabilities (December 2025). [https://coderabbit.ai/blog/ai-generated-code-security-vulnerabilities](https://coderabbit.ai/blog/ai-generated-code-security-vulnerabilities)
- Cook, J. Forbes. Vibe coding has a massive security problem (March 2026). [https://www.forbes.com/sites/jodiecook/2026/03/20/vibe-coding-has-a-massive-security-problem](https://www.forbes.com/sites/jodiecook/2026/03/20/vibe-coding-has-a-massive-security-problem)
- Snyk. The highs and lows of vibe coding. [https://snyk.io/articles/the-highs-and-lows-of-vibe-coding](https://snyk.io/articles/the-highs-and-lows-of-vibe-coding)
- Retool. Vibe coding risks. [https://retool.com/blog/vibe-coding-risks](https://retool.com/blog/vibe-coding-risks)
- Kognitos. Why vibe coding breaks in production. [https://www.kognitos.com/blog/why-vibe-coding-breaks-in-production](https://www.kognitos.com/blog/why-vibe-coding-breaks-in-production)
- LaSoft. We audited a vibe-coded SaaS product and found 9 critical issues. [https://lasoft.org/blog/we-audited-a-vibe-coded-saas-product-and-found-9-critical-issues](https://lasoft.org/blog/we-audited-a-vibe-coded-saas-product-and-found-9-critical-issues)
- Autonoma. Vibe coding failures: documented production cases (2026). [https://www.getautonoma.com/blog/vibe-coding-failures](https://www.getautonoma.com/blog/vibe-coding-failures)
- Reddit. r/microsaas: production failure at 50 concurrent users. [https://www.reddit.com/r/microsaas/comments/1rgxqe5/](https://www.reddit.com/r/microsaas/comments/1rgxqe5/)
- Azati. Vibe coding hidden cost without code review. [https://azati.ai/blog/vibe-coding-hidden-cost-without-code-review](https://azati.ai/blog/vibe-coding-hidden-cost-without-code-review)
- arXiv. Vibe coding in practice. [https://arxiv.org/html/2510.00328v1](https://arxiv.org/html/2510.00328v1)
- Blincoe, K. et al. ICSE 2026 SEIP. Vibe coding study. [https://kblincoe.github.io/publications/2026_ICSE_SEIP_vibe-coding.pdf](https://kblincoe.github.io/publications/2026_ICSE_SEIP_vibe-coding.pdf)
- Osmani, A. Vibe coding is not the same as AI-assisted engineering (November 2025). [https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98](https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98)
- Stack Overflow. Developer Survey 2025. [https://survey.stackoverflow.co/2025/](https://survey.stackoverflow.co/2025/)
- Builder.io. Vibe coding limitations: from prototype to production. [https://www.builder.io/m/explainers/vibe-coding-limitations](https://www.builder.io/m/explainers/vibe-coding-limitations)
- Charter Global. Can vibe coding produce production-grade software? [https://www.charterglobal.com/can-vibe-coding-produce-production-grade-software](https://www.charterglobal.com/can-vibe-coding-produce-production-grade-software)
- Thoughtworks. Can vibe coding produce production-grade software? [https://www.thoughtworks.com/en-us/insights/blog/generative-ai/can-vibe-coding-produce-production-grade-software](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/can-vibe-coding-produce-production-grade-software)
- METR. AI-assisted development study (July 2025). [https://metr.org/blog/2025-07-22-vibe-coding-study/](https://metr.org/blog/2025-07-22-vibe-coding-study/)
- Willison, S. Vibe engineering (October 2025). [https://simonwillison.net/2025/Oct/7/vibe-engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering)
- Superblocks. What is enterprise vibe coding? [https://www.superblocks.com/blog/what-is-enterprise-vibe-coding](https://www.superblocks.com/blog/what-is-enterprise-vibe-coding)
- OpenAI. Introducing Codex. [https://openai.com/index/introducing-codex/](https://openai.com/index/introducing-codex/)
- Hexaware. Vibe coding vs. traditional software development. [https://hexaware.com/blogs/vibe-coding-vs-traditional-software-development-a-complete-comparison](https://hexaware.com/blogs/vibe-coding-vs-traditional-software-development-a-complete-comparison)
- Trickle. Vibe coding vs. traditional development. [https://trickle.so/blog/vibe-coding-vs-traditional-development](https://trickle.so/blog/vibe-coding-vs-traditional-development)
- Google Cloud. What is vibe coding? [https://cloud.google.com/discover/what-is-vibe-coding](https://cloud.google.com/discover/what-is-vibe-coding)