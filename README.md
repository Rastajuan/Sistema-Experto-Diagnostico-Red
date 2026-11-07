# Rule-based expert system for initial network connectivity diagnosis

**Languages:** **English** | [Español](README.es.md)

A **rule-based expert system** built in Python for the **5071 · Artificial Intelligence Models, NF2** module of the 2026–2027 Specialisation Course in Artificial Intelligence and Big Data.

This project guides users through common Windows networking checks and proposes an **initial, indicative diagnosis** based on their answers. Its knowledge base contains **20 rules (R01–R20)**. A **forward-chaining inference engine** derives additional facts and provides a readable trace explaining which rules contributed to the result.

> [!IMPORTANT]
> **Educational prototype, not a definitive diagnostic tool.** It does not run network probes, independently verify user responses, or change network settings. A probable diagnosis does not establish the actual root cause with certainty.

## Features

- Guides manual checks involving **Wi-Fi and Ethernet**, **IPv4**, the default gateway, IP reachability with `ping`, and DNS resolution with `nslookup`.
- Applies explicit rules to user-supplied facts and infers additional facts by forward chaining.
- Displays an initial diagnosis, recommendations, and an **inference trace** with rule identifiers and explanations.
- Covers selected cases such as apparently working connectivity, possible DNS failures, possible external connectivity problems, and local versus broader network issues.
- Detects contradictory assignments to known facts and raises an exception rather than silently overriding them.

## Architecture

```text
src/
  sistema_experto_red.py       # User interaction, input validation, results
  reglas.py                    # Knowledge base: rules R01–R20
  motor_inferencia.py          # Rule evaluation, forward chaining, trace
pruebas/
  prueba_motor_inferencia.py   # Automated rule and engine checks
README.md                      # English documentation
README.es.md                   # Documentación en español
LICENSE                        # MIT licence
requirements.txt               # Intentionally empty
.gitignore
```

The responsibilities are deliberately separated: `reglas.py` represents domain knowledge; `motor_inferencia.py` evaluates conditions and applies conclusions without embedding networking-specific concepts; `sistema_experto_red.py` collects answers and presents the diagnosis. A Python dictionary acts as working memory. Rule evaluation continues until a complete pass adds no new facts.

## Requirements

- **Python 3.13**, used during development. Only the Python **standard library** is required; there are no third-party dependencies.
- An interactive terminal for providing answers.
- Windows for following the manual networking instructions supplied by the interface. The inference-engine tests do not require Windows.

`requirements.txt` is intentionally empty. A virtual environment is recommended for reproducibility but not required.

## Run on Windows (PowerShell)

From the repository root:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m src.sistema_experto_red
```

Alternatively, if a compatible Python environment is already activated:

```powershell
python -m src.sistema_experto_red
```

The interactive application asks about observed network behaviour. When a `?` help option is offered, it explains how to perform the corresponding check **manually**. The program **does not run those commands itself**.

**Language note:** the interactive interface, its prompts and the inference trace are written in Spanish. English documentation does not imply an English-localised application.

## Example: a possible DNS issue

An illustrative scenario:

1. The Wi-Fi interface is connected, and the default gateway responds.
2. A public IP address responds to `ping`.
3. DNS lookup for the test domain fails.
4. The inference engine activates a sequence of rules, including **R15**, identifies a **possible DNS resolution problem**, and recommends checking configured DNS servers and repeating name-resolution tests.

**Interpretation:** this combination suggests a DNS-related issue but does not identify the exact underlying cause. A successful or failed ICMP `ping` does not, on its own, establish the state of every network protocol.

## Automated tests

Run from the repository root:

```powershell
python -m pruebas.prueba_motor_inferencia
```

The suite contains **21 automated checks**: one for each of the 20 rules and one for conflicting facts. It supplies predefined facts and checks expected conclusions and inference traces.

**Recorded audit result:** **21/21 passed**, using Python 3.13.5 in the review environment, without functional code changes. This verifies the programmed scenarios only. It does **not** establish complete coverage, real-world diagnostic accuracy, or compatibility with every Windows environment.

## Scope, limitations and knowledge-selection bias

| Area | Known limitation | Practical consequence |
| --- | --- | --- |
| Inputs | Users enter results manually; answers are not verified. | Incorrect answers may lead to inappropriate inferences. |
| Knowledge coverage | Only 20 selected rules are implemented. | Unrepresented faults may not receive a suitable diagnosis. |
| Protocols | Focuses on IPv4, Wi-Fi/Ethernet, ICMP and basic DNS. | No dedicated analysis of IPv6, proxies, firewalls, complex routes or application-specific problems. |
| ICMP checks | No reply to `ping` may result from filtering. | A failed ping is not proof that Internet access is unavailable. |
| Tests | A fixed set of rule scenarios and one conflict scenario is checked. | Passing tests does not prove defect-free behaviour or field accuracy. |
| Conflicts | Contradictions raise `ValueError`. | There is no advanced rule prioritisation or conflict-resolution strategy. |

### Knowledge-selection bias

This system is **not trained on datasets**. Its main potential bias comes from **which situations and rules were selected during design**: common IPv4 connectivity problems receive more attention than other scenarios. This can produce incomplete assessments for cases outside that coverage. Better coverage would require expert review, updated technical references and a wider range of test scenarios.

## Safety and privacy

- Does **not** change network adapters, routes, DNS servers or other system settings.
- Does **not** automatically run network commands or request credentials.
- Offers guidance only; recommendations must be evaluated before making actual changes.
- When sharing logs or cases publicly, remove internal IP addresses, hostnames, personal information and other parties' sensitive configuration details.

## Future work (not implemented)

- Extend the knowledge base to IPv6 and other networking scenarios.
- Add integration tests and anonymised real-world cases.
- Introduce explicit priorities and controlled conflict resolution.
- Improve structured result reporting and validation.

These are **potential improvements**, not existing features.

## Authorship and project context

**Juan Bello Fernández.** Academic practice project exploring knowledge representation, rule-based reasoning, modular architecture and explainable inferences.

## Generative AI disclosure

**ChatGPT was used as a supporting tool** for learning, reviewing rule logic, debugging, preparing tests and improving documentation. Development involved iterative review and execution; publication does not imply that every line of text or code was produced without AI assistance. The author remains responsible for the published work, its interpretation and maintenance.

## Licence

**MIT License. Copyright (c) 2026 Juan Bello Fernández.**

The code may be used, copied, modified and redistributed, including commercially, subject to the conditions in [LICENSE](LICENSE). Copies or substantial portions of the software must retain the copyright notice and MIT licence text. MIT does not require visible attribution in a derived application's user interface or publication of modifications.

The software is provided **without warranty** and is **not a certified professional network diagnostic tool**. The licence covers the content released in this repository and does not grant rights to third-party trademarks, services or materials.
