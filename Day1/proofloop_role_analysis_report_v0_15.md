# ProofLoop Role Selection Transparency Report v0.15

Generated: `2026-10-08T05:08:17.369465+00:00`  
Database: `C:\Users\psychoGanon\Desktop\BuilidingMyWayIntoAI\Day1\proofloop_enriched.db`  
Database access: **read-only**

## Purpose

This revision turns the first exploratory battery into a more defensible role-selection evidence report. It still does **not** choose Application #001. Its job is to expose the evidence, contradictions, and candidate-review paths clearly enough that the eventual choice can be defended.

## Methodology guardrails

- No role is selected solely by this battery.
- NO SALES is modeled as strong exclusion evidence vs contextual review evidence.
- Regex word boundaries are used to prevent obvious substring false positives such as commissioning->commission.
- Location feasibility combines primary location, secondary locations, workplace_type, is_remote, actual remote wording, office-day wording, and relocation wording.
- US - Remote in a secondary location is not automatically treated as permission to work from Utah.
- Relocation assistance is not treated as permission to begin remotely.
- Experience and education signals are extracted preferentially from the qualifications section.
- Resume/evidence overlap is a discovery aid and not a qualification or fit score.
- The deep-review pool uses explainable bands and is not a hidden final ranking.
- Compensation is preserved with interval and currency.

## Executive summary

- **current api roles:** 815
- **us remote anywhere:** 44
- **strong us remote:** 20
- **relocation supported us roles:** 250
- **sales excluded roles:** 84
- **sales context review roles:** 210
- **deep review pool emitted:** 75

### Location classification counts

| location_category | roles |
| --- | --- |
| D_US_LOCATION_UNCLEAR | 346 |
| C_US_RELOCATION_SUPPORTED | 250 |
| E_NON_US_OR_JURISDICTION_MISMATCH | 170 |
| B_US_REMOTE_AMBIGUOUS | 24 |
| A_US_REMOTE_STRONG | 20 |
| D_US_ONSITE_OR_HYBRID | 5 |

### Sales classification counts

| sales_classification | roles |
| --- | --- |
| NO_SALES_SIGNAL_FOUND | 521 |
| REVIEW_SALES_CONTEXT | 210 |
| EXCLUDE_STRONG_SALES | 84 |

### Technical-core counts

| technical_core_level | roles |
| --- | --- |
| MEDIUM | 323 |
| HIGH | 197 |
| LOW | 168 |
| NONE_DETECTED | 127 |

### Review-priority counts

| review_priority | roles |
| --- | --- |
| P3_BACKGROUND | 284 |
| LOW_TECHNICAL_PRIORITY | 259 |
| P2_REVIEW | 129 |
| EXCLUDED_SALES | 84 |
| P1_DEEP_REVIEW | 59 |

## 1. Source status

| source_status | roles |
| --- | --- |
| api_only | 1 |
| html_only | 3 |
| matched | 814 |

## 2. Work-arrangement field behavior

| is_remote | workplace_type | roles |
| --- | --- | --- |
| 1 | Hybrid | 509 |
| NULL | NULL | 256 |
| 0 | OnSite | 29 |
| 1 | Remote | 21 |

## 3. Primary location distribution

<details>
<summary>All primary locations (25 rows)</summary>

| location | roles |
| --- | --- |
| San Francisco | 562 |
| Singapore | 38 |
| Tokyo, Japan | 27 |
| London, UK | 23 |
| US - Remote | 22 |
| Washington, DC | 22 |
| Dublin, Ireland | 19 |
| Seattle | 19 |
| New York City | 18 |
| Munich, Germany | 9 |
| Paris, France | 9 |
| Sydney, Australia | 8 |
| Ontario - Remote | 7 |
| Seoul, South Korea | 7 |
| Delhi, India | 4 |
| São Paulo | 4 |
| Abu Dhabi, UAE | 3 |
| Bangalore - Remote | 2 |
| Madrid, Spain | 2 |
| Mountain View | 2 |
| Mumbai, India | 2 |
| Stockholm, Sweden | 2 |
| Zurich, Switzerland | 2 |
| Australia - Remote | 1 |
| India - Remote | 1 |

</details>

## 4. Team distribution

<details>
<summary>All teams (83 rows)</summary>

| team | roles |
| --- | --- |
| Applied AI Engineering | 65 |
| Technical Success | 63 |
| Marketing | 37 |
| Sales | 37 |
| Support Delivery | 34 |
| Hardware | 33 |
| Finance | 30 |
| Forward Deployed Engineering | 30 |
| Security | 26 |
| Compute | 24 |
| Datacenter Design | 24 |
| Software | 21 |
| Robotics | 20 |
| Data Science | 18 |
| Codex - Engineering | 16 |
| OpenAI for Gov | 15 |
| Trust & Safety | 15 |
| Ads Solutions | 14 |
| Applied AI | 14 |
| Applied AI Infrastructure | 13 |
| Safety Systems | 13 |
| Technical Program Management | 13 |
| Strategic Finance | 12 |
| Account Associates | 10 |
| Legal | 10 |
| Product Management | 10 |
| Agents | 9 |
| Core Product & Platform \| API | 8 |
| Foundations | 8 |
| IT | 8 |
| Partnerships | 8 |
| Product Design | 8 |
| Research | 8 |
| Communications | 7 |
| Runtime | 7 |
| Scaling | 7 |
| Support Operations | 7 |
| Growth | 6 |
| Post-training | 6 |
| Recruiting | 6 |
| Fleet Clusters | 5 |
| Intelligence & Investigations | 5 |
| Strategy & Operations | 5 |
| Global Affairs | 4 |
| Research Program Management | 4 |
| Workload | 4 |
| Alignment | 3 |
| Corporate Security | 3 |
| Go To Market | 3 |
| Human Data | 3 |
| Inference | 3 |
| Model Policy | 3 |
| Special Situations | 3 |
| Systems | 3 |
| Workplace | 3 |
| AI for Chip Design | 2 |
| Executive Operations | 2 |
| Frontiers Clusters | 2 |
| G&A | 2 |
| Hardware Engineering | 2 |
| Life Sciences | 2 |
| People | 2 |
| People Systems & Operations | 2 |
| Product Policy | 2 |
| Supercomputing | 2 |
| Support Automation | 2 |
| Total Rewards | 2 |
| Training | 2 |
| Business Operations | 1 |
| Codex – Developer Experience | 1 |
| Consumer Devices | 1 |
| Creative | 1 |
| Emerging Talent | 1 |
| Employee Relations | 1 |
| GTM Innovation | 1 |
| HRBP | 1 |
| Human Resources | 1 |
| Kernels | 1 |
| Manufacturing & Ops | 1 |
| People Innovation Labs | 1 |
| Product Partnerships | 1 |
| Reasoning | 1 |
| User Operations | 1 |

</details>

## 5. US-remote evidence inventory

These are roles where `US - Remote` appears as a primary or secondary location. The location classification keeps strong remote evidence separate from ambiguous hybrid/secondary evidence.

<details>
<summary>US-Remote anywhere (44 rows)</summary>

| title | team | primary | secondary | workplace | location_class | sales | technical | evidence_overlap | years_mentions | relocation | office_days | salary | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ChatGPT Performance Engineer | Applied AI Engineering | San Francisco | New York City; Seattle; US - Remote |  | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 | 7+ years | NO |  | USD 347000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Business Development Lead, Compute Strategy | Compute | US - Remote | New York City; Seattle; San Francisco | Hybrid | B_US_REMOTE_AMBIGUOUS | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 8+ years | NO |  | USD 333000.0–370000.0 / 1 YEAR | P3_BACKGROUND |
| Community Engagement Lead, Ohio | Compute | US - Remote |  | OnSite | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 2 | 8+ years | NO |  | USD 176000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Data Center Compute, OpenHouse Savannah 2026 | Compute | US - Remote | Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | LOW | 3 |  | NO |  | USD 125000.0–400000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Development Lead | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 6+ years | NO |  | USD 225000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Development Planner, Industrial Compute | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | REVIEW_SALES_CONTEXT | NONE_DETECTED | 3 | 8+ years | NO |  | USD 225000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Economic Development Lead | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | REVIEW_SALES_CONTEXT | NONE_DETECTED | 2 | 6+ years | NO |  | USD 176000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Infrastructure Operations & Sustainability Lead | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | LOW | 2 | 12+ years | NO |  | USD 223000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Physical Network & Structured Cabling Engineer | Compute | San Francisco | Seattle; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | LOW | 5 | 10+ years | NO |  | USD 257000.0–327000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Data Scientist, Cybersecurity | Data Science | US - Remote | New York City; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 6 | 5+ years | NO |  | USD 263000.0–515000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Compute Infrastructure, Critical Facilities Manager | Datacenter Design | San Francisco | Seattle; US - Remote | OnSite | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 | 8+ years | NO |  | USD 199000.0–302000.0 / 1 YEAR | P2_REVIEW |
| Critical Facilities Lead, Compute Infrastructure | Datacenter Design | US - Remote |  | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | LOW | 2 | 10+ years | NO |  | USD 199000.0–302000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Data Center Infrastructure Electrical Engineer | Datacenter Design | San Francisco | Seattle; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 7 | 10+ years; 15+ years | NO |  | USD 257000.0–327000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Data Center Infrastructure Engineering Program Manager (Network and Whitespace) | Datacenter Design | San Francisco | Seattle; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | LOW | 7 | 10+ years | NO |  | USD 226000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Hardware Operations Engineer | Datacenter Design | San Francisco | Seattle; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 6 | 8+ years | NO |  | USD 157000.0–302000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Industrial Compute | Datacenter Design | US - Remote |  | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | LOW | 3 |  | NO |  | USD 150000.0–300000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Land Development & Due Diligence Lead | Datacenter Design | US - Remote |  | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 1 | 8+ years | NO |  | USD 199000.0–327000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Powered Land Developer, Development & Power Projects | Datacenter Design | US - Remote | Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | LOW | 2 | 6+ years | NO |  | USD 223000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Abuse Investigator - Scams & Fraud | Intelligence & Investigations | US - Remote | New York City; Washington, DC; London, UK | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | LOW | 0 | two years of | NO |  | USD 158400.0–320000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Child Safety Enforcement Specialist | Intelligence & Investigations | San Francisco | Singapore; Dublin, Ireland; US - Remote; London, UK | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 |  | NO |  | USD 158400.0–220000.0 / 1 YEAR | P3_BACKGROUND |
| Software Engineer, Full Stack (People Innovation) | People Innovation Labs | US - Remote | San Francisco | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | LOW | 2 | 4+ years | NO |  | USD 153000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Research Lead, Policy Communications | Product Policy | San Francisco | US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 3 |  | YES | 3 | USD 347000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Product Policy Lead, Regulation | Product Policy | San Francisco | US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 1 |  | YES | 3 | USD 302000.0–335000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Technical Recruiter, Engineering Leadership | Recruiting | US - Remote | Seattle; San Francisco | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 0 |  | NO |  | USD 172000.0–295000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Technical Sourcer, Research SWE | Recruiting | San Francisco | New York City; Seattle; US - Remote |  | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 1 |  | NO |  | USD 136800.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Researcher, Safety Training, National Security | Safety Systems | San Francisco | Washington, DC; US - Remote |  | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 | 4+ years | NO |  | USD 380000.0–500000.0 / 1 YEAR | P3_BACKGROUND |
| Account Director, Digital Native Enterprise | Sales | San Francisco | New York City; Seattle; US - Remote |  | A_US_REMOTE_STRONG | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 | USD 234900.0–290000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Digital Native Large Enterprise | Sales | San Francisco | Seattle; US - Remote |  | A_US_REMOTE_STRONG | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 | USD 176000.0–350000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Digital Native New Business | Sales | San Francisco | New York City; Seattle; US - Remote |  | A_US_REMOTE_STRONG | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 | USD 189000.0–290000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Higher Education | Sales | San Francisco | New York City; Seattle; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | EXCLUDE_STRONG_SALES | MEDIUM | 4 | 10+ years | NO |  | USD 305000.0–352000.0 / 1 YEAR | EXCLUDED_SALES |
| Principal Security Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 3 |  | NO |  | USD 401000.0–510000.0 / 1 YEAR | P2_REVIEW |
| Principal Software Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | NO |  | USD 401000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Security Engineer, Agent Security | Security | San Francisco | US - Remote |  | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | HIGH | 2 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P3_BACKGROUND |
| Security Engineer, Application Security | Security | San Francisco | US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Security Engineer, Detection and Response | Security | San Francisco | New York City; Seattle; US - Remote |  | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | HIGH | 6 |  | NO |  | USD 266000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Security Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 3 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Security Program Manager | Security | US - Remote | New York City; Seattle; Washington, DC; San Francisco | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 5+ years | NO |  | USD 129600.0–310000.0 / 1 YEAR | P2_REVIEW |
| Senior Technical Program Manager - Security | Security | US - Remote | New York City; Seattle; Washington, DC; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 | 5+ years | NO |  | USD 165400.0–285000.0 / 1 YEAR | P3_BACKGROUND |
| Software Engineer, Host Assurance | Security | San Francisco | Seattle; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Security Observability | Security | San Francisco | New York City; Seattle; US - Remote |  | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES |  | USD 293000.0–325000.0 / 1 YEAR | P2_REVIEW |
| Technical Threat Investigator, Threat Intel Engineering | Security | San Francisco | New York City; US - Remote | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES |  | USD 347000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Vendor Security Technical Program Manager | Security | US - Remote | Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | NO |  | USD 231300.0–256500.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Enterprise | Technical Success | San Francisco | New York City; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 | USD 251000.0–278000.0 / 1 YEAR | P1_DEEP_REVIEW |

</details>

## 6. Strong US-remote roles

<details>
<summary>A_US_REMOTE_STRONG (20 rows)</summary>

| title | team | primary | secondary | workplace | location_class | sales | technical | evidence_overlap | years_mentions | relocation | office_days | salary | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Data Center Compute, OpenHouse Savannah 2026 | Compute | US - Remote | Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | LOW | 3 |  | NO |  | USD 125000.0–400000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Development Lead | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 6+ years | NO |  | USD 225000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Development Planner, Industrial Compute | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | REVIEW_SALES_CONTEXT | NONE_DETECTED | 3 | 8+ years | NO |  | USD 225000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Economic Development Lead | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | REVIEW_SALES_CONTEXT | NONE_DETECTED | 2 | 6+ years | NO |  | USD 176000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Infrastructure Operations & Sustainability Lead | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | LOW | 2 | 12+ years | NO |  | USD 223000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Data Scientist, Cybersecurity | Data Science | US - Remote | New York City; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 6 | 5+ years | NO |  | USD 263000.0–515000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Critical Facilities Lead, Compute Infrastructure | Datacenter Design | US - Remote |  | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | LOW | 2 | 10+ years | NO |  | USD 199000.0–302000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Industrial Compute | Datacenter Design | US - Remote |  | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | LOW | 3 |  | NO |  | USD 150000.0–300000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Land Development & Due Diligence Lead | Datacenter Design | US - Remote |  | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 1 | 8+ years | NO |  | USD 199000.0–327000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Powered Land Developer, Development & Power Projects | Datacenter Design | US - Remote | Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | LOW | 2 | 6+ years | NO |  | USD 223000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Account Director, Digital Native Enterprise | Sales | San Francisco | New York City; Seattle; US - Remote |  | A_US_REMOTE_STRONG | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 | USD 234900.0–290000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Digital Native Large Enterprise | Sales | San Francisco | Seattle; US - Remote |  | A_US_REMOTE_STRONG | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 | USD 176000.0–350000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Digital Native New Business | Sales | San Francisco | New York City; Seattle; US - Remote |  | A_US_REMOTE_STRONG | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 | USD 189000.0–290000.0 / 1 YEAR | EXCLUDED_SALES |
| Principal Security Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 3 |  | NO |  | USD 401000.0–510000.0 / 1 YEAR | P2_REVIEW |
| Principal Software Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | NO |  | USD 401000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Security Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 3 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Senior Technical Program Manager - Security | Security | US - Remote | New York City; Seattle; Washington, DC; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 | 5+ years | NO |  | USD 165400.0–285000.0 / 1 YEAR | P3_BACKGROUND |
| Software Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Technical Threat Investigator, Threat Intel Engineering | Security | San Francisco | New York City; US - Remote | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES |  | USD 347000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Vendor Security Technical Program Manager | Security | US - Remote | Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | NO |  | USD 231300.0–256500.0 / 1 YEAR | P1_DEEP_REVIEW |

</details>

## 7. Relocation-supported US roles

These roles explicitly mention relocation assistance. This is preserved as a separate path from remote work; it does not imply permission to begin from Utah.

<details>
<summary>C_US_RELOCATION_SUPPORTED (250 rows)</summary>

| title | team | primary | secondary | workplace | location_class | sales | technical | evidence_overlap | years_mentions | relocation | office_days | salary | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Account Associate - SF | Account Associates | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | LOW | 2 | 3+ years; 3+ years | YES | 3 | USD 108000.0–120000.0 / 1 YEAR | EXCLUDED_SALES |
| Researcher, Alignment CoT Monitorability | Alignment | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES | 3 | USD 295000.0–500000.0 / 1 YEAR | P2_REVIEW |
| Growth - Lifecycle Lead (B2B) | Applied AI | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 | 10+ years | YES | 3 | USD 239000.0–325000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Subject Matter Expert, Investment Banking | Applied AI | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 6 | 2+ years | YES | 3 | USD 185000.0–205000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Android Engineer, Ad Formats | Applied AI Engineering | San Francisco | San Francisco | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 4+ years | YES |  | USD 230000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Android Engineer, Plugin Developer Platform | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 185000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Data Engineer | Applied AI Engineering | San Francisco | Mountain View | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 3+ years; 8+ years | YES |  | USD 235000.0–385000.0 / 1 YEAR | P3_BACKGROUND |
| Data Engineering Manager, Growth & Revenue | Applied AI Engineering | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 6 |  | YES |  | USD 459000.0–536000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Full Stack Software Engineer, Product Explorations | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 0 |  | YES |  | USD 347000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Full-Stack Engineer, ChatGPT Education & Learning | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 3 |  | YES | 3 | USD 185000.0–490000.0 / 1 YEAR | P2_REVIEW |
| Product Manager, Technology Vertical | Applied AI Engineering | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES | 3 | USD 266000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Ad Formats | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 | 7+ years | YES |  | USD 347000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Ads Integrity | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES |  | USD 293000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Ads Manager | Applied AI Engineering | Seattle |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 6 | 7+ years | YES |  | USD 347000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Infrastructure - Core Experimentation | Applied AI Engineering | Seattle |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES |  | USD 347000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Monetization Delivery | Applied AI Engineering | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 4 | 10+ years | YES |  | USD 347000.0–445000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Software Engineer, Monetization Product & Platform | Applied AI Engineering | San Francisco | Seattle |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 7+ years | YES |  | USD 347000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Plugin Developer Platform | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES | 3 | USD 185000.0–490000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Plugin Ecosystem | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 |  | YES | 3 | USD 185000.0–490000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Search Infrastructure | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Shop/Feed Ads | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 |  | YES |  | USD 347000.0–445000.0 / 1 YEAR | P3_BACKGROUND |
| Engineering Manager, Core Services | Applied AI Infrastructure | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 |  | YES |  | USD 293000.0–385000.0 / 1 YEAR | P3_BACKGROUND |
| Software Engineer, Cloud Infrastructure | Applied AI Infrastructure | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 | 5+ years | YES |  | USD 230000.0–490000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Core Services | Applied AI Infrastructure | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 230000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Developer Productivity | Applied AI Infrastructure | San Francisco | New York City; Seattle; Mountain View |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 5+ years; 3+ years | YES |  | USD 210000.0–490000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Resilience Engineering | Applied AI Infrastructure | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES |  | USD 230000.0–490000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Full Stack Software Engineer, Cybersecurity Products | Codex - Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Full Stack Software Engineer, Sales Platform | Codex - Engineering | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 5+ years | YES | 3 | USD 266000.0–455000.0 / 1 YEAR | P2_REVIEW |
| Product Manager, Learning | Codex - Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 0 | 10+ years | YES | 3 | USD 293000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Communications Manager, Monetization | Communications | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 1 | 12+ years | YES |  | USD 297000.0–330000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Internal Communications Lead, Enterprise & Growth | Communications | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 2 | 10+ years; 1-2 years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Internal Communications, Research and Product | Communications | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 | 5+ years | YES | 3 | USD 171000.0–190000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Research Communications Manager | Communications | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 | 7+ years | YES |  | USD 185000.0–205000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategy & Systems Manager, Communications | Communications | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P3_BACKGROUND |
| Performance Modeling Engineer | Compute | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 |  | YES | 3 | USD 347000.0–445000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Performance Modeling Engineer ~2 | Compute | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 | 1–2 years; 2 years of | YES | 3 | USD 347000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Performance Modeling Lead | Compute | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 1 |  | YES | 3 | USD 347000.0–445000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Software Engineer, Agent Infrastructure | Compute | San Francisco | New York City; London, UK |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 230000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Workload Porting & Performance Engineer | Compute | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES | 3 | USD 347000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Personnel Security Specialist | Corporate Security | San Francisco | Washington, DC | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 3 |  | YES | 3 | USD 126000.0–175000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Special Programs Security Manager (CSSO/CPSO) | Corporate Security | Washington, DC | San Francisco | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 |  | YES | 3 | USD 158000.0–225000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Creative Resource Manager, Business Marketing | Creative | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 10+ years | YES | 3 | USD 287000.0–318000.0 / 1 YEAR | P2_REVIEW |
| Applied Data Science & Insights Leader - GTM Intelligence Solutions and Technical Success | Data Science | San Francisco |  | OnSite | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 7 | 10+ years | YES | 3 | USD 441000.0–515000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Data Scientist, Business | Data Science | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 5 | At least 10+ years; 10+ years | YES | 3 | USD 345000.0–440000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Data Scientist, Codex | Data Science | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 5+ years | YES | 3 | USD 230000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Data Scientist, Financial Engineering | Data Science | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 3 | 5+ years | YES | 3 | USD 230000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Data Scientist, Infrastructure | Data Science | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 4 | 5+ years | YES | 3 | USD 230000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Data Scientist, Platform and B2B Products | Data Science | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 4 | 5+ years | YES | 3 | USD 230000.0–385000.0 / 1 YEAR | EXCLUDED_SALES |
| Data Scientist, Product | Data Science | San Francisco | Seattle |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 4 | 5+ years | YES | 3 | USD 230000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Machine Learning Data Scientist, Forecasting | Data Science | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 7+ years | YES | 3 | USD 340000.0–500000.0 / 1 YEAR | P2_REVIEW |
| 3P Systems Architect | Datacenter Design | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 |  | YES | 3 | USD 342000.0–555000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Employee Relations Partner | Employee Relations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 | 10+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Member of Executive Operations | Executive Operations | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 2 | 4 to 12 years; 12 years of | YES | 3 | USD 62.98–110.58 / 1 HOUR | LOW_TECHNICAL_PRIORITY |
| Member of Executive Operations, Seattle | Executive Operations | Seattle |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 2 | 4 to 7 years; 7 years of | YES | 3 | USD 62.98–86.54 / 1 HOUR | LOW_TECHNICAL_PRIORITY |
| Accounting Manager | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 | 6+ years | YES | 3 | USD 162000.0–180000.0 / 1 YEAR | P2_REVIEW |
| Business Systems Lead, Procure-to-Pay | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 8 | 6+ years | YES | 3 | USD 272000.0–302000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Contract Management Lead (Procurement) | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 5 |  | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Corporate Development, Deal Lead | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 12+ years | YES | 3 | USD 333000.0–370000.0 / 1 YEAR | P3_BACKGROUND |
| Head of Sourcing Enablement & Delivery | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 12+ years | YES | 3 | USD 266000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Lead Revenue Accounting, Technical (Strategic Partnerships) | Finance | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 1 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Lead, Revenue Accounting, Technical | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Lead, Technical Accounting (Compute Infrastructure) | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 3 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| M&A Finance Integration Lead | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 1 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | EXCLUDED_SALES |
| Manager, Revenue Accounting, Technical (Strategic Commercial Deals) | Finance | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 5+ years | YES | 3 | USD 162000.0–180000.0 / 1 YEAR | P2_REVIEW |
| Order Management & Billing Lead — Cloud Marketplaces & Partnerships | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 5 | 6+ years | YES | 3 | USD 158000.0–205000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Payroll Initiatives Lead | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 3 | 8+ years | YES | 3 | USD 221000.0–245000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Manager, Accounts Payable - Compute | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 5 | 8+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Manager, Extended Workforce Program | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 4 | 7+ years | YES |  | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Manager, Financial Reporting | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P2_REVIEW |
| Senior Manager, Technical Revenue Accounting, Ads | Finance | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 3 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Sourcing Lead, Professional Services – Human Data | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 3 | 8+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Sourcing Leader, Professional Services | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 4 | 10+ years; 5+ years | YES | 3 | USD 266000.0–295000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Technology Negotiations Lead | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 3 | 10+ years | YES | 3 | USD 234000.0–295000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Tax Director, Business Advisory and Strategic Finance | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 2 | 12+ years | YES | 3 | USD 347000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Full Stack Engineer, Fleet Scheduling | Fleet Clusters | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 230000.0–490000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Fleet Infrastructure | Fleet Clusters | San Francisco | New York City |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 |  | YES | 3 | USD 230000.0–490000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Software Engineer, Fleet Management | Fleet Clusters | San Francisco | New York City |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 230000.0–490000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Research Developer Productivity | Fleet Clusters | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES | 3 | USD 230000.0–325000.0 / 1 YEAR | P2_REVIEW |
| Deployment Lead, FDE - SF | Forward Deployed Engineering | San Francisco | New York City |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 7+ years | YES | 3 | USD 230000.0–294000.0 / 1 YEAR | P2_REVIEW |
| Deployment Lead, FDE- NYC | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 7+ years | YES | 3 | USD 230000.0–294000.0 / 1 YEAR | P2_REVIEW |
| Deployment Lead, Life Sciences- NYC | Forward Deployed Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 7+ years | YES | 3 | USD 207000.0–294000.0 / 1 YEAR | P2_REVIEW |
| Deployment Lead, Semiconductors- SF | Forward Deployed Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 7+ years | YES | 3 | USD 200000.0–295000.0 / 1 YEAR | P2_REVIEW |
| Forward Deployed Engineer (FDE) - SF | Forward Deployed Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 | 5+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P2_REVIEW |
| Forward Deployed Engineer (FDE) - Seattle | Forward Deployed Engineering | Seattle |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 | 5+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P2_REVIEW |
| Forward Deployed Engineer (FDE), Financial Services- NYC | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 6 | 5+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Forward Deployed Engineer (FDE), Healthcare - NYC | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 6+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P2_REVIEW |
| Forward Deployed Engineer (FDE), Healthcare - SF | Forward Deployed Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 6+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P2_REVIEW |
| Forward Deployed Engineer (FDE), Healthcare - Seattle | Forward Deployed Engineering | Seattle |  | OnSite | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 6+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P2_REVIEW |
| Forward Deployed Engineer (FDE), Legal-NYC | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 6 | 5+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Forward Deployed Engineer (FDE), Legal-SF | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 6 | 5+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Forward Deployed Software Engineer - NYC | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 3 | 7+ years | YES | 3 | USD 153000.0–325000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Forward Deployed Software Engineer - SF | Forward Deployed Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 3 | 7+ years | YES | 3 | USD 185000.0–325000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Forward Deployed Software Engineer - Seattle | Forward Deployed Engineering | Seattle |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 3 | 7+ years | YES | 3 | USD 153000.0–325000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Manager, Forward Deployed Engineering- NYC | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 3 | 10+ years; 2+ years | YES | 3 | USD 302000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| RE / RS - Foundations, Search | Foundations | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 1 |  | YES | 3 | USD 380000.0–850000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| US External Affairs Associate, Global Affairs | Global Affairs | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 2 |  | YES |  | USD 171000.0–280000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Hardware / Software CoDesign Engineer - 3P | Hardware | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 3 | 4+ years | YES | 3 | USD 381000.0–485000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Mechanical Engineer, Hardware Systems | Hardware | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 | 7+ years; 10+ years | YES | 3 | USD 266000.0–455000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Networking Operating System Firmware Engineer | Hardware | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Product Manufacturing Engineer - PCBA | Hardware | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES | 3 | USD 207000.0–365000.0 / 1 YEAR | P2_REVIEW |
| Rack Power Engineer | Hardware | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 6 | at least 10 years; 10 years of | YES | 3 | USD 287000.0–485000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Signal Integrity Engineer | Hardware | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 | at least 10 years; 10 years of | YES | 3 | USD 225000.0–445000.0 / 1 YEAR | P3_BACKGROUND |
| Software Engineer, Manufacturing Infrastructure | Hardware | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 | 7+ years | YES |  | USD 310000.0–460000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Systems Software Engineer, Management Plane | Hardware | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 7 | 7+ years | YES |  | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Systems Software Engineer, Security, First Party Hardware | Hardware | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 6 | 7+ years | YES |  | USD 230000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Wireless Regulatory Engineer - SAR | Hardware Engineering | Mountain View | San Francisco | OnSite | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 6 |  | YES | 4 | USD 318000.0–423000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Research Program Manager – Adversarial Model Research | Human Data | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 1 |  | YES | 3 | USD 239000.0–328000.0 / 1 YEAR | P3_BACKGROUND |
| Software Engineer, Research - Human Data | Human Data | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 3 |  | YES | 3 | USD 295000.0–385000.0 / 1 YEAR | P2_REVIEW |
| IT Support Specialist | IT | Seattle | Washington, DC; San Francisco; London, UK | OnSite | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES | 5 | USD 60.58–108.17 / 1 HOUR | P1_DEEP_REVIEW |
| Senior Staff Software Engineer, Identity Infrastructure Engineering | IT | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 10+ years | YES | 3 | USD 347000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Full Stack Engineer, Intelligence Systems | Intelligence & Investigations | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 4+ years | YES | 3 | USD 266000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Red Team Specialist - Cyber | Intelligence & Investigations | San Francisco | Seattle; Washington, DC | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 3 |  | YES | 3 | USD 198000.0–320000.0 / 1 YEAR | P2_REVIEW |
| Senior Counsel, AI Product (Enterprise/API) | Legal | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 8+ years | YES | 3 | USD 330000.0–366000.0 / 1 YEAR | P2_REVIEW |
| Senior Counsel, Commercial (Infrastructure) | Legal | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 2 | 8+ years | YES |  | USD 330000.0–366000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Counsel, Corporate (M&A) | Legal | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 | 8+ years | YES | 3 | USD 280000.0–350000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Counsel, Litigation & Regulatory | Legal | San Francisco | New York City; Washington, DC | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 0 | 10+ years | YES | 3 | USD 330000.0–366000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Product Counsel | Legal | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 8+ years | YES | 3 | USD 330000.0–366000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Enterprise Field Marketer | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 8+ years | YES | 3 | USD 227000.0–252000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Executive Programs Lead, Americas | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 0 | 10+ years | YES |  | USD 287000.0–318000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Global Head of Events | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 1 | 14+ years | YES | 3 | USD 361000.0–401000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Industry Product Marketing Manager | Marketing | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 3 | 6+ years | YES | 3 | USD 221000.0–245000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Marketing Lead, API Models & Research | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 | 12+ years | YES | 3 | USD 374000.0–415000.0 / 1 YEAR | P3_BACKGROUND |
| Product Marketing Lead, ChatGPT Work | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 1 | 12+ years | YES | 3 | USD 284000.0–315000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Marketing Manager, Cybersecurity | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 4 | 7+ years | YES | 3 | USD 221000.0–245000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Marketing Manager, IT Admin and Governance | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 6 | 8+ years | YES | 3 | USD 221000.0–245000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Senior Webinar & Digital Events Strategist | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 2 | 10+ years | YES | 3 | USD 266000.0–295000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Model Policy Manager, Multimodal Safety | Model Policy | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 3 |  | YES | 3 | USD 266000.0–335000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Applied AI Architect, Government | OpenAI for Gov | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | HIGH | 6 |  | YES | 3 | USD 234000.0–335000.0 / 1 YEAR | EXCLUDED_SALES |
| Cyber Enablement Lead, Gov | OpenAI for Gov | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES | 3 | USD 207000.0–230000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Enablement Lead, Government | OpenAI for Gov | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 3 | 6+ years | YES | 3 | USD 207000.0–295000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Federal Account Director, National Security | OpenAI for Gov | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 261000.0–335000.0 / 1 YEAR | EXCLUDED_SALES |
| Forward Deployed Engineer, Gov | OpenAI for Gov | Washington, DC | Seattle; San Francisco | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 | 5+ years | YES | 3 | USD 145800.0–280000.0 / 1 YEAR | P3_BACKGROUND |
| Program Manager, Government Trusted Access | OpenAI for Gov | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 3 | 5–10 years; 10 years of | YES | 3 | USD 162000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Research Engineer / Research Scientist - Personal AGI, Memory | Post-training | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES | 3 | USD 380000.0–500000.0 / 1 YEAR | P2_REVIEW |
| Research Engineer / Research Scientist - Personal AGI, Personalization | Post-training | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES | 3 | USD 380000.0–500000.0 / 1 YEAR | P2_REVIEW |
| Research Engineer / Research Scientist, Health | Post-training | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 4 |  | YES | 3 | USD 380000.0–500000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Research Engineer / Research Scientist- Personal AGI (Post Training) | Post-training | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 380000.0–500000.0 / 1 YEAR | P2_REVIEW |
| Research Engineer/Research Scientist - Personal AGI, North Stars | Post-training | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 380000.0–500000.0 / 1 YEAR | P2_REVIEW |
| Research Engineer/Research Scientist- Personal AGI, Model Experience | Post-training | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 380000.0–500000.0 / 1 YEAR | P2_REVIEW |
| Product Design Lead, Growth - Codex | Product Design | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 0 |  | YES |  | USD 347000.0–405000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Designer, Accessibility | Product Design | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 |  | YES |  | USD 245000.0–310000.0 / 1 YEAR | P2_REVIEW |
| Product Designer, Codex | Product Design | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 |  | YES | 3 | USD 245000.0–310000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Designer, Consumer Verticals | Product Design | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 1 |  | YES |  | USD 245000.0–310000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Designer, Engineering Acceleration | Product Design | Seattle | San Francisco | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES |  | USD 245000.0–310000.0 / 1 YEAR | P2_REVIEW |
| Product Designer, Identity and Safety | Product Design | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES |  | USD 245000.0–310000.0 / 1 YEAR | P2_REVIEW |
| Product Designer, Payments | Product Design | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 |  | YES |  | USD 245000.0–310000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Designer, Youth | Product Design | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 |  | YES |  | USD 245000.0–310000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Manager, API Agents | Product Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 1 | 5+ years | YES |  | USD 293000.0–325000.0 / 1 YEAR | P3_BACKGROUND |
| Product Manager, API Infrastructure | Product Management | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 |  | YES | 3 | USD 325000.0–347000.0 / 1 YEAR | P3_BACKGROUND |
| Product Manager, Core Models | Product Management | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 2 |  | YES | 3 | USD 347000.0–490000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Manager, Enterprise Identity | Product Management | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 10+ years | YES |  | USD 347000.0–490000.0 / 1 YEAR | P3_BACKGROUND |
| Product Manager, Financial Engineering | Product Management | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 1 | 6+ years | YES | 3 | USD 293000.0–325000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Manager, Multimodal Safety | Product Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 2 | 6+ years | YES |  | USD 293000.0–325000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Manager, Sensitive Deployments | Product Management | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 |  | YES |  | USD 347000.0–385000.0 / 1 YEAR | P3_BACKGROUND |
| Product Manager, Youth | Product Management | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 1 | 10+ years | YES |  | USD 293000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Rosalind Life Sciences Product Manager | Product Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 3 |  | YES |  | USD 347000.0–468000.0 / 1 YEAR | P2_REVIEW |
| Research Engineer/Research Scientist, RL/Reasoning | Reasoning | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 3 |  | YES | 3 | USD 295000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Recruiter, AI/ML Research | Recruiting | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 1 |  | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Machine Learning Engineer, Multimodal Perception and Authentication | Research | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES |  | USD 342000.0–399000.0 / 1 YEAR | P2_REVIEW |
| Researcher, Synthetic RL | Research | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 1 |  | YES | 3 | USD 295000.0–445000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Software Engineer - Research Platform, Consumer Devices | Research | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 | 7+ years | YES | 3 | USD 293000.0–325000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Research Program Manager | Research Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 2 | 5+ years | YES | 3 | USD 239000.0–328000.0 / 1 YEAR | P3_BACKGROUND |
| Field Engineer | Robotics | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 7 | 5+ years | YES |  | USD 225000.0–318000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Inference Engineer, Robotics | Robotics | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 1 |  | YES | 3 | USD 380000.0–380000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Lead Safety Engineer, Robotics | Robotics | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 1 |  | YES |  | USD 381000.0–423000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Software Engineer, Distributed Data Systems - Robotics | Robotics | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 |  | YES | 3 | USD 230000.0–385000.0 / 1 YEAR | P3_BACKGROUND |
| Software Engineer, ML Systems & Training Architecture | Robotics | San Francisco |  | OnSite | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES |  | USD 295000.0–380000.0 / 1 YEAR | P2_REVIEW |
| Training - Runtime Foundations Engineer | Runtime | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 266000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Training Performance Engineer | Runtime | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 3 |  | YES | 3 | USD 295000.0–500000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Training: ML Framework Engineer | Runtime | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 3 |  | YES | 3 | USD 295000.0–500000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Research Program Manager, Frontier Assurance | Safety Systems | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 |  | YES | 3 | USD 239000.0–328000.0 / 1 YEAR | P3_BACKGROUND |
| Researcher, Agent Safety, Oversight and System Mitigations | Safety Systems | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 3 |  | YES | 3 | USD 380000.0–500000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Researcher, Agent Safety, Training and Evaluations | Safety Systems | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 |  | YES | 3 | USD 380000.0–500000.0 / 1 YEAR | P3_BACKGROUND |
| Researcher, Multimodal Safety | Safety Systems | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 |  | YES | 3 | USD 380000.0–500000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Account Director, Commercial | Sales | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 3 | at least 3+ years; 5+ years; 3+ years | YES | 3 | USD 198000.0–220000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Digital Natives Growth | Sales | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 189000.0–220500.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Healthcare | Sales | San Francisco | New York City; Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 189000.0–240000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Insurance | Sales | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 3 | 4+ years | YES | 3 | USD 189000.0–240000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Large Enterprise | Sales | San Francisco | New York City; Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 189000.0–240000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Life Sciences | Sales | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 189000.0–240000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Startups Expansion | Sales | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 378000.0–441000.0 / 1 YEAR | EXCLUDED_SALES |
| Strategic Pursuits Lead | Sales | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | NONE_DETECTED | 4 | 10+ years | YES | 3 | USD 302000.0–352000.0 / 1 YEAR | EXCLUDED_SALES |
| Product Manufacturing & Quality Engineer | Scaling | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 3 |  | YES | 3 | USD 123000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Software Engineer, Data Infrastructure | Scaling | San Francisco | New York City; Seattle; Mountain View |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 | 4+ years; 4+ years | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Engineering Manager, Client Platform Engineering | Security | San Francisco | New York City; Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES |  | USD 401000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Forward Deployed Security Engineer | Security | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 | 5+ years | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Network Engineer | Security | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 |  | YES | 3 | USD 347000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Research Engineer, Privacy | Security | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES |  | USD 0.0–500000.0 / 1 YEAR | P2_REVIEW |
| Security Engineer, Application Security | Security | Seattle |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Security Engineer, Application Security | Security | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Privacy Engineering | Security | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES |  | USD 230000.0–325000.0 / 1 YEAR | P2_REVIEW |
| Android Systems Engineer, Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES | 4 | USD 266000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Backend Engineer, Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 | 7+ years | YES | 4 | USD 293000.0–325000.0 / 1 YEAR | P2_REVIEW |
| Camera Software Engineer, Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES |  | USD 347000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Connectivity Software Engineer, Consumer Devices | Software | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 7 |  | YES | 4 | USD 347000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Firmware Engineer, RTOS, Consumer Devices | Software | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 4 | 10+ years | YES | 4 | USD 347000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Release Engineer \| Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES | 4 | USD 207000.0–365000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Private Computing | Software | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 2 | 5+ years | YES |  | USD 230000.0–385000.0 / 1 YEAR | P3_BACKGROUND |
| Software Engineer, Quality & Developer Tools \| Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES | 4 | USD 207000.0–365000.0 / 1 YEAR | P1_DEEP_REVIEW |
| System Performance Engineer, Consumer Devices | Software | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES |  | USD 347000.0–385000.0 / 1 YEAR | P2_REVIEW |
| System Software Engineer, Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 |  | YES |  | USD 347000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Systems Integration Engineer, Build Systems \| Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 5+ years | YES | 4 | USD 207000.0–365000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Systems Integration Manager \| Consumer Devices | Software | San Francisco |  | OnSite | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES | 4 | USD 290000.0–365000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Systems Test Engineer, End-to-End Validation \| Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 |  | YES | 4 | USD 230000.0–290000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Finance Manager - Hardware Consolidations | Strategic Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 2 | 8+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Finance, Ads | Strategic Finance | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 3 | 8+ years; 2+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Finance, B2B Partnerships | Strategic Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 5 | 8+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Finance, International & Marketing | Strategic Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 10+ years; 2+ years | YES | 3 | USD 234000.0–325000.0 / 1 YEAR | P2_REVIEW |
| Strategic Finance, Partnerships | Strategic Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 5 | 8+ years | YES |  | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| AI Support Engineer, Government - San Francisco, CA | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 8 | 8+ years | YES | 3 | USD 180000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| AI Support Engineer, Government - Washington, D.C. | Support Delivery | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 8 | 8+ years | YES | 3 | USD 162000.0–234000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Dedicated Support Engineering Lead | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 12+ years; 6+ years | YES | 3 | USD 284000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Senior Support Engineer - San Francisco | Support Delivery | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 | 8+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Support Delivery Lead | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 10+ years; 5+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | P2_REVIEW |
| Support Delivery Lead | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 8+ years; 4+ years | YES | 3 | USD 284000.0–315000.0 / 1 YEAR | P2_REVIEW |
| Support Delivery Lead, Ads | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 5 | 12+ years; 6+ years | YES | 3 | USD 284000.0–315000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Support Delivery Lead, Government | Support Delivery | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 8 | 12+ years; 6+ years | YES | 3 | USD 284000.0–315000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Support Program Manager, Support Delivery | Support Delivery | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 4 | 8+ years | YES |  | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Technical Program Manager, Support Delivery | Support Delivery | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 4 | 8+ years | YES |  | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Engagement Manager, User Operations | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 3 |  | YES | 3 | USD 279000.0–310000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Engagement Specialist, User Operations | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 8+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P2_REVIEW |
| Support Operations Lead | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 10+ years; 4+ years | YES | 3 | USD 279000.0–310000.0 / 1 YEAR | P3_BACKGROUND |
| Support Vendor Manager | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 5 | 5+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Technical Systems Program Manager, User Operations | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 8+ years | YES |  | USD 216000.0–240000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Collective Communication | Systems | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 |  | YES | 3 | USD 380000.0–500000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Technical Program Manager, AI Safety & Safeguards | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 4 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Technical Program Manager, Cloud AI Partnerships | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Technical Program Manager, Compute Infrastructure | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 5+ years | YES | 3 | USD 257000.0–335000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Technical Program Manager, Developer Velocity | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Technical Program Manager, Enterprise | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Technical Program Manager, Model Deployment & Capacity | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 2 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Technical Program Manager, Multimodal | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Technical Program Manager, Partnerships | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 3 |  | YES | 3 | USD 207000.0–230000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Technical Program Manager, Storage & Data Infrastructure | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 5 |  | YES | 3 | USD 257000.0–445000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Technical Program Manager, Strategic Initiatives | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 3 |  | YES | 3 | USD 257000.0–445000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Applied AI Engineer, API Platform, Digital Natives | Technical Success | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 8+ years | YES | 3 | USD 251000.0–278000.0 / 1 YEAR | P2_REVIEW |
| Applied AI Engineer, API Platform, Digital Natives | Technical Success | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 8+ years | YES | 3 | USD 251000.0–278000.0 / 1 YEAR | P2_REVIEW |
| Applied AI Engineer, Agent Enablement | Technical Success | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 8 | 4–6 years; 6 years of | YES | 3 | USD 197000.0–280000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Plugins | Technical Success | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 7 | 4-6 years; 6 years of | YES | 3 | USD 197000.0–280000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Startups | Technical Success | San Francisco | New York City |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 | 5+ years | YES | 3 | USD 211000.0–278000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Demo Experience Engineer, Technical Success | Technical Success | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 3 |  | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | P2_REVIEW |
| Early Access Deployment Engineer | Technical Success | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 6 | 4+ years | YES | 3 | USD 250000.0–330000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Manager, Applied AI Architect | Technical Success | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 8+ years; 3+ years | YES | 3 | USD 280000.0–300000.0 / 1 YEAR | P2_REVIEW |
| Manager, Applied AI Engineering (Codex) | Technical Success | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 8+ years; 2+ years | YES | 3 | USD 302000.0–335000.0 / 1 YEAR | P2_REVIEW |
| Manager, Applied AI Engineering (Digital Natives) | Technical Success | San Francisco | New York City; Seattle; Mountain View | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 6 | 8+ years; 2+ years | YES | 3 | USD 302000.0–335000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Partner Applied AI Engineer | Technical Success | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 8+ years | YES | 3 | USD 197000.0–278000.0 / 1 YEAR | P2_REVIEW |
| Compensation Business Partner, GTM | Total Rewards | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 1 | 6+ years | YES | 3 | USD 180000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Researcher, Training | Training | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 1 |  | YES | 3 | USD 300000.0–600000.0 / 1 YEAR | P3_BACKGROUND |
| Cyber Operations Lead, Critical Harm Operations | Trust & Safety | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 5 | 8+ years; 4+ years | YES | 3 | USD 252000.0–335000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| User Safety & Risk Operations Analyst - Global Response (Weekend Shift) | Trust & Safety | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 4 | 5+ years | YES | 3 | USD 189000.0–210000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |

</details>

## 8. Revised NO SALES analysis

v0.15 separates strong exclusion evidence from contextual sales-adjacent terms. It also uses word-boundary regexes so terms such as **commissioning** do not match **commission**.

<details>
<summary>Strong sales exclusions (84 rows)</summary>

| title | team | primary | secondary | workplace | location_class | sales | technical | evidence_overlap | years_mentions | relocation | office_days | salary | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APAC Sales Development Leader | Account Associates | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 2 | 10+ years | NO |  |  | EXCLUDED_SALES |
| Account Associate - EMEA | Account Associates | Dublin, Ireland |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | LOW | 2 | 6+ years; 4+ years | YES | 3 |  | EXCLUDED_SALES |
| Account Associate - EMEA (German Speaking) | Account Associates | Dublin, Ireland |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | LOW | 2 | 6+ years; 4+ years | YES | 3 |  | EXCLUDED_SALES |
| Account Associate - SF | Account Associates | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | LOW | 2 | 3+ years; 3+ years | YES | 3 | USD 108000.0–120000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Associate - Singapore (ANZ Market) | Account Associates | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | LOW | 2 | 6+ years; 4+ years | NO |  |  | EXCLUDED_SALES |
| Account Associate - Singapore (Korean-speaking) | Account Associates | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | LOW | 2 | 6+ years; 4+ years | NO |  |  | EXCLUDED_SALES |
| Account Associate, Japan | Account Associates | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | LOW | 4 | 5+ years; 7-10 years; 10 years of | NO |  |  | EXCLUDED_SALES |
| Account Associate- EMEA (French Speaking) | Account Associates | Dublin, Ireland |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | LOW | 2 | 6+ years; 4+ years; 2-3 years; 3 years of | YES | 3 |  | EXCLUDED_SALES |
| Sales Development Leader - Tokyo | Account Associates | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | LOW | 4 | 10+ years | NO |  |  | EXCLUDED_SALES |
| Sales Development Manager, Enterprise (AMER) | Account Associates | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | NONE_DETECTED | 4 | 10+ years | NO |  | USD 261000.0–305000.0 / 1 YEAR | EXCLUDED_SALES |
| Client Partner, Ads Solutions | Ads Solutions | San Francisco | New York City |  | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 | 10+ years; 3+ years | NO |  | USD 239000.0–273000.0 / 1 YEAR | EXCLUDED_SALES |
| Client Partner, Ads Solutions (Spanish Speaking) | Ads Solutions | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 | 10+ years; 3+ years | YES | 3 |  | EXCLUDED_SALES |
| Client Partner, Ads Solutions - Travel | Ads Solutions | San Francisco | New York City | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 | 10+ years; 3+ years | NO |  | USD 216000.0–273000.0 / 1 YEAR | EXCLUDED_SALES |
| Partner Solutions Engineer, Ads Solutions - San Francisco | Ads Solutions | San Francisco |  |  | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | NONE_DETECTED | 7 | 5+ years | NO |  | USD 234000.0–260000.0 / 1 YEAR | EXCLUDED_SALES |
| Regional Client Partner, Ads Solutions (Mumbai) | Ads Solutions | Mumbai, India |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 | 10+ years; 3+ years | YES | 3 |  | EXCLUDED_SALES |
| Regional Manager, Ads Solutions (APAC) | Ads Solutions | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 2 | 12+ years; 5+ years | YES | 3 |  | EXCLUDED_SALES |
| Solutions Engineer, Ads Solutions - San Francisco | Ads Solutions | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | NONE_DETECTED | 7 | 5+ years | NO |  | USD 234000.0–260000.0 / 1 YEAR | EXCLUDED_SALES |
| Solutions Engineer, Ads Solutions - Singapore | Ads Solutions | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 7 | 5+ years | NO |  |  | EXCLUDED_SALES |
| Growth - Digital Marketing (Enterprise) | Applied AI | San Francisco | New York City | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | LOW | 4 | 10+ years; 6+ years | NO |  | USD 239000.0–325000.0 / 1 YEAR | EXCLUDED_SALES |
| Software Engineer, Caching Infrastructure | Applied AI Infrastructure | San Francisco |  |  | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | LOW | 4 | 5+ years | NO |  | USD 230000.0–385000.0 / 1 YEAR | EXCLUDED_SALES |
| Data Scientist, B2B Demand Generation, Growth & Measurement | Data Science | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | MEDIUM | 6 | 10+ years | NO |  | USD 293000.0–385000.0 / 1 YEAR | EXCLUDED_SALES |
| Data Scientist, Platform and B2B Products | Data Science | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 4 | 5+ years | YES | 3 | USD 230000.0–385000.0 / 1 YEAR | EXCLUDED_SALES |
| M&A Finance Integration Lead | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 1 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | EXCLUDED_SALES |
| B2B Marketing Manager, DACH | Marketing | Munich, Germany |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 3 | 12+ years | NO |  |  | EXCLUDED_SALES |
| Lead, Ads Prospecting & Customer Intelligence | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  | USD 287000.0–318000.0 / 1 YEAR | EXCLUDED_SALES |
| Applied AI Architect, Government | OpenAI for Gov | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | HIGH | 6 |  | YES | 3 | USD 234000.0–335000.0 / 1 YEAR | EXCLUDED_SALES |
| Capture Manager, OpenAI for Government | OpenAI for Gov | Washington, DC |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 | 10+ years | NO |  | USD 221000.0–295000.0 / 1 YEAR | EXCLUDED_SALES |
| Federal Account Director, National Security | OpenAI for Gov | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 261000.0–335000.0 / 1 YEAR | EXCLUDED_SALES |
| Global Account Director, International Organisations, ME & LATAM | OpenAI for Gov | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | LOW | 3 | 10+ years | YES | 3 |  | EXCLUDED_SALES |
| Partner Director, HCL, Wipro & Cognizant | Partnerships | San Francisco | Seattle | OnSite | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | LOW | 3 |  | NO |  | USD 380000.0–420000.0 / 1 YEAR | EXCLUDED_SALES |
| AWS Specialist Seller, Strategic Pursuits | Sales | San Francisco | Seattle |  | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | LOW | 2 | 15+ years | NO |  | USD 302000.0–335000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Commercial | Sales | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 3 | at least 3+ years; 5+ years; 3+ years | YES | 3 | USD 198000.0–220000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Digital Native | Sales | Seoul, South Korea |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 |  | EXCLUDED_SALES |
| Account Director, Digital Native Enterprise | Sales | San Francisco | New York City; Seattle; US - Remote |  | A_US_REMOTE_STRONG | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 | USD 234900.0–290000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Digital Native Large Enterprise | Sales | San Francisco | Seattle; US - Remote |  | A_US_REMOTE_STRONG | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 | USD 176000.0–350000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Digital Native New Business | Sales | San Francisco | New York City; Seattle; US - Remote |  | A_US_REMOTE_STRONG | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 | USD 189000.0–290000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Digital Natives | Sales | Sydney, Australia |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 |  | YES | 3 |  | EXCLUDED_SALES |
| Account Director, Digital Natives | Sales | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 |  | EXCLUDED_SALES |
| Account Director, Digital Natives | Sales | Delhi, India | Mumbai, India | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | NO |  |  | EXCLUDED_SALES |
| Account Director, Digital Natives - France | Sales | Paris, France |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | NO | 3 |  | EXCLUDED_SALES |
| Account Director, Digital Natives - Nordics | Sales | Stockholm, Sweden |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | NO | 3 |  | EXCLUDED_SALES |
| Account Director, Digital Natives Growth | Sales | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 189000.0–220500.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Digital Natives \| MENA | Sales | Abu Dhabi, UAE |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | NO | 3 |  | EXCLUDED_SALES |
| Account Director, Financial Services Industry - Japan | Sales | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 |  | YES | 3 |  | EXCLUDED_SALES |
| Account Director, Government | Sales | Australia - Remote | Sydney, Australia | Remote | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | LOW | 4 | 10+ years | NO |  |  | EXCLUDED_SALES |
| Account Director, Healthcare | Sales | San Francisco | New York City; Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 189000.0–240000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Higher Education | Sales | San Francisco | New York City; Seattle; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | EXCLUDE_STRONG_SALES | MEDIUM | 4 | 10+ years | NO |  | USD 305000.0–352000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Insurance | Sales | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 3 | 4+ years | YES | 3 | USD 189000.0–240000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Large Enterprise | Sales | Seoul, South Korea |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 |  | EXCLUDED_SALES |
| Account Director, Large Enterprise | Sales | London, UK |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 |  | NO |  |  | EXCLUDED_SALES |
| Account Director, Large Enterprise | Sales | San Francisco | New York City; Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 189000.0–240000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Large Enterprise | Sales | Munich, Germany | Berlin, Germany | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 |  | NO |  |  | EXCLUDED_SALES |
| Account Director, Large Enterprise | Sales | Delhi, India | India - Remote | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 |  | NO |  |  | EXCLUDED_SALES |
| Account Director, Large Enterprise | Sales | Sydney, Australia |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 |  | EXCLUDED_SALES |
| Account Director, Large Enterprise (FSI) | Sales | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 1 |  | YES | 3 |  | EXCLUDED_SALES |
| Account Director, Large Enterprise - Tokyo | Sales | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 |  | YES | 3 |  | EXCLUDED_SALES |
| Account Director, Life Sciences | Sales | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 189000.0–240000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Mid-Market | Sales | Sydney, Australia |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 3 |  | NO |  |  | EXCLUDED_SALES |
| Account Director, Mid-Market | Sales | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 3 |  | NO |  |  | EXCLUDED_SALES |
| Account Director, Mid-Market | Sales | India - Remote | Mumbai, India; Delhi, India | Remote | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 3 |  | NO |  |  | EXCLUDED_SALES |
| Account Director, Public Sector - Tokyo | Sales | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 1 |  | YES | 3 |  | EXCLUDED_SALES |
| Account Director, Startups | Sales | Stockholm, Sweden |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 2 |  | NO |  |  | EXCLUDED_SALES |
| Account Director, Startups (Mandarin-Speaking) | Sales | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | NO | 3 |  | EXCLUDED_SALES |
| Account Director, Startups Expansion | Sales | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | YES | 3 | USD 378000.0–441000.0 / 1 YEAR | EXCLUDED_SALES |
| Account Director, Startups \| Tokyo | Sales | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 2 |  | NO |  |  | EXCLUDED_SALES |
| Senior Vendor Manager - SMB Sales | Sales | Dublin, Ireland |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 8 | 8+ years | NO |  |  | EXCLUDED_SALES |
| Strategic Pursuits Lead | Sales | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | EXCLUDE_STRONG_SALES | NONE_DETECTED | 4 | 10+ years | YES | 3 | USD 302000.0–352000.0 / 1 YEAR | EXCLUDED_SALES |
| Technical Program Manager, Applied Infrastructure | Technical Program Management | San Francisco |  |  | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | LOW | 4 | 7+ years | NO |  | USD 257000.0–445000.0 / 1 YEAR | EXCLUDED_SALES |
| Applied AI Architect | Technical Success | Delhi, India | Mumbai, India; Bangalore - Remote | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | YES | 3 |  | EXCLUDED_SALES |
| Applied AI Architect | Technical Success | San Francisco |  |  | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  | USD 156600.0–276000.0 / 1 YEAR | EXCLUDED_SALES |
| Applied AI Architect | Technical Success | Seoul, South Korea |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | YES | 3 |  | EXCLUDED_SALES |
| Applied AI Architect | Technical Success | Sydney, Australia |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | YES | 3 |  | EXCLUDED_SALES |
| Applied AI Architect | Technical Success | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | YES | 3 |  | EXCLUDED_SALES |
| Applied AI Architect | Technical Success | New York City |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  | USD 156600.0–276000.0 / 1 YEAR | EXCLUDED_SALES |
| Applied AI Architect - Tokyo | Technical Success | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  |  | EXCLUDED_SALES |
| Applied AI Architect, Digital Natives | Technical Success | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  |  | EXCLUDED_SALES |
| Applied AI Architect, Digital Natives | Technical Success | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  | USD 221000.0–278000.0 / 1 YEAR | EXCLUDED_SALES |
| Applied AI Architect, Digital Natives (Strategics) | Technical Success | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  | USD 218000.0–278000.0 / 1 YEAR | EXCLUDED_SALES |
| Applied AI Architect, Education | Technical Success | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | HIGH | 6 |  | YES | 3 |  | EXCLUDED_SALES |
| Applied AI Architect, Enterprise | Technical Success | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  | USD 221000.0–276000.0 / 1 YEAR | EXCLUDED_SALES |
| Applied AI Architect, Healthcare & Life Sciences | Technical Success | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  | USD 221000.0–278000.0 / 1 YEAR | EXCLUDED_SALES |
| Applied AI Architect, Large Enterprise | Technical Success | London, UK |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | YES | 3 |  | EXCLUDED_SALES |
| Applied AI Architect, Large Enterprise | Technical Success | Munich, Germany |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  |  | EXCLUDED_SALES |
| Applied AI Architect, Retail | Technical Success | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | MEDIUM | 6 |  | NO |  | USD 217000.0–276000.0 / 1 YEAR | EXCLUDED_SALES |

</details>

<details>
<summary>Sales context requiring manual review (210 rows)</summary>

| title | team | primary | secondary | workplace | location_class | sales | technical | evidence_overlap | years_mentions | relocation | office_days | salary | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Agency Partner, Ads Solutions | Ads Solutions | New York City |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 |  | NO |  | USD 216000.0–273000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| EMEA Vendor Lead, Ad Sales | Ads Solutions | Dublin, Ireland |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 5+ years | NO | 3 |  | P3_BACKGROUND |
| Applied AI Software Engineer, GTM Growth Engineering | Applied AI | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 6 | 4+ years | NO |  | USD 266000.0–405000.0 / 1 YEAR | P2_REVIEW |
| Growth - Digital Marketing (Business) | Applied AI | San Francisco | New York City | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 4 | 8+ years; 6+ years | NO |  | USD 239000.0–325000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Software Engineer, GTM Growth Engineering | Applied AI | San Francisco |  | OnSite | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 4 | 4+ years | NO |  | USD 266000.0–405000.0 / 1 YEAR | P3_BACKGROUND |
| Software Engineer, Native Learning Experiences | Applied AI | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 5 | 5+ years; 5+ years | NO |  | USD 266000.0–385000.0 / 1 YEAR | P3_BACKGROUND |
| Data Engineer | Applied AI Engineering | San Francisco | Mountain View | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 3+ years; 8+ years | YES |  | USD 235000.0–385000.0 / 1 YEAR | P3_BACKGROUND |
| Data Engineer, Core Experimentation | Applied AI Engineering | Seattle |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 3+ years; 8+ years | NO |  | USD 347000.0–385000.0 / 1 YEAR | P3_BACKGROUND |
| Data Engineering Manager, Growth & Revenue | Applied AI Engineering | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 6 |  | YES |  | USD 459000.0–536000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Ads Manager | Applied AI Engineering | Seattle |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 6 | 7+ years | YES |  | USD 347000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Enterprise Verticals | Applied AI Engineering | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 6 |  | NO |  | USD 293000.0–325000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Financial Engineering | Applied AI Engineering | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 2 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P3_BACKGROUND |
| Software Engineer, Healthcare | Applied AI Engineering | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 7 | 5+ years | NO |  | USD 347000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Monetization Data Systems | Applied AI Engineering | Mountain View |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 6 | minimum of 7+ years; 7+ years | NO |  | USD 293000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Staff & Software Engineer, Payments & Billing, Consumer Monetization | Applied AI Engineering | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 5 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P3_BACKGROUND |
| Tech Lead Manager, Education | Applied AI Engineering | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 2 |  | NO |  | USD 401000.0–445000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Full Stack Software Engineer, Sales Platform | Codex - Engineering | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 5+ years | YES | 3 | USD 266000.0–455000.0 / 1 YEAR | P2_REVIEW |
| Product Manager, Learning | Codex - Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 0 | 10+ years | YES | 3 | USD 293000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Software Engineer, Codex Enterprise | Codex - Engineering | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 4 |  | NO |  | USD 230000.0–385000.0 / 1 YEAR | P3_BACKGROUND |
| Developer Experience Engineer, Cyber | Codex – Developer Experience | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 5 |  | NO |  | USD 198000.0–335000.0 / 1 YEAR | P3_BACKGROUND |
| B2B Communications Manager, LATAM | Communications | São Paulo |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 0 |  | NO |  |  | P3_BACKGROUND |
| Communications Manager, Monetization | Communications | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 1 | 12+ years | YES |  | USD 297000.0–330000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Internal Communications Lead, Enterprise & Growth | Communications | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 2 | 10+ years; 1-2 years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Business Development Lead, Compute Strategy | Compute | US - Remote | New York City; Seattle; San Francisco | Hybrid | B_US_REMOTE_AMBIGUOUS | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 8+ years | NO |  | USD 333000.0–370000.0 / 1 YEAR | P3_BACKGROUND |
| Capacity Systems Software Engineer | Compute | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 5 | 5+ years | NO |  | USD 347000.0–445000.0 / 1 YEAR | P3_BACKGROUND |
| Development Lead | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 6+ years | NO |  | USD 225000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Development Planner, Industrial Compute | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | REVIEW_SALES_CONTEXT | NONE_DETECTED | 3 | 8+ years | NO |  | USD 225000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Economic Development Lead | Compute | US - Remote |  | Remote | A_US_REMOTE_STRONG | REVIEW_SALES_CONTEXT | NONE_DETECTED | 2 | 6+ years | NO |  | USD 176000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Infrastructure Sourcing Operations Lead | Compute | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 6 | 8+ years | NO |  | USD 226000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Software Engineer, API Enterprise Controls | Core Product & Platform \| API | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 6 | 9+ years | NO |  | USD 266000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Creative Resource Manager, Business Marketing | Creative | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 10+ years | YES | 3 | USD 287000.0–318000.0 / 1 YEAR | P2_REVIEW |
| Analytics Engineer, GTM | Data Science | San Francisco | New York City | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 6 | 10+ years | NO |  | USD 220000.0–335000.0 / 1 YEAR | P2_REVIEW |
| Applied Data Science & Insights Leader - GTM Intelligence Solutions and Technical Success | Data Science | San Francisco |  | OnSite | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 7 | 10+ years | YES | 3 | USD 441000.0–515000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Data Scientist, B2B Strategy & Intelligence | Data Science | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 4 |  | NO |  | USD 347000.0–510000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Data Scientist, Business | Data Science | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 5 | At least 10+ years; 10+ years | YES | 3 | USD 345000.0–440000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Data Scientist, SMB Ads Growth | Data Science | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 5 | 5+ years | NO |  | USD 293000.0–515000.0 / 1 YEAR | P3_BACKGROUND |
| Machine Learning Data Scientist, Forecasting | Data Science | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 7+ years | YES | 3 | USD 340000.0–500000.0 / 1 YEAR | P2_REVIEW |
| Strategic Sourcing Manager, Compute Infrastructure | Datacenter Design | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 10+ years | NO |  | USD 226000.0–285000.0 / 1 YEAR | P3_BACKGROUND |
| Strategic Sourcing Manager, Data Center Infrastructure, Electrical | Datacenter Design | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 2 | 8+ years | NO |  | USD 226000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Sourcing Manager, Data Center Infrastructure, Mechanical | Datacenter Design | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 2 | 8+ years | NO |  | USD 226000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Sourcing Manager, Data Center Infrastructure, Owner Furnished Equipment | Datacenter Design | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 2 | 8+ years | NO |  | USD 226000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Contract Management Lead (Procurement) | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 5 |  | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Corporate Development, Deal Lead | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 12+ years | YES | 3 | USD 333000.0–370000.0 / 1 YEAR | P3_BACKGROUND |
| Deal Operations, EMEA | Finance | Dublin, Ireland |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 4 | 8+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Head of Sourcing Enablement & Delivery | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 12+ years | YES | 3 | USD 266000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Lead Revenue Accounting, Technical (Strategic Partnerships) | Finance | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 1 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Lead, Revenue Accounting, Technical | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Lead, Technical Accounting (Compute Infrastructure) | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 3 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Manager, Revenue Accounting | Finance | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 3 |  | NO |  | USD 162000.0–180000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Manager, Revenue Accounting, Technical (Strategic Commercial Deals) | Finance | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 5+ years | YES | 3 | USD 162000.0–180000.0 / 1 YEAR | P2_REVIEW |
| Order Management & Billing Lead — Cloud Marketplaces & Partnerships | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 5 | 6+ years | YES | 3 | USD 158000.0–205000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Pricing Operations Lead | Finance | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 4 | 6+ years | NO |  | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Pricing Strategist, GTM | Finance | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 0 |  | NO |  | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Manager, Technical Revenue Accounting, Ads | Finance | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 3 | 10+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Sourcing Lead, Professional Services – Human Data | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 3 | 8+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Sourcing Leader, Professional Services | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 4 | 10+ years; 5+ years | YES | 3 | USD 266000.0–295000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Technology Negotiations Lead | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 3 | 10+ years | YES | 3 | USD 234000.0–295000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Tax Director, Business Advisory and Strategic Finance | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 2 | 12+ years | YES | 3 | USD 347000.0–385000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Forward Deployed Engineer (FDE), Financial Services- NYC | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 6 | 5+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Forward Deployed Engineer (FDE), Healthcare - NYC | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 6+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P2_REVIEW |
| Forward Deployed Engineer (FDE), Healthcare - SF | Forward Deployed Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 6+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P2_REVIEW |
| Forward Deployed Engineer (FDE), Healthcare - Seattle | Forward Deployed Engineering | Seattle |  | OnSite | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 6+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P2_REVIEW |
| Backend Software Engineer, GTM Innovation | GTM Innovation | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 4 | 6+ years | NO |  | USD 347000.0–445000.0 / 1 YEAR | P3_BACKGROUND |
| Agent Standards Architect, Global Affairs | Global Affairs | Washington, DC | New York City | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 3 |  | NO |  | USD 171000.0–280000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Applied AI Engineer | Go To Market | Abu Dhabi, UAE |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer, Digital Natives | Go To Market | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| GTM Strategy & Operations, Policy | Go To Market | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 1 |  | NO |  | USD 239000.0–265000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| APAC Vendor Lead, Ads - Singapore | Growth | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 5+ years | YES | 3 |  | P3_BACKGROUND |
| APAC Vendor Lead, Ads - Sydney | Growth | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 5+ years | YES | 3 |  | P3_BACKGROUND |
| Growth Lead, France | Growth | Paris, France |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | LOW | 2 | 10+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Growth Lead, Japan | Growth | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | LOW | 2 | 10+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Growth Lead, SEA | Growth | Singapore | Singapore | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | LOW | 2 | 10+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| North America Vendor Lead, Ads | Growth | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 5+ years | NO |  | USD 239000.0–239000.0 / 1 YEAR | P3_BACKGROUND |
| Hardware Strategic Sourcing & Manufacturing Partnerships Manager | Hardware | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 3 |  | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Hardware Strategic Sourcing Manager, Optics | Hardware | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 6 |  | NO |  | USD 226000.0–378000.0 / 1 YEAR | P2_REVIEW |
| Supply Chain Program Manager (SCPM) - AI Infrastructure | Hardware | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 2 | 8+ years | NO |  | USD 226000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Program Manager, Technology Capital Builds | IT | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 3 |  | NO |  |  | P3_BACKGROUND |
| Associate General Counsel, Commercial – Infrastructure | Legal | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 2 | 12+ years | NO |  | USD 381000.0–423000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Counsel, Commercial | Legal | San Francisco |  | Hybrid | D_US_ONSITE_OR_HYBRID | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 7+ years | NO | 3 | USD 252000.0–280000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Legal Contract Manager, Public Sector | Legal | Washington, DC |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 7+ years | NO |  | USD 216000.0–240000.0 / 1 YEAR | P3_BACKGROUND |
| Senior Commercial Counsel, APAC | Legal | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 10+ years | NO | 3 |  | LOW_TECHNICAL_PRIORITY |
| Senior Counsel, AI Product (Enterprise/API) | Legal | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 8+ years | YES | 3 | USD 330000.0–366000.0 / 1 YEAR | P2_REVIEW |
| Senior Counsel, Commercial (Infrastructure) | Legal | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 2 | 8+ years | YES |  | USD 330000.0–366000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Counsel, France | Legal | Paris, France |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 |  | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Senior Product Counsel | Legal | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 8+ years | YES | 3 | USD 330000.0–366000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Ads Marketing Manager, Japan | Marketing | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | LOW | 2 |  | NO |  |  | LOW_TECHNICAL_PRIORITY |
| B2B Marketing Lead, ANZ | Marketing | Sydney, Australia |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 3 | 10+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| B2B Marketing Lead, India | Marketing | Mumbai, India |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 10+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Consumer Marketing Lead, Korea | Marketing | Seoul, South Korea |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 10+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Enterprise Field Marketer | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 8+ years | YES | 3 | USD 227000.0–252000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Executive Programs Lead, Americas | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 0 | 10+ years | YES |  | USD 287000.0–318000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Global Head of Events | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 1 | 14+ years | YES | 3 | USD 361000.0–401000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Growth Marketing Manager - Web & Organic, SMB Ads | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 4–7 years; 7 years of | NO |  | USD 198000.0–219000.0 / 1 YEAR | P3_BACKGROUND |
| Growth Marketing Manager, SMB Ads | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 7 | 4-7 years; 7 years of | NO |  | USD 198000.0–219000.0 / 1 YEAR | P2_REVIEW |
| Industry Product Marketing Manager | Marketing | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 3 | 6+ years | YES | 3 | USD 221000.0–245000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Integrated Marketing Manager, EMEA | Marketing | Dublin, Ireland |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 2 |  | NO |  |  | P3_BACKGROUND |
| Integrated Marketing Manager, Hardware | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 3 | 5–8 years; 8 years of | NO |  | USD 225000.0–250000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Integrated Marketing Manager, Product & Model Launches | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 0 | 10+ years | NO |  | USD 287000.0–318000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Lifecycle Marketing Manager, SMB Ads | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 3 |  | NO |  | USD 227000.0–252000.0 / 1 YEAR | P3_BACKGROUND |
| Partner Marketing Manager, Ads | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 3 | 8+ years | NO |  | USD 227000.0–252000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Partner Marketing Manager, Technology Partners & ISVs | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 0 | 10+ years | NO |  | USD 287000.0–318000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Marketing Lead, ChatGPT Work | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 1 | 12+ years | YES | 3 | USD 284000.0–315000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Marketing Manager, Advertising | Marketing | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 |  | NO |  | USD 225000.0–250000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Marketing Manager, Cybersecurity | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 4 | 7+ years | YES | 3 | USD 221000.0–245000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Marketing Manager, IT Admin and Governance | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 6 | 8+ years | YES | 3 | USD 221000.0–245000.0 / 1 YEAR | P1_DEEP_REVIEW |
| SMB Innovation Sales & Strategy Lead | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 2 | 8-10 years; 10 years of | NO |  | USD 227000.0–252000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Scaled Programs Lead, SMB Ads | Marketing | San Francisco | New York City | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 |  | NO |  | USD 287000.0–318000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Senior Web Experience Strategist | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 2 | 10+ years | NO |  | USD 287000.0–318000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Startup Content Marketing Manager | Marketing | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 2 | 4+ years | NO |  | USD 198000.0–219000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Applied AI Engineer, Government, International | OpenAI for Gov | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 5 |  | YES | 3 |  | P3_BACKGROUND |
| Partnerships Operations Lead, OAI for Government | OpenAI for Gov | Washington, DC |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 3 | 7+ years | NO |  | USD 221000.0–266000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Delivery Lead, Cyber | OpenAI for Gov | Washington, DC |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 5 | 10+ years | NO |  | USD 266000.0–370000.0 / 1 YEAR | P3_BACKGROUND |
| Strategy and Operations, OpenAI for Government | OpenAI for Gov | Washington, DC |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 3 |  | NO |  | USD 221000.0–258000.0 / 1 YEAR | P3_BACKGROUND |
| Business Development Manager, Product Partnerships | Partnerships | Munich, Germany |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 0 | 10+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Business Development Manager, Product Partnerships | Partnerships | Paris, France |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 0 | 10+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Head of Marketplace | Partnerships | New York City | New York City | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 15+ years | NO |  | USD 400000.0–445000.0 / 1 YEAR | P3_BACKGROUND |
| Partner Director - AWS Alliance Partnership, Japan | Partnerships | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 8+ years | NO |  |  | P3_BACKGROUND |
| Partner Director, ANZ | Partnerships | Sydney, Australia |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | LOW | 5 | 7+ years | YES | 3 |  | LOW_TECHNICAL_PRIORITY |
| Partner Director, McKinsey Alliance | Partnerships | San Francisco |  | OnSite | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 |  | NO |  | USD 380000.0–420000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Partner Director, PwC | Partnerships | San Francisco | New York City; Seattle | OnSite | D_US_ONSITE_OR_HYBRID | REVIEW_SALES_CONTEXT | LOW | 2 |  | NO | 3 | USD 380000.0–420000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Business Recruiter, APAC | People | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 | 7+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Product Design Lead, Growth - Codex | Product Design | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 0 |  | YES |  | USD 347000.0–405000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Designer, Accessibility | Product Design | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 |  | YES |  | USD 245000.0–310000.0 / 1 YEAR | P2_REVIEW |
| Product Manager, Enterprise Identity | Product Management | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 10+ years | YES |  | USD 347000.0–490000.0 / 1 YEAR | P3_BACKGROUND |
| Product Manager, Financial Services | Product Management | San Francisco | New York City |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 4 |  | NO |  | USD 401000.0–530000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Rosalind Life Sciences Product Manager | Product Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 3 |  | YES |  | USD 347000.0–468000.0 / 1 YEAR | P2_REVIEW |
| Platform Product Partnerships Lead | Product Partnerships | San Francisco | New York City | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 2 | 10+ years | NO |  | USD 266000.0–370000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Research Program Manager, Data Acquisition | Research Program Management | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 5 |  | NO |  | USD 239000.0–328000.0 / 1 YEAR | P3_BACKGROUND |
| Product Manufacturing & Quality Engineer | Scaling | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 3 |  | YES | 3 | USD 123000.0–285000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| IT Software Architect, SaaS Enablement and Governance | Security | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 7 | 10+ years | NO |  | USD 266000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, HSM Infrastructure Security, Consumer Devices | Software | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 5 | 5+ years | NO |  | USD 347000.0–445000.0 / 1 YEAR | P3_BACKGROUND |
| Business Lead, Special Situations | Special Situations | San Francisco | New York City | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 |  | NO |  | USD 333000.0–370000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Deal Lead, Special Situations | Special Situations | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 0 |  | NO |  | USD 333000.0–401000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Physical Engineering Business Lead (Special Situations) | Special Situations | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 2 |  | NO |  | USD 333000.0–370000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Finance Manager - Hardware Consolidations | Strategic Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 2 | 8+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Pricing Strategist | Strategic Finance | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 1 | 6+ years; 3+ years | NO |  | USD 234000.0–260000.0 / 1 YEAR | P3_BACKGROUND |
| Strategic Finance, Ads | Strategic Finance | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 3 | 8+ years; 2+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Finance, B2B Partnerships | Strategic Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 5 | 8+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Finance, B2B Product | Strategic Finance | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 3 | 7+ years | NO |  | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Strategic Finance, Compute | Strategic Finance | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 7+ years | NO |  | USD 234000.0–260000.0 / 1 YEAR | P3_BACKGROUND |
| Strategic Finance, International & Marketing | Strategic Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 10+ years; 2+ years | YES | 3 | USD 234000.0–325000.0 / 1 YEAR | P2_REVIEW |
| Strategic Finance, Partnerships | Strategic Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 5 | 8+ years | YES |  | USD 234000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Deal Operations, APAC | Strategy & Operations | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 4 | 8+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| GTM Strategy & Operations, Professional Services | Strategy & Operations | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 8+ years | NO |  | USD 293000.0–325000.0 / 1 YEAR | P3_BACKGROUND |
| Strategy & Operations Lead, UK | Strategy & Operations | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | NONE_DETECTED | 1 |  | YES | 3 |  | LOW_TECHNICAL_PRIORITY |
| AI Support Engineer - Dublin | Support Delivery | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | NO |  |  | P3_BACKGROUND |
| AI Support Engineer - Dublin (Weekend Shift) | Support Delivery | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | NO |  |  | P3_BACKGROUND |
| AI Support Engineer - San Francisco | Support Delivery | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | NO |  | USD 180000.0–260000.0 / 1 YEAR | P2_REVIEW |
| AI Support Engineer - San Francisco (Weekend Shift) | Support Delivery | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | NO |  | USD 180000.0–260000.0 / 1 YEAR | P2_REVIEW |
| AI Support Engineer - Singapore | Support Delivery | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Singapore (Korean Speaking) | Support Delivery | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Singapore (Weekend Shift) | Support Delivery | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Tokyo | Support Delivery | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Tokyo (Korean Speaking) | Support Delivery | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Tokyo (Weekend Shift) | Support Delivery | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Toronto | Support Delivery | Ontario - Remote |  | Remote | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 5+ years | NO |  | CAD 200000.0–290000.0 / 1 YEAR | P3_BACKGROUND |
| AI Support Engineer - Toronto (Weekend Shift) | Support Delivery | Ontario - Remote |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | NO |  |  | P3_BACKGROUND |
| AI Support Engineer, Government - San Francisco, CA | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 8 | 8+ years | YES | 3 | USD 180000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| AI Support Engineer, Government - Washington, D.C. | Support Delivery | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 8 | 8+ years | YES | 3 | USD 162000.0–234000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Dedicated Support Engineer - Dublin | Support Delivery | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 7 |  | NO |  |  | P3_BACKGROUND |
| Dedicated Support Engineer - London | Support Delivery | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 7 |  | NO |  |  | P3_BACKGROUND |
| Dedicated Support Engineer - San Francisco | Support Delivery | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 7 |  | NO |  | USD 180000.0–260000.0 / 1 YEAR | P2_REVIEW |
| Dedicated Support Engineer - Singapore | Support Delivery | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 7 |  | YES | 3 |  | P3_BACKGROUND |
| Dedicated Support Engineer - Tokyo | Support Delivery | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 7 |  | YES | 3 |  | P3_BACKGROUND |
| Dedicated Support Engineer - Toronto | Support Delivery | Ontario - Remote |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 7 |  | NO |  |  | P3_BACKGROUND |
| Support Delivery Lead | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 10+ years; 5+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | P2_REVIEW |
| Support Delivery Lead | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 8+ years; 4+ years | YES | 3 | USD 284000.0–315000.0 / 1 YEAR | P2_REVIEW |
| Support Delivery Lead - Toronto | Support Delivery | Ontario - Remote |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 5+ years; 10+ years | NO |  | CAD 297000.0–330000.0 / 1 YEAR | P3_BACKGROUND |
| Support Delivery Lead, Ads | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 5 | 12+ years; 6+ years | YES | 3 | USD 284000.0–315000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Support Delivery Lead, EMEA - Dublin | Support Delivery | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 4+ years; 8+ years | YES | 3 |  | P3_BACKGROUND |
| Strategy & Operations Programs, Support | Support Operations | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 4 | at least 5 years; 8+ years; 5 years of | NO |  | USD 216000.0–310000.0 / 1 YEAR | P3_BACKGROUND |
| Support Operations Lead | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 10+ years; 4+ years | YES | 3 | USD 279000.0–310000.0 / 1 YEAR | P3_BACKGROUND |
| Support Program Manager, Partnerships | Support Operations | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 8+ years | NO |  | USD 216000.0–310000.0 / 1 YEAR | P3_BACKGROUND |
| Support Vendor Manager | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 5 | 5+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Technical Systems Program Manager, User Operations | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 8+ years | YES |  | USD 216000.0–240000.0 / 1 YEAR | P2_REVIEW |
| Technical Program Manager, AI Safety & Safeguards | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 4 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Technical Program Manager, Applied API & Product | Technical Program Management | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 1 | 15+ years | NO |  | USD 207000.0–445000.0 / 1 YEAR | P3_BACKGROUND |
| Technical Program Manager, Cloud AI Partnerships | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Technical Program Manager, Enterprise | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Applied AI Architect, Partner | Technical Success | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | NO |  |  | P3_BACKGROUND |
| Applied AI Delivery Lead | Technical Success | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 7+ years | NO |  | USD 234000.0–335000.0 / 1 YEAR | P3_BACKGROUND |
| Applied AI Engineer | Technical Success | Seoul, South Korea |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer | Technical Success | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer | Technical Success | Delhi, India | Mumbai, India; Bangalore - Remote | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer - Tokyo | Technical Success | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer, Agent Enablement | Technical Success | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 8 | 4–6 years; 6 years of | YES | 3 | USD 197000.0–280000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Cyber | Technical Success | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 9 | 5+ years | NO |  |  | P3_BACKGROUND |
| Applied AI Engineer, Cyber | Technical Success | San Francisco | New York City | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 9 | 5+ years | NO |  | USD 211000.0–292000.0 / 1 YEAR | P2_REVIEW |
| Applied AI Engineer, Cyber \| Tokyo | Technical Success | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 9 | 5+ years | NO |  |  | P3_BACKGROUND |
| Applied AI Engineer, Enterprise | Technical Success | San Francisco | New York City; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 | USD 251000.0–278000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Enterprise | Technical Success | São Paulo |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | NO |  |  | P3_BACKGROUND |
| Applied AI Engineer, Plugins | Technical Success | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 7 | 4-6 years; 6 years of | YES | 3 | USD 197000.0–280000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Demo Experience Engineer, Technical Success | Technical Success | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 3 |  | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | P2_REVIEW |
| Early Access Deployment Engineer | Technical Success | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 6 | 4+ years | YES | 3 | USD 250000.0–330000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Enablement Lead (Builder) - Tokyo | Technical Success | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | LOW | 5 | 4+ years | YES | 3 |  | LOW_TECHNICAL_PRIORITY |
| Manager, Applied AI Architect | Technical Success | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 8+ years; 3+ years | YES | 3 | USD 280000.0–300000.0 / 1 YEAR | P2_REVIEW |
| Manager, Applied AI Architect (India) | Technical Success | Bangalore - Remote |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 4 | 10+ years; 4+ years | NO |  |  | P3_BACKGROUND |
| Manager, Applied AI Architects | Technical Success | Paris, France |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 4 | 10+ years; 4+ years | YES | 3 |  | P3_BACKGROUND |
| Manager, Applied AI Architects | Technical Success | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 4 | 10+ years; 4+ years | NO |  |  | P3_BACKGROUND |
| Manager, Applied AI Architects | Technical Success | London, UK |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 4 | 10+ years; 4+ years | YES | 3 |  | P3_BACKGROUND |
| Manager, Applied AI Architects - Digital Natives | Technical Success | Munich, Germany |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 4 | 10+ years; 4+ years | YES | 3 |  | P3_BACKGROUND |
| Manager, Applied AI Engineering (Digital Natives) | Technical Success | San Francisco | New York City; Seattle; Mountain View | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 6 | 8+ years; 2+ years | YES | 3 | USD 302000.0–335000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Manager, Applied AI Engineering (Startups) | Technical Success | San Francisco | Mountain View | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | NONE_DETECTED | 4 |  | NO |  | USD 302000.0–335000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Partner AI Deployment Engineer - AWS | Technical Success | Bangalore - Remote | Mumbai, India; Delhi, India |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | LOW | 2 | 8+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Technical Program Manager, Global Programs — Applied AI Engineering | Technical Success | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 4 | at least 10+ years; 10+ years | NO |  | USD 251000.0–280000.0 / 1 YEAR | P3_BACKGROUND |
| Senior Support Specialist, Ads | Trust & Safety | Ontario - Remote |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 7 | 6+ years | NO |  | CAD 170000.0–188000.0 / 1 YEAR | P3_BACKGROUND |
| Senior Support Specialist, Ads | Trust & Safety | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 7 | 6+ years | NO |  | USD 189000.0–280000.0 / 1 YEAR | P2_REVIEW |
| Trust & Safety Ads Operations Analyst, Programs | Trust & Safety | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | LOW | 4 | 8+ years | NO |  | USD 252000.0–280000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Manager, Senior Support Engineering | User Operations | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 4 | 10+ years; 5+ years | YES | 3 |  | P3_BACKGROUND |
| Senior Manager, Occupancy Planning & Workplace Strategy | Workplace | San Francisco |  | Hybrid | D_US_ONSITE_OR_HYBRID | REVIEW_SALES_CONTEXT | NONE_DETECTED | 2 | 8+ years | NO | 3 | USD 203000.0–225000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |

</details>

## 9. Deep-review candidate pool

This is **not a final ranking**. Roles enter this pool only through explicit rules combining technical-core evidence, documented-evidence overlap, NO-SALES handling, and a plausible US-remote / relocation / US-location path.

| title | team | primary | secondary | workplace | location_class | sales | technical | evidence_overlap | years_mentions | relocation | office_days | salary | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Data Scientist, Cybersecurity | Data Science | US - Remote | New York City; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 6 | 5+ years | NO |  | USD 263000.0–515000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Technical Threat Investigator, Threat Intel Engineering | Security | San Francisco | New York City; US - Remote | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES |  | USD 347000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Vendor Security Technical Program Manager | Security | US - Remote | Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | NO |  | USD 231300.0–256500.0 / 1 YEAR | P1_DEEP_REVIEW |
| Principal Software Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | NO |  | USD 401000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Host Assurance | Security | San Francisco | Seattle; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Data Center Infrastructure Electrical Engineer | Datacenter Design | San Francisco | Seattle; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 7 | 10+ years; 15+ years | NO |  | USD 257000.0–327000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Enterprise | Technical Success | San Francisco | New York City; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 | USD 251000.0–278000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Security Engineer, Detection and Response | Security | San Francisco | New York City; Seattle; US - Remote |  | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | HIGH | 6 |  | NO |  | USD 266000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Hardware Operations Engineer | Datacenter Design | San Francisco | Seattle; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 6 | 8+ years | NO |  | USD 157000.0–302000.0 / 1 YEAR | P1_DEEP_REVIEW |
| ChatGPT Performance Engineer | Applied AI Engineering | San Francisco | New York City; Seattle; US - Remote |  | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 | 7+ years | NO |  | USD 347000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Security Engineer, Application Security | Security | San Francisco | US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Agent Enablement | Technical Success | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 8 | 4–6 years; 6 years of | YES | 3 | USD 197000.0–280000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Business Systems Lead, Procure-to-Pay | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 8 | 6+ years | YES | 3 | USD 272000.0–302000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Networking Operating System Firmware Engineer | Hardware | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Manufacturing Infrastructure | Hardware | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 | 7+ years | YES |  | USD 310000.0–460000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Plugins | Technical Success | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 7 | 4-6 years; 6 years of | YES | 3 | USD 197000.0–280000.0 / 1 YEAR | P1_DEEP_REVIEW |
| IT Support Specialist | IT | Seattle | Washington, DC; San Francisco; London, UK | OnSite | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES | 5 | USD 60.58–108.17 / 1 HOUR | P1_DEEP_REVIEW |
| Engineering Manager, Client Platform Engineering | Security | San Francisco | New York City; Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES |  | USD 401000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Quality & Developer Tools \| Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES | 4 | USD 207000.0–365000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Senior Support Engineer - San Francisco | Support Delivery | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 | 8+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied Data Science & Insights Leader - GTM Intelligence Solutions and Technical Success | Data Science | San Francisco |  | OnSite | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 7 | 10+ years | YES | 3 | USD 441000.0–515000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Systems Software Engineer, Management Plane | Hardware | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 7 | 7+ years | YES |  | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Field Engineer | Robotics | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 7 | 5+ years | YES |  | USD 225000.0–318000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Connectivity Software Engineer, Consumer Devices | Software | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 7 |  | YES | 4 | USD 347000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Network Engineer | Security | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 |  | YES | 3 | USD 347000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Senior Software Engineer - Research Platform, Consumer Devices | Research | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 | 7+ years | YES | 3 | USD 293000.0–325000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Growth - Lifecycle Lead (B2B) | Applied AI | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 | 10+ years | YES | 3 | USD 239000.0–325000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Ads Manager | Applied AI Engineering | Seattle |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 6 | 7+ years | YES |  | USD 347000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Plugin Ecosystem | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 |  | YES | 3 | USD 185000.0–490000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Product Marketing Manager, IT Admin and Governance | Marketing | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 6 | 8+ years | YES | 3 | USD 221000.0–245000.0 / 1 YEAR | P1_DEEP_REVIEW |
| System Software Engineer, Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 |  | YES |  | USD 347000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Systems Test Engineer, End-to-End Validation \| Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 6 |  | YES | 4 | USD 230000.0–290000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Early Access Deployment Engineer | Technical Success | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 6 | 4+ years | YES | 3 | USD 250000.0–330000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Subject Matter Expert, Investment Banking | Applied AI | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 6 | 2+ years | YES | 3 | USD 185000.0–205000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Forward Deployed Engineer (FDE), Financial Services- NYC | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 6 | 5+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Forward Deployed Engineer (FDE), Legal-NYC | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 6 | 5+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Forward Deployed Engineer (FDE), Legal-SF | Forward Deployed Engineering | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 6 | 5+ years | YES | 3 | USD 185000.0–300000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Systems Software Engineer, Security, First Party Hardware | Hardware | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 6 | 7+ years | YES |  | USD 230000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Data Engineering Manager, Growth & Revenue | Applied AI Engineering | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 6 |  | YES |  | USD 459000.0–536000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Systems Integration Engineer, Build Systems \| Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 5+ years | YES | 4 | USD 207000.0–365000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Dedicated Support Engineering Lead | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 12+ years; 6+ years | YES | 3 | USD 284000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Infrastructure - Core Experimentation | Applied AI Engineering | Seattle |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES |  | USD 347000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Search Infrastructure | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Camera Software Engineer, Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES |  | USD 347000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Android Engineer, Ad Formats | Applied AI Engineering | San Francisco | San Francisco | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 4+ years | YES |  | USD 230000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Contract Management Lead (Procurement) | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 5 |  | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Senior Staff Software Engineer, Identity Infrastructure Engineering | IT | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 10+ years | YES | 3 | USD 347000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Technical Program Manager, Compute Infrastructure | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 5+ years | YES | 3 | USD 257000.0–335000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Resilience Engineering | Applied AI Infrastructure | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES |  | USD 230000.0–490000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Performance Modeling Engineer ~2 | Compute | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 | 1–2 years; 2 years of | YES | 3 | USD 347000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Forward Deployed Security Engineer | Security | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 | 5+ years | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Security Engineer, Application Security | Security | Seattle |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Security Engineer, Application Security | Security | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Systems Integration Manager \| Consumer Devices | Software | San Francisco |  | OnSite | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES | 4 | USD 290000.0–365000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Software Engineer, Cloud Infrastructure | Applied AI Infrastructure | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 | 5+ years | YES |  | USD 230000.0–490000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Order Management & Billing Lead — Cloud Marketplaces & Partnerships | Finance | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 5 | 6+ years | YES | 3 | USD 158000.0–205000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Cyber Enablement Lead, Gov | OpenAI for Gov | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | YES | 3 | USD 207000.0–230000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Support Vendor Manager | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 5 | 5+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Principal Security Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 3 |  | NO |  | USD 401000.0–510000.0 / 1 YEAR | P2_REVIEW |
| Security Engineer, Infrastructure Security | Security | US - Remote | New York City; Seattle; San Francisco | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 3 |  | NO |  | USD 266000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Security Program Manager | Security | US - Remote | New York City; Seattle; Washington, DC; San Francisco | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 5+ years | NO |  | USD 129600.0–310000.0 / 1 YEAR | P2_REVIEW |
| Compute Infrastructure, Critical Facilities Manager | Datacenter Design | San Francisco | Seattle; US - Remote | OnSite | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 | 8+ years | NO |  | USD 199000.0–302000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Security Observability | Security | San Francisco | New York City; Seattle; US - Remote |  | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 |  | YES |  | USD 293000.0–325000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Plugin Developer Platform | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES | 3 | USD 185000.0–490000.0 / 1 YEAR | P2_REVIEW |
| Release Engineer \| Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES | 4 | USD 207000.0–365000.0 / 1 YEAR | P2_REVIEW |
| Technical Program Manager, AI Safety & Safeguards | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 4 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Research Developer Productivity | Fleet Clusters | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES | 3 | USD 230000.0–325000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, ML Systems & Training Architecture | Robotics | San Francisco |  | OnSite | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES |  | USD 295000.0–380000.0 / 1 YEAR | P2_REVIEW |
| Android Systems Engineer, Consumer Devices | Software | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES | 4 | USD 266000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Technical Program Manager, Multimodal | Technical Program Management | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | YES | 3 | USD 207000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Android Engineer, Plugin Developer Platform | Applied AI Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 185000.0–385000.0 / 1 YEAR | P2_REVIEW |
| Full Stack Software Engineer, Cybersecurity Products | Codex - Engineering | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 266000.0–445000.0 / 1 YEAR | P2_REVIEW |
| Full Stack Software Engineer, Sales Platform | Codex - Engineering | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 5+ years | YES | 3 | USD 266000.0–455000.0 / 1 YEAR | P2_REVIEW |
| Software Engineer, Fleet Management | Fleet Clusters | San Francisco | New York City |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 |  | YES | 3 | USD 230000.0–490000.0 / 1 YEAR | P2_REVIEW |

## 10. Candidate dossiers for deep-review pool

### Data Scientist, Cybersecurity — Data Science

- **Priority:** P1_DEEP_REVIEW — Strong current US-remote evidence; 6 documented-evidence vocabulary categories overlap
- **Location:** A_US_REMOTE_STRONG (HIGH) — workplace_type=Remote and US - Remote appears in primary or secondary locations
- **Primary / secondary:** US - Remote / New York City, San Francisco
- **Workplace metadata:** workplace_type='Remote', is_remote=1
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 6 categories: support, automation, scripting_programming, sql_data, network_identity_device, uat_testing
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 263000.0–515000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/894ce80d-c587-4ef0-92d2-b16deb9a06b9/application

### Software Engineer, Infrastructure Security — Security

- **Priority:** P1_DEEP_REVIEW — Strong current US-remote evidence; 5 documented-evidence vocabulary categories overlap
- **Location:** A_US_REMOTE_STRONG (HIGH) — workplace_type=Remote and US - Remote appears in primary or secondary locations
- **Primary / secondary:** US - Remote / New York City, Seattle, San Francisco
- **Workplace metadata:** workplace_type='Remote', is_remote=1
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 5 categories: support, api_integrations, automation, scripting_programming, network_identity_device
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/98ad9beb-4f91-496c-bd16-ac0b2a8d5bb2/application

### Technical Threat Investigator, Threat Intel Engineering — Security

- **Priority:** P1_DEEP_REVIEW — Strong current US-remote evidence; 5 documented-evidence vocabulary categories overlap
- **Location:** A_US_REMOTE_STRONG (HIGH) — workplace_type=Remote and US - Remote appears in primary or secondary locations
- **Primary / secondary:** San Francisco / New York City, US - Remote
- **Workplace metadata:** workplace_type='Remote', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, automation, scripting_programming, sql_data
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Remote context:** for diverse stakeholders. - Comfort operating independently in ambiguous, fast-moving problem spaces with minimal oversight. This is a remote role with close collaboration required across teams in the US and UK. While the role is remote, regular in-person engagement with our San Francisco (SF) headquarters will be expected. Relocation assistance is available for candidates who wish to relocate to SF.
- **Relocation context:** s teams in the US and UK. While the role is remote, regular in-person engagement with our San Francisco (SF) headquarters will be expected. Relocation assistance is available for candidates who wish to relocate to SF. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of AI systems a
- **Salary component(s):** USD 347000.0–510000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/f01b7084-a68d-4e30-ace9-6b5e6d90c517/application

### Vendor Security Technical Program Manager — Security

- **Priority:** P1_DEEP_REVIEW — Strong current US-remote evidence; 5 documented-evidence vocabulary categories overlap
- **Location:** A_US_REMOTE_STRONG (HIGH) — workplace_type=Remote and US - Remote appears in primary or secondary locations
- **Primary / secondary:** US - Remote / Seattle, San Francisco
- **Workplace metadata:** workplace_type='Remote', is_remote=1
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 5 categories: troubleshooting, api_integrations, automation, network_identity_device, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 231300.0–256500.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/3ae71c21-60dd-42b2-a913-58df05988976/application

### Principal Software Engineer, Infrastructure Security — Security

- **Priority:** P1_DEEP_REVIEW — Strong current US-remote evidence; 4 documented-evidence vocabulary categories overlap
- **Location:** A_US_REMOTE_STRONG (HIGH) — workplace_type=Remote and US - Remote appears in primary or secondary locations
- **Primary / secondary:** US - Remote / New York City, Seattle, San Francisco
- **Workplace metadata:** workplace_type='Remote', is_remote=1
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 4 categories: support, api_integrations, automation, network_identity_device
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 401000.0–510000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/ace42c6d-8663-4b30-9337-ec70cf071d73/application

### Software Engineer, Host Assurance — Security

- **Priority:** P1_DEEP_REVIEW — US-Remote appears in posting locations but remote status needs manual confirmation; 7 evidence-overlap categories
- **Location:** B_US_REMOTE_AMBIGUOUS (MEDIUM) — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** San Francisco / Seattle, US - Remote
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 7 categories: support, api_integrations, automation, scripting_programming, network_identity_device, uat_testing, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/0b9e565a-ae5f-40fc-8350-b59f71f76df1/application

### Data Center Infrastructure Electrical Engineer — Datacenter Design

- **Priority:** P1_DEEP_REVIEW — US-Remote appears in posting locations but remote status needs manual confirmation; 7 evidence-overlap categories
- **Location:** B_US_REMOTE_AMBIGUOUS (MEDIUM) — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** San Francisco / Seattle, US - Remote
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 7 categories: support, troubleshooting, api_integrations, scripting_programming, network_identity_device, uat_testing, documentation
- **Experience-year mentions:** 10+ years; 15+ years
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 257000.0–327000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/e602cd50-002d-4ace-bb30-19db0afcf635/application

### Applied AI Engineer, Enterprise — Technical Success

- **Priority:** P1_DEEP_REVIEW — US-Remote appears in posting locations but remote status needs manual confirmation; 6 evidence-overlap categories
- **Location:** B_US_REMOTE_AMBIGUOUS (MEDIUM) — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** San Francisco / New York City, US - Remote
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** HIGH (6 categories)
- **Evidence overlap:** 6 categories: troubleshooting, api_integrations, automation, scripting_programming, uat_testing, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** how OpenAI’s products evolve. This role is based in our SF or NYC office. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Partner directly with enterprise customers to identify high-value opportunities and translate them into technical architectures, implementation plans, evaluation strategies, and measurable success criteria. -
- **Office requirement context:** ctly influencing how OpenAI’s products evolve. This role is based in our SF or NYC office. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Partner directly with enterprise customers to identify high-value opportunities and translate them into
- **Salary component(s):** USD 251000.0–278000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/01091aed-427d-4e10-8cdb-fb500cf55bb9/application

### Security Engineer, Detection and Response — Security

- **Priority:** P1_DEEP_REVIEW — US-Remote appears in posting locations but remote status needs manual confirmation; 6 evidence-overlap categories
- **Location:** B_US_REMOTE_AMBIGUOUS (MEDIUM) — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** San Francisco / New York City, Seattle, US - Remote
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 6 categories: troubleshooting, automation, scripting_programming, network_identity_device, documentation, crm_saas
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 266000.0–385000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/f956b77c-3cc5-4fdd-9463-2a6e5047e57c/application

### Hardware Operations Engineer — Datacenter Design

- **Priority:** P1_DEEP_REVIEW — US-Remote appears in posting locations but remote status needs manual confirmation; 6 evidence-overlap categories
- **Location:** B_US_REMOTE_AMBIGUOUS (MEDIUM) — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** San Francisco / Seattle, US - Remote
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 6 categories: support, troubleshooting, api_integrations, automation, network_identity_device, documentation
- **Experience-year mentions:** 8+ years
- **Education signals:** EQUIVALENT_EXPERIENCE
- **Salary component(s):** USD 157000.0–302000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/b9a4a809-a965-4dbe-aeef-6ce1593903dd/application

### ChatGPT Performance Engineer — Applied AI Engineering

- **Priority:** P1_DEEP_REVIEW — US-Remote appears in posting locations but remote status needs manual confirmation; 5 evidence-overlap categories
- **Location:** B_US_REMOTE_AMBIGUOUS (MEDIUM) — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** San Francisco / New York City, Seattle, US - Remote
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 5 categories: api_integrations, scripting_programming, sql_data, network_identity_device, uat_testing
- **Experience-year mentions:** 7+ years
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 347000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/38ddaa2c-a490-427a-8457-0e92bf00138c/application

### Security Engineer, Application Security — Security

- **Priority:** P1_DEEP_REVIEW — US-Remote appears in posting locations but remote status needs manual confirmation; 5 evidence-overlap categories
- **Location:** B_US_REMOTE_AMBIGUOUS (MEDIUM) — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** San Francisco / US - Remote
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, scripting_programming, uat_testing, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** ed in San Francisco, Seattle or New York City but may consider remote work. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Perform Security Assessments: Conduct regular security assessments, code reviews, and penetration testing to identify vulnerabilities in applications and software. - Develop and Implement Security Tools: Desi
- **Office requirement context:** erred to be based in San Francisco, Seattle or New York City but may consider remote work. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Perform Security Assessments: Conduct regular security assessments, code reviews, and penetration testi
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/0322d6d8-6588-4209-a304-83e768063a25/application

### Applied AI Engineer, Agent Enablement — Technical Success

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** HIGH (7 categories)
- **Evidence overlap:** 8 categories: support, troubleshooting, api_integrations, automation, scripting_programming, network_identity_device, uat_testing, documentation
- **Experience-year mentions:** 4–6 years; 6 years of
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** ts, and user expectations. This role is based in our San Francisco office. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Own the technical partner journey for priority agent enablement integrations—from use-case selection and readiness assessment through architecture, prototype, implementation, evaluation, launch, rollout, and ongo
- **Office requirement context:** rprise constraints, and user expectations. This role is based in our San Francisco office. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Own the technical partner journey for priority agent enablement integrations—from use-case selection an
- **Salary component(s):** USD 197000.0–280000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/c1a28411-266b-487b-8ef3-03efb254fc36/application

### Business Systems Lead, Procure-to-Pay — Finance

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 8 categories: support, troubleshooting, api_integrations, automation, scripting_programming, sql_data, uat_testing, documentation
- **Experience-year mentions:** 6+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** deeper process and module design. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design, build, and operate integrations across Oracle Fusion, Zip, and connected systems using APIs, events, messaging, and batch interfaces where appropriate. - Build first-party procurement applications, back
- **Office requirement context:** specialists on deeper process and module design. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design, build, and operate integrations across Oracle Fusion, Zip, and connected systems using APIs, ev
- **Salary component(s):** USD 272000.0–302000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/c0e1f65b-4731-48b3-ac60-93a269266494/application

### Networking Operating System Firmware Engineer — Hardware

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (6 categories)
- **Evidence overlap:** 7 categories: support, troubleshooting, api_integrations, automation, scripting_programming, network_identity_device, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** hardware, and vendor boundaries. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL - Design, develop, and maintain custom NOS images for large-scale AI fabrics, using open source components from SONiC, FRR, and related networking stacks. - Integrate, build and configure Linux kernel components,
- **Office requirement context:** across software, hardware, and vendor boundaries. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL - Design, develop, and maintain custom NOS images for large-scale AI fabrics, using open source components
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/f6b9903c-9034-436b-a4ec-4c8643a6d0dd/application

### Software Engineer, Manufacturing Infrastructure — Hardware

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (6 categories)
- **Evidence overlap:** 7 categories: troubleshooting, api_integrations, automation, scripting_programming, network_identity_device, uat_testing, documentation
- **Experience-year mentions:** 7+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** yment, and output of these systems as well their continued maintenance and SLAs. Location: San Francisco, CA (Hybrid: 3 days/week onsite). Relocation assistance available. In this role, you will: - Design, develop, and maintain the software infrastructure for manufacturing process execution and data export. - Own integration across internal customers and vendor systems and processes. - Build and maintain the CI, release
- **Salary component(s):** USD 310000.0–460000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/3b08148d-085e-4835-9934-1b7f60e0fdce/application

### Applied AI Engineer, Plugins — Technical Success

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** HIGH (6 categories)
- **Evidence overlap:** 7 categories: support, troubleshooting, api_integrations, automation, scripting_programming, uat_testing, documentation
- **Experience-year mentions:** 4-6 years; 6 years of
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** eful in ChatGPT and Codex. This role is based in our San Francisco office. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Own the technical partner journey for priority B2B plugins—from pitch and readiness assessment through architecture, build, evaluation, submission, launch, and ongoing maintenance. - Identify strong plugin use
- **Office requirement context:** but genuinely useful in ChatGPT and Codex. This role is based in our San Francisco office. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Own the technical partner journey for priority B2B plugins—from pitch and readiness assessment through
- **Salary component(s):** USD 197000.0–280000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/ca9e0aeb-6df1-4b73-8ec0-2e9e124712f1/application

### IT Support Specialist — IT

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** Seattle / Washington, DC, San Francisco, London, UK
- **Workplace metadata:** workplace_type='OnSite', is_remote=0
- **Relocation assistance:** YES
- **Office days detected:** 5
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 7 categories: support, troubleshooting, automation, scripting_programming, network_identity_device, documentation, crm_saas
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** ments. This role is based out of our Bellevue, London, Washington DC, or San Francisco office and requires 5 days in office per week. We offer relocation assistance to new employees. In this role, you will: - Improve Support Systems and Processes: Collaborate with cross-functional teams to identify opportunities for improvement, support the creation and maintenance of repeatable workflows (such as onboarding and dev
- **Office requirement context:** onments. This role is based out of our Bellevue, London, Washington DC, or San Francisco office and requires 5 days in office per week. We offer relocation assistance to new employees. In this role, you will: - Improve Support Systems and Processes: Collaborate with cross-functional teams to identify opportunitie
- **Salary component(s):** USD 60.58–108.17 / 1 HOUR
- **Apply URL:** https://jobs.ashbyhq.com/openai/49ae54dc-3d33-4107-8112-63fac1ee86ca/application

### Engineering Manager, Client Platform Engineering — Security

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / New York City, Seattle
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 7 categories: troubleshooting, automation, scripting_programming, ticketing_itsm, network_identity_device, documentation, crm_saas
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** uting to open-source tooling, engineering communities, or cross-company technical standards. This role is based in San Francisco, CA. We offer relocation assistance to new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of AI systems and seek to safely deploy
- **Salary component(s):** USD 401000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/5df9e349-f8e1-4cfd-ba20-ec9e4115d564/application

### Software Engineer, Quality & Developer Tools | Consumer Devices — Software

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 4
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 7 categories: support, troubleshooting, api_integrations, automation, scripting_programming, network_identity_device, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** idation and release readiness. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Test infrastructure & frameworks: Design, implement, and maintain a unified test framework for device software across unit, integration, system, and end-to-end testing, with reproducible runs and integrations
- **Office requirement context:** ble systems for validation and release readiness. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Test infrastructure & frameworks: Design, implement, and maintain a unified test framework for device s
- **Salary component(s):** USD 207000.0–365000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/1ba666a4-0be2-4bd0-ad51-39ed7164c241/application

### Senior Support Engineer - San Francisco — Support Delivery

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 7 categories: support, troubleshooting, api_integrations, automation, scripting_programming, sql_data, documentation
- **Experience-year mentions:** 8+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** l be low volume, high difficulty. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Be among the foremost technical and troubleshooting experts for our API platform at OpenAI. You are the last line of defense before the core Engineering team. - Proactively identify and implement opportunitie
- **Office requirement context:** of this role will be low volume, high difficulty. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Be among the foremost technical and troubleshooting experts for our API platform at OpenAI. You are the
- **Salary component(s):** USD 234000.0–260000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/5431666c-530b-49c0-b67e-32477f9eaf5e/application

### Applied Data Science & Insights Leader - GTM Intelligence Solutions and Technical Success — Data Science

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='OnSite', is_remote=0
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 7 categories: support, automation, scripting_programming, sql_data, uat_testing, documentation, crm_saas
- **Experience-year mentions:** 10+ years
- **Education signals:** EQUIVALENT_EXPERIENCE
- **Relocation context:** back to Product and Research. This role is based in San Francisco, CA. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. THE VISION - Build a unified GTM intelligence layer that connects product telemetry, customer health, revenue, support tier, lifecycle stage, field activity, and qualitative feedback. - Turn adoption breadth, usage depth, sentiment, a
- **Office requirement context:** loop from the field back to Product and Research. This role is based in San Francisco, CA. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. THE VISION - Build a unified GTM intelligence layer that connects product telemetry, customer health, revenue, support tier, life
- **Salary component(s):** USD 441000.0–515000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/93f558c1-c944-4ddc-b102-addc9446de3d/application

### Systems Software Engineer, Management Plane — Hardware

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 7 categories: troubleshooting, api_integrations, automation, scripting_programming, network_identity_device, uat_testing, documentation
- **Experience-year mentions:** 7+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** evidence, and help carry platforms from bring-up through production deployment. Location: San Francisco, CA (Hybrid: 3 days/week onsite) Relocation assistance available. IN THIS ROLE, YOU WILL: - Design, develop, and maintain low-level firmware and system software for first-party AI hardware manageability, including BMC software, Redfish services, gNMI telemetry, firmware update and recovery flows, BIOS/UEFI interactions
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/21229750-8bd1-4134-a20e-2a8922b88806/application

### Field Engineer — Robotics

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 7 categories: support, troubleshooting, api_integrations, automation, scripting_programming, ticketing_itsm, documentation
- **Experience-year mentions:** 5+ years
- **Education signals:** BACHELORS
- **Relocation context:** pressure, and motivated by making real systems work reliably at scale. This role will be based in San Francisco, CA 5 days per week and offer relocation assistance to new employees. In this role, you will: - Serve as an engineering owner for keeping a fleet of robotic workcells online in daily operation. - Diagnose, fix, mitigate, or escalate issues spanning mechanics, electronics, controls, software interfaces,
- **Salary component(s):** USD 225000.0–318000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/d8ebcb30-c789-4e75-bf9b-a1e3fb09dd2f/application

### Connectivity Software Engineer, Consumer Devices — Software

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 4
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (2 categories)
- **Evidence overlap:** 7 categories: support, troubleshooting, api_integrations, automation, scripting_programming, network_identity_device, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** le connectivity infrastructure. This role is based in San Francisco, CA. We use a hybrid work model of 4 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design, implement, and debug Bluetooth/BLE and Wi-Fi features across kernel drivers, BlueZ/wpa_supplicant/hostapd, and systemd/D-Bus services - Deliver robust pairing, bonding, and provisioning flows (GATT/GA
- **Office requirement context:** ity, and fleet-scale connectivity infrastructure. This role is based in San Francisco, CA. We use a hybrid work model of 4 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design, implement, and debug Bluetooth/BLE and Wi-Fi features across kernel drivers, BlueZ/wpa_supplica
- **Salary component(s):** USD 347000.0–385000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/9b2c68f2-5ce8-44f9-a30c-d8016ac66d86/application

### Network Engineer — Security

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (6 categories)
- **Evidence overlap:** 6 categories: troubleshooting, api_integrations, automation, scripting_programming, ticketing_itsm, network_identity_device
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** surably reduces operational toil. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of AI systems and seek to safely deploy
- **Office requirement context:** omation that measurably reduces operational toil. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence b
- **Salary component(s):** USD 347000.0–510000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/9f78c41f-8d39-46c9-b9c3-c3b075905b24/application

### Senior Software Engineer - Research Platform, Consumer Devices — Research

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 6 categories: support, troubleshooting, api_integrations, automation, scripting_programming, uat_testing
- **Experience-year mentions:** 7+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** remain reliable and reusable. This role is based in San Francisco, CA. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Build web applications, APIs, data models, and backend services for AI research workflows. - Build tools to author and manage evaluation tasks, rubrics, graders, suites, and rollout configurations, including
- **Office requirement context:** underlying systems remain reliable and reusable. This role is based in San Francisco, CA. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Build web applications, APIs, data models, and backend services for AI research workflows. - Build tool
- **Salary component(s):** USD 293000.0–325000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/6d9925f4-3d0a-4710-8304-032d0080d12d/application

### Growth - Lifecycle Lead (B2B) — Applied AI

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 6 categories: troubleshooting, api_integrations, automation, scripting_programming, network_identity_device, crm_saas
- **Experience-year mentions:** 10+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** h value and build durable habits. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Partner with B2B product to set the company-wide vision, roadmap, and operating model for lifecycle and owned-channel engagement. - Partner with Engineering, Product, Data Science, and Analytics to shape the to
- **Office requirement context:** businesses reach value and build durable habits. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Partner with B2B product to set the company-wide vision, roadmap, and operating model for lifecycle and
- **Salary component(s):** USD 239000.0–325000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/effa8b95-3b2d-4f57-8fcd-b3c9b3c142ba/application

### Software Engineer, Ads Manager — Applied AI Engineering

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** Seattle / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 6 categories: support, api_integrations, automation, scripting_programming, uat_testing, documentation
- **Experience-year mentions:** 7+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** easurement systems, marketplaces, or enterprise ad-tech integrations. Location This role is exclusively based in our Seattle office. We offer relocation assistance to new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of AI systems and seek to safely deploy
- **Salary component(s):** USD 347000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/5a4eed17-29d5-41cb-856e-09bfdaffe017/application

### Software Engineer, Plugin Ecosystem — Applied AI Engineering

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 6 categories: troubleshooting, api_integrations, automation, network_identity_device, uat_testing, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** n through implementation and release. This role is based in San Francisco. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design and ship APIs, SDKs, and services that developers use to extend ChatGPT and Codex. - Build intuitive experiences that help users discover, install, and use plugins to get more done. - Make plugins easi
- **Office requirement context:** gnosis and design through implementation and release. This role is based in San Francisco. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design and ship APIs, SDKs, and services that developers use to extend ChatGPT and Codex. - Build intui
- **Salary component(s):** USD 185000.0–490000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/e42305bf-2266-4dff-82ad-42be7ddac495/application

### Product Marketing Manager, IT Admin and Governance — Marketing

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 6 categories: support, automation, network_identity_device, uat_testing, documentation, crm_saas
- **Experience-year mentions:** 8+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** at scale. WORKPLACE & LOCATION This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. Occasional travel will be required. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of A
- **Office requirement context:** hnology safely and at scale. WORKPLACE & LOCATION This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. Occasional travel will be required. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that gener
- **Salary component(s):** USD 221000.0–245000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/c6cb3f11-8e1f-4e34-b407-6a3327e39f2e/application

### System Software Engineer, Consumer Devices — Software

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 6 categories: support, troubleshooting, api_integrations, automation, scripting_programming, network_identity_device
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** Location: San Francisco, CA (Hybrid: 4 days onsite/week). Relocation assistance available. About the Team: We build foundational platform software that enables reliable, secure, and performant products. The team works across system layers and partners closely with adjacent engineering groups to deliver robust capabilities from concept through la
- **Salary component(s):** USD 347000.0–385000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/20f525b7-f958-4c95-a055-f914ab3adb95/application

### Systems Test Engineer, End-to-End Validation | Consumer Devices — Software

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 4
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 6 categories: troubleshooting, api_integrations, automation, scripting_programming, network_identity_device, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** es across multiple components. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Design end-to-end test coverage: Develop structured test plans and reproducible procedures for user journeys, realistic usage patterns, edge cases, degraded conditions, and failure scenarios across devices, se
- **Office requirement context:** d diagnosing failures across multiple components. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Design end-to-end test coverage: Develop structured test plans and reproducible procedures for user jou
- **Salary component(s):** USD 230000.0–290000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/393b88d7-1fbc-466a-9108-a7c1bafeb8d8/application

### Early Access Deployment Engineer — Technical Success

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 6 categories: support, troubleshooting, automation, scripting_programming, uat_testing, documentation
- **Experience-year mentions:** 4+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** uld be built, refined, or scaled. This role is based in San Francisco. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. In this role, you will: - Engage deeply with strategic customers during the earliest alpha stages to understand their goals, workflows, technical constraints, and highest-value opportunities. - Translate emerging and ambiguous model cap
- **Office requirement context:** eedback, on what should be built, refined, or scaled. This role is based in San Francisco. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. In this role, you will: - Engage deeply with strategic customers during the earliest alpha stages to understand their goals, work
- **Salary component(s):** USD 250000.0–330000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/ee6b7ece-ffcb-4546-8b4c-ef755ec21c14/application

### Subject Matter Expert, Investment Banking — Applied AI

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 6 categories: support, troubleshooting, api_integrations, automation, uat_testing, documentation
- **Experience-year mentions:** 2+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** nced bankers can trust and use. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. About the Role We are looking for a Subject Matter Expert in Investment Banking to help define what excellent AI-assisted banking work looks like and turn that standard into better models and products. You will bring deep, current knowle
- **Office requirement context:** work that experienced bankers can trust and use. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. About the Role We are looking for a Subject Matter Expert in Investment Banking to help define what excellent AI-assisted banking
- **Salary component(s):** USD 185000.0–205000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/4705a853-46e6-4f91-884c-61e54de91b0e/application

### Forward Deployed Engineer (FDE), Financial Services- NYC — Forward Deployed Engineering

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** New York City / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 6 categories: troubleshooting, api_integrations, automation, scripting_programming, uat_testing, documentation
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** x/introducing-chatgpt-financial-services/. This role is based in New York. We use a hybrid work model of 3 days in the office per week. We offer relocation assistance. Travel up to 50% may be required. IN THIS ROLE, YOU WILL - Design and ship production AI systems around models, owning integrations, data flows, reliability, observability, and on-call readiness across financial workflows. - Lead discovery and scopin
- **Office requirement context:** /openai.com/index/introducing-chatgpt-financial-services/. This role is based in New York. We use a hybrid work model of 3 days in the office per week. We offer relocation assistance. Travel up to 50% may be required. IN THIS ROLE, YOU WILL - Design and ship production AI systems around models, owning integrations, data flows, r
- **Salary component(s):** USD 185000.0–300000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/7f76be3a-38d0-4ff4-b997-9f1672e78bc0/application

### Forward Deployed Engineer (FDE), Legal-NYC — Forward Deployed Engineering

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** New York City / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 6 categories: support, troubleshooting, automation, scripting_programming, uat_testing, documentation
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** er legal market. This role is based in San Francisco or New York City. We use a hybrid work model of three days in the office per week and offer relocation assistance. Travel up to 50% may be required. IN THIS ROLE, YOU WILL - Embed with law firms and legal teams to understand their workflows, identify high-value opportunities, and select the right initial use cases to prove value. - Build full-stack systems that d
- **Office requirement context:** counts and the broader legal market. This role is based in San Francisco or New York City. We use a hybrid work model of three days in the office per week and offer relocation assistance. Travel up to 50% may be required. IN THIS ROLE, YOU WILL - Embed with law firms and legal teams to understand their workflows, identify high-value
- **Salary component(s):** USD 185000.0–300000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/51977acc-b1f8-48af-bde6-95ddba936d65/application

### Forward Deployed Engineer (FDE), Legal-SF — Forward Deployed Engineering

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** New York City / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 6 categories: support, troubleshooting, automation, scripting_programming, uat_testing, documentation
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** er legal market. This role is based in San Francisco or New York City. We use a hybrid work model of three days in the office per week and offer relocation assistance. Travel up to 50% may be required. IN THIS ROLE, YOU WILL - Embed with law firms and legal teams to understand their workflows, identify high-value opportunities, and select the right initial use cases to prove value. - Build full-stack systems that d
- **Office requirement context:** counts and the broader legal market. This role is based in San Francisco or New York City. We use a hybrid work model of three days in the office per week and offer relocation assistance. Travel up to 50% may be required. IN THIS ROLE, YOU WILL - Embed with law firms and legal teams to understand their workflows, identify high-value
- **Salary component(s):** USD 185000.0–300000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/832094fd-4d89-4fe4-bc18-9ba88d347a18/application

### Systems Software Engineer, Security, First Party Hardware — Hardware

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 6 categories: support, troubleshooting, automation, scripting_programming, network_identity_device, uat_testing
- **Experience-year mentions:** 7+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** , and implementation into validation evidence that can support launch decisions. Location: San Francisco, CA (Hybrid: 3 days/week onsite) Relocation assistance available. IN THIS ROLE, YOU WILL: - Own security requirements, threat models, validation strategy, and launch-readiness evidence for first-party hardware platforms from early design through production deployment. - Design and review secure boot, measured boot,
- **Salary component(s):** USD 230000.0–385000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/1c48f39f-60ea-4636-87ed-8b4b4f5243e5/application

### Data Engineering Manager, Growth & Revenue — Applied AI Engineering

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** MEDIUM (2 categories)
- **Evidence overlap:** 6 categories: support, troubleshooting, api_integrations, automation, scripting_programming, sql_data
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** tandards, and a hiring and development plan that matches the domain’s ambition. This role is based in our San Francisco headquarters. We offer relocation assistance for new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of AI systems and seek to safely deploy
- **Salary component(s):** USD 459000.0–536000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/acbf80cd-20a7-47fe-aaf9-3e9224d1570c/application

### Systems Integration Engineer, Build Systems | Consumer Devices — Software

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 4
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (6 categories)
- **Evidence overlap:** 5 categories: troubleshooting, api_integrations, automation, scripting_programming, uat_testing
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** ad of fighting infrastructure. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. In This Role, You Will - Own and evolve Bazel and yocto-based build and test workflows in a polyrepo environment - Design and maintain Starlark rules, macros, toolchains, and integrations that make builds hermetic, reproducible, and eas
- **Office requirement context:** ping products instead of fighting infrastructure. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. In This Role, You Will - Own and evolve Bazel and yocto-based build and test workflows in a polyrepo environment - Design and mai
- **Salary component(s):** USD 207000.0–365000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/9104a37c-6ae0-499b-a2f7-2785e63b5f0c/application

### Dedicated Support Engineering Lead — Support Delivery

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (6 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, api_integrations, automation, uat_testing
- **Experience-year mentions:** 12+ years; 6+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** gineering leaders and executives. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role you will... - Set the strategy for Dedicated Support Engineering. Define the function’s charter, service model, priorities, and growth plan. Translate customer needs and company priorities into clear decisions about where
- **Office requirement context:** with customer engineering leaders and executives. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role you will... - Set the strategy for Dedicated Support Engineering. Define the function’s charter, service model, prio
- **Salary component(s):** USD 284000.0–385000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/deacd43e-9c1b-467c-96e2-11f4f6bdb139/application

### Software Engineer, Infrastructure - Core Experimentation — Applied AI Engineering

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** Seattle / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, automation, sql_data, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** teams move faster with more confidence. LOCATION This role is based in Bellevue, WA. The team works in person three days per week and offers relocation assistance to new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of AI systems and seek to safely deploy
- **Salary component(s):** USD 347000.0–385000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/823a05bf-33fb-4d94-9dd8-571723d27b1a/application

### Software Engineer, Search Infrastructure — Applied AI Engineering

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, api_integrations, automation, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** ct capabilities, and demand grow. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design and evolve the services that coordinate search classification, retrieval, ranking, and model inference, working closely with researchers and partner engineering teams to bring new capabilities into product
- **Office requirement context:** as models, product capabilities, and demand grow. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design and evolve the services that coordinate search classification, retrieval, ranking, and model inf
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/7caed1e8-c6f6-4569-9d45-2d7a7a56a025/application

### Camera Software Engineer, Consumer Devices — Software

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, api_integrations, automation, scripting_programming
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** the entire camera stack. This role is based in San Francisco, CA. We follow a hybrid work model with four days per week in the office and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL - Bring up new camera sensors and modules on prototype and production boards, including link stability, sensor control, and correct power, reset, and clock sequencing. - Develop and maintain low-level camera so
- **Salary component(s):** USD 347000.0–385000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/1dc05fc7-ceb7-4827-a905-9d1beb77a4a0/application

### Android Engineer, Ad Formats — Applied AI Engineering

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / San Francisco
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 5 categories: support, api_integrations, automation, network_identity_device, uat_testing
- **Experience-year mentions:** 4+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** , mobile monetization, or large-scale consumer mobile applications. Location This role is exclusively based in our San Francisco HQ. We offer relocation assistance to new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of AI systems and seek to safely deploy
- **Salary component(s):** USD 230000.0–385000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/7daff2af-1686-43fe-85c0-ca912c8747ac/application

### Contract Management Lead (Procurement) — Finance

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 5 categories: support, api_integrations, automation, uat_testing, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** EQUIVALENT_EXPERIENCE
- **Relocation context:** , continuously improving service. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Own the product vision and roadmap for an AI-led contracting help desk, translating user needs into a scalable, measurable service for contract intake, triage, and lifecycle management. - Build and continuously
- **Office requirement context:** sted, measurable, continuously improving service. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Own the product vision and roadmap for an AI-led contracting help desk, translating user needs into a s
- **Salary component(s):** USD 216000.0–240000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/c8750f8c-0e56-49c0-b34a-251c1797d816/application

### Senior Staff Software Engineer, Identity Infrastructure Engineering — IT

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 5 categories: troubleshooting, api_integrations, automation, scripting_programming, network_identity_device
- **Experience-year mentions:** 10+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** n mission-critical systems. This role is based in San Francisco, CA. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of AI systems and seek to safely deploy
- **Office requirement context:** nd operational rigor in mission-critical systems. This role is based in San Francisco, CA. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence b
- **Salary component(s):** USD 347000.0–510000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/72a58872-70e2-4340-a259-e9bea3596883/application

### Technical Program Manager, Compute Infrastructure — Technical Program Management

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 5 categories: support, api_integrations, automation, network_identity_device, documentation
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** oduction-ready capacity at scale. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Lead end-to-end delivery of both New Compute SKUs and large-scale GPU clusters across an external partner ecosystem while supporting capacity planning for training and inference. - Ability to contextually dri
- **Office requirement context:** ip to deliver production-ready capacity at scale. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Lead end-to-end delivery of both New Compute SKUs and large-scale GPU clusters across an external partn
- **Salary component(s):** USD 257000.0–335000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/8fb1615c-34bf-47c4-a1d1-b7b2f836bbd3/application

### Software Engineer, Resilience Engineering — Applied AI Infrastructure

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 5 categories: troubleshooting, automation, scripting_programming, network_identity_device, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** BACHELORS
- **Relocation context:** h technologies. - Knowledge of security best practices in cloud environments. This role is exclusively based in our San Francisco HQ. We offer relocation assistance to new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of AI systems and seek to safely deploy
- **Salary component(s):** USD 230000.0–490000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/1faee5e7-3b2f-4d8c-9a6f-ff0f2a4a42a7/application

### Performance Modeling Engineer ~2 — Compute

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / Seattle
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 5 categories: support, automation, scripting_programming, network_identity_device, documentation
- **Experience-year mentions:** 1–2 years; 2 years of
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** re and hardware/software systems. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance. Key Responsibilities - Support the development and maintenance of performance modeling tools and frameworks - Assist in building models to evaluate system behavior across compute, memory, networking, and interconnect subsystems - Help analyze distribu
- **Office requirement context:** ale infrastructure and hardware/software systems. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance. Key Responsibilities - Support the development and maintenance of performance modeling tools and frameworks - Assist in building models to evaluat
- **Salary component(s):** USD 347000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/4f6be73e-9a1d-4ec6-8b0e-b2af0b4becfb/application

### Forward Deployed Security Engineer — Security

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** Washington, DC / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 5 categories: support, api_integrations, scripting_programming, network_identity_device, uat_testing
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** le is preferred to be based in Washington DC but may consider remote work. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. Travel to and working from customer sites is required for this role. In this role, you will: - Deeply embed with our most strategic public sector customers to implement and maintain robust security controls. - Be a design and technica
- **Office requirement context:** rations. This role is preferred to be based in Washington DC but may consider remote work. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. Travel to and working from customer sites is required for this role. In this role, you will: - Deeply embed with our most strateg
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/89d61ae8-1ce1-4187-9edd-da8029979e41/application

### Security Engineer, Application Security — Security

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** Seattle / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, scripting_programming, uat_testing, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** ed in San Francisco, Seattle or New York City but may consider remote work. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Perform Security Assessments: Conduct regular security assessments, code reviews, and penetration testing to identify vulnerabilities in applications and software. - Develop and Implement Security Tools: Desi
- **Office requirement context:** erred to be based in San Francisco, Seattle or New York City but may consider remote work. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Perform Security Assessments: Conduct regular security assessments, code reviews, and penetration testi
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/1e110226-448a-4c0b-b0e4-d0f5df579fbf/application

### Security Engineer, Application Security — Security

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** New York City / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, scripting_programming, uat_testing, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** ed in San Francisco, Seattle or New York City but may consider remote work. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Perform Security Assessments: Conduct regular security assessments, code reviews, and penetration testing to identify vulnerabilities in applications and software. - Develop and Implement Security Tools: Desi
- **Office requirement context:** erred to be based in San Francisco, Seattle or New York City but may consider remote work. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Perform Security Assessments: Conduct regular security assessments, code reviews, and penetration testi
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/ec5a5d98-6314-44d9-9466-8d4d7ee866f6/application

### Systems Integration Manager | Consumer Devices — Software

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='OnSite', is_remote=0
- **Relocation assistance:** YES
- **Office days detected:** 4
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 5 categories: support, api_integrations, automation, uat_testing, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** ex hardware-software products. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Lead and grow the team: Hire, manage, mentor, and develop engineers and lab operations staff responsible for test infrastructure, automation, device labs, and release validation. - Own validation strategy and
- **Office requirement context:** e systems for complex hardware-software products. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Lead and grow the team: Hire, manage, mentor, and develop engineers and lab operations staff responsibl
- **Salary component(s):** USD 290000.0–365000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/831960f4-a877-4c41-8fda-17fd321c0230/application

### Software Engineer, Cloud Infrastructure — Applied AI Infrastructure

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (2 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, api_integrations, automation, network_identity_device
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** e, reliable, secure systems - Are comfortable with ambiguity and rapid change This role is exclusively based in our San Francisco HQ. We offer relocation assistance to new employees. About OpenAI OpenAI is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity. We push the boundaries of the capabilities of AI systems and seek to safely deploy
- **Salary component(s):** USD 230000.0–490000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/12342ebb-dcd4-45e2-b875-fc5447fdb7d8/application

### Order Management & Billing Lead — Cloud Marketplaces & Partnerships — Finance

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** MEDIUM (2 categories)
- **Evidence overlap:** 5 categories: support, automation, uat_testing, documentation, crm_saas
- **Experience-year mentions:** 6+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** and financial integrity at scale. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Own end-to-end daily Order Management and Billing performance for an assigned cloud marketplace or partner portfolio, including AWS, GCP, Oracle Cloud, GovCloud, or future channels, spanning order intake, usage i
- **Office requirement context:** tomer outcomes, and financial integrity at scale. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Own end-to-end daily Order Management and Billing performance for an assigned cloud marketplace or part
- **Salary component(s):** USD 158000.0–205000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/1e28e1f0-2580-46d9-b5ba-55c77d706f81/application

### Cyber Enablement Lead, Gov — OpenAI for Gov

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** Washington, DC / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (2 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, automation, scripting_programming, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** n, and better cyber outcomes. This role is based in Washington, D.C. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. Travel and regular work from government customer sites are required. IN THIS ROLE, YOU WILL - Set the vision and own the execution of Daybreak’s government enablement strategy, from audience research and learning objectives to curricul
- **Office requirement context:** ity, sustained adoption, and better cyber outcomes. This role is based in Washington, D.C. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. Travel and regular work from government customer sites are required. IN THIS ROLE, YOU WILL - Set the vision and own the executio
- **Salary component(s):** USD 207000.0–230000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/a244270d-9308-4124-82d5-9c0b91eae1f2/application

### Support Vendor Manager — Support Operations

- **Priority:** P1_DEEP_REVIEW — Strong technical/evidence overlap; Explicit relocation assistance may make non-Utah role financially possible
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** MEDIUM (2 categories)
- **Evidence overlap:** 5 categories: support, troubleshooting, automation, documentation, crm_saas
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** nd launch and scale new programs. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. 1-2 weeks of travel per quarter may be required. YOU’LL BE RESPONSIBLE FOR: - End-to-end vendor leadership: Own day-to-day oversight, relationship health, and executive-level accountability for multiple support vendors/BPOs. - Perfor
- **Office requirement context:** new workflows and launch and scale new programs. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. 1-2 weeks of travel per quarter may be required. YOU’LL BE RESPONSIBLE FOR: - End-to-end vendor leadership: Own day-to-day oversi
- **Salary component(s):** USD 216000.0–240000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/d4084bb6-f9fa-46df-87ef-da6caed88455/application

### Principal Security Engineer, Infrastructure Security — Security

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 3 evidence-overlap categories
- **Location:** A_US_REMOTE_STRONG (HIGH) — workplace_type=Remote and US - Remote appears in primary or secondary locations
- **Primary / secondary:** US - Remote / New York City, Seattle, San Francisco
- **Workplace metadata:** workplace_type='Remote', is_remote=1
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 3 categories: api_integrations, automation, network_identity_device
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 401000.0–510000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/8f1b8c6b-b414-4026-a434-6ca32c3b3e0d/application

### Security Engineer, Infrastructure Security — Security

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 3 evidence-overlap categories
- **Location:** A_US_REMOTE_STRONG (HIGH) — workplace_type=Remote and US - Remote appears in primary or secondary locations
- **Primary / secondary:** US - Remote / New York City, Seattle, San Francisco
- **Workplace metadata:** workplace_type='Remote', is_remote=1
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 3 categories: api_integrations, automation, network_identity_device
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/f51f750f-a737-4441-8f96-30133a2a8049/application

### Security Program Manager — Security

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** B_US_REMOTE_AMBIGUOUS (MEDIUM) — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** US - Remote / New York City, Seattle, Washington, DC, San Francisco
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 4 categories: support, api_integrations, automation, documentation
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 129600.0–310000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/6fd50ace-941b-4559-992f-e53f9b76c9a0/application

### Compute Infrastructure, Critical Facilities Manager — Datacenter Design

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 3 evidence-overlap categories
- **Location:** B_US_REMOTE_AMBIGUOUS (MEDIUM) — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** San Francisco / Seattle, US - Remote
- **Workplace metadata:** workplace_type='OnSite', is_remote=0
- **Relocation assistance:** NO
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 3 categories: support, troubleshooting, network_identity_device
- **Experience-year mentions:** 8+ years
- **Education signals:** none detected in extracted qualification section
- **Salary component(s):** USD 199000.0–302000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/4d104ebe-64ff-4421-94c3-03a8982b19ea/application

### Software Engineer, Security Observability — Security

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 3 evidence-overlap categories
- **Location:** B_US_REMOTE_AMBIGUOUS (MEDIUM) — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** San Francisco / New York City, Seattle, US - Remote
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (2 categories)
- **Evidence overlap:** 3 categories: support, scripting_programming, sql_data
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** oy, and maintain robust software solutions that support our security and detection capabilities. This role is open to remote employees, or relocation assistance is available to one of our OpenAI offices in San Francisco, Seattle, or New York City. In this role, you will: - Design and develop scalable software systems that facilitate security observability across our infrastructure. - Build and maintain data pipelines that c
- **Salary component(s):** USD 293000.0–325000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/1e4e9985-babf-4bd9-8fe8-a2016250780d/application

### Software Engineer, Plugin Developer Platform — Applied AI Engineering

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 4 categories: api_integrations, automation, uat_testing, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** ioritize, and the tradeoffs you make. This role is based in San Francisco. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. What You’ll Do - Design and ship APIs, SDKs, and services that developers use to extend ChatGPT and Codex. - Make plugins easier to create, test, publish, update, and share. - Improve compatibility and consistency across ChatGPT and C
- **Office requirement context:** problems you prioritize, and the tradeoffs you make. This role is based in San Francisco. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. What You’ll Do - Design and ship APIs, SDKs, and services that developers use to extend ChatGPT and Codex. - Make plugins easier
- **Salary component(s):** USD 185000.0–490000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/71838fdf-4476-490c-81b6-4bf0746f6774/application

### Release Engineer | Consumer Devices — Software

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 4
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 4 categories: api_integrations, automation, scripting_programming, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** e to ship together seamlessly. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Design and operate CI/CD pipelines for multi-component builds (bootloader, firmware, OS images, backend, companion apps) using hermetic toolchains. - Define versioning and branching strategies; automate prom
- **Office requirement context:** ardware and software to ship together seamlessly. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Design and operate CI/CD pipelines for multi-component builds (bootloader, firmware, OS images, backend
- **Salary component(s):** USD 207000.0–365000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/63f7f0b3-ba2c-437b-87ba-ec476729f071/application

### Technical Program Manager, AI Safety & Safeguards — Technical Program Management

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** HIGH (5 categories)
- **Evidence overlap:** 4 categories: troubleshooting, api_integrations, automation, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** e will vary by opening and level. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Partner with product, engineering, research, and design to shape technical roadmaps, long-term platform direction, and safeguards priorities across ChatGPT, API, enterprise, and cloud environments. - Trans
- **Office requirement context:** s areas and scope will vary by opening and level. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Partner with product, engineering, research, and design to shape technical roadmaps, long-term platform
- **Salary component(s):** USD 207000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/3a05c5d7-fdd9-4e0e-823a-2ae08b59958b/application

### Software Engineer, Research Developer Productivity — Fleet Clusters

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 4 categories: support, api_integrations, scripting_programming, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** earch. This role is based in San Francisco, CA. For a San Francisco role, we use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. You might thrive in this role if you: - Have supported large monorepo development and deployment before - Are a proficient Python programmer working in large monorepos - Are proficient with Docker and Kubernetes - Experienced in CI
- **Office requirement context:** for OpenAI’s research. This role is based in San Francisco, CA. For a San Francisco role, we use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. You might thrive in this role if you: - Have supported large monorepo development and deployment before - Are a proficient Python
- **Salary component(s):** USD 230000.0–325000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/e6d5ca02-f30b-4ac5-a69d-c947efb430f9/application

### Software Engineer, ML Systems & Training Architecture — Robotics

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='OnSite', is_remote=0
- **Relocation assistance:** YES
- **Office days detected:** not detected
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 4 categories: troubleshooting, automation, scripting_programming, network_identity_device
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** gment without a lot of ego or process overhead. This role will be based in San Francisco, CA and be expected in office 5 days per week and offer relocation assistance to new employees. In this role, you will: - Review, improve, and clean up code across training frameworks and adjacent infrastructure. - Identify risky or low-quality changes before they land, and raise the code quality bar without slowing the team down.
- **Salary component(s):** USD 295000.0–380000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/9117987a-7a59-449e-a702-89e8d0e8cb60/application

### Android Systems Engineer, Consumer Devices — Software

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 4
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 4 categories: support, troubleshooting, api_integrations, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** t patterns are still evolving. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Build deeply integrated Android experiences: Design and implement product experiences that take advantage of Android platform capabilities. - Work across the Android platform: Develop against Android framewo
- **Office requirement context:** m, APIs, and product patterns are still evolving. This role is based in San Francisco, CA. We use a hybrid work model of four days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Build deeply integrated Android experiences: Design and implement product experiences that take advanta
- **Salary component(s):** USD 266000.0–385000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/b08126cc-8134-45f0-aeb3-4b00e96547de/application

### Technical Program Manager, Multimodal — Technical Program Management

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** HIGH (4 categories)
- **Evidence overlap:** 4 categories: troubleshooting, api_integrations, automation, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** able mechanisms that teams adopt. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Build a system for mining production conversations and product signals to identify representative multimodal workflows, user needs, and failure modes. - Establish and maintain evaluations for the highest-pr
- **Office requirement context:** al work into durable mechanisms that teams adopt. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. IN THIS ROLE, YOU WILL: - Build a system for mining production conversations and product signals to identify representative multi
- **Salary component(s):** USD 207000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/9b017213-6467-413f-b72c-59678c5d8bae/application

### Android Engineer, Plugin Developer Platform — Applied AI Engineering

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 4 categories: support, api_integrations, automation, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** ioritize, and the tradeoffs you make. This role is based in San Francisco. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Build Android experiences for plugins, connectors, and interactive apps within ChatGPT. - Develop reusable Android components and interfaces that support a growing ecosystem of developer-built experiences. -
- **Office requirement context:** problems you prioritize, and the tradeoffs you make. This role is based in San Francisco. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Build Android experiences for plugins, connectors, and interactive apps within ChatGPT. - Develop reusa
- **Salary component(s):** USD 185000.0–385000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/e6e5e4b6-a1d9-4a4e-beef-8d3befef08c0/application

### Full Stack Software Engineer, Cybersecurity Products — Codex - Engineering

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type='Hybrid', is_remote=1
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 4 categories: troubleshooting, api_integrations, automation, uat_testing
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** high bar for earning user trust. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Build end-to-end workflows for vulnerability discovery, security scanning, red teaming, findings review, remediation, and reruns. - Design and operate backend services for long-running security work, includi
- **Office requirement context:** rvability, and a high bar for earning user trust. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Build end-to-end workflows for vulnerability discovery, security scanning, red teaming, findings review
- **Salary component(s):** USD 266000.0–445000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/88654e7f-4e23-4e75-8e54-18c10d09b093/application

### Full Stack Software Engineer, Sales Platform — Codex - Engineering

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** REVIEW_SALES_CONTEXT — Sales-adjacent context exists, but no strong sales-function evidence was detected
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 4 categories: support, api_integrations, automation, scripting_programming
- **Experience-year mentions:** 5+ years
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** s needs into full-stack software. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design and deliver full-stack web applications and integrations that support go to market workflows - Define platform and application boundaries that let other teams extend our go to market systems while prote
- **Office requirement context:** complex business needs into full-stack software. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design and deliver full-stack web applications and integrations that support go to market workflows - D
- **Salary component(s):** USD 266000.0–455000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/1f7c6071-ad3a-4903-9b05-4684f5c1a7c8/application

### Software Engineer, Fleet Management — Fleet Clusters

- **Priority:** P2_REVIEW — Potentially workable geography or relocation path; 4 evidence-overlap categories
- **Location:** C_US_RELOCATION_SUPPORTED (HIGH) — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / New York City
- **Workplace metadata:** workplace_type=None, is_remote=None
- **Relocation assistance:** YES
- **Office days detected:** 3
- **Sales classification:** NO_SALES_SIGNAL_FOUND — No strong or contextual sales signal detected by current rules
- **Technical core:** MEDIUM (3 categories)
- **Evidence overlap:** 4 categories: api_integrations, automation, network_identity_device, documentation
- **Experience-year mentions:** none detected in extracted qualification section
- **Education signals:** none detected in extracted qualification section
- **Relocation context:** overall research user experience. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design and build systems to manage both cloud and bare-metal fleets at scale. - Develop tools that integrate low-level hardware metrics with high-level job scheduling and cluster management algorithms. - Le
- **Office requirement context:** treamlining the overall research user experience. This role is based in San Francisco, CA. We use a hybrid work model of 3 days in the office per week and offer relocation assistance to new employees. In this role, you will: - Design and build systems to manage both cloud and bare-metal fleets at scale. - Develop tools that inte
- **Salary component(s):** USD 230000.0–490000.0 / 1 YEAR
- **Apply URL:** https://jobs.ashbyhq.com/openai/7809102e-e82a-4678-bf7c-221de8acc0d6/application


## 11. Named-interest inventory

Broad inventory of titles likely to deserve human attention because they contain support, technical operations, deployment, IT support, program-management, security-investigation, or applied-AI language.

<details>
<summary>Named-interest roles (89 rows)</summary>

| title | team | primary | secondary | workplace | location_class | sales | technical | evidence_overlap | years_mentions | relocation | office_days | salary | priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Partner Solutions Engineer, Ads Solutions - San Francisco | Ads Solutions | San Francisco |  |  | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | NONE_DETECTED | 7 | 5+ years | NO |  | USD 234000.0–260000.0 / 1 YEAR | EXCLUDED_SALES |
| Solutions Engineer, Ads Solutions - San Francisco | Ads Solutions | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | EXCLUDE_STRONG_SALES | NONE_DETECTED | 7 | 5+ years | NO |  | USD 234000.0–260000.0 / 1 YEAR | EXCLUDED_SALES |
| Solutions Engineer, Ads Solutions - Singapore | Ads Solutions | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | EXCLUDE_STRONG_SALES | NONE_DETECTED | 7 | 5+ years | NO |  |  | EXCLUDED_SALES |
| Applied AI Engineer, Codex Core Agent | Codex - Engineering | San Francisco | New York City; Seattle; London, UK |  | D_US_LOCATION_UNCLEAR | NO_SALES_SIGNAL_FOUND | HIGH | 4 |  | NO |  | USD 230000.0–385000.0 / 1 YEAR | P3_BACKGROUND |
| Applied AI Engineer | Go To Market | Abu Dhabi, UAE |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer, Digital Natives | Go To Market | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| IT Support Dublin, EMEA Regional Lead | IT | Dublin, Ireland |  | OnSite | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES | 5 |  | P3_BACKGROUND |
| IT Support Specialist | IT | Seattle | Washington, DC; San Francisco; London, UK | OnSite | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES | 5 | USD 60.58–108.17 / 1 HOUR | P1_DEEP_REVIEW |
| ITAV Deployment Engineer | IT | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 7 |  | NO |  | USD 187000.0–207000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Applied AI Engineer, Cyber, Government | OpenAI for Gov | Washington, DC |  | Hybrid | D_US_LOCATION_UNCLEAR | NO_SALES_SIGNAL_FOUND | HIGH | 7 | 7+ years | NO |  | USD 211000.0–302000.0 / 1 YEAR | P2_REVIEW |
| Applied AI Engineer, Government | OpenAI for Gov | Washington, DC |  | Hybrid | D_US_LOCATION_UNCLEAR | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 | 7+ years | NO |  | USD 211000.0–302000.0 / 1 YEAR | P3_BACKGROUND |
| Applied AI Engineer, Government, International | OpenAI for Gov | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 5 |  | YES | 3 |  | P3_BACKGROUND |
| Security Program Manager | Security | US - Remote | New York City; Seattle; Washington, DC; San Francisco | Hybrid | B_US_REMOTE_AMBIGUOUS | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 5+ years | NO |  | USD 129600.0–310000.0 / 1 YEAR | P2_REVIEW |
| Technical Threat Investigator, Threat Intel Engineering | Security | San Francisco | New York City; US - Remote | Remote | A_US_REMOTE_STRONG | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES |  | USD 347000.0–510000.0 / 1 YEAR | P1_DEEP_REVIEW |
| AI Support Engineer - Dublin | Support Delivery | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | NO |  |  | P3_BACKGROUND |
| AI Support Engineer - Dublin (Weekend Shift) | Support Delivery | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | NO |  |  | P3_BACKGROUND |
| AI Support Engineer - San Francisco | Support Delivery | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | NO |  | USD 180000.0–260000.0 / 1 YEAR | P2_REVIEW |
| AI Support Engineer - San Francisco (Weekend Shift) | Support Delivery | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | NO |  | USD 180000.0–260000.0 / 1 YEAR | P2_REVIEW |
| AI Support Engineer - Singapore | Support Delivery | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Singapore (Korean Speaking) | Support Delivery | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Singapore (Weekend Shift) | Support Delivery | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Tokyo | Support Delivery | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Tokyo (Korean Speaking) | Support Delivery | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Tokyo (Weekend Shift) | Support Delivery | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| AI Support Engineer - Toronto | Support Delivery | Ontario - Remote |  | Remote | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 5+ years | NO |  | CAD 200000.0–290000.0 / 1 YEAR | P3_BACKGROUND |
| AI Support Engineer - Toronto (Weekend Shift) | Support Delivery | Ontario - Remote |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 8 | 8+ years | NO |  |  | P3_BACKGROUND |
| AI Support Engineer, Biosciences - San Francisco | Support Delivery | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | NO_SALES_SIGNAL_FOUND | HIGH | 8 | 8+ years; 8+ years | NO |  | USD 180000.0–260000.0 / 1 YEAR | P2_REVIEW |
| AI Support Engineer, Government - San Francisco, CA | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 8 | 8+ years | YES | 3 | USD 180000.0–260000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| AI Support Engineer, Government - Washington, D.C. | Support Delivery | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | NONE_DETECTED | 8 | 8+ years | YES | 3 | USD 162000.0–234000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Dedicated Support Engineer - Dublin | Support Delivery | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 7 |  | NO |  |  | P3_BACKGROUND |
| Dedicated Support Engineer - London | Support Delivery | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 7 |  | NO |  |  | P3_BACKGROUND |
| Dedicated Support Engineer - San Francisco | Support Delivery | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 7 |  | NO |  | USD 180000.0–260000.0 / 1 YEAR | P2_REVIEW |
| Dedicated Support Engineer - Singapore | Support Delivery | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 7 |  | YES | 3 |  | P3_BACKGROUND |
| Dedicated Support Engineer - Tokyo | Support Delivery | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 7 |  | YES | 3 |  | P3_BACKGROUND |
| Dedicated Support Engineer - Toronto | Support Delivery | Ontario - Remote |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 7 |  | NO |  |  | P3_BACKGROUND |
| Dedicated Support Engineering Lead | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 12+ years; 6+ years | YES | 3 | USD 284000.0–385000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Senior Support Engineer - Dublin | Support Delivery | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 7 | 5+ years | YES | 3 |  | P3_BACKGROUND |
| Senior Support Engineer - San Francisco | Support Delivery | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | HIGH | 7 | 8+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Senior Support Engineer - Singapore | Support Delivery | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 7 | 8+ years | YES | 3 |  | P3_BACKGROUND |
| Senior Support Engineer - Toronto | Support Delivery | Ontario - Remote |  | Remote | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 7 | 8+ years | NO |  | CAD 261000.0–290000.0 / 1 YEAR | P3_BACKGROUND |
| Support Delivery Lead | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 10+ years; 5+ years | YES | 3 | USD 234000.0–260000.0 / 1 YEAR | P2_REVIEW |
| Support Delivery Lead | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 8+ years; 4+ years | YES | 3 | USD 284000.0–315000.0 / 1 YEAR | P2_REVIEW |
| Support Delivery Lead - Toronto | Support Delivery | Ontario - Remote |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 5+ years; 10+ years | NO |  | CAD 297000.0–330000.0 / 1 YEAR | P3_BACKGROUND |
| Support Delivery Lead, Ads | Support Delivery | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | LOW | 5 | 12+ years; 6+ years | YES | 3 | USD 284000.0–315000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Support Delivery Lead, EMEA - Dublin | Support Delivery | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 4+ years; 8+ years | YES | 3 |  | P3_BACKGROUND |
| Support Delivery Lead, Government | Support Delivery | Washington, DC |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 8 | 12+ years; 6+ years | YES | 3 | USD 284000.0–315000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Support Program Manager, Support Delivery | Support Delivery | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 4 | 8+ years | YES |  | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Technical Program Manager, Support Delivery | Support Delivery | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 4 | 8+ years | YES |  | USD 216000.0–240000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Engagement Manager, User Operations | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | 3 |  | YES | 3 | USD 279000.0–310000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Product Engagement Specialist, User Operations | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 8+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P2_REVIEW |
| Strategy & Operations Programs, Support | Support Operations | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 4 | at least 5 years; 8+ years; 5 years of | NO |  | USD 216000.0–310000.0 / 1 YEAR | P3_BACKGROUND |
| Support Operations Lead | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 2 | 10+ years; 4+ years | YES | 3 | USD 279000.0–310000.0 / 1 YEAR | P3_BACKGROUND |
| Support Program Manager, Partnerships | Support Operations | San Francisco |  |  | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 3 | 8+ years | NO |  | USD 216000.0–310000.0 / 1 YEAR | P3_BACKGROUND |
| Support Vendor Manager | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 5 | 5+ years | YES | 3 | USD 216000.0–240000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Technical Systems Program Manager, User Operations | Support Operations | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | MEDIUM | 4 | 8+ years | YES |  | USD 216000.0–240000.0 / 1 YEAR | P2_REVIEW |
| Applied AI Engineer | Technical Success | Seoul, South Korea |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer | Technical Success | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer | Technical Success | Delhi, India | Mumbai, India; Bangalore - Remote | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer - Tokyo | Technical Success | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer, API Platform, Digital Natives | Technical Success | New York City |  | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 8+ years | YES | 3 | USD 251000.0–278000.0 / 1 YEAR | P2_REVIEW |
| Applied AI Engineer, API Platform, Digital Natives | Technical Success | San Francisco | Seattle | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 8+ years | YES | 3 | USD 251000.0–278000.0 / 1 YEAR | P2_REVIEW |
| Applied AI Engineer, Agent Enablement | Technical Success | San Francisco |  |  | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 8 | 4–6 years; 6 years of | YES | 3 | USD 197000.0–280000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Codex | Technical Success | Paris, France |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer, Codex | Technical Success | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer, Codex | Technical Success | Madrid, Spain |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer, Codex | Technical Success | Munich, Germany |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer, Codex | Technical Success | São Paulo |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 | 5+ years | NO |  |  | P3_BACKGROUND |
| Applied AI Engineer, Codex | Technical Success | San Francisco |  |  | D_US_LOCATION_UNCLEAR | NO_SALES_SIGNAL_FOUND | MEDIUM | 3 | 5+ years | NO |  | USD 211000.0–278000.0 / 1 YEAR | P3_BACKGROUND |
| Applied AI Engineer, Codex | Technical Success | Sydney, Australia |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 5 | 5+ years | YES |  |  | P3_BACKGROUND |
| Applied AI Engineer, Codex \| Tokyo | Technical Success | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 5 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer, Cyber | Technical Success | Singapore |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 9 | 5+ years | NO |  |  | P3_BACKGROUND |
| Applied AI Engineer, Cyber | Technical Success | San Francisco | New York City | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | HIGH | 9 | 5+ years | NO |  | USD 211000.0–292000.0 / 1 YEAR | P2_REVIEW |
| Applied AI Engineer, Cyber \| Tokyo | Technical Success | Tokyo, Japan |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 9 | 5+ years | NO |  |  | P3_BACKGROUND |
| Applied AI Engineer, Enterprise | Technical Success | San Francisco | New York City; US - Remote | Hybrid | B_US_REMOTE_AMBIGUOUS | REVIEW_SALES_CONTEXT | HIGH | 6 |  | YES | 3 | USD 251000.0–278000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Enterprise | Technical Success | São Paulo |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 6 |  | NO |  |  | P3_BACKGROUND |
| Applied AI Engineer, Plugins | Technical Success | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 7 | 4-6 years; 6 years of | YES | 3 | USD 197000.0–280000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Applied AI Engineer, Quants | Technical Success | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 7 |  | YES | 3 |  | P3_BACKGROUND |
| Applied AI Engineer, Startups | Technical Success | San Francisco | New York City |  | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | LOW | 2 | 5+ years | YES | 3 | USD 211000.0–278000.0 / 1 YEAR | LOW_TECHNICAL_PRIORITY |
| Applied AI Engineer, Startups | Technical Success | Tokyo, Japan |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | LOW | 2 | 5+ years | YES | 3 |  | LOW_TECHNICAL_PRIORITY |
| Applied AI Engineer, Startups (Codex) | Technical Success | London, UK |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | NO |  |  | P3_BACKGROUND |
| Applied AI Engineer, Startups (Codex) | Technical Success | Paris, France |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | NO |  |  | P3_BACKGROUND |
| Applied AI Engineer, Startups (Codex) | Technical Success | Munich, Germany |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | MEDIUM | 5 |  | NO |  |  | P3_BACKGROUND |
| Early Access Deployment Engineer | Technical Success | San Francisco |  | Hybrid | C_US_RELOCATION_SUPPORTED | REVIEW_SALES_CONTEXT | HIGH | 6 | 4+ years | YES | 3 | USD 250000.0–330000.0 / 1 YEAR | P1_DEEP_REVIEW |
| Partner AI Deployment Engineer - AWS | Technical Success | Bangalore - Remote | Mumbai, India; Delhi, India |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | LOW | 2 | 8+ years | NO |  |  | LOW_TECHNICAL_PRIORITY |
| Partner Applied AI Engineer | Technical Success | San Francisco | New York City | Hybrid | C_US_RELOCATION_SUPPORTED | NO_SALES_SIGNAL_FOUND | MEDIUM | 4 | 8+ years | YES | 3 | USD 197000.0–278000.0 / 1 YEAR | P2_REVIEW |
| Senior Support Specialist, Ads | Trust & Safety | Ontario - Remote |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | MEDIUM | 7 | 6+ years | NO |  | CAD 170000.0–188000.0 / 1 YEAR | P3_BACKGROUND |
| Senior Support Specialist, Ads | Trust & Safety | San Francisco |  | Hybrid | D_US_LOCATION_UNCLEAR | REVIEW_SALES_CONTEXT | MEDIUM | 7 | 6+ years | NO |  | USD 189000.0–280000.0 / 1 YEAR | P2_REVIEW |
| Technical Operations Analyst, User Safety & Risk | Trust & Safety | London, UK |  | Hybrid | E_NON_US_OR_JURISDICTION_MISMATCH | NO_SALES_SIGNAL_FOUND | HIGH | 6 | 5+ years | NO |  |  | P3_BACKGROUND |
| Manager, Senior Support Engineering | User Operations | Dublin, Ireland |  |  | E_NON_US_OR_JURISDICTION_MISMATCH | REVIEW_SALES_CONTEXT | HIGH | 4 | 10+ years; 5+ years | YES | 3 |  | P3_BACKGROUND |

</details>

## 12. Experience and education diagnostics

<details>
<summary>Experience-year mentions from qualification sections (432 rows)</summary>

| title | team | location | qualification_method | mentions | contexts |
| --- | --- | --- | --- | --- | --- |
| APAC Sales Development Leader | Account Associates | Singapore | whole_description_fallback | 10+ years | regional sales leadership on how to capture and accelerate enterprise demand. You may thrive in this role if you - Have 10+ years of experience in enterprise sales, revenue, or GTM leadership. - Bring significant experience leading SDR or pipeline generation organizations across APAC. - Have experience managing distributed, multicultural teams acr |
| Account Associate - EMEA | Account Associates | Dublin, Ireland | whole_description_fallback | 6+ years; 4+ years | munication while building a deep understanding of how leading companies adopt AI. We are looking for individuals with 4-6+ years of professional experience (2-3 of those in a full 360 closing role) who are motivated to grow into world-class enterprise sellers over time. While many individuals in this role go on to become Account Directors or take \|\| I-enabled GTM workflows (GPTs/agents) to scale prospecting and qualification You may thrive in this role if… |
| Account Associate - EMEA (German Speaking) | Account Associates | Dublin, Ireland | whole_description_fallback | 6+ years; 4+ years | munication while building a deep understanding of how leading companies adopt AI. We are looking for individuals with 4-6+ years of professional experience (with 2-3 of those in a full 360 sales closing role) who are motivated to grow into world-class enterprise sellers over time. While many individuals in this role go on to become Account Direct \|\| I-enabled GTM workflows (GPTs/agents) to scale prospecting and qualification You may thrive in this role if… |
| Account Associate - SF | Account Associates | San Francisco | whole_description_fallback | 3+ years; 3+ years | munication while building a deep understanding of how leading companies adopt AI. We are looking for individuals with 1-3+ years of professional sales experience who are motivated to grow into world-class enterprise sellers over time. While many individuals in this role go on to become Account Directors or take on broader GTM roles, progression i \|\| enabled GTM workflows (GPTs/agents) to scale prospecting and qualification You may thrive in this role if y… |
| Account Associate - Singapore (ANZ Market) | Account Associates | Singapore | whole_description_fallback | 6+ years; 4+ years | munication while building a deep understanding of how leading companies adopt AI. We are looking for individuals with 4-6+ years of professional experience who are motivated to grow into world-class enterprise sellers over time. While many individuals in this role go on to become Account Directors or take on broader GTM roles, progression is base \|\| I-enabled GTM workflows (GPTs/Agents) to scale prospecting and qualification You may thrive in this role if… |
| Account Associate - Singapore (Korean-speaking) | Account Associates | Singapore | whole_description_fallback | 6+ years; 4+ years | munication while building a deep understanding of how leading companies adopt AI. We are looking for individuals with 4-6+ years of professional experience who are motivated to grow into world-class enterprise sellers over time. While many individuals in this role go on to become Account Directors or take on broader GTM roles, progression is base \|\| n this role if you: - Speak fluent business-level Korean, as you will be engaging with Korean-speaking cust… |
| Account Associate, Japan | Account Associates | Tokyo, Japan | heading:qualifications | 5+ years; 7-10 years; 10 years of | perating in an ambiguous and fast-moving environment Preferred Qualifications - 7-10 years of total work experience - 3-5+ years of relevant experience in SDR, BDR, inside sales, startup sales, enterprise/commercial AD, or similar GTM roles - Some closing or full-cycle sales experience is strongly preferred - Can build trust quickly with Japanese \|\| wnership, strong judgment, and comfort operating in an ambiguous and fast-moving environment Preferred Qual… |
| Account Associate- EMEA (French Speaking) | Account Associates | Dublin, Ireland | whole_description_fallback | 6+ years; 4+ years; 2-3 years; 3 years of | munication while building a deep understanding of how leading companies adopt AI. We are looking for individuals with 4-6+ years of professional experience (with 2-3 years of those in a full 360 sales closing role) who are motivated to grow into world-class enterprise sellers over time. While many individuals in this role go on to become Account \|\| I-enabled GTM workflows (GPTs/agents) to scale prospecting and qualification You may thrive in this role if … |
| Sales Development Leader - Tokyo | Account Associates | Tokyo, Japan | whole_description_fallback | 10+ years | the Japanese market back into the broader APAC and global GTM organization YOU MAY THRIVE IN THIS ROLE IF YOU - Have 6–10+ years of experience in sales, business development, or GTM roles, with significant experience in the Japanese market - Bring experience managing SDRs, BDRs, or business development teams in enterprise SaaS, cloud, platform, o |
| Sales Development Manager, Enterprise (AMER) | Account Associates | San Francisco | whole_description_fallback | 10+ years | rket feedback and customer insights back into the broader GTM organization YOU MAY THRIVE IN THIS ROLE IF YOU: - Have 6–10+ years of experience in sales, business development, or GTM roles - Bring experience managing SDRs or business development teams in enterprise SaaS or platform businesses - Have a strong understanding of enterprise prospecting |
| Client Partner, Ads Solutions | Ads Solutions | San Francisco | heading:you might thrive in this role if you | 10+ years; 3+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Has 10+ years of experience in performance marketing, digital marketing, or client-facing strategy and consulting roles. - Has 3+ years of experience as proven advisor influencing executives and clients. - Has experience owning reven \|\| years of experience in performance marketing, digital marketing, or client-facing strategy and consulting roles. - Has 3+ years of experience as proven advisor influencing executives… |
| Client Partner, Ads Solutions (Spanish Speaking) | Ads Solutions | Dublin, Ireland | heading:you might thrive in this role if you | 10+ years; 3+ years | You might thrive in this role if you: - Have 10+ years of experience in performance marketing, digital marketing, or client-facing strategy and consulting roles. - Have 3+ years of experience as proven advisor influencing executives and clients. - Fluent in Spanish & Englis \|\| years of experience in performance marketing, digital marketing, or client-facing strategy and consulting roles. - Have 3+ years of experience as proven advisor influencing executiv… |
| Client Partner, Ads Solutions - Travel | Ads Solutions | San Francisco | heading:you might thrive in this role if you | 10+ years; 3+ years | You might thrive in this role if you: - Have 10+ years of experience in digital advertising, performance marketing, client strategy, consulting, or enterprise sales. - Have experience working with Travel advertisers, such as airlines, hotels, cruise line, online travel agen \|\| ertisers, such as airlines, hotels, cruise line, online travel agencies, travel marketplaces, or tourism boards. - Have 3+ years of experience advising and influencing senior execut… |
| Customer Success Manager - Ads Solutions (Spanish speaking) | Ads Solutions | Dublin, Ireland | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 5-10+ years of experience in digital advertising, account management, customer success, consulting or a related client-facing role. - Have experience managing advertiser or agency relationships in a platform, publisher, or adtech e |
| Customer Success Manager, Ads Solutions (New York City) | Ads Solutions | New York City | heading:you might thrive in this role if you | 10+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Has 5-10+ years of experience in digital advertising, account management, customer success, consulting or a related client-facing role. - Has experience managing advertiser or agency relationships in a platform, publisher, or adtech en |
| Customer Success Manager, Ads Solutions (San Francisco) | Ads Solutions | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 5-10+ years of experience in digital advertising, account management, customer success, consulting or a related client-facing role. - Have experience managing advertiser or agency relationships in a platform, publisher, or adtech e |
| Customer Success Manager, Ads Solutions (Seattle) | Ads Solutions | Seattle | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 5-10+ years of experience in digital advertising, account management, customer success, consulting or a related client-facing role. - Have experience managing advertiser or agency relationships in a platform, publisher, or adtech e |
| EMEA Vendor Lead, Ad Sales | Ads Solutions | Dublin, Ireland | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you have: - 5+ years of experience in vendor operations, commercial operations, outsourced sales, or a scaled revenue organization. - Experience in Ads, advertiser growth, performance marketing, or a comparable SMB sales motion. - Working k |
| Partner Solutions Engineer, Ads Solutions - San Francisco | Ads Solutions | San Francisco | heading:requirements | 5+ years | ams on technical capabilities, integrations, and evolving product features. You will thrive in this role if you: - Have 5+ years of experience in solutions engineering, sales engineering, technical account management, adtech, martech, or a related client-facing technical role. - Have hands-on experience with digital advertising measurement, pixel |
| Regional Client Partner, Ads Solutions (Mumbai) | Ads Solutions | Mumbai, India | heading:you might thrive in this role if you | 10+ years; 3+ years | You might thrive in this role if you: - Have 10+ years of experience in performance marketing, digital marketing, or client-facing strategy and consulting roles. - Have 3+ years of experience as proven advisor influencing executives and clients. - Have experience owning rev \|\| years of experience in performance marketing, digital marketing, or client-facing strategy and consulting roles. - Have 3+ years of experience as proven advisor influencing executiv… |
| Regional Manager, Ads Solutions (APAC) | Ads Solutions | Singapore | heading:you might thrive in this role if | 12+ years; 5+ years | You might thrive in this role if: - Have 12+ years of experience in digital advertising, media, technology, or related commercial leadership roles. - Have 5+ years of experience leading high-performing sales, account management, customer success, or revenue teams. - Hav \|\| Have 12+ years of experience in digital advertising, media, technology, or related commercial leadership roles. - Have 5+ years of experience leading high-performing sales, account mana… |
| Solutions Engineer, Ads Solutions - San Francisco | Ads Solutions | San Francisco | heading:requirements | 5+ years | ams on technical capabilities, integrations, and evolving product features. You will thrive in this role if you: - Have 5+ years of experience in solutions engineering, sales engineering, technical account management, adtech, martech, or a related client-facing technical role. - Have hands-on experience with digital advertising measurement, pixel |
| Solutions Engineer, Ads Solutions - Singapore | Ads Solutions | Singapore | heading:requirements | 5+ years | ams on technical capabilities, integrations, and evolving product features. You will thrive in this role if you: - Have 5+ years of experience in solutions engineering, sales engineering, technical account management, adtech, martech, or a related client-facing technical role. - Have hands-on experience with digital advertising measurement, pixel |
| Applied AI Software Engineer, GTM Growth Engineering | Applied AI | San Francisco | whole_description_fallback | 4+ years | privacy, security, reliability, human oversight, and safe operational rollout. You might be a great fit if you have: - 4+ years of software, backend, applied AI, or product-engineering experience building reliable production systems. - Experience building AI agents, LLM-powered applications, or other model-driven workflows that operated on real |
| Backend Software Engineer - Codex for Finance | Applied AI | San Francisco | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 5+ years of professional software engineering experience, with a strong track record of building and operating production backend systems. - Proficiency in one or more backend languages, such as Python, Go, Rust, or TypeScript, |
| Full Stack Software Engineer - Codex for Finance | Applied AI | San Francisco | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 5+ years of professional software engineering experience, with a strong track record of building and shipping production software across the stack. - Expertise in TypeScript, React, and modern web technologies, along with strong |
| Full Stack Software Engineer, Gov | Applied AI | Washington, DC | heading:you might thrive in this role if you | 9+ years | You might thrive in this role if you: - 9+ years of relevant engineering experience at tech and product-driven companies - Proficiency with JavaScript, React, and other web technologies - Proficiency with some backend language (we use Python) - Some experience with un |
| Growth - Digital Marketing (Business) | Applied AI | San Francisco | heading:you might thrive in this role if you | 8+ years; 6+ years | You might thrive in this role if you: - 8+ years of B2B growth, demand generation, or performance marketing experience, ideally in high-growth technology or subscription businesses. - 6+ years of deep, hands-on experience leading paid marketing across channels, includ \|\| demand generation, or performance marketing experience, ideally in high-growth technology or subscription businesses. - 6+ years of deep, hands-on experience leading paid marketing across… |
| Growth - Digital Marketing (Consumer) | Applied AI | San Francisco | heading:you might thrive in this role if you | 8+ years; 6+ years | You might thrive in this role if you have: - 8+ years of consumer growth, acquisition, or performance marketing experience, ideally for a scaled global technology, marketplace, subscription, or mobile product. - 6+ years of deep, hands-on experience leading paid marketing \|\| rformance marketing experience, ideally for a scaled global technology, marketplace, subscription, or mobile product. - 6+ years of deep, hands-on experience leading paid marketing ac… |
| Growth - Digital Marketing (Enterprise) | Applied AI | San Francisco | heading:you might thrive in this role if you | 10+ years; 6+ years | You might thrive in this role if you have: - 10+ years of B2B growth, demand generation, or performance marketing experience, including meaningful ownership of enterprise programs. - 6+ years of deep, hands-on experience leading paid marketing across channels, including Pai \|\| rowth, demand generation, or performance marketing experience, including meaningful ownership of enterprise programs. - 6+ years of deep, hands-on experience leading paid marketing … |
| Growth - Lifecycle Lead | Applied AI | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you have: - 10+ years of experience in lifecycle, CRM, retention, growth, product marketing, or marketing technology, ideally in a global consumer or subscription business. - A track record of building and scaling lifecycle tooling or platfo |
| Growth - Lifecycle Lead (B2B) | Applied AI | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you have: - 10+ years of experience in lifecycle, CRM, retention, growth, product marketing, or marketing technology, ideally in a global B2B business serving self serve small businesses, enterprises, and developers. - A track record of buil |
| Software Engineer, GTM Growth Engineering | Applied AI | San Francisco | heading:requirements | 4+ years | eed, product quality, accessibility, reliability, privacy, safety, and operational simplicity. What We're Looking For - 4+ years of experience as a software, product, or full-stack engineer building high-quality, user-facing products. - Strong frontend or full-stack engineering skills, with comfort across modern web applications, APIs, data model |
| Software Engineer, Native Learning Experiences | Applied AI | San Francisco | heading:requirements | 5+ years; 5+ years | adeoffs across speed, quality, scalability, and operational simplicity in a 0-to-1 product area. Qualifications: - Have 5+ years of experience as a software engineer working on applied AI or user-facing systems - Former founder, or early engineer at a startup who built a product from scratch is a plus - Substantial experience building and operati \|\| new tools. - You have strong opinions about product craft but can adjust quickly as evidence comes in. Nice… |
| Subject Matter Expert, Investment Banking | Applied AI | San Francisco | heading:requirements | 2+ years | ify domain knowledge, and ensure responsible financial-services deployment. You Might Thrive in This Role If You - Have 2+ years of investment banking experience, including live transaction execution and the production of high-quality analyses, financial models, and client materials. Demonstrated ability and judgment matter more than title or ten |
| Android Engineer, Ad Formats | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | 4+ years | You might thrive in this role if you - Have 4+ years of professional software engineering experience with meaningful Android ownership. - Have a track record of building and shipping high-quality Android applications in production, especially for user-facing, performance- |
| Android Engineer, Applied Foundations | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | 4+ years | You might thrive in this role if you: - Have 4+ years of professional software engineering experience. - Have a proven track record of building high-quality Android applications in production. - Are fluent in Kotlin (and/or Java) and familiar with Android development tools |
| ChatGPT Performance Engineer | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | 7+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 7+ years of experience in software engineering with a strong track record in performance or reliability of high-scale distributed systems. - Are deeply comfortable with performance profiling tools and tracing systems. - Have exp |
| Data Engineer | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | 3+ years; 8+ years | You might thrive in this role if you: - Have 3+ years of experience as a data engineer and 8+ years of any software engineering experience(including data engineering). - Proficiency in at least one programming language commonly used within Data Engineering, such as Python, \|\| You might thrive in this role if you: - Have 3+ years of experience as a data engineer and 8+ years of any software engineering experience(including data engineering). - Proficiency … |
| Data Engineer, Core Experimentation | Applied AI Engineering | Seattle | heading:you might thrive in this role if you | 3+ years; 8+ years | You might thrive in this role if you: - Have 3+ years of experience as a data engineer and 8+ years of any software engineering experience(including data engineering). - Proficiency in at least one programming language commonly used within Data Engineering, such as Python, \|\| You might thrive in this role if you: - Have 3+ years of experience as a data engineer and 8+ years of any software engineering experience(including data engineering). - Proficiency … |
| Founding Full Stack Software Engineer, Legal | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | 6+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 6+ years of professional software engineering experience. - Have built and shipped full-stack applications end-to-end, from early prototypes through production systems. - Are excited by ambiguous, open-ended problems and can tur |
| Full Stack Software Engineer, Education | Applied AI Engineering | San Francisco | whole_description_fallback | 5+ years | ucts that may inform both consumer and B2B education experiences over time Your background might look something like: - 5+ years of professional engineering experience (excluding internships) in relevant roles at tech and product-driven companies - Former founder, or early engineer at a startup who has built a product from scratch is a plus - Pro |
| Software Engineer, Ad Formats | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | 7+ years | You might thrive in this role if you: - Have 7+ years of experience building high-scale consumer product experiences, creative systems, ads systems, or platform infrastructure. - Have a track record of architecting and delivering complex systems that power user-facing expe |
| Software Engineer, Ads Manager | Applied AI Engineering | Seattle | heading:you might thrive in this role if you | 7+ years | You might thrive in this role if you: - Have 7+ years of experience building high-scale consumer, enterprise, marketplace, or ads-related systems. - Have a track record of architecting and delivering complex distributed systems, APIs, or advertiser-facing platforms. - Have |
| Software Engineer, Consumer Health | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | 5+ years | duct engineer who has shipped consumer-facing products and cares deeply about usability, performance, and craft. - Have 5+ years of experience building and shipping production software. - Have deep experience in at least one of mobile, frontend, or full-stack product development. - Enjoy working closely with design and product partners and contri |
| Software Engineer, Habitat (Online Data) | Applied AI Engineering | Seattle | heading:requirements | 8+ years; 3+ years | many internal teams - Experience with multi-region systems, consistency semantics, and failover design QUALIFICATIONS - 8+ years of industry experience building production software, including 3+ years leading large-scale, complex projects or technical initiatives as a tech lead or senior IC - Strong passion for building distributed systems at sca \|\| semantics, and failover design QUALIFICATIONS - 8+ years of industry experience building production softwar… |
| Software Engineer, Healthcare | Applied AI Engineering | San Francisco | heading:requirements | 5+ years | this role if you: - Are a strong backend or full-stack engineer who enjoys building durable production systems. - Have 5+ years of experience writing maintainable, production-quality software. - Have strong experience with backend services, APIs, data systems, or distributed systems. - Are comfortable reasoning about system architecture, data mo |
| Software Engineer, Integrity Foundations | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | at least 3 years; 3 years of | You might thrive in this role if you: - Have at least 3 years of professional software engineering experience. - Have experience setting up and maintaining production backend services and data pipelines. - Have a humble attitude, an eagerness to help your colleagues, and a desire \|\| You might thrive in this role if you: - Have at least 3 years of professional software engineering experience. - Have experience setting up and maintaining production backend … |
| Software Engineer, Monetization Data Systems | Applied AI Engineering | Mountain View | heading:you might thrive in this role if you | minimum of 7+ years; 7+ years | You might thrive in this role if you: - Possess a minimum of 7+ years of professional software engineering experience with deep experience building and operating production software systems, backend services, or distributed systems at scale. - Are highly proficient in at least one general \|\| You might thrive in this role if you: - Possess a minimum of 7+ years of professional software engineering experience with deep experience building and operating prod… |
| Software Engineer, Monetization Delivery | Applied AI Engineering | San Francisco | heading:requirements | 10+ years | ring orgs to ensure the infra layer is flexible, performant, and resilient You might thrive in this role if you: - Have 10+ years of experience building and operating large-scale distributed systems - Have experience designing mission-critical systems with demanding reliability, performance, and correctness requirements - Think in systems—architec |
| Software Engineer, Monetization ML Infrastructure | Applied AI Engineering | San Francisco | heading:requirements | 7+ years | teams to accelerate the development and deployment of advertising systems. You might thrive in this role if you: - Have 7+ years of professional software engineering experience building large-scale distributed systems or machine learning infrastructure. - Have experience building platforms that support machine learning workflows, including data p |
| Software Engineer, Monetization Product & Platform | Applied AI Engineering | San Francisco | heading:requirements | 7+ years | , culture, and best practices within a fast-moving, multidisciplinary team YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 7+ years of experience building high-scale consumer, enterprise, or ads-related systems - Have a track record of architecting and delivering complex distributed systems with high reliability and performance requirements - Are co |
| Software Engineer, Scaled Abuse | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | at least 5 years; at least 2 years; 5 years of | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have at least 5 years of software engineering experience in backend and data systems. - Have at least 2 years experience in fraud or abuse analysis, investigation, and/or operations - Can dive into our codebase, intuit how it works, and be a \|\| IVE IN THIS ROLE IF YOU: - Have at least 5 years of software engineering experience in backend and data systems. - Have at least 2 years experience in fraud or abuse analysis… |
| iOS Engineer, Applied Foundations | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | 4+ years | You might thrive in this role if you: - Have 4+ years of professional software engineering experience. - Have a proven track record of building high-quality iOS applications in production, especially for systems that need to be reliable and resilient at scale. - Have owned |
| Software Engineer - Privacy & Compliance | Applied AI Infrastructure | San Francisco | heading:requirements | 5+ years | tion that elevate trustworthy data access patterns across the organization. YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE - 5+ years of industry experience building and operating backend or infrastructure systems in production. - Strong software engineering fundamentals, with fluency in at least one major programming language (e.g., Python, Go, Rust, |
| Software Engineer, Build Systems / CI | Applied AI Infrastructure | San Francisco | whole_description_fallback | 5+ years | tems - Postgres, Kafka, and internal services used to power engineering platforms You May Be A Strong Fit If You - Have 5+ years of software engineering experience, including significant experience building infrastructure or tooling for developers. - Have hands-on experience with Bazel, Buck, Pants, Gradle, or similar build systems, and understan |
| Software Engineer, Caching Infrastructure | Applied AI Infrastructure | San Francisco | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 5+ years of experience building and scaling distributed systems, with a strong focus on caching, load balancing, or storage systems. - Have deep expertise with Redis, Memcached, or similar solutions, including clustering, durabi |
| Software Engineer, ChatGPT Infrastructure | Applied AI Infrastructure | London, UK | heading:you might thrive in this role if you | 4+ years | Take ownership of projects from design and implementation through deployment and ongoing improvement. Qualifications - 4+ years of professional software engineering experience, including significant experience building backend or distributed systems. - Strong proficiency in at least one general-purpose programming language and experience writing |
| Software Engineer, Cloud Infrastructure | Applied AI Infrastructure | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you: - Have 5+ years building core infrastructure - Have experience operating orchestration systems such as Kubernetes at scale - Have experience building abstractions over cloud platforms - Take pride in building and operating scalable, re |
| Software Engineer, Cloud Infrastructure | Applied AI Infrastructure | London, UK | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you: - Have 5+ years building core infrastructure - Have experience operating orchestration systems such as Kubernetes at scale - Have experience building abstractions over cloud platforms - Take pride in building and operating scalable, re |
| Software Engineer, Database Systems | Applied AI Infrastructure | San Francisco | heading:you might thrive in this role if you | 4+ years; 2+ years | ility, correctness, and reliability - Thrive in fast-paced environments with high autonomy and impact Qualifications: - 4+ years of relevant industry experience, with 2+ years leading large scale, complex projects or teams as an engineer or tech lead - Experience with distributed systems at scale, with a strong focus on performance, reliability, \|\| fast-paced environments with high autonomy and impact Qualifications: - 4+ years of relevant industry experi… |
| Software Engineer, Developer Productivity | Applied AI Infrastructure | San Francisco | heading:requirements | 5+ years; 3+ years | s includes an on-call rotation to respond to critical incidents as needed. You might thrive in this role if you: - Have 5+ years of experience in engineering, including 3+ years of experience in infrastructure building tooling for developers. - Have experience-driven empathy for the tools, frustrations, and processes that slow engineering teams d \|\| ical incidents as needed. You might thrive in this role if you: - Have 5+ years of experience in engineerin… |
| Full Stack Engineer, Enterprise Expansions | Codex - Engineering | San Francisco | whole_description_fallback | 7+ years | take on, and turn those insights into prototypes and production features. Your background might look something like: - 7+ years of professional software engineering experience, excluding internships, building and shipping user-facing products. - Strong frontend engineering skills and experience building production web applications with modern fr |
| Full Stack Software Engineer, Sales Platform | Codex - Engineering | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you: - 5+ years of professional software engineering experience, excluding internships, on product-driven teams. - Experience building large-scale, full-stack software applications in collaboration with cross-functional teams. - Make s |
| Product Engineer, Full Stack - Agents | Codex - Engineering | San Francisco | heading:you might thrive in this role if you | 7+ years | You might thrive in this role if you have: - 7+ years of professional full-stack or product engineering experience, ideally building user-facing products in product-driven or enterprise environments. - A track record of shipping polished user-facing products and production |
| Product Manager, Learning | Codex - Engineering | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 10+ years of product management experience with strong leadership, xfn collaboration, and communication skills. - Bring experience in education, EdTech, or learning research, or are eager to dive into complex, research-driven pro |
| Software Engineer, Cloud Agents | Codex - Engineering | San Francisco | whole_description_fallback | 9+ years | Deploy services that can operate across different environments and clouds. Your background might look something like: - 9+ years of professional engineering experience, excluding internships, in relevant roles at technology and product-driven companies. - Experience leading large-scale backend, platform, or infrastructure projects from ambiguous |
| Software Engineer, Enterprise Controls | Codex - Engineering | San Francisco | heading:requirements | 9+ years | testing, observability, production debugging, and continuous improvement. Your background might look something like: - 9+ years of professional backend software engineering experience, excluding internships, building and operating production services. - Deep backend engineering expertise and a track record of shipping complex product or platform |
| Software Engineer, OpenAI Presence | Codex - Engineering | San Francisco | heading:requirements | 9+ years | requirements into working software. Your background might look something like: - 9+ years of professional engineering experience, excluding internships, in backend, platform, or product engineering roles. - A track record of hands-on technical leadership, including setting architecture, breaking complex prob |
| Communications Manager, Monetization | Communications | San Francisco | heading:you might thrive in this role if you | 12+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 12+ years of communications experience, with deep experience in ads and monetization at a high-growth technology company. - Strong press instincts and relationships, with a track record of shaping narratives and landing impactful |
| Internal Communications Lead, Enterprise & Growth | Communications | San Francisco | whole_description_fallback | 10+ years; 1-2 years | and feedback, and turn successful approaches into practices others can use. YOU WILL THRIVE IN THIS ROLE IF YOU HAVE: - 10+ years of relevant experience in internal or executive communications, marketing communications, operations, or a related field, with demonstrated ownership of complex communications programs. People Management experience (1-2 \|\| ions, or a related field, with demonstrated ownership of complex communications programs. People Managemen… |
| Internal Communications, Enterprise & Growth | Communications | San Francisco | heading:you might thrive in this role if you | 3+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 3+ years of experience in internal communications, event coordination, marketing communications, operations, or a related field. - Experience supporting internal events, team meetings, All Hands, or employee engagement moments. |
| Internal Communications, Research and Product | Communications | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you: - Have 5+ years of experience in internal communications, product communications, journalism, or a related field, ideally with exposure to research or technical teams. - Bring strong writing, editing, and storytelling skills, with an e |
| Research Communications Manager | Communications | San Francisco | heading:you might thrive in this role if you | 7+ years | You might thrive in this role if you have: 7+ years of experience in research, science, technology, or safety-related communications. Demonstrated experience working directly with scientists, engineers, researchers, or technical leaders. Strong understanding of AI, machi |
| Strategy & Systems Manager, Communications | Communications | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 10+ years of experience, including significant experience in strategy and operations, business operations, or program leadership, with a track record of working closely with senior leaders to drive complex cross-functional initia |
| Business Development Lead, Compute Strategy | Compute | US - Remote | heading:qualifications | 8+ years | Qualifications - Have 8+ years of experience in business development, strategic partnerships, private equity, corporate development, project development, or infrastructure finance, with relevant experience in at least one focus area above. - Have a d |
| Capacity Systems Software Engineer | Compute | San Francisco | heading:qualifications | 5+ years | Qualifications - 5+ years of experience in software engineering, platform engineering, infrastructure engineering, or related technical disciplines. - Strong programming experience in Python, Go, Java, TypeScript, or similar languages. - Experie |
| Community Engagement Lead, Ohio | Compute | US - Remote | heading:qualifications | 8+ years | Qualifications - 8+ years in community affairs, public engagement, or corporate communications. - Proven track record engaging diverse community stakeholders for large infrastructure or technology projects. - Strong public speaking and facilitat |
| Data Center Hardware Quality & Reliability Engineer | Compute | San Francisco | heading:requirements | 8+ years; 3+ years | lectrical, mechanical, computer, materials, reliability engineering, physics, or equivalent experience; MS preferred. • 8+ years in hardware quality/reliability, server/rack systems, or mission-critical infrastructure; 3+ years owning field-failure, RMA, or CAPA outcomes. • Solid working understanding of hardware and system architecture across bo \|\| nce; MS preferred. • 8+ years in hardware quality/reliability, server/rack systems, or mission-critical inf… |
| Development Lead | Compute | US - Remote | heading:requirements | 6+ years | mendations and prepare the readiness package for transition into design, construction, and operations. Qualifications - 6+ years in land development, infrastructure development, data center development, energy-project development, electrical, mechanical, civil or environmental engineering, or related project delivery. - Experience advancing large |
| Development Planner, Industrial Compute | Compute | US - Remote | heading:requirements | 8+ years | oks that allow OpenAI to scale shell-capacity decisions across regions and infrastructure generations. Qualifications - 8+ years of experience in data center development, infrastructure planning, capacity planning, real estate development, construction planning, program controls, or a related field. - Experience developing or managing portfolio-l |
| Economic Development Lead | Compute | US - Remote | heading:qualifications | 6+ years | Qualifications - 6+ years in economic development, public-private partnerships, infrastructure development, government affairs, or a related field. - Experience structuring and negotiating incentive packages for large infrastructure, energy, tec |
| Infrastructure Operations & Sustainability Lead | Compute | US - Remote | heading:requirements | 12+ years | ity practices to scale across sites, geographies, infrastructure partners, and technology generations. Qualifications - 12+ years of experience in sustainability, infrastructure operations, environmental strategy, data center infrastructure, the built environment, or a related field. - Experience leading sustainability or operational-improvement p |
| Infrastructure Sourcing Operations Lead | Compute | San Francisco | heading:requirements | 8+ years | s aging decisions and material risks, quantifies schedule or commercial impact, and recommends action. Qualifications - 8+ years of experience in sourcing operations, procurement, infrastructure program management, construction operations, supply chain, or a related field, or equivalent demonstrated experience. - Demonstrated ownership of complex |
| Performance Modeling Engineer ~2 | Compute | San Francisco | heading:qualifications | 1–2 years; 2 years of | Qualifications - 1–2 years of experience in software engineering, systems modeling, performance analysis, or related technical work - Strong programming skills and experience building technical tools, scripts, or frameworks - Familiarity with sys \|\| Qualifications - 1–2 years of experience in software engineering, systems modeling, performance analysis, or related technical work - Strong programming skills and experience building technical tools, scripts,… |
| Physical Network & Structured Cabling Engineer | Compute | San Francisco | heading:requirements | 10+ years | s. Qualifications - Bachelor’s degree in Engineering, Telecommunications, or related field, or equivalent experience. - 10+ years of experience designing and delivering physical network infrastructure and structured cabling systems for large-scale data centers, including responsibility for design decisions, construction coordination, and operation |
| Site Operations Technician | Compute | San Francisco | heading:qualifications | 2+ years | - Have an Associate's degree, technical certification, military experience, or equivalent practical experience. - Have 2+ years supporting data center operations, facilities, hardware operations, manufacturing, industrial operations, or mission-critical infrastructure. - Have experience working in technical or operational environments requiring |
| Software Engineer, Workload Enablement | Compute | San Francisco | heading:qualifications | 5+ years | Qualifications - BS in CS/EE (or equivalent practical experience). - 5+ years in one or more of: ML systems, performance engineering, distributed systems, or HPC. - Strong hands-on experience with: - PyTorch and modern LLM training/inference stacks - Large-scale distributed training concepts (dat |
| Systems Generalist, GPT Infrastructure | Compute | San Francisco | heading:qualifications | 8+ years | Qualifications - 8+ years of professional software engineering experience building large-scale distributed systems, infrastructure platforms, or cloud services, or equivalent depth of experience. - Strong programming skills in one or more of C++ |
| Technical Program Manager, Infrastructure Systems & Tooling | Compute | San Francisco | heading:requirements | 8+ years | on and process improvements that make the organization more predictable, scalable, and effective. Qualifications - Have 8+ years of experience in technical program management, operations program management, infrastructure delivery, operations transformation, or a comparable role in a complex technical environment. - Have led end-to-end software o |
| Technical Program Manager, Manufacturing Operations | Compute | Singapore | heading:qualifications | 8+ years | Qualifications - 8+ years of experience in technical program management, manufacturing operations, NPI, hardware operations, or a related field. - Experience leading complex hardware products from development through qualification, production ra |
| Full Stack Software Engineer, API Experience | Core Product & Platform \| API | New York City | whole_description_fallback | 5+ years | ew NYC-based team with broad ownership over OpenAI’s developer experience. Your background might look something like: - 5+ years of professional engineering experience, excluding internships, in product-driven engineering teams. - Strong experience with TypeScript, React, and modern web application development. - Proficiency in one or more backen |
| Machine Learning Engineer, API Multicloud | Core Product & Platform \| API | San Francisco | heading:requirements | 3+ years | IKE: - Master’s or PhD in Computer Science, Machine Learning, or a related field, or equivalent practical experience. - 3+ years of professional engineering experience in relevant ML, infrastructure, or product-driven engineering roles. - Strong ML engineering experience building, training, fine-tuning, evaluating, or deploying production AI syst |
| Software Engineer, API Enterprise Controls | Core Product & Platform \| API | San Francisco | whole_description_fallback | 9+ years | uest routing, and distributed services, with strong operational ownership. Your background might look something like: - 9+ years of professional engineering experience, excluding internships, in relevant backend, platform, or product-driven engineering roles. - Exceptional backend engineering depth paired with strong product judgment and a track |
| Software Engineer, API Frontiers | Core Product & Platform \| API | New York City | whole_description_fallback | 5+ years | into better observability, diagnostics, and lasting product improvements. Your background might look something like: - 5+ years of experience building and operating backend services or developer-facing APIs in production. - Strong software engineering fundamentals, with practical knowledge of distributed systems, concurrency, and asynchronous ex |
| Software Engineer, API Multicloud | Core Product & Platform \| API | San Francisco | heading:requirements | 7+ years | y, incident diagnosis, reliability improvements, and practical automation. Your background might look something like: - 7+ years of experience leading cloud infrastructure or distributed systems projects from architecture through launch and ongoing production ownership. - Strong distributed systems fundamentals and the ability to reason about per |
| Software Engineer, API Multimodal | Core Product & Platform \| API | San Francisco | whole_description_fallback | 7+ years | nch and ongoing iteration, while raising the team’s engineering standards. Your background might look something like: - 7+ years of professional experience, excluding internships, in backend, infrastructure, platform, or product engineering roles. - A track record of designing, building, and operating production backend services, developer-facing |
| Software Engineer, API Safety | Core Product & Platform \| API | San Francisco | whole_description_fallback | 7+ years | unch and ongoing iteration, while raising the team’s engineering standards Your background might look something like: - 7+ years of professional experience, excluding internships, in backend, infrastructure, platform, or product engineering roles. - A track record of designing, building, and operating production backend services, developer-facing |
| Corporate Security GSOC Operator | Corporate Security | San Francisco | whole_description_fallback | 5+ years | in routine training, drills, and skill development to maintain readiness. You may be a fit for this role if you have - 5+ years of experience in GSOC, corporate security, or protective operations, or a bachelor’s degree in a relevant field. - Military, law enforcement, or emergency operations center experience may substitute for traditional GSOC |
| Creative Resource Manager, Business Marketing | Creative | San Francisco | whole_description_fallback | 10+ years | urce decisions, strengthen planning, and support a sustainable creative organization. We’re looking for someone with: - 10+ years of experience personally owning creative resource management, workforce planning, or talent allocation across multiple disciplines and concurrent programs. - A strong understanding of design, copy, motion, video, and we |
| Analytics Engineer, GTM | Data Science | San Francisco | heading:you might thrive in this role if you | 10+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU - Have 10+ years of experience in a relevant data role within fast-moving, results-oriented organizations. - Can independently structure and own ambiguous, high-impact business problems from initial framing through recommendation and ex |
| Applied Data Science & Insights Leader - GTM Intelligence Solutions and Technical Success | Data Science | San Francisco | heading:you might thrive in this role if you | 10+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 10+ years of experience in applied data science, analytics, machine learning, quantitative strategy, or a closely related field. - Deep technical skill in SQL and Python, with the ability to move from raw tables to production-qua |
| Data Scientist, Ads Demand | Data Science | San Francisco | heading:what we're looking for | 7+ years | What We're Looking For Required - 7+ years of experience in data science or analytics within an ads platform, marketplace, or performance-oriented B2B business. - Demonstrated business impact through advertiser demand growth, improved delivery or ROAS, stronger |
| Data Scientist, B2B Demand Generation, Growth & Measurement | Data Science | San Francisco | heading:what we’re looking for | 10+ years | What We’re Looking For - 10+ years in a quantitative role such as Data Science, B2B Demand Gen Marketing Science, Growth Analytics, Decision Science, with meaningful experience supporting B2B marketing, demand generation, pipeline growth, or enterprise a |
| Data Scientist, Business | Data Science | San Francisco | heading:you might thrive in this role if you | At least 10+ years; 10+ years | You might thrive in this role if you have: - At least 10+ years of experience in Data Science roles within dynamic, outcome-driven organizations. - Expertise in statistics and causal inference, applied in both experimentation and observational causal inference studies. - Proficiency \|\| You might thrive in this role if you have: - At least 10+ years of experience in Data Science roles within dynamic, outcome-driven organizations. - Expertise in statistics … |
| Data Scientist, Codex | Data Science | San Francisco | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE - 5+ years in a quantitative role at a developer-facing or high-growth product - Fluency in SQL and Python; comfort with experiment design and causal inference - Experience defining product metrics tied to user value - Ability to |
| Data Scientist, Cybersecurity | Data Science | US - Remote | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE - 5+ years of experience in data science, applied research, analytics, or a related quantitative field, with a track record of owning ambiguous, high-impact problems. - Experience in cybersecurity, trust and safety, fraud or abuse |
| Data Scientist, Financial Engineering | Data Science | San Francisco | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE - 5+ years in a quantitative role (data science, product analytics, or experimentation) in high-growth or fintech environments - Fluency in SQL and Python, with a track record designing and interpreting A/B tests and quasi-experim |
| Data Scientist, Infrastructure | Data Science | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you have: - 5+ years of experience in a quantitative role navigating ambiguous environments, ideally in infrastructure, systems, or platform domains at a high-growth company or research org - Experience defining and operationalizing metrics |
| Data Scientist, Platform and B2B Products | Data Science | San Francisco | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE - 5+ years in a quantitative role in ambiguous, high-growth environments (platforms, APIs, or B2B products a plus) - Depth in SQL and Python, with a track record proposing, designing, and running rigorous experiments - Experience |
| Data Scientist, Product | Data Science | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you have: - 5+ years experience in a quantitative role navigating highly ambiguous environments, ideally as an early data scientist or product analyst at a hyper-growth product company or research org - Proposed, designed, and run rigorous |
| Data Scientist, SMB Ads Growth | Data Science | San Francisco | heading:what we're looking for | 5+ years | What We're Looking For Required - 5+ years of experience in data science or growth analytics within an ads platform, marketplace, or high-growth B2B environment. - Proven track record of deploying machine learning models (propensity, LTV) that significantly move |
| Machine Learning Data Scientist, Forecasting | Data Science | San Francisco | heading:you might thrive in this role if you | 7+ years | nced degree (MS or PhD) in a quantitative field (e.g., Statistics, Computer Science, Economics, Operations Research). - 7+ years of experience in applied data science, with deep hands-on exposure to forecasting, predictive modeling, or marketplace systems. - Expertise in time-series forecasting techniques and practical understanding of model trad |
| CPU/Storage/PoP-WAN Program Manager | Datacenter Design | San Francisco | heading:qualifications | 8+ years | Qualifications - 8+ years of experience in technical program management, infrastructure deployment, network deployment, or data center operations - Strong experience delivering programs involving compute, storage, networking, or large-scale infr |
| Commissioning Program Manager, Infrastructure Delivery | Datacenter Design | San Francisco | heading:requirements | 5+ years | execution and incorporating them into future commissioning standards, workflows, dashboards, and KPIs. Qualifications - 5+ years of experience in program management, project management, construction management, engineering, commissioning, facilities, project controls, or infrastructure delivery. - Hands-on experience working in construction or co |
| Commissioning Project Lead, Data Center Delivery | Datacenter Design | San Francisco | heading:requirements | 10+ years | ess, closeout, and lessons learned to support a reliable transition from construction into operations. Qualifications - 10+ years of experience in commissioning, construction, engineering, technical program management, or project delivery for mission-critical facilities or similarly complex technical infrastructure. - Demonstrated experience leadi |
| Compute Infrastructure, Critical Facilities Manager | Datacenter Design | San Francisco | heading:qualifications | 8+ years | Qualifications - 8+ years of experience operating mission-critical facilities, data centers, industrial infrastructure, or large-scale technical operations environments. - Possess strong knowledge of electrical distribution systems, generators, |
| Critical Facilities Lead, Compute Infrastructure | Datacenter Design | US - Remote | heading:qualifications | 10+ years | Qualifications - Have 10+ years of experience in large-scale data center facility operations, commissioning, or critical infrastructure engineering. - Are deeply familiar with liquid-cooled IT systems, including CDU and in-rack/in-row manifold design, |
| Data Center Controls Network Engineer | Datacenter Design | San Francisco | heading:requirements | 8+ years | rotocol incompatibilities, time synchronization drift, and intermittent device communication failures. Qualifications - 8+ years of relevant experience in controls engineering, industrial automation, OT networking, mission-critical facilities, or similar critical infrastructure environments. - Strong expertise in resilient OT network architecture |
| Data Center Infrastructure Electrical Engineer | Datacenter Design | San Francisco | heading:requirements | 10+ years; 15+ years | ctrical design, safety, testing discipline, documentation quality, reliability, and operational rigors Qualifications - 10+ years of electrical engineering experience in mission-critical facilities such as data centers or comparable critical infrastructure. - Bachelor’s degree in electrical engineering, power systems, or a related discipline. - St \|\| mfortable operating in fast-moving environments with incomplete information and changing priorities. Prefe… |
| Data Center Infrastructure Engineering Program Manager (Network and Whitespace) | Datacenter Design | San Francisco | heading:requirements | 10+ years | infrastructure delivery, data center deployment, or comparable complex execution environments, typically gained through 10+ years of relevant work or equivalent depth of experience. - Proven ability to operate within ambiguous, cross-functional engineering programs with shifting requirements, urgent timelines, and high-stakes operational risk, dri |
| Datacenter Networking Technician, AI Compute Deployment - Stargate | Datacenter Design | San Francisco | heading:qualifications | 7+ years | Qualifications - Have 7+ years of experience in large-scale datacenter network deployment, structured cabling, or physical-layer installation. - Possess deep knowledge of fiber/copper plant design, cabling standards, and hyperscale network best pract |
| Electrical Commissioning Lead | Datacenter Design | San Francisco | heading:requirements | 8+ years | built evidence, test records, and outstanding issue disposition are complete and usable by operations. Qualifications - 8+ years of electrical commissioning, electrical construction, field engineering, startup, testing, or owner representative experience on complex technical infrastructure projects. - Strong knowledge of electrical distribution, |
| Hardware Operations Engineer | Datacenter Design | San Francisco | heading:qualifications | 8+ years | Qualifications - 8+ years of experience supporting large-scale datacenter hardware infrastructure, with experience in a senior technician, sustaining engineering, or hardware operations leadership role. - Deep expertise with server platforms, GP |
| Land Development & Due Diligence Lead | Datacenter Design | US - Remote | heading:qualifications | 8+ years | Qualifications - 8+ years in land development, civil/environmental engineering, or data center diligence. - Knowledge of permitting, entitlements, and AHJ engagement. - Strong project management and technical review skills. - Experience managing |
| Manufacturing Quality Engineer – Datacenter Infrastructure | Datacenter Design | San Francisco | heading:requirements | 10+ years | oject milestones. - Participate in project quality, commissioning, and operational readiness meetings. Qualifications - 10+ years in manufacturing quality management, supplier quality engineering, process improvement, or datacenter engineering/operations. - Bachelor’s degree in engineering, manufacturing, construction management, or related field |
| Mechanical Commissioning Lead | Datacenter Design | San Francisco | heading:requirements | 8+ years | ce, test records, trend data, and outstanding issue disposition are complete and usable by operations. Qualifications - 8+ years of mechanical commissioning, mechanical construction, field engineering, startup, testing, balancing coordination, controls verification, or owner representative experience on complex technical infrastructure projects. |
| Network Operations Engineer, AI Networking | Datacenter Design | San Francisco | heading:qualifications | 5+ years | helor’s degree in Computer Science, Network Engineering, or a related discipline, or equivalent practical experience. - 5+ years of experience operating large-scale data center, cloud, AI, or HPC network infrastructure. - Experience supporting production network environments with high-availability requirements. - Hands-on experience with one or m |
| PCBA Manufacturing Engineer | Datacenter Design | Singapore | heading:qualifications | 5+ years | s - Bachelor's degree in Electrical Engineering, Mechanical Engineering, Manufacturing Engineering, or related field. - 5+ years supporting high-volume PCBA manufacturing. - Experience with SMT manufacturing, PCB fabrication, and electronic assembly processes. - Strong understanding of manufacturing process control, yield improvement, and statist |
| Powered Land Developer, Development & Power Projects | Datacenter Design | US - Remote | heading:qualifications | 6+ years | Qualifications - 6+ years in energy infrastructure, energy project development, site development, data center development, or related project delivery roles. - Strong understanding of utility coordination, interconnection processes, and developm |
| Quality Engineer, Rack Infrastructure & Site Operations | Datacenter Design | Singapore | heading:requirements | 10+ years | travel as needed (estimated 30%) to manufacturing sites, datacenter locations, and partner facilities. Qualifications - 10+ years in manufacturing quality management, supplier quality engineering, process improvement, or datacenter engineering/operations. - Bachelor’s degree in engineering, manufacturing, construction management, or related field |
| Strategic Sourcing Manager, Compute Infrastructure | Datacenter Design | San Francisco | heading:qualifications | 10+ years | Qualifications - 10+ years of strategic sourcing and vendor management experience, with deep expertise in compute systems and hardware supply chains. - Demonstrated leadership sourcing for high-performance compute, accelerators, and data-center s |
| Strategic Sourcing Manager, Data Center Infrastructure, Electrical | Datacenter Design | San Francisco | heading:requirements | 8+ years | or's degree in Supply Chain, Engineering, Construction Management, Business, Operations, Finance, or a related field. - 8+ years of experience in strategic sourcing, procurement, supplier management, or infrastructure supply chain management. - Experience sourcing major infrastructure systems, industrial equipment, mission-critical facilities, or |
| Strategic Sourcing Manager, Data Center Infrastructure, Mechanical | Datacenter Design | San Francisco | heading:requirements | 8+ years | or's degree in Supply Chain, Engineering, Construction Management, Business, Operations, Finance, or a related field. - 8+ years of experience in strategic sourcing, procurement, supplier management, or infrastructure supply chain management. - Experience sourcing major infrastructure systems, industrial equipment, mission-critical facilities, or |
| Strategic Sourcing Manager, Data Center Infrastructure, Owner Furnished Equipment | Datacenter Design | San Francisco | heading:requirements | 8+ years | or's degree in Supply Chain, Engineering, Construction Management, Business, Operations, Finance, or a related field. - 8+ years of experience in strategic sourcing, procurement, supplier management, or infrastructure supply chain management. - Experience sourcing major infrastructure systems, industrial equipment, mission-critical facilities, or |
| Software Engineer, Applied Emerging Talent (2027) | Emerging Talent | San Francisco | whole_description_fallback | 0-1 years; 1 years of | ster’s degree in Computer Science, Computer Engineering, relevant technical field, or equivalent practical experience - 0-1 years of experience in software engineering or a relevant field - Proficiency with JavaScript, React, and some backend languages (we use Python) - Some experience with relational databases like Postgres/MySQL - Interest in AI \|\| er’s degree in Computer Science, Computer Engineering, relevant technical field, or equivalent practical e… |
| Senior Employee Relations Partner | Employee Relations | San Francisco | whole_description_fallback | 10+ years | e trust, engagement, and long-term cultural health. You may thrive in this role if you have: - A Bachelor’s degree with 10+ years of experience in employee relations or other People roles, ideally in high-growth, fast-paced, and highly dynamic environments. Experience in tech, research, or mission-driven orgs is a plus. - A non-conventional mindse |
| Member of Executive Operations | Executive Operations | San Francisco | heading:you might thrive in this role if you | 4 to 12 years; 12 years of | You might thrive in this role if you have - 4 to 12 years of executive support, executive operations, or similar experience. - Experience supporting one or more senior leaders in a fast-paced, high-growth environment. - Demonstrated experience managing complex calendars, sched \|\| You might thrive in this role if you have - 4 to 12 years of executive support, executive operations, or similar experience. - Experience supporting one or more senior leaders in… |
| Member of Executive Operations, Seattle | Executive Operations | Seattle | heading:you might thrive in this role if you | 4 to 7 years; 7 years of | You might thrive in this role if you have - 4 to 7 years of executive support, executive operations, or similar experience. - Experience supporting one or more senior leaders in a fast-paced, high-growth environment. - Demonstrated experience managing complex calendars, sched \|\| You might thrive in this role if you have - 4 to 7 years of executive support, executive operations, or similar experience. - Experience supporting one or more senior leaders in a… |
| Accounting Manager | Finance | San Francisco | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you have: - 6+ years of progressive accounting experience, with demonstrated ownership of close processes and experience reviewing others’ work or managing in outsourced support. - A strong general accounting foundation and practical knowle |
| Asset Compliance Program Lead, Hardware | Finance | San Francisco | whole_description_fallback | 8+ years | erating discipline, smarter workflows, and more AI-enabled ways of working. You might thrive in the role if you: - Have 8+ years of experience in hardware operations, supply chain, manufacturing, asset management, procurement operations, audit, risk and controls, or a similarly control-intensive environment; including experience owning or improvi |
| Business Systems Lead, Procure-to-Pay | Finance | San Francisco | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you: - Have 6+ years of experience in enterprise integrations, software engineering, or business systems engineering, with substantial hands-on responsibility for building and operating production solutions. - Can personally write, review, |
| Corporate Development, Deal Lead | Finance | San Francisco | heading:you might thrive in this role if you | 12+ years | You might thrive in this role if you have: - 12+ years of experience leading M&A or strategic transactions from start to finish - in corporate development, private equity, investment banking, venture investing, and/or product. - Deep experience analyzing emerging technologi |
| Deal Operations, EMEA | Finance | Dublin, Ireland | heading:requirements | 8+ years | ns to recommend improvements to commercial policies, processes, and tools. You might thrive in this role if you have: - 8+ years of experience in Deal Desk, commercial finance, pricing, sales operations, or a related function, preferably in a high-growth technology environment. - Hands-on experience reviewing and structuring complex enterprise de |
| Head of Sourcing Enablement & Delivery | Finance | San Francisco | heading:you might thrive in this role if you | 12+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 12+ years of experience in strategic sourcing, procurement, vendor management, or commercial leadership, with strong judgment about supplier choices, negotiations, contracts, and risk. - Have built or transformed a procurement ca |
| Head of Treasury Markets | Finance | San Francisco | heading:requirements | 12+ years | ury infrastructure with appropriate review, documentation, and governance. You might thrive in this role if you have: - 12+ years of relevant experience across investment management, corporate treasury, capital markets, banking, asset management, interest rate risk management, complex capital structures, credit markets, or related finance roles. - |
| Lead Revenue Accounting, Technical (Strategic Partnerships) | Finance | San Francisco | heading:requirements | 10+ years | rengthen the team’s ability to influence commercial decisions proactively. You might thrive in this role if you have: - 10+ years of technical revenue accounting or related advisory experience, with deep ASC 606 expertise and experience leading complex workstreams or teams. - Significant experience supporting large, bespoke commercial deals, strat |
| Lead, Corporate Technical Accounting and Strategic Transactions | Finance | San Francisco | heading:requirements | 10+ years | A, CA, or equivalent accounting qualification, or bring comparable demonstrated technical-accounting expertise. - Bring 10+ years of progressive experience in technical accounting, accounting advisory, public accounting, corporate controllership, or complex financial reporting, with meaningful industry or transaction experience and a record of lea |
| Lead, Revenue Accounting, Technical | Finance | San Francisco | heading:requirements | 10+ years | requirements, and billing-versus-revenue differences. You might thrive in this role if you have: - 10+ years of technical revenue accounting, revenue recognition, or related advisory experience, with deep ASC 606 expertise and experience leading complex workstreams. - Significant experience partnering with commercial Deal Desk |
| Lead, Technical Accounting (Compute Infrastructure) | Finance | San Francisco | heading:requirements | 10+ years | lusions in a way that supports audit, reporting, and operational needs. - CPA or equivalent accounting qualification. - 10+ years of progressive accounting experience. - Prior public accounting experience at the manager or senior manager level. - Strong technical accounting foundation under U.S. GAAP. - Hands-on experience preparing or reviewing t |
| M&A Finance Integration Lead | Finance | San Francisco | heading:you might thrive in this role if you | 10+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 10+ years of experience across M&A, deal integration and finance transformation, ideally in an Investment Banking/PE backed environment and/or high-growth technology company. - Demonstrated experience leading multiple, concurrent |
| Manager, Revenue Accounting, Technical (Strategic Commercial Deals) | Finance | San Francisco | heading:requirements | 5+ years | guidance that make strategic-deal execution more consistent and scalable. You might thrive in this role if you have: - 5+ years of technical revenue accounting or related advisory experience, with strong ASC 606 expertise and experience independently owning complex analyses and workstreams. - Experience working in or closely with a deal-desk fun |
| Manager, Technical & Operational Accounting | Finance | San Francisco | heading:you might thrive in this role if you | 5+ years | A, CA, or equivalent accounting qualification, or bring comparable demonstrated technical-accounting expertise. - Bring 5+ years of progressive experience in technical accounting, accounting advisory, public accounting, corporate controllership, or complex financial reporting, with meaningful industry or transaction experience. - Demonstrate broa |
| Order Management & Billing Lead — Cloud Marketplaces & Partnerships | Finance | San Francisco | heading:requirements | 6+ years | portfolio insights to broader governance and operating-model improvements. You might thrive in this role if you have: - 6+ years of progressive experience in Billing Operations, Order Management, partner billing, cloud marketplace operations, or complex usage-based billing environments. - Experience with one or more cloud marketplaces, partner-bi |
| Payroll Initiatives Lead | Finance | San Francisco | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - 8+ years of progressive experience in payroll operations, preferably in a fast-paced or high-growth environment. - Strong working knowledge of global payroll regulations and standard best practices. - Experience leading M&A payr |
| Pricing Operations Lead | Finance | San Francisco | heading:requirements | 6+ years | execution and drive improvements that reduce ambiguity, delays, and rework You might thrive in this role if you: - Have 6+ years of experience leading pricing operations or closely related monetization, commercialization, or revenue operations work - Have a strong track record of helping implement complex pricing or packaging decisions across cro |
| Senior Manager, Accounts Payable - Compute | Finance | San Francisco | heading:requirements | 8+ years | and fallback, and measure service, risk, and verified capacity outcomes. You might thrive in this role if you: - Bring 8+ years in AP, payments, or related finance operations, or equivalent experience, with personal ownership of complex, high-value supplier obligations and material exceptions from executed contract through invoice approval, paym |
| Senior Manager, Extended Workforce Program | Finance | San Francisco | heading:requirements | 7+ years | umentation, and tools that help the broader team operate more effectively. YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 7+ years of progressive experience in extended workforce, contingent workforce, procurement operations, workforce operations, or a related field. - Have substantial client-side experience building and operating an extended workf |
| Senior Manager, Financial Reporting | Finance | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you have: - 10+ years of progressive accounting experience (including 4+ in external reporting), with a strong track record owning GAAP financial statements/disclosures in dynamic and high-growth environments (Big 4 and public company experi |
| Senior Manager, Technical Revenue Accounting, Ads | Finance | San Francisco | heading:requirements | 10+ years | tation, and repeatable Finance workflows with appropriate review controls. You might thrive in this role if you have: - 10+ years of progressive experience in revenue accounting, including direct ownership of complex ASC 606 judgments and operational execution. - Demonstrated leadership to independently set direction, prioritize across competing r |
| Sr. Integrations Engineer, Supply Chain Technology | Finance | San Francisco | heading:requirements | 10+ years | requirements. You might thrive in this role if you - Bring 10+ years of experience in integration development, architecture, and design, with a track record of delivering and operating production systems. - Have hands-on proficiency with at least two integration platforms, such as Workat |
| Strategic Sourcing Lead, Professional Services – Human Data | Finance | San Francisco | heading:you might thrive in this role if you | 8+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 8+ years of progressive experience in strategic sourcing, procurement, or category management, with significant depth in Professional Services. - Have owned Professional Services category strategy and sourcing end to end—from in |
| Strategic Sourcing Leader, Professional Services | Finance | San Francisco | heading:you might thrive in this role if you | 10+ years; 5+ years | You might thrive in this role if you: - Have 10+ years of progressive strategic sourcing, procurement or category management experience, with substantial depth across multiple Professional Services categories and ownership from strategy through supplier performance. - Bring \|\| epth across multiple Professional Services categories and ownership from strategy through supplier performance. - Bring 5+ years of people leadership experience, including formal re… |
| Strategic Technology Negotiations Lead | Finance | San Francisco | heading:requirements | 10+ years | t intelligence, and stronger negotiation practices for Strategic Sourcing. YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 10+ years of experience leading complex commercial negotiations in strategic sourcing, technology procurement, strategic partnerships, deal strategy, corporate development, or a related field. - Are an expert negotiator who enjoy |
| Tax Director, Business Advisory and Strategic Finance | Finance | San Francisco | heading:you might thrive in this role if you | 12+ years | You might thrive in this role if you: - A J.D. with 12+ years of progressive tax experience, ideally with experience across a law firm, accounting firm, financial institution, or high-growth multinational business. An LL.M. in Taxation is a plus. - Broad tax expertise and a demons |
| Deployment Lead (DL), FDE - Singapore | Forward Deployed Engineering | Singapore | heading:requirements | 7+ years | and KPIs; run pre-/post-deployment measurement and report to exec sponsors. You’ll thrive in this role if you: - Bring 7+ years of customer‑facing technical delivery leadership. - Track record of successfully leading large, complex, high-stakes customer engagements where customer outcomes depended on tight coordination and fast decision making, |
| Deployment Lead (DL), FDE - Tokyo | Forward Deployed Engineering | Tokyo, Japan | heading:requirements | 7+ years | and KPIs; run pre-/post-deployment measurement and report to exec sponsors. You’ll thrive in this role if you: - Bring 7+ years of customer‑facing technical delivery leadership. - Track record of successfully leading large, complex, high-stakes customer engagements where customer outcomes depended on tight coordination and fast decision making, |
| Deployment Lead, FDE - SF | Forward Deployed Engineering | San Francisco | heading:requirements | 7+ years | report to exec sponsors. - Shape how we engage Financial Services customers You’ll thrive in this role if you: - Bring 7+ years of customer‑facing technical delivery leadership - Track record of successfully leading large, complex, high-stakes customer engagements where customer outcomes depended on tight coordination and fast decision making, i |
| Deployment Lead, FDE- NYC | Forward Deployed Engineering | New York City | heading:requirements | 7+ years | and KPIs; run pre-/post-deployment measurement and report to exec sponsors. You’ll thrive in this role if you: - Bring 7+ years of customer‑facing technical delivery leadership - Track record of successfully leading large, complex, high-stakes customer engagements where customer outcomes depended on tight coordination and fast decision making, i |
| Deployment Lead, Life Sciences- NYC | Forward Deployed Engineering | San Francisco | heading:requirements | 7+ years | t and report to exec sponsors. - Shape how we engage Life Sciences customers You’ll thrive in this role if you: - Bring 7+ years of customer‑facing technical delivery leadership and have expertise in the Life Sciences space. - Track record of successfully leading large, complex, high-stakes customer engagements where customer outcomes depended on |
| Deployment Lead, Semiconductors- SF | Forward Deployed Engineering | San Francisco | heading:requirements | 7+ years | exec sponsors. - Help define how OpenAI engages Semiconductor customers. You might thrive in this role if you: - Bring 7+ years of customer‑facing technical delivery leadership. - Have deep expertise in Semiconductor workflows, including RTL design, verification, EDA tooling, and physical implementation. - Track record of successfully leading la |
| Forward Deployed Engineer (FDE) - SF | Forward Deployed Engineering | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work - Have scoped and delivered complex systems in fast-moving or ambiguous environments - Write and review production-grade code across f |
| Forward Deployed Engineer (FDE) - Seattle | Forward Deployed Engineering | Seattle | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work - Have scoped and delivered complex systems in fast-moving or ambiguous environments - Write and review production-grade code across f |
| Forward Deployed Engineer (FDE), Financial Services- NYC | Forward Deployed Engineering | New York City | heading:requirements | 5+ years | product capabilities, and platform gaps in real-world financial use cases. YOU MIGHT THRIVE IN THIS ROLE IF YOU - Bring 5+ years of software engineering, ML engineering, or technical deployment experience with customer-facing ownership in financial services or adjacent regulated industries. - Have owned complex AI or data-driven systems end-to-en |
| Forward Deployed Engineer (FDE), Healthcare - NYC | Forward Deployed Engineering | New York City | heading:requirements | 6+ years | cal primitives for healthcare and other regulated enterprise environments. You might thrive in this role if you - Bring 6+ years of software engineering, ML/AI engineering, solutions engineering, technical consulting, or comparable experience, with the technical depth - Have operated as a senior engineer, tech lead, or deployment owner who is tru |
| Forward Deployed Engineer (FDE), Healthcare - SF | Forward Deployed Engineering | San Francisco | heading:requirements | 6+ years | al primitives for healthcare and other regulated enterprise environments. You might thrive in this role if you: - Bring 6+ years of software engineering, ML/AI engineering, solutions engineering, technical consulting, or comparable experience, with the technical depth - Have operated as a senior engineer, tech lead, or deployment owner who is tru |
| Forward Deployed Engineer (FDE), Healthcare - Seattle | Forward Deployed Engineering | Seattle | heading:requirements | 6+ years | cal primitives for healthcare and other regulated enterprise environments. You might thrive in this role if you - Bring 6+ years of software engineering, ML/AI engineering, solutions engineering, technical consulting, or comparable experience, with the technical depth - Have operated as a senior engineer, tech lead, or deployment owner who is tru |
| Forward Deployed Engineer (FDE), Legal-NYC | Forward Deployed Engineering | New York City | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU - Bring 5+ years of software engineering, ML engineering, or technical deployment experience with customer-facing ownership in financial services or adjacent regulated industries. - Have experience with legal technology, legal services, |
| Forward Deployed Engineer (FDE), Legal-SF | Forward Deployed Engineering | New York City | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU - Bring 5+ years of software engineering, ML engineering, or technical deployment experience with customer-facing ownership in financial services or adjacent regulated industries. - Have experience with legal technology, legal services, |
| Forward Deployed Engineer - London | Forward Deployed Engineering | London, UK | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work - Have scoped and delivered complex systems in fast-moving or ambiguous environments - Write and review production-grade code across f |
| Forward Deployed Engineer - London (Spanish-speaking) | Forward Deployed Engineering | London, UK | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you - Bring 6+ years of engineering or technical deployment experience that includes customer-facing work - Professional fluency in Spanish and English is required, as this role supports Spanish-speaking customers - Have scoped and delivere |
| Forward Deployed Engineer - Madrid (Spanish-speaking) | Forward Deployed Engineering | Madrid, Spain | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you - Bring 6+ years of engineering or technical deployment experience that includes customer-facing work - Professional fluency in Spanish and English is required, as this role supports Spanish-speaking customers - Have scoped and delivere |
| Forward Deployed Engineer - Munich | Forward Deployed Engineering | Munich, Germany | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work - Have scoped and delivered complex systems in fast-moving or ambiguous environments - Write and review production-grade code across f |
| Forward Deployed Engineer - Paris | Forward Deployed Engineering | Paris, France | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work - Have scoped and delivered complex systems in fast-moving or ambiguous environments - Write and review production-grade code across f |
| Forward Deployed Engineer - Seoul | Forward Deployed Engineering | Seoul, South Korea | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work. - Have scoped and delivered complex systems in fast-moving or ambiguous environments. - Write and review production-grade code across |
| Forward Deployed Engineer - Singapore | Forward Deployed Engineering | Singapore | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work. - Have scoped and delivered complex systems in fast-moving or ambiguous environments. - Write and review production-grade code across |
| Forward Deployed Engineer - Sydney | Forward Deployed Engineering | Sydney, Australia | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work. - Have scoped and delivered complex systems in fast-moving or ambiguous environments. - Write and review production-grade code across |
| Forward Deployed Engineer - Tokyo | Forward Deployed Engineering | Tokyo, Japan | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work - Have scoped and delivered complex systems in fast-moving or ambiguous environments - Write and review production-grade code across f |
| Forward Deployed Engineer - UAE | Forward Deployed Engineering | Abu Dhabi, UAE | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work - Have scoped and delivered complex systems in fast-moving or ambiguous environments - Write and review production-grade code across f |
| Forward Deployed Engineer - Zurich | Forward Deployed Engineering | Zurich, Switzerland | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience that includes customer-facing work - Have scoped and delivered complex systems in fast-moving or ambiguous environments - Write and review production-grade code across f |
| Forward Deployed Software Engineer - NYC | Forward Deployed Engineering | New York City | heading:requirements | 7+ years | ined from customer engagements to scale the Forward Deployed Engineering function. You’ll thrive in this role if you: - 7+ years of professional full stack engineering experience (excluding internships) in relevant roles at tech and product-driven companies - customer-facing experience is highly desirable - Former founder, or early engineer at a |
| Forward Deployed Software Engineer - SF | Forward Deployed Engineering | San Francisco | heading:requirements | 7+ years | ined from customer engagements to scale the Forward Deployed Engineering function. You’ll thrive in this role if you: - 7+ years of professional full stack engineering experience (excluding internships) in relevant roles at tech and product-driven companies - customer-facing experience is highly desirable - Former founder, or early engineer at a |
| Forward Deployed Software Engineer - Seattle | Forward Deployed Engineering | Seattle | heading:requirements | 7+ years | ined from customer engagements to scale the Forward Deployed Engineering function. You’ll thrive in this role if you: - 7+ years of professional full stack engineering experience (excluding internships) in relevant roles at tech and product-driven companies - customer-facing experience is highly desirable - Former founder, or early engineer at a |
| Manager, Forward Deployed Engineer - Tokyo | Forward Deployed Engineering | Tokyo, Japan | heading:you might thrive in this role if you | 8+ years; 2+ years | You might thrive in this role if you: - Bring 8+ years of engineering or technical delivery experience, including 2+ years managing high-performing FDE or customer-facing engineers - Have led high-pressure technical projects from prototype to production - Write and review p \|\| You might thrive in this role if you: - Bring 8+ years of engineering or technical delivery experience, including 2+ years managing high-performing FDE or customer-facing engineers … |
| Manager, Forward Deployed Engineering- NYC | Forward Deployed Engineering | New York City | heading:you might thrive in this role if you | 10+ years; 2+ years | You might thrive in this role if you - Bring 10+ years of engineering or technical delivery experience, including 2+ years managing high-performing FDE or customer-facing engineers. - Have led high-pressure technical projects from prototype to production. - Write and review \|\| You might thrive in this role if you - Bring 10+ years of engineering or technical delivery experience, including 2+ years managing high-performing FDE or customer-facing engineers.… |
| Full-Stack SWE, Data Acquisition (Foundations) | Foundations | San Francisco | heading:qualifications | 4+ years | QUALIFICATIONS: - BS/MS/PhD in Computer Science or a related field. - 4+ years of industry experience in full-stack development. - Proficiency in frontend frameworks (React, Vue, or similar) and backend technologies such as Python, Node.js, or Go. - Strong expertise in RESTful APIs, GraphQL, and d |
| Software Engineer, Data Acquisition | Foundations | San Francisco | heading:qualifications | 4+ years | Qualifications: - BS/MS/PhD in Computer Science or a related field. - 4+ years of industry experience in software development. - Experience with large web crawlers a plus - Strong expertise in large stateful distributed systems and data processing. - Proficiency in Kubernetes, and Infrastructure-a |
| Software Engineer, Frontier Systems - Power Management | Frontiers Clusters | San Francisco | heading:requirements | 7+ years | nation between software-driven power management and hardware capabilities. You might thrive in this role if you have: - 7+ years of software engineering experience with a focus on solving large-scale, system-level challenges. - Strong proficiency in Python and familiarity with automation and scripting tools (e.g., shell scripting). - Experience w |
| Software Engineer, Hardware Health | Frontiers Clusters | San Francisco | heading:you might thrive in this role if you | 7+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 7+ years of industry experience in software or infrastructure engineering. - Strong proficiency with Python and shell scripting. - Experience building large-scale distributed systems or infrastructure platforms. - Comfort diggin |
| HRBP, Consumer Devices | G&A | San Francisco | whole_description_fallback | five years of | y, clarity, and rigor, including when established playbooks do not exist. We’re Seeking - Deep HRBP expertise: At least five years of experience as an HR Business Partner supporting hardware, engineering, or similarly technical organizations in fast-moving environments. - Experience with multidisciplinary teams: An ability to understand and support or |
| Senior Technical Recruiter, Consumer Devices - Singapore | G&A | Singapore | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you: - Have 8+ years recruiting in highly technical domains. - Demonstrate success hiring across hardware, software, design, research, and/or operations. - Influence with clear data and market insight; communicate crisply with executives an |
| Backend Software Engineer, GTM Innovation | GTM Innovation | San Francisco | heading:you’ll thrive in this role if you | 6+ years | You’ll thrive in this role if you: - Have 6+ years of experience as a software engineer working on applied AI or user-facing systems - Former founder, or early engineer at a startup who built a product from scratch is a plus - Domain experience or demonstrated interest |
| US Congressional Lead | Global Affairs | Washington, DC | heading:you might thrive in this role if you | 8+ years | ificial intelligence but thoughtful about its potential risks. We're looking for a blend of: - Demonstrated experience (8+ years) and credibility working with the U.S. federal government, particularly the legislative branch. - Demonstrated knowledge and understanding of the U.S. government, its institutions and legislative processes, and the key |
| APAC Vendor Lead, Ads - Singapore | Growth | Singapore | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you have: - 5+ years of experience in vendor operations, commercial operations, outsourced sales, or a scaled revenue organization - Experience in Ads, advertiser growth, performance marketing, or a comparable SMB sales motion - Working kno |
| APAC Vendor Lead, Ads - Sydney | Growth | Singapore | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you have: - 5+ years of experience in vendor operations, commercial operations, outsourced sales, or a scaled revenue organization - Experience in Ads, advertiser growth, performance marketing, or a comparable SMB sales motion - Working kno |
| Growth Lead, France | Growth | Paris, France | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you have: - 10+ years of experience across product growth, data science, or growth strategy and operations, with hands-on execution in a fast-moving technology company. - A user-first track record of turning local research and behavior into |
| Growth Lead, Japan | Growth | Tokyo, Japan | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you have: - 10+ years of experience across product growth, growth marketing, data science, or growth strategy and operations, with hands-on execution in a fast-moving technology company. - A user-first track record of turning local research |
| Growth Lead, SEA | Growth | Singapore | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you have: - 10+ years of experience across product growth, growth marketing, data science, or growth strategy and operations, with hands-on execution in a fast-moving technology company. - A user-first track record of turning local research |
| North America Vendor Lead, Ads | Growth | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you have: - 5+ years of experience in vendor operations, commercial operations, outsourced sales, or a scaled revenue organization - Experience in Ads, advertiser growth, performance marketing, or a comparable SMB sales motion - Working kno |
| HR Business Partner, EMEA | HRBP | Paris, France | whole_description_fallback | 8+ years | vide a consistent and high-quality employee experience across EMEA. We’re Seeking - Strong HR foundation: Approximately 8+ years of HR experience, including meaningful experience partnering directly with managers in fast-paced, high-growth, or complex international environments as a Senior HR Generalist or HR Business Partner. - French employee r |
| ASIC Firmware Engineer, Modeling | Hardware | San Francisco | heading:requirements | 5+ years | and debug issues raised in the field. - Set up monitoring, integration testing and diagnostics tools. QUALIFICATIONS - 5+ years of experience working in embedded SW space. - Ability to thrive in ambiguity and learn new technologies. - Strong programming skills in C/C++ and/or Rust. - Experience developing high throughput, low latency and multi-t |
| ASIC Package SI/PI Engineer | Hardware | San Francisco | heading:requirements | 5+ years | for early architecture exploration, design-space optimization, and repeatable SI/PI sign-off. Required Qualifications - 5+ years of experience in signal integrity, power integrity, high-speed interconnect design, PDN design and package electrical design. - Strong understanding of signal-integrity and power-integrity fundamentals, including transm |
| Advanced Packaging Reliability Engineer | Hardware | San Francisco | heading:you might thrive in this role if you | 8+ years | cture, power delivery, package integration, materials, cooling, and system-level interactions. MINIMUM QUALIFICATIONS - 8+ years of industry experience & knowledge of semiconductor package reliability principles and failure mechanisms, including electromigration, solder-joint fatigue, interfacial delamination, dielectric cracking, via failure, wa |
| Component and Product Quality Engineer, Interconnects | Hardware | San Francisco | heading:you might thrive in this role if you | 7+ years | You might thrive in this role if you: - 7+ years of experience in quality engineering, manufacturing quality, supplier quality, or reliability for interconnects or high-speed hardware used in servers, networking, storage, or high-performance compute systems. - Hands-o |
| Design Verification Engineer | Hardware | San Francisco | heading:you might thrive in this role if you | 3+ years | You might thrive in this role if you have: - BS/MS in EE/CE/CS or equivalent with 3+ years of experience in hardware verification. - Proven success verifying complex IP or SoC designs in industry-standard flows - Proficient in SystemVerilog, UVM, and common simulation and debug tools (e.g., VCS, Questa, Verdi |
| Hardware / Software CoDesign Engineer - 3P | Hardware | San Francisco | heading:qualifications | 4+ years | Qualifications - 4+ years of industry experience, including experience harnessing compute at scale and optimizing ML platform code to run efficiently on target hardware. - Strong experience in software/hardware co-design - Deep understanding of |
| Manufacturing Test Engineer | Hardware | Singapore | heading:requirements | 5+ years | g, Computer Engineering, Manufacturing Engineering, or a related technical field, or equivalent practical experience. - 5+ years of experience in manufacturing test engineering, product test, NPI test development, or related hardware test roles. - Experience with one or more of the following on servers and/or AI Accelerators: - ICT or structural |
| Mechanical Engineer, Hardware Systems | Hardware | San Francisco | heading:requirements | 7+ years; 10+ years | T THRIVE IN THIS ROLE IF YOU: - Bachelor’s degree in Mechanical Engineering, or a related field (Master’s preferred). - 7+ years of industry experience in mechanical design, simulation, and validation for IT hardware - Proficiency in CAD tools and FEA - Strong understanding of mechanical design, material properties, manufacturing methods, and tes \|\| nted, and able to work independently or collaboratively in cross-functional engineering environments PREFER… |
| Physical Design Engineer | Hardware | San Francisco | heading:qualifications | 2+ years; 0-1 year | Qualifications: - BS w/ 4+ or MS with 2+ years or PhD with 0-1 year(s) of relevant industry experience in physical design and methodology development - Demonstrated success in taping out complex silicon designs - Hands-on experience with block physical implementatio \|\| Qualifications: - BS w/ 4+ or MS with 2+ years or PhD with 0-1 year(s) of relevant industry experience in physical design and methodology development - Demonstrated success in taping out co… |
| Rack Power Engineer | Hardware | San Francisco | heading:requirements | at least 10 years; 10 years of | th safety and compliance teams to address applicable product requirements. You might thrive in this role if you: - Have at least 10 years of industry experience in power electronics or power delivery systems, including hands-on design and qualification of high-power rack or data center power systems. - Have a master’s degree in Electrical Engineering, Pow \|\| and compliance teams to address applicable product requirements. You might thrive in this role if … |
| Signal Integrity Engineer | Hardware | San Francisco | heading:you might thrive in this role if you | at least 10 years; 10 years of | You might thrive in this role if you: - Have at least 10 years of industry experience, including experience design hardware system and SerDes testing for data center applications - Have a strong bias toward action, and won’t take no for an answer. - Have experience and good knowled \|\| You might thrive in this role if you: - Have at least 10 years of industry experience, including experience design hardware system and SerDes testing for data center applica… |
| Software Engineer, Manufacturing Infrastructure | Hardware | San Francisco | heading:you might thrive in this role if you | 7+ years | You might thrive in this role if you have: - 7+ years of hands-on experience, or exceptional accomplishments demonstrating equivalent expertise, in system software, platform software, hardware diagnostics, and cloud infrastructure. - Strong programming skills in C, C++, Ru |
| Supply Chain Operations Program Manager, AI Infrastructure | Hardware | San Francisco | heading:requirements | 8+ years | factory builds and field deployments as needed (domestic and international travel) You Might Thrive in this role if: - 8+ years of experience in Operations, Engineering, Program Management, or equivalent, within hardware development, manufacturing, or supply chain domains (compute, networking, datacenter, or similarly complex systems) - Proven t |
| Supply Chain Program Manager (SCPM) - AI Infrastructure | Hardware | San Francisco | heading:requirements | 8+ years | ions Minimum Qualifications - Bachelor’s degree in Supply Chain, Engineering, Operations, Business, or related field. - 8+ years of experience in Supply Chain Program Management, Material Program Management, Commodity Management, Strategic Sourcing, or related hardware supply chain roles. - Experience supporting complex hardware products through |
| Systems Software Engineer, Management Plane | Hardware | San Francisco | heading:requirements | 7+ years | hat help OpenAI and partner teams reproduce, operate, and improve the platform. YOU MIGHT THRIVE IN THIS ROLE IF YOU: - 7+ years of hands-on experience, or exceptional accomplishments demonstrating equivalent expertise, in low-level system software, embedded software, firmware, BMC software, platform software, device drivers, or hardware diagnost |
| Systems Software Engineer, Security, First Party Hardware | Hardware | San Francisco | heading:requirements | 7+ years | ity and operational risk, and drive durable fixes with engineering owners. YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 7+ years of hands-on experience, or exceptional accomplishments demonstrating equivalent expertise, in hardware security, embedded security, firmware security, platform security, or low-level systems security. - Experience shipp |
| Tech Lead, Deployment & Operations — Custom Infrastructure | Hardware | San Francisco | heading:you might thrive in this role if you | 8+ years | le - Have a bias toward ownership and are comfortable jumping into urgent technical issues when needed QUALIFICATIONS - 8+ years of engineering experience in hardware systems, infrastructure, data center deployment, production operations, systems engineering, silicon bring-up, or related technical domains - Strong technical depth in one or more o |
| Hardware Exploratory | Hardware Engineering | Singapore | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you: - Have 6+ years of experience in consumer hardware, consumer electronics, or advanced product development. - Bring deep technical fluency in mechanical, electrical, or systems engineering (cross-disciplinary experience a plus). - Have |
| Program Manager, Human Data | Human Data | San Francisco | heading:requirements | 1-2 years; 2 years of | ration typical of start-ups, you’ll feel right at home. - You have some relevant experience. Ideally, you have at least 1-2 years of relevant experience and are eager to grow within a role that challenges and develops your skills. \|\| tion typical of start-ups, you’ll feel right at home. - You have some relevant experience. Ideally, you have at least 1-2 years of relevant experience and are eager to grow within a role that challenges and develops your skil… |
| IT Audiovisual Operations Engineer | IT | San Francisco | heading:requirements | 5+ years | alidate results, handle failures, and measure reductions in manual effort. You might thrive in this role if you have: - 5+ years of experience implementing and troubleshooting enterprise AV systems, including installation, commissioning, and working from technical designs; hands-on experience with Logitech, Cisco, QSYS and Google Meet conferencin |
| Senior Staff Software Engineer, Identity Infrastructure Engineering | IT | San Francisco | heading:requirements | 10+ years | perational excellence, and long-term ownership of critical infrastructure. You might thrive in this role if you have: - 10+ years building and operating large-scale infrastructure, platform, or backend systems. - Deep experience with cloud infrastructure, identity systems, distributed systems, and infrastructure-as-code. - Experience leading compl |
| Software Engineer, Model Inference | Inference | San Francisco | heading:you might thrive in this role if you | at least 5 years; 5 years of | ce. - Own problems end-to-end, and are willing to pick up whatever knowledge you're missing to get the job done. - Have at least 5 years of professional software engineering experience. - Have or can quickly gain familiarity with PyTorch, NVidia GPUs and the software stacks that optimize them (e.g. NCCL, CUDA), as well as HPC technologies such as InfiniB \|\| problems end-to-end, and are willing to pick up whatever knowledge you're missing to get the job do… |
| Abuse Investigator - Scams & Fraud | Intelligence & Investigations | US - Remote | heading:you might thrive in this role if you | two years of | st five years investigating online scams, financial fraud, cybercrime or related forms of online abuse. - Have at least two years of experience conducting applied abuse research or improving investigative practices. - Write clear, well-supported reports and explain findings to technical and nontechnical audiences. - Understand how AI products can be |
| Full Stack Engineer, Intelligence Systems | Intelligence & Investigations | San Francisco | heading:you might thrive in this role if you | 4+ years | You might thrive in this role if you have / are: - 4+ years of experience as a software engineer - Experience designing, building, and operating production software, ideally for intelligence, investigations, security, research, or other complex analytical workflows. - A track re |
| Software Engineer, Accelerators | Kernels | San Francisco | heading:you might thrive in this role if you | 3+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 3+ years of experience working on AI infrastructure, including kernels, systems, or hardware-software co-design - Hands-on experience with accelerator platforms for AI at data center scale (e.g., TPUs, custom silicon, explorator |
| Associate General Counsel, Commercial – Infrastructure | Legal | San Francisco | heading:you might thrive in this role if you | 12+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 12+ years of legal experience, primarily in commercial legal roles. - Deep, hands-on experience drafting, negotiating, and advising on colocation and data center agreements. - Experience with one or more of the following: first-p |
| Counsel, Commercial | Legal | San Francisco | heading:you might thrive in this role if you | 7+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 7+ years of experience across in-house and technology-focused law firm roles. - Bring a strong background in drafting and negotiating complex commercial contracts. - Are comfortable operating in an entrepreneurial environment, a |
| Legal Contract Manager, Public Sector | Legal | Washington, DC | heading:requirements | 7+ years | se on implications for government contracts and compliance programs. We're seeking someone with experience including: - 7+ years of experience in government contracting, contract management, or technology transactions, with significant exposure to U.S. federal acquisition regulations (FAR/DFARS). - JD, law degree, or relevant contract management |
| Senior Commercial Counsel, APAC | Legal | Singapore | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 10+ years of experience across in-house and technology-focused law firm roles. - Bring a strong background in drafting and negotiating complex commercial contracts. - Are comfortable operating in an entrepreneurial environment, a |
| Senior Counsel, AI Product (Enterprise/API) | Legal | San Francisco | heading:requirements | 8+ years | B products and help shape cross-functional strategies for addressing them. You might thrive in this role if you: - Have 8+ years of experience with a mix of in-house or technology-focused law firm roles. - Have a JD and license or qualification to practice in CA. - Understand the letter of the law and can approach problems in a practical, princip |
| Senior Counsel, Commercial (Infrastructure) | Legal | San Francisco | heading:requirements | 8+ years | support OpenAI’s infrastructure development at speed while managing risk. You might thrive in this role if you: - Have 8+ years of legal experience, with substantial focus on technology transactions and commercial contracting. - Have a JD and license or qualification to practice in CA. - A mix of in-house and top-tier law firm experience. - Expe |
| Senior Counsel, Corporate (M&A) | Legal | San Francisco | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you: - Have 8+ years of combined, transactional-focused legal experience with fast-paced technology companies and law firms - Have a strong sense of ownership, are inquisitive and enthusiastic about technology, enjoy being continually chall |
| Senior Counsel, Litigation & Regulatory | Legal | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 10+ years of regulatory investigations and/or litigation experience, including substantial experience at technology companies and law firms. - Have personally set strategy and led complex matters from initial inquiry through reso |
| Senior Product Counsel | Legal | San Francisco | heading:requirements | 8+ years | o changing priorities, and take ownership of emerging issues across teams. You might thrive in this role if you: - Have 8+ years of relevant legal experience, including substantial product counseling for consumer devices, software embedded in hardware, gained in-house, at a technology-focused law firm, or both. - Can work with engineers on embedd |
| Operations Exploratory | Manufacturing & Ops | Singapore | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you: - Have 6+ years of experience in hardware operations, manufacturing, or supply chain for consumer electronics or similar industries. - Have successfully taken at least one product from concept through mass production. - Are fluent in N |
| B2B Marketing Lead, ANZ | Marketing | Sydney, Australia | heading:qualifications | 10+ years | QUALIFICATIONS - 10+ years of experience in B2B, enterprise, field, demand generation, or integrated marketing, with substantial ANZ B2B market experience - Proven experience driving measurable B2B pipeline and adoption through integrated demand |
| B2B Marketing Lead, India | Marketing | Mumbai, India | heading:you might thrive in this role if you | 10+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 10+ years of experience in B2B or integrated marketing, ideally within technology, platforms, or high-growth environments. - Proven track record of building and executing B2B marketing programs that support enterprise or partner- |
| B2B Marketing Manager, DACH | Marketing | Munich, Germany | heading:you might thrive in this role if you | 12+ years | You might thrive in this role if you: - Have 12+ years of experience in integrated B2B, regional, field, demand generation, or account-based marketing, ideally in enterprise technology, cloud, AI, or SaaS. - Have a proven track record of driving measurable pipeline and reve |
| Consumer Marketing Lead, Korea | Marketing | Seoul, South Korea | heading:qualifications | 10+ years | Qualifications: - 10+ years of marketing experience, with a strong record of building consumer brands and driving product growth in Korea. - Deep understanding of Korean culture, consumer behavior, media, creators, platforms, and marketing dynamic |
| Consumer Marketing Manager, Japan | Marketing | Tokyo, Japan | heading:qualifications | 7+ years | Qualifications: - 7+ years of marketing experience, with a strong track record of delivering high-impact consumer campaigns and measurable user or usage growth in Japan. - Deep understanding of the Japanese consumer landscape, cultural context, a |
| Developer Marketing Lead, APAC | Marketing | Singapore | heading:qualifications | 10+ years | Qualifications - 10+ years of experience in developer marketing, technical marketing, product marketing for developer products, community-led technology marketing, or integrated marketing for technical platforms. - Proven track record building cr |
| Enterprise Field Marketer | Marketing | San Francisco | heading:you might thrive in this role if you | 8+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 8+ years of experience in enterprise field marketing, ABM, regional marketing, sales enablement, or related B2B growth roles supporting complex sales motions. - Have a track record of creating measurable pipeline impact through |
| Executive Programs Lead, Americas | Marketing | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 10+ years of experience building or leading executive programs, customer engagement, enterprise marketing, experience centers, field marketing, or a comparable enterprise capability. - Have led and developed a high-performing tea |
| Global Head of Events | Marketing | San Francisco | heading:you might thrive in this role if you | 14+ years | You might thrive in this role if you - 14+ years of experience in global events, experiential marketing, and large-scale production, including leadership of teams, budgets, and programs across multiple markets. - A track record of creating distinctive flagship experie |
| Growth Marketing Manager - Web & Organic, SMB Ads | Marketing | San Francisco | heading:you might thrive in this role if you | 4–7 years; 7 years of | You Might Thrive in This Role If You - Bring 4–7 years of experience in growth marketing, web strategy, organic acquisition, conversion optimization, or product growth, with measurable acquisition, activation, or revenue impact. - Apply strong analytical judgment across fun \|\| You Might Thrive in This Role If You - Bring 4–7 years of experience in growth marketing, web strategy, organic acquisition, conversion optimization, or product growth, with measura… |
| Growth Marketing Manager, SMB Ads | Marketing | San Francisco | heading:you might thrive in this role if you | 4-7 years; 7 years of | You Might Thrive in This Role If You: - Have 4-7 years of experience in growth marketing, lifecycle marketing, GTM engineering, marketing operations, product growth, demand generation, or performance marketing. - Have shipped campaigns, experiments, automations, landing pag \|\| You Might Thrive in This Role If You: - Have 4-7 years of experience in growth marketing, lifecycle marketing, GTM engineering, marketing operations, product growth, demand generati… |
| Industry Product Marketing Manager | Marketing | San Francisco | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you have: - Have 6+ years of experience in product marketing, industry marketing, vertical marketing, enterprise GTM, or adjacent B2B technology roles - PMM experience in either Life Sciences, Banking, Healthcare, or another regulated/high-trust |
| Integrated Marketing Manager - LATAM | Marketing | São Paulo | whole_description_fallback | 12+ years | r trade-offs and build forward plans that account for creative lead times and local market conditions. What you bring - 12+ years of technology marketing experience across Brazil and Spanish-speaking LATAM, with a proven record of leading integrated B2C programs and hands-on experience marketing AI products. - Deep local market knowledge and an in |
| Integrated Marketing Manager, Hardware | Marketing | San Francisco | heading:you might thrive in this role if you | 5–8 years; 8 years of | You might thrive in this role if you: - Have 5–8 years of experience in product marketing, brand marketing, lifecycle marketing, growth marketing, audience strategy, partnerships, or related fields. - Bring deep familiarity with AI products, foundation models, generative AI \|\| You might thrive in this role if you: - Have 5–8 years of experience in product marketing, brand marketing, lifecycle marketing, growth marketing, audience strategy, partnerships, o… |
| Integrated Marketing Manager, Product & Model Launches | Marketing | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have ~10+ years of experience in B2B product marketing, integrated marketing, launches, and/or a related technology go-to-market role. We care more about the scope, quality, and complexity of your work than an exact number of years. - |
| Marketing Scientist | Marketing | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have deep expertise (10+ years) in advertising measurement, including experimentation, incrementality testing, attribution, and econometric approaches such as MMM. - Are a hands-on senior individual contributor who works directly with large datasets |
| Partner Marketing Manager, Ads | Marketing | San Francisco | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you: - Have 8+ years experience in partner marketing, platform marketing, product marketing, ecosystem marketing, or a related role in advertising or technology. - Understand the digital advertising ecosystem and how advertisers work across |
| Partner Marketing Manager, Technology Partners & ISVs | Marketing | San Francisco | whole_description_fallback | 10+ years | on, engagement, and partner health, and use insights to improve programs. You might thrive in this role, if you have: - 10+ years of experience in partner marketing, product marketing, strategic alliances, ecosystem marketing, or enterprise go-to-market roles. - Experience developing and executing joint go-to-market programs with strategic technol |
| Product Marketing Lead, API Models & Research | Marketing | San Francisco | heading:you might thrive in this role if you | 12+ years | You might thrive in this role if you: - Have 12+ years of experience in product marketing across AI, developer platforms, enterprise technology, cloud, or other complex technical products. - You love the craft of product marketing and storytelling, and bring the curiosity, |
| Product Marketing Lead, ChatGPT Work | Marketing | San Francisco | heading:requirements | 12+ years | ge, retention, team penetration, customer preference, and business impact. YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 12+ years of experience in product marketing, product strategy, or closely related go-to-market leadership roles, including ownership of a complex software, platform, or AI product. - A strong track record of defining product and |
| Product Marketing Manager, Cybersecurity | Marketing | San Francisco | heading:you might thrive in this role if you | 7+ years | You might thrive in this role if you: - Have 7+ years of experience in product marketing, industry marketing, cybersecurity marketing, enterprise GTM, or an adjacent B2B technology role. - Have marketed technical enterprise products to security, developer, IT, risk, or C-s |
| Product Marketing Manager, IT Admin and Governance | Marketing | San Francisco | heading:you might thrive in this role if you | 8+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 8+ years of experience in enterprise product marketing or a closely related go-to-market role, ideally across SaaS, cloud platforms, security, identity, infrastructure, or AI products. - Demonstrated experience marketing to IT a |
| SMB Innovation Sales & Strategy Lead | Marketing | San Francisco | heading:you might thrive in this role if you | 8-10 years; 10 years of | You Might Thrive in This Role If You - Bring approximately 8-10 years of experience in business incubation, growth, strategy, business operations, product strategy, or consulting, with substantial ownership of implementation and commercial results. - Understand SMB customers and self-serv \|\| You Might Thrive in This Role If You - Bring approximately 8-10 years of experience in business incubation, growth, strategy, business operations, product strategy, o… |
| Senior Web Experience Strategist | Marketing | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 10+ years of experience leading web strategy, digital experience, UX, or product strategy, either in-house at a technology company, relevant agency and/or consultancy. - Have shaped and improved complex websites, preferably for B |
| Senior Webinar & Digital Events Strategist | Marketing | San Francisco | heading:requirements | 10+ years | w-value formats, and create reusable programming and activation playbooks. YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 10+ years of experience across B2B webinars, digital events, experience marketing, content programming, or integrated campaigns, ideally within a complex or technical category. - A track record of building programs that create qu |
| Startup Content Marketing Manager | Marketing | San Francisco | heading:you might thrive in this role if you | 4+ years | You might thrive in this role if you: - Have 4+ years of experience in B2B, content, customer, or integrated marketing. - Have worked with startup, founder, builder, or developer audiences and understand what earns their attention and trust. - Can point to content campaign |
| Applied AI Engineer, Cyber, Government | OpenAI for Gov | Washington, DC | heading:requirements | 7+ years | ou’ll thrive in this role if you: - Hold an active TS/SCI clearance and a current, active full-scope polygraph. - Bring 7+ years of hands-on technical experience in cybersecurity, cyber operations, or security-focused software engineering, including work directly with government customers or national security mission teams. - Have practical exper |
| Applied AI Engineer, Government | OpenAI for Gov | Washington, DC | heading:you’ll thrive in this role if you | 7+ years | You’ll thrive in this role if you: - Hold an active TS/SCI clearance - Bring 7+ years of technical consulting (or equivalent) experience with public sector customers (U.S. federal preferred), bridging technical teams and senior stakeholders. - Have successfully led GenAI or traditional ML implementations |
| Capture Manager, OpenAI for Government | OpenAI for Gov | Washington, DC | heading:requirements | 10+ years | fine capture/proposal processes for greater effectiveness over time. We're seeking someone with experience including: - 10+ years selling information technology services to governments, including US intelligence community and international public sector customers. - Designing and executing complex deal and capture strategies within government cont |
| Enablement Lead, Government | OpenAI for Gov | Washington, DC | heading:you might thrive in this role if you | 6+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 6+ years of experience in customer-facing, enablement, instructional, adoption, or transformation roles, engaging executive, business, and technical audiences in government or similarly complex enterprise environments. - Underst |
| Forward Deployed Engineer, Gov | OpenAI for Gov | Washington, DC | heading:requirements | 5+ years | eep teams moving through clarity, judgment, and consistent follow-through. You might thrive in this role if you - Bring 5+ years of engineering or technical deployment experience, ideally in customer-facing or government environments. - Active TS/SCI clearance or equivalent - Have scoped and delivered complex systems in fast-moving or ambiguous c |
| Global Account Director, International Organisations, ME & LATAM | OpenAI for Gov | London, UK | heading:requirements | 10+ years | opportunities that advance responsible public-sector adoption of AI. We’re seeking someone with experience including - 10+ years in government, diplomacy, national security, international development, multilateral institutions, public-sector technology sales, business development, consulting, transformation, systems integration, or a closely rela |
| Partnerships Operations Lead, OAI for Government | OpenAI for Gov | Washington, DC | heading:requirements | 7+ years | provements that reduce cycle time, eliminate recurring friction, and enable the partner team to scale. Qualifications - 7+ years of experience in operations, Revenue Operations, Sales Operations, Deal Desk, go-to-market business operations, or complex program management. - A track record of building operating processes and cross-functional workfl |
| Program Manager, Government Trusted Access | OpenAI for Gov | Washington, DC | heading:requirements | 5–10 years; 10 years of | ing meaningful differences between programs. You might thrive in this role if you: - Hold an active TS clearance - Have 5–10 years of experience in program management, strategy and operations, product operations, trust and safety, risk operations, support operations, government technology, implementation, or a related field. - Have led complex, cro \|\| g meaningful differences between programs. You might thrive in this role if you: - Hold an active TS clea… |
| Strategic Delivery Lead, Cyber | OpenAI for Gov | Washington, DC | heading:requirements | 10+ years | Government TS/SCI clearance, with a strong preference for an active Counterintelligence or Full Scope Polygraph - Have 10+ years of experience in cybersecurity, national security consulting, delivery leadership, or senior program management roles, driving complex technical initiatives across cross-functional teams to deliver results for national |
| Strategic Delivery Lead, Department of Energy & Science | OpenAI for Gov | Washington, DC | heading:requirements | 10+ years | ivery commitments aligned with available resources and approved capabilities. YOU’LL THRIVE IN THIS ROLE IF YOU: - Have 10+ years of experience leading complex technical programs, customer delivery, or transformation initiatives, including substantial work with DOE, U.S. national labs, or comparable federal science institutions. - Can meet custome |
| Business Development Manager, Product Partnerships | Partnerships | Munich, Germany | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you have: - 10+ years of experience in product partnerships or partnership business development within the technology industry. - Fluency in English and German. - Demonstrated success leading high-impact local and international partnerships |
| Business Development Manager, Product Partnerships | Partnerships | Paris, France | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you have: - 10+ years of experience in business development or product partnerships within the technology industry. - Fluency in English and French - Demonstrated success leading high-impact local and international partnerships involving maj |
| Head of Marketplace | Partnerships | New York City | heading:qualifications | 15+ years | Qualifications - 15+ years of experience in marketplaces, platforms, ecosystems, product, partnerships, or general management. - Proven experience owning a scaled B2B marketplace or platform business with measurable commercial and customer outcom |
| Partner Director - AWS Alliance Partnership, Japan | Partnerships | Tokyo, Japan | heading:qualifications | 8+ years | ed. - Detailed knowledge of APN onboarding, ACE, AWS Marketplace, funding models, and AWS co-sell workflows required. - 8+ years of experience in partnerships, cloud alliances, ecosystem sales, business development, consulting partnerships, or related GTM roles within SaaS, cloud, AI, or platform businesses. - Significant experience building and |
| Partner Director, ANZ | Partnerships | Sydney, Australia | heading:requirements | 7+ years | commercial terms, dedicated personnel commitments, and reporting cadences. You might thrive in this role if you have: - 7+ years of experience in alliances, partner success, or sales in enterprise software or systems integration environments. - Deep experience in partner onboarding and activation, ideally with hyperscale cloud or enterprise SaaS |
| Business Recruiter, APAC | People | Singapore | whole_description_fallback | 7+ years | t intelligence and insights to stakeholders, influencing hiring decisions and shaping talent strategy. We’re seeking: - 7+ years of full-cycle recruiting experience, ideally in-house at high-growth or high-bar environments. - Proven track record of hiring for business functions (e.g. Sales, Technical Success, RevOps, Partnerships, User Ops), pref |
| Workday Engineer | People | San Francisco | heading:you might thrive in this role if you | 5-10 years; 10 years of | You might thrive in this role if you have - 5-10 years of experience in Workday engineering, integrations, platform automation, or adjacent systems engineering roles - Strong hands-on experience with Workday technologies such as EIB, Studio, Cloud Connect, Extend, reporting \|\| You might thrive in this role if you have - 5-10 years of experience in Workday engineering, integrations, platform automation, or adjacent systems engineering roles - Strong hands-… |
| Software Engineer, Full Stack (People Innovation) | People Innovation Labs | US - Remote | whole_description_fallback | 4+ years | agers, designers, and people in operations to create cutting-edge products Your background might look something like: - 4+ years of professional engineering experience (excluding internships) in relevant roles at tech and product-driven companies - Former founder, or early engineer at a startup who built a product from scratch is a plus - Interes |
| Product Manager, API Agents | Product Management | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you: - Have 5+ years of product management or related industry experience. - Proven track record of building for developers, with strong intuition for designing clear, flexible APIs and primitives that scale from early experimentation to pr |
| Product Manager, Enterprise Identity | Product Management | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 10+ years of product management experience leading large-scale enterprise products. - Have strong product judgment and can simplify complex problems. - Work effectively with technical teams and ship high-quality products. - Are a |
| Product Manager, Financial Engineering | Product Management | San Francisco | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you: - Have 6+ years of product management or related industry experience. - Obtained a bachelor's degree in Accounting, Finance, Computer Science, Engineering, Information Systems, Analytics, Mathematics, Physics, Applied Sciences, or a re |
| Product Manager, Multimodal Safety | Product Management | San Francisco | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you: - Have 6+ years of product management or related industry roles, with specific expertise in AI safety, trust & safety, integrity, or related domains. - Are deeply curious and interested in interdisciplinary fields such as human-compute |
| Product Manager, Youth | Product Management | San Francisco | heading:you might thrive in this role if you | 10+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 10+ years of product management experience leading large-scale consumer or platform products. - Have experience building for teenagers - Have strong product judgment and can simplify complex problems. - Work effectively with tech |
| Platform Product Partnerships Lead | Product Partnerships | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you - 10+ years of experience in product partnerships, product management, or developer relations. - Demonstrated success structuring and negotiating complex commercial and technical deals, with strong negotiation skills with a focus o |
| Recruiting Coordinator - Contract | Recruiting | San Francisco | heading:you might thrive in this role if you | 2+ years | You might thrive in this role if you: - Have 2+ years of experience in a fast paced recruiting coordinator position. - Are passionate about candidate experience: we see our candidates as our guests, and we are their hosts. It is the coordinator's job to ensure a smooth exp |
| Senior Technical Sourcer, Applications Engineering | Recruiting | San Francisco | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 5+ years of experience in technical sourcing, with a focus on engineering or technical roles. - A proven track record of successfully sourcing candidates across a range of software engineering and technical disciplines. - A stro |
| Technical Recruiter | Recruiting | San Francisco | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - 8+ years of progressive recruiting experience in high-growth, premier tech environments - Proven success hiring in niche and competitive technical talent markets - Strong interpersonal skills and the ability to build trust with |
| Senior Software Engineer - Research Platform, Consumer Devices | Research | San Francisco | heading:you might thrive in this role if you | 7+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 7+ years of professional software engineering experience. - Have strong full-stack experience across web applications, backend services, APIs, and data models, including ownership of complex systems spanning multiple services or |
| Research Program Manager | Research Program Management | San Francisco | heading:you might thrive in this role if you | 5+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 5+ years of experience in research program management, technical program management, or related roles in fast-moving environments. - Can engage substantively with researchers and engineers on topics such as model training, exper |
| Actuator Design Engineer | Robotics | San Francisco | heading:requirements | 7+ years | s. Preferred qualifications - Bachelor’s degree in Mechanical Engineering, Robotics, Mechatronics, or a related field - 7+ years of experience designing electromechanical systems, robotic actuators, or precision mechatronic hardware. - Experience developing actuators for robotics, automation, aerospace, automotive, or other high-performance dynam |
| Actuator Gear Design Engineer | Robotics | San Francisco | heading:requirements | 5+ years | Preferred qualifications: - Bachelor’s degree in Mechanical Engineering, Robotics, Mechatronics, or a related field. - 5+ years of experience designing gears systems, robotic actuators, or precision mechatronic hardware. - Experience developing transmission elements for robotics, automation, aerospace, automotive, or other high-performance dynam |
| Electrical Engineer, Robotics | Robotics | San Francisco | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you: - Have 6+ years of experience developing electrical systems for robotics, consumer electronics, medical devices, wearables, cameras, or other tightly integrated electromechanical products. - Have personally owned hardware from concept |
| Field Engineer | Robotics | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you: - Have 5+ years of experience supporting electromechanical, robotic, automation, or human-in-the-loop systems in production, R&D, lab, field, or operational environments. - Can independently troubleshoot messy real-world failures under |
| PCB Layout Engineer, Robotics | Robotics | San Francisco | heading:requirements | 6+ years | ntain component-library assets such as symbols, footprints, and 3D models. You might thrive in this role if you: - Have 6+ years of experience designing complex, multilayer PCBs. - Are fluent in Cadence Allegro PCB Designer and Constraint Manager. - Have strong HDI design experience, including fine-pitch BGAs, microvias, blind and buried vias, vi |
| Robotics Software Engineer | Robotics | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you: - Have 5+ years of professional software engineering experience developing and shipping production-quality systems in robotics or hardware-integrated environments. - Have extensive experience integrating and deploying industrial automa |
| Researcher, Safety Training, National Security | Safety Systems | San Francisco | heading:you might thrive in this role if you | 4+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Bring 4+ years of relevant AI safety research experience, including RLHF, adversarial training, or robustness. - Have a degree in computer science, machine learning, or a related field, and strong deep learning research or engineering |
| Software Engineer, Safety Engineering | Safety Systems | San Francisco | heading:requirements | 5+ years | dustry standard for AI safety, and prepare the world for more capable AGI. You might thrive in this role if you: - Have 5+ years of relevant engineering experience at tech and product-driven companies - Are proficient with JavaScript, React, and other web technologies - Are proficient with at least one backend language (we use Python) - Have expe |
| AWS Specialist Seller, Strategic Pursuits | Sales | San Francisco | heading:you might thrive in this role if you | 15+ years | You might thrive in this role if you: - Have 15+ years of experience in enterprise sales, strategic business development, cloud partnerships, or complex technology go-to-market roles. - Have a strong track record of shaping and closing large-scale enterprise technology deal |
| Account Director, Commercial | Sales | New York City | heading:you might thrive in this role if you | at least 3+ years; 5+ years; 3+ years | You might thrive in this role if you: - Have 5+ years of relevant software sales experience, and at least 3+ years of closing experience, including ownership of SMB, mid-market, or commercial sales cycles. - Have a demonstrated track record of meeting or exceeding revenue targets. - Bring strong discovery, qualification, pipeline-ge \|\| You might thrive in this role if you: - Have 5+ years of relevant software sales experience, and at least 3+ years of clo… |
| Account Director, Government | Sales | Australia - Remote | heading:requirements | 10+ years | opportunities that advance responsible public-sector adoption of AI. We’re seeking someone with experience including - 10+ years in government, public-sector technology sales, business development, consulting, transformation, systems integration, or a closely related field, with meaningful ownership of complex customer outcomes. - Direct governme |
| Account Director, Higher Education | Sales | San Francisco | heading:requirements | 10+ years | e forums, industry events, customer advisory discussions, and the broader higher education ecosystem. Qualifications: - 10+ years of experience selling platform-as-a-service and/or software-as-a-service solutions, with a sustained record of meeting or exceeding meaningful revenue targets through complex, multi-year enterprise sales motions. - Dire |
| Account Director, Insurance | Sales | New York City | heading:you might thrive in this role if you | 4+ years | thrive in this role if you: - 14+ total years selling complex enterprise software or platform-as-a-service solutions. - 4+ years selling to Financial Insurance organizations. - Proven success achieving annual revenue targets >$2M+ in regulated industries. - Experience managing C-suite relationships. - Strong understanding of financial services wo |
| Senior Vendor Manager - SMB Sales | Sales | Dublin, Ireland | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you: - Have 8+ years of experience in vendor management, sales operations, scaled sales execution, vendor leadership, or commercial operations. - Have direct experience managing outsourced sales or revenue-generating vendor operations. - Ha |
| Strategic Pursuits Lead | Sales | San Francisco | heading:you might thrive in this role if you | 10+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 10+ years in strategic partnerships, complex enterprise GTM, platform sales, business development, corporate strategy, or strategic deal execution in high-growth technology. - Proven ability to lead high-ambiguity, multi-threaded |
| Data Center Design Engineer, Electrical | Scaling | San Francisco | heading:requirements | 10+ years | relationships. - Oversee quality assurance and resolve risks to meet safety and operational standards. Qualifications - 10+ years of experience in data center design, operation, and maintenance. - Proven track record of leading operational and technical activities in large-scale data centers. - Extensive expertise in MEP design, operation, and mai |
| Hardware Engineer, Test | Scaling | San Francisco | heading:you might thrive in this role if you | at least 10 years; 10 years of | You might thrive in this role if you: - Have at least 10 years of industry experience, including experience testing or supporting hardware design teams for datacenter applications - Proven experience in hardware testing and validation, with hands-on experience with oscilloscopes, p \|\| You might thrive in this role if you: - Have at least 10 years of industry experience, including experience testing or supporting hardware design teams for datacenter applic… |
| Software Engineer, Data Infrastructure | Scaling | San Francisco | heading:you might thrive in this role if you | 4+ years; 4+ years | You might thrive in this role if you: - Have 4+ years in data infrastructure engineering OR - Have 4+ years in infrastructure engineering with a strong interest in data - Take pride in building and operating scalable, reliable, secure systems - Are comfortable with ambigui \|\| You might thrive in this role if you: - Have 4+ years in data infrastructure engineering OR - Have 4+ years in infrastructure engineering with a strong interest in data - Take pride … |
| Forward Deployed Security Engineer | Security | Washington, DC | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you have: - An active US security clearance. - 5+ years of security engineering experience, with an emphasis on infrastructure security, application security, network security, datacenter security, and systems engineering. - Familiarity with deployment models, including to c |
| IT Software Architect, SaaS Enablement and Governance | Security | San Francisco | whole_description_fallback | 10+ years | ional readiness - Support model design, ownership, SLAs, escalation paths, and lifecycle management What You'll Bring - 10+ years of experience in enterprise architecture, business systems architecture, IT architecture, SaaS governance, integration architecture, or a related technical leadership role. - Strong understanding of SaaS operating model |
| Security Program Manager | Security | US - Remote | heading:requirements | 5+ years | able to influence a variety of cross-functional and executive audiences, and build durable trust with partners. - Have 5+ years of experience leading complex cross-functional programs, with a proven record of successful partnership in security, IT, infrastructure, privacy, trust, product risk, or other technical domains. - Have carried programs |
| Senior Technical Program Manager - Security | Security | US - Remote | heading:requirements | 5+ years | nd leader—able to influence across technical and non-technical audiences, and build durable trust with partners. - Have 5+ years of experience leading complex technical programs focused on infrastructure security, data privacy, compliance, or enterprise platform capabilities. - Are deeply fluent in the intersection of engineering systems, securit |
| Staff Security Reliability Engineer | Security | San Francisco | heading:you might thrive in this role if you | 10+ years | You might thrive in this role if you: - Have 10+ years of hands-on experience operating and architecting mission-critical infrastructure in high-reliability environments - Have experience running Security Infrastructure - Have been the senior technical owner for the design |
| Backend Engineer, Consumer Devices | Software | San Francisco | heading:you might thrive in this role if you | 7+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 7+ years of professional software engineering experience, with a focus on backend systems. - Have a proven track record of building and scaling systems from early stage to large scale. - Are proficient with Python and Go, and fa |
| Firmware Engineer, RTOS, Consumer Devices | Software | San Francisco | heading:requirements | 10+ years | e engineering practices. You might thrive in this role if you: - Have deep experience shipping embedded systems (around 10+ years). - Are proficient in C and C++. - Are familiar with embedded toolchains, operating systems, and debugging tools. - Have experience with both rapid prototyping and scalable product development. - (Nice to have) Have exp |
| Software Engineer, HSM Infrastructure Security, Consumer Devices | Software | San Francisco | heading:requirements | 5+ years | HSM development, applied cryptography, secure key management, and certificate infrastructure. Minimum Qualifications - 5+ years experience building secure embedded firmware for constrained environments - Deep programming experience in C, C++, or Rust. You Might Thrive in This Role If You Have - A strong track record of designing, implementing, d |
| Software Engineer, Private Computing | Software | San Francisco | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you: - Care deeply about user privacy and security - Have 5+ years of experience in professional software engineering - Have experience building and scaling confidential computing or encryption technologies in production environments - Have experience with Kubernetes and cloud orchestr |
| Systems Integration Engineer, Build Systems \| Consumer Devices | Software | San Francisco | heading:qualifications | 5+ years | Qualifications: - 5+ years of engineering experience, including significant experience building infrastructure and tooling for developers - Hands-on experience with Bazel, Buck, Gradle, or similar build systems, and understand the trade offs of h |
| Director, Compute & Infrastructure FP&A | Strategic Finance | San Francisco | heading:you might thrive in this role if you | 10+ years; 2+ years | You Might Thrive in This Role If You Have - 10+ years in strategic finance, with experience in infrastructure, cloud, hardware, or compute-intensive environments - 2+ years in investment banking - Must have experience running an FP&A team at the corporate level or business \|\| 10+ years in strategic finance, with experience in infrastructure, cloud, hardware, or compute-intensive environments - 2+ years in investment banking - Must have experience running … |
| Finance Manager - Hardware Consolidations | Strategic Finance | San Francisco | heading:requirements | 8+ years | orting, and processes to support continued growth without adding friction. You might thrive in this role if you have: - 8+ years of progressive finance experience with significant exposure to hardware, manufacturing, or complex supply chain businesses - A passion for helping build world-class finance teams and driving business and financial outco |
| Hardware Finance Manager | Strategic Finance | San Francisco | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - 8+ years of prior consumer hardware or complex physical-product finance experience. - Deep, hands-on expertise across multiple relevant domains, with demonstrated ownership in at least two. - Demonstrated leadership of ambiguous |
| Head of Finance - Data Centers | Strategic Finance | San Francisco | heading:requirements | 10+ years | experience in investment banking or private equity. This is a strong preferred part of the background for this role. - 10+ years of experience across strategic finance, infrastructure finance, project development, or related fields. - Strong command of project finance, capital project economics, capex and cash flow forecasting, budget management, |
| Pricing Strategist | Strategic Finance | San Francisco | heading:you might thrive in this role if you | 6+ years; 3+ years | You might thrive in this role if you - Have 6+ years of experience in a strategy role (e.g., consulting or business operations). - Have 3+ years of hands-on consumer pricing and monetization experience, with a track record of developing and launching self-serve subscripti \|\| in this role if you - Have 6+ years of experience in a strategy role (e.g., consulting or business operations). - Have 3+ years of hands-on consumer pricing and monetization experienc… |
| Strategic Finance Lead, Corporate Finance and Capital Strategy | Strategic Finance | San Francisco | heading:you might thrive in this role if you | 12+ years | You might thrive in this role if you have: - 12+ years of experience across strategic finance, corporate finance, capital markets, investment banking, infrastructure finance, or related fields. - A strong understanding of capital structure, financing strategy, debt markets, |
| Strategic Finance, Ads | Strategic Finance | San Francisco | heading:you might thrive in this role if you | 8+ years; 2+ years | You might thrive in this role if you have: - 8+ years of experience in investment banking, consulting, or buy-side investing, coupled with operating experience at a fast-paced, scaling technology company. - 2+ years in Ads Finance, with Ads P&L ownership and experience sup \|\| ng, consulting, or buy-side investing, coupled with operating experience at a fast-paced, scaling technology company. - 2+ years in Ads Finance, with Ads P&L ownership and experience… |
| Strategic Finance, B2B Partnerships | Strategic Finance | San Francisco | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - 8+ years of experience in investment banking, consulting, or buy-side investing and operational experience at a fast-paced, scaling company. - A strong ability to critically evaluate opportunities and risks in financials. - Expe |
| Strategic Finance, B2B Product | Strategic Finance | San Francisco | heading:requirements | 7+ years | s and data that leaders use to manage B2B growth and financial performance YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 7+ years of experience in strategic finance, product or commercial finance, investment banking, private equity or venture capital, or another analytically rigorous role - Direct ownership of strategic finance, product finance, c |
| Strategic Finance, Compute | Strategic Finance | San Francisco | heading:you might thrive in this role if you | 7+ years | You might thrive in this role if you have: - 7+ years in a finance and strategy operating role at a high-growth technology company - Background in infrastructure, data centers, compute, cloud, semiconductors, or a related industry strongly preferred - Strong financial mode |
| Strategic Finance, International & Marketing | Strategic Finance | San Francisco | heading:you might thrive in this role if you | 10+ years; 2+ years | You might thrive in this role if you have: - 10+ years of progressive experience across Strategic Finance, investment banking, consulting, private equity, or related operating roles. - 2+ years of Strategic Finance experience at a high-growth technology company, including m \|\| sive experience across Strategic Finance, investment banking, consulting, private equity, or related operating roles. - 2+ years of Strategic Finance experience at a high-growth tec… |
| Strategic Finance, Partnerships | Strategic Finance | San Francisco | heading:you might thrive in this role if you | 8+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - 8+ years of experience in investment banking, consulting, or buy-side investing coupled with operational experience at a fast-paced, scaling company. - A strong ability to critically evaluate opportunities and risks in financial |
| Deal Operations, APAC | Strategy & Operations | Singapore | heading:requirements | 8+ years | rns to recommend improvements to commercial policies, processes, and tools. YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE - 8+ years of experience in Deal Desk, commercial finance, pricing, sales operations, or a related function, preferably in a high-growth technology environment. - Hands-on experience reviewing and structuring complex enterprise de |
| GTM Strategy & Operations, Professional Services | Strategy & Operations | San Francisco | whole_description_fallback | 8+ years | repeatable product-plus-services offerings that accelerate durable product adoption. We’re looking for someone with: - 8+ years of experience in GTM Strategy & Operations, Business Operations, Strategic Finance, management consulting, or a comparable role, including direct experience in a technology Professional Services, implementation, systems |
| Program Manager, Business Marketing | Strategy & Operations | San Francisco | whole_description_fallback | 7+ years | solutions that people adopt and that remain useful as the business grows. You might thrive in this role, if you have: - 7+ years of experience in strategy and operations, business operations, program or project management, or related work across multiple teams and concurrent priorities. - A track record of personally organizing and leading cross- |
| Engineering Manager, Cooperative Systems | Support Automation | San Francisco | heading:you might thrive in this role if you | at least 7 years; 12+ years; 3+ years | E IF YOU - Have 12+ years of experience in engineering, including 3+ years of experience in engineering management, and at least 7 years as an IC engineer - Are a hands-on builder who enjoys operating across the stack - Have deep experience applying AI, and are ready to experiment with frontier approaches - Bring strong technical judgment across systems \|\| YOU MIGHT THRIVE IN THIS ROLE IF YOU - Have 12+ years of experience in engineering, including 3+ yea… |
| Engineering Manager, Cooperative Systems | Support Automation | Seattle | heading:you might thrive in this role if you | at least 7 years; 12+ years; 3+ years | E IF YOU - Have 12+ years of experience in engineering, including 3+ years of experience in engineering management, and at least 7 years as an IC engineer - Are a hands-on builder who enjoys operating across the stack - Have deep experience applying AI, and are ready to experiment with frontier approaches - Bring strong technical judgment across systems \|\| YOU MIGHT THRIVE IN THIS ROLE IF YOU - Have 12+ years of experience in engineering, including 3+ yea… |
| AI Support Engineer - Dublin | Support Delivery | Dublin, Ireland | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - Dublin (Weekend Shift) | Support Delivery | Dublin, Ireland | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - San Francisco | Support Delivery | San Francisco | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - San Francisco (Weekend Shift) | Support Delivery | San Francisco | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - Singapore | Support Delivery | Singapore | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - Singapore (Korean Speaking) | Support Delivery | Singapore | heading:you might thrive in this role if you | 8+ years | is role if you have: - Speak fluent business-level Korean, as you will be working with Korean-speaking customers - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - Singapore (Weekend Shift) | Support Delivery | Singapore | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - Tokyo | Support Delivery | Tokyo, Japan | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - Tokyo (Korean Speaking) | Support Delivery | Tokyo, Japan | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - Speak fluent business-level Korean. - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - Tokyo (Weekend Shift) | Support Delivery | Tokyo, Japan | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - Toronto | Support Delivery | Ontario - Remote | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you: - Have 5+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer - Toronto (Weekend Shift) | Support Delivery | Ontario - Remote | heading:you might thrive in this role if you | 8+ years | You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer, Biosciences - San Francisco | Support Delivery | San Francisco | heading:requirements | 8+ years; 8+ years | supportive, rigorous, and customer-focused culture within User Operations. You might thrive in this role if you: - Have 8+ years of experience in technical support, support engineering, escalations, technical account management, solutions operations, product operations, incident management, or a related customer-facing technical role. - Bring mea \|\| ns involving scientific tools and workflows while recognizing when specialized scientific expertise is requ… |
| AI Support Engineer, Government - San Francisco, CA | Support Delivery | San Francisco | heading:requirements | 8+ years | on call coverage, as needed, to support business and customer needs. You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| AI Support Engineer, Government - Washington, D.C. | Support Delivery | Washington, DC | heading:requirements | 8+ years | on call coverage, as needed, to support business and customer needs. You might thrive in this role if you have: - Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. - Are comfortable using emerging technologies (ie |
| Dedicated Support Engineering Lead | Support Delivery | San Francisco | heading:you might thrive in this role if you | 12+ years; 6+ years | You might thrive in this role if you... - Have 12+ years of experience in technical customer-facing roles, including 6+ years of leadership responsibility for enterprise Support Engineering, Technical Account Management, or a comparable function supporting complex production \|\| You might thrive in this role if you... - Have 12+ years of experience in technical customer-facing roles, including 6+ years of leadership responsibility for enterprise Support En… |
| Senior Support Engineer - Dublin | Support Delivery | Dublin, Ireland | heading:you might thrive in this role if you | 5+ years | puter Science or a related field. A strong software engineering foundation is important for this role’s success. - Have 5+ years of experience in technical operations roles such as SRE/NOC, designing monitoring systems and resolving production issues in fast-paced and mission-critical environments. A strong track record of troubleshooting complex |
| Senior Support Engineer - San Francisco | Support Delivery | San Francisco | heading:you might thrive in this role if you | 8+ years | puter Science or a related field. A strong software engineering foundation is important for this role’s success. - Have 8+ years of experience in technical operations roles such as SRE/NOC, designing monitoring systems and resolving production issues in fast-paced and mission-critical environments. A strong track record of troubleshooting complex |
| Senior Support Engineer - Singapore | Support Delivery | Singapore | heading:you might thrive in this role if you | 8+ years | puter Science or a related field. A strong software engineering foundation is important for this role’s success. - Have 8+ years of experience in technical operations roles such as SRE/NOC, designing monitoring systems and resolving production issues in fast-paced and mission-critical environments. A strong track record of troubleshooting complex |
| Senior Support Engineer - Toronto | Support Delivery | Ontario - Remote | heading:you might thrive in this role if you | 8+ years | puter Science or a related field. A strong software engineering foundation is important for this role’s success. - Have 8+ years of experience in technical operations roles such as SRE/NOC, designing monitoring systems and resolving production issues in fast-paced and mission-critical environments. A strong track record of troubleshooting complex |
| Support Delivery Lead | Support Delivery | San Francisco | heading:qualifications | 10+ years; 5+ years | Qualifications: - Have 10+ years of experience in technical support engineering or software engineering - Have 5+ years of experience leading technical support engineering or software engineering teams, ideally in high-scale or fast-paced environments \|\| Qualifications: - Have 10+ years of experience in technical support engineering or software engineering - Have 5+ years of experience leading technical support engineering or software engineering teams, i… |
| Support Delivery Lead | Support Delivery | San Francisco | heading:qualifications | 8+ years; 4+ years | Qualifications: - Have 8+ years of experience in technical support engineering or software engineering - Have 4+ years of experience leading technical support engineering or software engineering teams, ideally in high-scale or fast-paced environments \|\| Qualifications: - Have 8+ years of experience in technical support engineering or software engineering - Have 4+ years of experience leading technical support engineering or software engineering teams, ide… |
| Support Delivery Lead - Toronto | Support Delivery | Ontario - Remote | heading:qualifications | 5+ years; 10+ years | Qualifications: - Have 5+ years of experience leading and managing technical support engineering or software engineering teams, ideally in high-scale or fast-paced environments. - Have 10+ years of experience in technical support engineering or softwa \|\| g technical support engineering or software engineering teams, ideally in high-scale or fast-paced environments. - Have 10+ years of experience in technical support engineering or software engineering - H… |
| Support Delivery Lead, Ads | Support Delivery | San Francisco | heading:you might thrive in this role if you | 12+ years; 6+ years | You might thrive in this role if you: - Have 12+ years of experience in Support Delivery, Customer Operations, Ads Operations, or similar environments, including 6+ years of direct people management. - Have experience supporting advertising products and workflows, with demo \|\| ve 12+ years of experience in Support Delivery, Customer Operations, Ads Operations, or similar environments, including 6+ years of direct people management. - Have experience suppo… |
| Support Delivery Lead, EMEA - Dublin | Support Delivery | Dublin, Ireland | heading:qualifications | 4+ years; 8+ years | Qualifications: - Have 4+ years of experience leading technical support engineering or software engineering teams, ideally in high-scale or fast-paced environments. - Have 8+ years of experience in technical support engineering or software engineering \|\| g technical support engineering or software engineering teams, ideally in high-scale or fast-paced environments. - Have 8+ years of experience in technical support engineering or software engineering. - H… |
| Support Delivery Lead, Government | Support Delivery | Washington, DC | heading:requirements | 12+ years; 6+ years | needs, while contributing to the broader Support Delivery leadership team. You might thrive in this role if you have: - 12+ years of experience in technical support engineering, software engineering, customer engineering, site reliability, infrastructure, or a related technical field. - 6+ years of experience leading technical support engineering, \|\| ineering, software engineering, customer engineering, site reliability, infrastructure, or a related techn… |
| Support Program Manager, Support Delivery | Support Delivery | San Francisco | heading:requirements | 8+ years | ontributing to its long-term success and influence across the organization You might thrive in this role if you: - Have 8+ years of experience in program management, operations, or support engineering, with a focus on building scalable processes and tooling - Have shipped or maintained tools and automations (dashboards, ETL pipelines, low-code ap |
| Technical Program Manager, Support Delivery | Support Delivery | San Francisco | heading:requirements | 8+ years | ontributing to its long-term success and influence across the organization You might thrive in this role if you: - Have 8+ years of experience in program management, operations, or support engineering, with a focus on building scalable processes and tooling - Have shipped or maintained tools and automations (dashboards, ETL pipelines, low-code ap |
| Product Engagement Specialist, User Operations | Support Operations | San Francisco | heading:you might thrive in this role if you | 8+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 8+ years of experience in product launch coordination, especially within a customer support environment (internal and/or external). - Bring product management, technical program management, or similarly hands-on experience takin |
| Strategy & Operations Programs, Support | Support Operations | San Francisco | heading:you might thrive in this role if you | at least 5 years; 8+ years; 5 years of | You might thrive in this role if you: - Have 8+ years of experience in operations, strategy, and consulting, with at least 5 years of experience building and leading customer-facing operations. You have a history of high impact work in a technical environment. - Are non-traditional – this role will require leveraging technology and concepts that ar \|\| You might thrive in this role if you: - Have 8+ years of experience in operations, strategy, and consulti… |
| Support Operations Lead | Support Operations | San Francisco | heading:you might thrive in this role if you | 10+ years; 4+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 10+ years of experience in support operations including 4+ years leading senior individual contributors with a strong track record of coaching, driving accountability, and improving performance and automation adoption at scale. - \|\| YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 10+ years of experience in support operations including 4+ years leading senior individual contributors with a strong track record of co… |
| Support Program Manager, Partnerships | Support Operations | San Francisco | heading:requirements | 8+ years | mprove partner-related support workflows and scale operations effectively. You might thrive in this role if you: - Have 8+ years of experience in program management, support operations, partnerships, or related roles within a fast-paced technology environment. - Have experience working closely with engineering teams to translate technical require |
| Support Vendor Manager | Support Operations | San Francisco | whole_description_fallback | 5+ years | aling constraints; translate operational signals into recommendations for leadership. WE’RE LOOKING FOR SOMEONE WITH: - 5+ years in vendor/BPO operations management, support operations, or partner performance leadership in a scaled environment. - Proven ability to run vendor governance: QBRs, SLA/KPI design, escalation paths, remediation plans, a |
| Technical Systems Program Manager, User Operations | Support Operations | San Francisco | heading:you might thrive in this role if you | 8+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: - You have 8+ years of experience driving high-impact technical programs in a program management, technical program management or adjacent role - Strong understanding of CRM workflows customer systems supporting user operations or support |
| Technical Program Manager, Applied API & Product | Technical Program Management | San Francisco | heading:you might thrive in this role if you | 15+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 10–15+ years of experience driving high-impact technical programs in product and platform domains. - Have strong technical acumen across front-end/client technologies, API development, and scalable systems architecture. - Have succe |
| Technical Program Manager, Applied Infrastructure | Technical Program Management | San Francisco | heading:you might thrive in this role if you | 7+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 7+ years of experience leading large-scale, technical infrastructure programs, especially in compute resource planning, system scalability, or platform engineering. - Understand how cloud infrastructure, distributed systems, and |
| Technical Program Manager, Compute Infrastructure | Technical Program Management | San Francisco | heading:you might thrive in this role if you | 5+ years | ROLE IF YOU: - Possess a degree in a hard science, or have a demonstrated track record of engineering expertise. - Have 5+ years of experience in program management for major projects including capital projects or hyperscaler infrastructure deployment. - Demonstrate the ability to serve as the go-to person solely responsible for driving and deliv |
| Technical Program Manager, People Innovation Labs | Technical Program Management | San Francisco | heading:you might thrive in this role if you | 7+ years | You might thrive in this role if you: - Have 7+ years of experience in technical program management, product operations, or a similar role leading complex software initiatives. - Have independently led multiple high-impact programs involving several technical and business |
| Applied AI Delivery Lead | Technical Success | San Francisco | heading:what we’re looking for | 7+ years | WHAT WE’RE LOOKING FOR - 7+ years of experience leading complex enterprise technology deployments, customer delivery programs, or transformation initiatives involving multiple teams and partners. - A track record of driving programs from scope through l |
| Applied AI Engineer, API Platform, Digital Natives | Technical Success | New York City | heading:you’ll thrive in this role if you | 8+ years | You’ll thrive in this role if you: - Bring 8+ years of deep, hands-on technical experience and an eagerness to work closely with customers. Our team consists of former startup founders, software and ML engineers, technical product managers and solution architects. - Have |
| Applied AI Engineer, API Platform, Digital Natives | Technical Success | San Francisco | heading:you’ll thrive in this role if you | 8+ years | You’ll thrive in this role if you: - Bring 8+ years of deep, hands-on technical experience and an eagerness to work closely with customers. Our team consists of former startup founders, software and ML engineers, technical product managers and solution architects. - Have |
| Applied AI Engineer, Agent Enablement | Technical Success | San Francisco | heading:requirements | 4–6 years; 6 years of | orm requirements, reference architectures, playbooks, and developer guidance. You’ll thrive in this role if you: - Have 4–6 years of professional software engineering or AI engineering experience and are strong enough technically to contribute to the platform itself while still enjoying hands-on coding. - Have operated in a customer or partner fac \|\| m requirements, reference architectures, playbooks, and developer guidance. You’ll thrive in this role if … |
| Applied AI Engineer, Codex | Technical Success | São Paulo | heading:you might thrive in this role if you | 5+ years | You might thrive in this role if you: - Have 5+ years of technical consulting, post-sales engineering, solutions architecture, or similar experience working directly with customers. - Are an active power user of AI coding tools and have deeply customized your own developer |
| Applied AI Engineer, Codex | Technical Success | San Francisco | heading:you’ll thrive in this role if you | 5+ years | You’ll thrive in this role if you: - Have 5+ years of technical consulting, post-sales engineering, solutions architecture, or similar experience working directly with customers. - Are an active power user of AI coding tools and have deeply customized your own developer |
| Applied AI Engineer, Codex | Technical Success | Sydney, Australia | heading:you’ll thrive in this role if you | 5+ years | You’ll thrive in this role if you: - Have 5+ years of relevant experience in software development, deployment engineering, data or infrastructure engineering, technical consulting, or solutions architecture. - Can build, debug, and evaluate production-relevant software |
| Applied AI Engineer, Cyber | Technical Success | Singapore | heading:requirements | 5+ years | stomer requirements, blockers, product gaps, and emerging cyber workflows. You might thrive in this role if you: - Have 5+ years of technical consulting, solutions engineering, security architecture, cyber advisory, deployment engineering, professional services, or equivalent customer-facing technical experience. - Bring strong cybersecurity doma |
| Applied AI Engineer, Cyber | Technical Success | San Francisco | heading:requirements | 5+ years | customer requirements, blockers, product gaps, and emerging cyber workflows. You'll thrive in this role if you: - Have 5+ years of technical consulting, solutions engineering, security architecture, cyber advisory, deployment engineering, professional services, or equivalent customer-facing technical experience. - Bring strong cybersecurity doma |
| Applied AI Engineer, Cyber \| Tokyo | Technical Success | Tokyo, Japan | heading:requirements | 5+ years | stomer requirements, blockers, product gaps, and emerging cyber workflows. You might thrive in this role if you: - Have 5+ years of technical consulting, solutions engineering, security architecture, cyber advisory, deployment engineering, professional services, or equivalent customer-facing technical experience. - Bring strong cybersecurity doma |
| Applied AI Engineer, Plugins | Technical Success | San Francisco | heading:requirements | 4-6 years; 6 years of | requirements, and implementation guidance. You might thrive in this role if you: - Have 4-6 years of professional software engineering experience and are strong enough technically to contribute to the platform itself while still enjoying hands-on coding. - Have built and operated production APIs, backend services, d \|\| requirements, and implementation guidance. You might thrive in this role if you: - Have 4-6 years of professional software engineering exp… |
| Applied AI Engineer, Startups | Technical Success | San Francisco | heading:you’ll thrive in this role if you | 5+ years | You’ll thrive in this role if you: - Have 5+ years of experience as a software engineer, ML engineer or equivalent, ideally in a startup environment; experience as a founder or founding engineer is highly valued. - Have passion for startups and a belief in their potenti |
| Applied AI Engineer, Startups | Technical Success | Tokyo, Japan | heading:you’ll thrive in this role if you | 5+ years | YOU’LL THRIVE IN THIS ROLE IF YOU: - Have 5+ years of experience as a software engineer, ML engineer or equivalent, ideally in a startup environment; experience as a founder or founding engineer is highly valued. - Have passion for startups and a belief in their potenti |
| Early Access Deployment Engineer | Technical Success | San Francisco | heading:you might thrive in this role if you | 4+ years | You might thrive in this role if you: - Have 4+ years of software engineering or equivalent technical experience, including meaningful customer-facing delivery and ownership of production systems. - Have a track record of rapidly turning ambiguous ideas into working protot |
| Enablement Lead (Builder) - Tokyo | Technical Success | Tokyo, Japan | heading:you’ll thrive in this role if you | 4+ years | YOU’LL THRIVE IN THIS ROLE IF YOU: - Have 4+ years of experience in customer-facing or instructional roles, engaging C-level and senior technical audiences in complex enterprise environments. - Possess exceptional presentation and communication skills, particularly when |
| Manager, Applied AI Architect | Technical Success | San Francisco | heading:you’ll thrive in this role if you | 8+ years; 3+ years | You’ll thrive in this role if you: - Bring 8+ years of experience in technical customer-facing roles, building and managing C-level technical and business relationships within complex, global organizations. - Have 3+ years of experience leading technical pre-sales teams, \|\| roles, building and managing C-level technical and business relationships within complex, global organizations. - Have 3+ years of experience leading technical pre-sales teams, with a … |
| Manager, Applied AI Architect (India) | Technical Success | Bangalore - Remote | heading:you might thrive in this role if you | 10+ years; 4+ years | cloud architecture, APIs, data integration, identity, security, privacy, evaluation, and enterprise deployment. - Bring 10+ years of experience in customer-facing technical roles such as solutions architecture, solutions engineering, technical account leadership, AI deployment, or technical consulting, including work with large and complex enterpr \|\| l account leadership, AI deployment, or technical consulting, including work with large and complex enterp… |
| Manager, Applied AI Architects | Technical Success | Paris, France | heading:you might thrive in this role if you | 10+ years; 4+ years | cloud architecture, APIs, data integration, identity, security, privacy, evaluation, and enterprise deployment. - Bring 10+ years of experience in customer-facing technical roles such as solutions architecture, solutions engineering, technical account leadership, AI deployment, or technical consulting, including work with large and complex enterpr \|\| l account leadership, AI deployment, or technical consulting, including work with large and complex enterp… |
| Manager, Applied AI Architects | Technical Success | Tokyo, Japan | heading:you might thrive in this role if you | 10+ years; 4+ years | cloud architecture, APIs, data integration, identity, security, privacy, evaluation, and enterprise deployment. - Bring 10+ years of experience in customer-facing technical roles such as solutions architecture, solutions engineering, technical account leadership, AI deployment, or technical consulting, including work with large and complex enterpr \|\| l account leadership, AI deployment, or technical consulting, including work with large and complex enterp… |
| Manager, Applied AI Architects | Technical Success | London, UK | heading:you might thrive in this role if you | 10+ years; 4+ years | cloud architecture, APIs, data integration, identity, security, privacy, evaluation, and enterprise deployment. - Bring 10+ years of experience in customer-facing technical roles such as solutions architecture, solutions engineering, technical account leadership, AI deployment, or technical consulting, including work with large and complex enterpr \|\| l account leadership, AI deployment, or technical consulting, including work with large and complex enterp… |
| Manager, Applied AI Architects - Digital Natives | Technical Success | Munich, Germany | heading:you might thrive in this role if you | 10+ years; 4+ years | cloud architecture, APIs, data integration, identity, security, privacy, evaluation, and enterprise deployment. - Bring 10+ years of experience in customer-facing technical roles such as solutions architecture, solutions engineering, technical account leadership, AI deployment, or technical consulting, including work with large and complex enterpr \|\| l account leadership, AI deployment, or technical consulting, including work with large and complex enterp… |
| Manager, Applied AI Engineering (Codex) | Technical Success | San Francisco | heading:you’ll thrive in this role if you | 8+ years; 2+ years | YOU’LL THRIVE IN THIS ROLE IF YOU - Have 8+ years of experience in deeply technical, customer-facing roles such as applied engineering, solutions architecture, deployment engineering, technical consulting, or similar roles. - Have 2+ years of experience leading technic \|\| as applied engineering, solutions architecture, deployment engineering, technical consulting, or similar roles. - Have 2+ years of experience leading technical teams, including hiring, m… |
| Manager, Applied AI Engineering (Codex) | Technical Success | Munich, Germany | heading:you’ll thrive in this role if you | 8+ years; 2+ years | YOU’LL THRIVE IN THIS ROLE IF YOU - Have 8+ years of experience in deeply technical, customer-facing roles such as applied engineering, solutions architecture, deployment engineering, technical consulting, or similar roles. - Have 2+ years of experience leading technic \|\| as applied engineering, solutions architecture, deployment engineering, technical consulting, or similar roles. - Have 2+ years of experience leading technical teams, including hiring, m… |
| Manager, Applied AI Engineering (Digital Natives) | Technical Success | San Francisco | heading:you’ll thrive in this role if you | 8+ years; 2+ years | YOU’LL THRIVE IN THIS ROLE IF YOU - Have 8+ years of experience in deeply technical, customer-facing roles such as applied engineering, solutions architecture, deployment engineering, technical consulting, or similar roles. - Have 2+ years of experience leading technic \|\| as applied engineering, solutions architecture, deployment engineering, technical consulting, or similar roles. - Have 2+ years of experience leading technical teams, with a demonstrated… |
| Partner AI Deployment Engineer - AWS | Technical Success | Bangalore - Remote | heading:you’ll thrive in this role if you | 8+ years | You’ll thrive in this role if you: - Have 8+ years of technical consulting (or equivalent) experience, managing C-level technical and business relationships with complex global organizations. - Operate as a technical leader and systems thinker, not just an individual co |
| Partner Applied AI Engineer | Technical Success | San Francisco | heading:you’ll thrive in this role if you | 8+ years | You’ll thrive in this role if you: - Have 8+ years of technical consulting (or equivalent) experience, managing C-level technical and business relationships with complex global organizations. - Have led complex technical projects and programs with many stakeholders, ide |
| Technical Program Manager, Global Programs — Applied AI Engineering | Technical Success | San Francisco | heading:you might thrive in this role if you | at least 10+ years; 10+ years | YOU MIGHT THRIVE IN THIS ROLE IF YOU - Bring at least 10+ years of technology-industry experience, with a track record in technical program management, technical strategy, technical GTM, industry programs, or technology consulting. Experience at hyperscalers, independent software ve \|\| YOU MIGHT THRIVE IN THIS ROLE IF YOU - Bring at least 10+ years of technology-industry experience, with a track record in technical program management, technical strategy, … |
| Compensation Business Partner, GTM | Total Rewards | San Francisco | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you have: - 6+ years of |
| Consumer Device Safety & Risk Operations Specialist, User Safety & Risk Operations | Trust & Safety | San Francisco | heading:requirements | 8+ years | ion, and transition them into durable homes across USRO and partner teams. You Might Thrive in This Role If You: - Have 8+ years of relevant experience in device safety, product safety, consumer hardware operations, technical program management, or a related field. - Have built a complex safety or risk program from an ambiguous starting point thr |
| Cyber Operations Lead, Critical Harm Operations | Trust & Safety | San Francisco | heading:requirements | 8+ years; 4+ years | epresent Cyber Operations in high-stakes discussions and launch decisions. You might thrive in this role if you: - Have 8+ years of experience in cybersecurity, cyber intelligence, threat intelligence, incident response, security research, or a related field, including 4+ years of leading teams. - Built and scaled a cyber operations, cyber intell \|\| rsecurity, cyber intelligence, threat intelligence, incident response, security research, or a related fiel… |
| Cyber Operations Strategist, Critical Harm Operations | Trust & Safety | Ontario - Remote | heading:requirements | 8+ years | Investigations to operationalize changes and drive launch readiness. You might thrive in this role if you have: - Have 8+ years of hands-on cybersecurity experience in offensive security, threat intelligence, incident response, security research, red teaming, application security, DFIR, malware analysis, or a related field. - Can reason deeply a |
| Device Safety & Risk Operations Specialist, User Safety & Risk Operations | Trust & Safety | San Francisco | heading:requirements | 8+ years | ion, and transition them into durable homes across USRO and partner teams. You Might Thrive in This Role If You: - Have 8+ years of relevant experience in device safety, product safety, consumer hardware operations, technical program management, or a related field. - Have built a complex safety or risk program from an ambiguous starting point thr |
| Regulatory Operations Analyst, User Safety & Risk Operations | Trust & Safety | San Francisco | heading:requirements | 8+ years | case quality audits, SLA tracking, escalation accuracy, and data analysis You Might Thrive in This Role If You: - Have 8+ years of experience in regulatory compliance, legal operations, and trust & safety, preferably in a global or high-growth tech environment - Have translated content moderation or online safety requirements into operational wo |
| Safety Response Operations Lead | Trust & Safety | San Francisco | heading:you might thrive in this role if you | 8+ years; 4+ years | You Might Thrive in This Role If You: - You have 8+ years of experience in Trust & Safety, Risk Operations, Investigations, Fraud, Annotation, or platform integrity. - You have 4+ years of direct people leadership or senior-level operational ownership, including coaching exper \|\| of experience in Trust & Safety, Risk Operations, Investigations, Fraud, Annotation, or platform integrity. - You have 4+ years of direct people leadership or senior-level operat… |
| Safety Response Operations Lead | Trust & Safety | Singapore | heading:you might thrive in this role if you | 5+ years; 4+ years | You Might Thrive in This Role If You: - You have 5+ years in Trust & Safety, Risk Operations, Investigations, Fraud, Annotation, or platform integrity. - You have 4+ years of people leadership or senior-level operational ownership. - You are a strong decision-maker in ambiguou \|\| have 5+ years in Trust & Safety, Risk Operations, Investigations, Fraud, Annotation, or platform integrity. - You have 4+ years of people leadership or senior-level operational o… |
| Senior Operations Analyst, User Safety & Risk Operations | Trust & Safety | San Francisco | heading:requirements | 8+ years | udgment and independence through coaching, calibration, and reusable tools. You Might Thrive in This Role If You - Have 8+ years of experience in trust and safety operations, investigations, incident response, product operations, technical program management, or another high-judgment, data-heavy operational field. - Have a track record as a scrap |
| Senior Program Manager, Consumer Device Safety Operations | Trust & Safety | San Francisco | heading:requirements | 8+ years | ition mature capabilities into durable homes across USRO and partner teams. YOU MIGHT THRIVE IN THIS ROLE IF YOU - Have 8+ years of experience in program management, technical program management, product operations, product safety, quality assurance, regulatory operations, incident management, healthcare operations, or another complex, high-accou |
| Senior Support Specialist, Ads | Trust & Safety | Ontario - Remote | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you: - Have 6+ years of experience in customer support, user operations, ads operations, Trust & Safety, risk operations, escalations, or a related field, including ownership of high-impact customer or advertiser cases. - Bring strong inves |
| Senior Support Specialist, Ads | Trust & Safety | San Francisco | heading:you might thrive in this role if you | 6+ years | You might thrive in this role if you: - Have 6+ years of experience in customer support, user operations, ads operations, Trust & Safety, risk operations, escalations, or a related field, including ownership of high-impact customer or advertiser cases. - Bring strong inves |
| Technical Operations Analyst, User Safety & Risk | Trust & Safety | London, UK | heading:requirements | 5+ years | dures, and maintenance expectations so others can run and improve the work. You Might Thrive in This Role If You - Have 5+ years of experience in technical operations, data analytics, trust and safety, risk operations, product operations, or a related field. - Are strong in SQL and comfortable working with unfamiliar datasets, schemas, joins, den |
| Trust & Safety Ads Operations Analyst, Programs | Trust & Safety | San Francisco | heading:requirements | 8+ years | rove speed, consistency, and scale while preserving appropriate human judgment. You might thrive in this role if you: - 8+ years of experience in program management, strategy and operations, product operations, technical program management, Trust & Safety, Risk Operations, Ads or Monetization Operations, or a related field. - Deep familiarity wit |
| User Safety & Risk Operations Analyst - Global Response (Weekend Shift) | Trust & Safety | Singapore | heading:requirements | 5+ years | 24/7 on-call rotation, including off-hours and weekend coverage as needed. YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 5+ years of experience in trust & safety, content moderation, investigations, fraud, or developer risk operations. - Have experience working in incident response, law enforcement response, or escalations management. - Leverage O |
| User Safety & Risk Operations Analyst - Global Response (Weekend Shift) | Trust & Safety | San Francisco | heading:requirements | 5+ years | e weekend shift each week (e.g., work weeks covering Saturday - Wednesday) YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have 5+ years of experience in trust & safety, content moderation, investigations, fraud, or developer risk operations. - Have experience working in incident response, law enforcement response, or escalations management. - Leverage O |
| Manager, Senior Support Engineering | User Operations | Dublin, Ireland | heading:you might thrive in this role if you | 10+ years; 5+ years | You might thrive in this role if you: - 10+ years of experience in technical support engineering, software engineering, site reliability engineering, or a related technical discipline, including hands-on experience supporting production systems at scale. - 5+ years of \|\| engineering, or a related technical discipline, including hands-on experience supporting production systems at scale. - 5+ years of experience managing engineers or leading complex, multi… |
| Data Scientist, Inference Capacity Optimization | Workload | San Francisco | heading:qualifications | 5+ years | ons Research, Applied Mathematics, Economics, or related quantitative discipline (or equivalent industry experience). - 5+ years of experience working in the infrastructure data science space. - Strong expertise in Python and SQL. - Experience building forecasting, optimization, or predictive models. - Strong understanding of experimentation, sta |
| Supply Chain Manager, Industrial Compute | Workload | San Francisco | heading:qualifications | 10+ years | fications - Bachelor's degree in Engineering, Supply Chain, Operations, Business, or equivalent practical experience. - 10+ years of experience leading technical supply chain, sourcing, manufacturing operations, or infrastructure delivery organizations. - Experience managing multidisciplinary technical teams. - Experience developing supplier strat |
| Technical Program Manager, Infrastructure Strategy & Delivery Operations | Workload | San Francisco | heading:qualifications | 8+ years | Qualifications - 8+ years leading complex technical programs, infrastructure delivery initiatives, or large-scale operational programs. - Experience leading highly cross-functional programs spanning engineering, manufacturing, supply chain, logi |
| Senior Manager, EHS - Robotics | Workplace | San Francisco | heading:requirements | 15+ years | porting that make site risks, actions, and performance visible to leadership. You’ll thrive in this role if you have: - 15+ years of progressive EHS experience, including significant leadership responsibility in robotics, advanced manufacturing, R&D, industrial, or similarly complex technical environments. - Strong technical knowledge across occup |
| Senior Manager, Occupancy Planning & Workplace Strategy | Workplace | San Francisco | heading:requirements | 8+ years | clear communication, coordinated execution, and successful transitions. YOU MIGHT THRIVE IN THIS ROLE IF YOU - Bring 5–8+ years of experience in occupancy planning, workplace strategy, space management, or a related field, with experience independently managing complex, multi-team or multi-site portfolios. - Have a strong track record of transla |

</details>

<details>
<summary>Education signals from qualification sections (64 rows)</summary>

| title | team | location | qualification_method | signals | contexts |
| --- | --- | --- | --- | --- | --- |
| Researcher, Alignment | Alignment | San Francisco | heading:you might thrive in this role if you | PHD; EQUIVALENT_EXPERIENCE | if you: - Are a team player – willing to do a variety of tasks that move the team forward. - Have a PhD or equivalent experience in research in computer science, computational science, data science, cognitive science, or similar fields. - Have strong engineering skills, particularly \|\| - Are a team player – willing to do a variety of tasks that move the team forward. - Have a PhD or equivalent experience in research in computer science, computational scie… |
| Engineering Manager, MLE | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | PHD | You might thrive in this role if you: - Master's/ PhD degree in Computer Science, Machine Learning, Data Science, or a related field. - Demonstrated experience in deep learning and transformers models - Experience with content unders |
| Machine Learning Engineer, Core Experimentation | Applied AI Engineering | Seattle | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | nding in machine learning, statistics, computer science, or a related field through formal study or equivalent practical experience. - Understand experimentation and statistical reasoning, especially why predictive accuracy is not the same as causal validity. - Treat calibration, uncertainty, provenance, priva |
| Machine Learning Engineer, Monetization AI/ML | Applied AI Engineering | San Francisco | heading:you might thrive in this role if you | PHD | You might thrive in this role if you: - Master's/ PhD degree in Computer Science, Machine Learning, Data Science, or a related field. - Demonstrated experience in deep learning and transformers models - Proficiency in frameworks like |
| Software Engineer, Resilience Engineering | Applied AI Infrastructure | San Francisco | heading:you might thrive in this role if you | BACHELORS | bility are considered in the design and development of new features and services. Qualifications: - Bachelor's degree in Computer Science, Information Technology, or a related field (or equivalent work experience). - Proven experience as an SWE focused on reliability or a similar role in a fast-p |
| Business Development Lead, Compute Strategy | Compute | US - Remote | heading:qualifications | EQUIVALENT_EXPERIENCE | term ROI. - Are comfortable navigating ambiguity in a fast-moving environment. - Hold a JD, MBA, or equivalent experience is preferred but not required. |
| Data Center Hardware Quality & Reliability Engineer | Compute | San Francisco | heading:requirements | MASTERS; BACHELORS; EQUIVALENT_EXPERIENCE | rical, mechanical, computer, materials, reliability engineering, physics, or equivalent experience; MS preferred. • 8+ years in hardware quality/reliability, server/rack systems, or mission-critical infrastructure; 3+ years owning field-failure, RMA, or CAPA outcomes. • Solid worki \|\| lity council and, as the team grows, mentor the 1P and 3P Field Quality Engineers. Qualifications • BS in electrical, mechanical, computer, materials, reliability engineerin… |
| Infrastructure Sourcing Operations Lead | Compute | San Francisco | heading:requirements | BACHELORS; EQUIVALENT_EXPERIENCE | ating in user acceptance testing, training users, and driving adoption of standardized processes. - Bachelor's degree in engineering, construction management, supply chain, business, operations, finance, or equivalent practical experience; relevant professional certification is a plus. \|\| r's degree in engineering, construction management, supply chain, business, operations, finance, or equivalent practical experience; relevant professional certification … |
| Physical Network & Structured Cabling Engineer | Compute | San Francisco | heading:requirements | EQUIVALENT_EXPERIENCE | ndards. Qualifications - Bachelor’s degree in Engineering, Telecommunications, or related field, or equivalent experience. - 10+ years of experience designing and delivering physical network infrastructure and structured cabling systems for large-scale data centers, including responsibility for desig |
| Site Operations Technician | Compute | San Francisco | heading:qualifications | EQUIVALENT_EXPERIENCE | Qualifications - Have an Associate's degree, technical certification, military experience, or equivalent practical experience. - Have 2+ years supporting data center operations, facilities, hardware operations, manufacturing, industrial operations, or mission-critical infrastructure. - Have experience wo |
| Software Engineer, Workload Enablement | Compute | San Francisco | heading:qualifications | BACHELORS; EQUIVALENT_EXPERIENCE | Qualifications - BS in CS/EE (or equivalent practical experience). - 5+ years in one or more of: ML systems, performance engineering, distributed systems, or HPC. - Strong hands-on experience with: - \|\| Qualifications - BS in CS/EE (or equivalent practical experience). - 5+ years in one or more of: ML systems, performance engineering, distributed systems, or HPC. - Strong hands-on experience with: - PyTorch and modern LLM training/inference st |
| Technical Program Manager, Infrastructure Systems & Tooling | Compute | San Francisco | heading:requirements | BACHELORS | aries, urgent timelines, and high operational stakes while maintaining rigor and momentum. - Hold a bachelor's degree in Engineering, Computer Science, Information Systems, Construction Management, Operations Management, Business, or an equivalent combination of education and practical experience |
| Machine Learning Engineer, API Multicloud | Core Product & Platform \| API | San Francisco | heading:requirements | PHD; EQUIVALENT_EXPERIENCE | evolving quickly, and reliability matters. YOUR BACKGROUND MIGHT LOOK SOMETHING LIKE: - Master’s or PhD in Computer Science, Machine Learning, or a related field, or equivalent practical experience. - 3+ years of professional engineering experience in relevant ML, infrastructure, or \|\| OOK SOMETHING LIKE: - Master’s or PhD in Computer Science, Machine Learning, or a related field, or equivalent practical experience. - 3+ years of professional engineering … |
| Applied Data Science & Insights Leader - GTM Intelligence Solutions and Technical Success | Data Science | San Francisco | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | a collaborative, high-accountability team culture. - An advanced degree in a quantitative field, or equivalent practical experience. |
| Data Scientist, B2B Strategy & Intelligence | Data Science | San Francisco | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | plex business problems. - Strong technical fluency with analytical tools such as SQL and Python, or equivalent experience using data to answer open-ended business questions. - Ability to connect data across product, customer, sales, revenue, market, and operational contexts to form a coherent view of |
| Machine Learning Data Scientist, Forecasting | Data Science | San Francisco | heading:you might thrive in this role if you | PHD; MASTERS | You might thrive in this role if you have: - Advanced degree (MS or PhD) in a quantitative field (e.g., Statistics, Computer Science, Economics, Operations Research). - 7+ years of experience in applied data science, with deep hands-on exposure to for \|\| You might thrive in this role if you have: - Advanced degree (MS or PhD) in a quantitative field (e.g., Statistics, Computer Science, Economics, Operations Research). - 7+ years of experience in applied d… |
| Data Center Controls Network Engineer | Datacenter Design | San Francisco | heading:requirements | MASTERS | Engineering, Network Engineering, Systems Engineering, or a related discipline. Preferred Skills - Master's degree in Electrical Engineering, Computer Engineering, Network Engineering, Systems Engineering, or a related discipline. - Experience leading multi-campus OT network integration, commi |
| Data Center Infrastructure Engineering Program Manager (Network and Whitespace) | Datacenter Design | San Francisco | heading:requirements | BACHELORS; EQUIVALENT_EXPERIENCE | kills, with the ability to produce crisp status reporting and drive action across matrixed teams. - Bachelor's degree in Engineering, Computer Science, Construction Management, Operations, Business, or a related technical or quantitative field, or equivalent practical experience. Preferred Skills \|\| ce, Construction Management, Operations, Business, or a related technical or quantitative field, or equivalent practical experience. Preferred Skills - Direct… |
| Hardware Operations Engineer | Datacenter Design | San Francisco | heading:qualifications | EQUIVALENT_EXPERIENCE | ing transitions. - Industry certifications such as CompTIA Server+, OEM hardware certifications, or equivalent experience. - Experience applying Environmental Health and Safety (EHS) practices in mission-critical datacenter environments. |
| Network Operations Engineer, AI Networking | Datacenter Design | San Francisco | heading:qualifications | EQUIVALENT_EXPERIENCE | fications - Bachelor’s degree in Computer Science, Network Engineering, or a related discipline, or equivalent practical experience. - 5+ years of experience operating large-scale data center, cloud, AI, or HPC network infrastructure. - Experience supporting production network environments with high-availabili |
| PCBA Manufacturing Engineer | Datacenter Design | Singapore | heading:qualifications | BACHELORS | Qualifications - Bachelor's degree in Electrical Engineering, Mechanical Engineering, Manufacturing Engineering, or related field. - 5+ years supporting high-volume PCBA manufacturing. - Experience with SMT manufac |
| Strategic Sourcing Manager, Data Center Infrastructure, Electrical | Datacenter Design | San Francisco | heading:requirements | BACHELORS | al agreements that support Industrial Compute's long-term infrastructure strategy. Qualifications - Bachelor's degree in Supply Chain, Engineering, Construction Management, Business, Operations, Finance, or a related field. - 8+ years of experience in strategic sourcing, procurement, supplier man |
| Strategic Sourcing Manager, Data Center Infrastructure, Mechanical | Datacenter Design | San Francisco | heading:requirements | BACHELORS | al agreements that support Industrial Compute's long-term infrastructure strategy. Qualifications - Bachelor's degree in Supply Chain, Engineering, Construction Management, Business, Operations, Finance, or a related field. - 8+ years of experience in strategic sourcing, procurement, supplier man |
| Strategic Sourcing Manager, Data Center Infrastructure, Owner Furnished Equipment | Datacenter Design | San Francisco | heading:requirements | BACHELORS | al agreements that support Industrial Compute's long-term infrastructure strategy. Qualifications - Bachelor's degree in Supply Chain, Engineering, Construction Management, Business, Operations, Finance, or a related field. - 8+ years of experience in strategic sourcing, procurement, supplier man |
| Software Engineer, Applied Emerging Talent (2027) | Emerging Talent | San Francisco | whole_description_fallback | EQUIVALENT_EXPERIENCE | chelor's or Master’s degree in Computer Science, Computer Engineering, relevant technical field, or equivalent practical experience - 0-1 years of experience in software engineering or a relevant field - Proficiency with JavaScript, React, and some backend languages (we use Python) - Some experience with relat |
| Contract Management Lead (Procurement) | Finance | San Francisco | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | e judgment; a JD, law degree, or comparable legal background is strongly preferred, but exceptional equivalent experience is welcome. - Have implemented or owned a contract lifecycle management (CLM) platform and can design templates, clause libraries, integrations, reporting, and scalable workflows. |
| Payroll Initiatives Lead | Finance | San Francisco | heading:you might thrive in this role if you | BACHELORS; EQUIVALENT_EXPERIENCE | nication skills, with the ability to partner effectively with internal and external stakeholders. - Bachelor's degree in Finance, Accounting, HR, or a related field, or equivalent practical experience. CPP certification is a plus. \|\| l and external stakeholders. - Bachelor's degree in Finance, Accounting, HR, or a related field, or equivalent practical experience. CPP certification is a plus. |
| Senior Manager, Accounts Payable - Compute | Finance | San Francisco | heading:requirements | EQUIVALENT_EXPERIENCE | ght thrive in this role if you: - Bring 8+ years in AP, payments, or related finance operations, or equivalent experience, with personal ownership of complex, high-value supplier obligations and material exceptions from executed contract through invoice approval, payment, and settlement. - Bring stro |
| Full-Stack SWE, Data Acquisition (Foundations) | Foundations | San Francisco | heading:qualifications | PHD; MASTERS; BACHELORS | QUALIFICATIONS: - BS/MS/PhD in Computer Science or a related field. - 4+ years of industry experience in full-stack development. - Proficiency in frontend frameworks (React, Vue, or similar) and backend tech \|\| QUALIFICATIONS: - BS/MS/PhD in Computer Science or a related field. - 4+ years of industry experience in full-stack development. - Proficiency in frontend frameworks (React, Vue, or similar) and backend \|\| QUALIFICATIONS: - BS/MS/PhD in Computer Sc… |
| Software Engineer, Data Acquisition | Foundations | San Francisco | heading:qualifications | PHD; MASTERS; BACHELORS | Qualifications: - BS/MS/PhD in Computer Science or a related field. - 4+ years of industry experience in software development. - Experience with large web crawlers a plus - Strong expertise in large stateful \|\| Qualifications: - BS/MS/PhD in Computer Science or a related field. - 4+ years of industry experience in software development. - Experience with large web crawlers a plus - Strong expertise in large stat \|\| Qualifications: - BS/MS/PhD in Computer S… |
| Advanced Packaging Reliability Engineer | Hardware | San Francisco | heading:you might thrive in this role if you | PHD; MASTERS | age regulation, high-current power delivery, or high-transient-current AI and HPC products. - MS or PhD in Mechanical Engineering, Electrical Engineering, Materials Science, Physics, or a related technical field. - Strong communication, cross-functional collaboration, and technical \|\| d voltage regulation, high-current power delivery, or high-transient-current AI and HPC products. - MS or PhD in Mechanical Engineering, Electrical Engineering, Materials Sc… |
| Design Verification Engineer | Hardware | San Francisco | heading:you might thrive in this role if you | MASTERS; BACHELORS | You might thrive in this role if you have: - BS/MS in EE/CE/CS or equivalent with 3+ years of experience in hardware verification. - Proven success verifying complex IP or SoC designs in industry-standard flows - Proficient in Sys \|\| You might thrive in this role if you have: - BS/MS in EE/CE/CS or equivalent with 3+ years of experience in hardware verification. - Proven success verifying complex IP or SoC designs in industry-standard flows - Proficient in |
| Hardware / Software CoDesign Engineer - 3P | Hardware | San Francisco | heading:qualifications | PHD | writers, compiler developers, system engineers, chip architects/microarchitects Preferred Skills - PhD in Computer Science and Engineering with a specialization in Computer Architecture, Parallel Computing. Compilers or other Systems - Strong understanding of LLMs and challenges re |
| Hardware Tools Engineer | Hardware | San Francisco | heading:you might thrive in this role if | EQUIVALENT_EXPERIENCE | monstrated ability to build and maintain software (projects, internships, research, open source, or equivalent experience). - Strong CS fundamentals: data structures, algorithms, debugging, and software design. - Proficiency in at least one of Rust, C++, or Python (and willingness to learn the rest). |
| Manufacturing Test Engineer | Hardware | Singapore | heading:requirements | EQUIVALENT_EXPERIENCE | ical Engineering, Computer Engineering, Manufacturing Engineering, or a related technical field, or equivalent practical experience. - 5+ years of experience in manufacturing test engineering, product test, NPI test development, or related hardware test roles. - Experience with one or more of the following on |
| Physical Design Engineer | Hardware | San Francisco | heading:qualifications | PHD; MASTERS; BACHELORS | Qualifications: - BS w/ 4+ or MS with 2+ years or PhD with 0-1 year(s) of relevant industry experience in physical design and methodology development - Demonstrated success in taping out complex silicon designs - Hands-on experience \|\| Qualifications: - BS w/ 4+ or MS with 2+ years or PhD with 0-1 year(s) of relevant industry experience in physical design and methodology development - Demonstrated success in taping out complex silicon designs - \|\| Qualifi… |
| Rack Power Engineer | Hardware | San Francisco | heading:requirements | EQUIVALENT_EXPERIENCE | systems. - Have a master’s degree in Electrical Engineering, Power Electronics, a related field, or equivalent practical experience. - Have strong knowledge of AC/DC rectifiers, power shelves, PSUs, and DC distribution, including three-phase inputs, power conversion topologies, control-loop stability, current |
| Wireless Regulatory Engineer - SAR | Hardware Engineering | Mountain View | heading:requirements | EQUIVALENT_EXPERIENCE | activities for wireless consumer products. YOU MIGHT THRIVE IN THIS ROLE IF YOU: - Have a Master’s degree or equivalent experience in Electrical Engineering, Computer Engineering, RF Engineering, or a related technical field. - Bring deep experience with SAR, RF exposure, or wireless regulatory tes |
| People Research Data Scientist, AI Fairness & Bias | People Systems & Operations | San Francisco | heading:you might thrive in this role if you | PHD | Science, Statistics, Economics, Data Science, Behavioral Science, or a related quantitative field; PhD preferred but not required. |
| Product Manager, Financial Engineering | Product Management | San Francisco | heading:you might thrive in this role if you | BACHELORS | his role if you: - Have 6+ years of product management or related industry experience. - Obtained a bachelor's degree in Accounting, Finance, Computer Science, Engineering, Information Systems, Analytics, Mathematics, Physics, Applied Sciences, or a related field. - Have proven experience working |
| Rosalind Life Sciences Product Manager | Product Management | San Francisco | heading:requirements | EQUIVALENT_EXPERIENCE | n, data quality, and biological interpretation with researchers; an advanced degree is helpful, but equivalent practical experience matters. - Combine strategic judgment with a hands-on builder mindset: prototype ideas, choose focused use cases, and stay close to execution. - Have built model evaluations or be |
| Field Engineer | Robotics | San Francisco | heading:you might thrive in this role if you | BACHELORS | ysical systems and running complex issues to ground without adding unnecessary complexity. - Hold a Bachelor's degree in Mechanical Engineering, Electrical Engineering, Mechatronics, Robotics, Computer Engineering, or a related field. Preferred qualifications - Familiarity with robot middleware, |
| Mechanical Engineer, Dynamometer and Actuator Testing Infrastructure | Robotics | San Francisco | heading:requirements | EQUIVALENT_EXPERIENCE | chanical interfaces. - Proficiency with CAD and drawing release workflows; NX, SolidWorks, Creo, or equivalent experience is welcome. - Experience with structural, thermal, fatigue, or modal analysis and applying results to practical hardware decisions. - Hands-on experience with assembly, machining, |
| Strategic Finance, Compute | Strategic Finance | San Francisco | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | ity with data systems, analytical tools, and large datasets preferred but not required - Bachelor’s degree or equivalent practical experience; technical undergraduate degree preferred but not required |
| AI Support Engineer - Dublin | Support Delivery | Dublin, Ireland | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - Dublin (Weekend Shift) | Support Delivery | Dublin, Ireland | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - San Francisco | Support Delivery | San Francisco | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - San Francisco (Weekend Shift) | Support Delivery | San Francisco | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - Singapore | Support Delivery | Singapore | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - Singapore (Korean Speaking) | Support Delivery | Singapore | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - Singapore (Weekend Shift) | Support Delivery | Singapore | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - Tokyo | Support Delivery | Tokyo, Japan | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - Tokyo (Korean Speaking) | Support Delivery | Tokyo, Japan | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - Tokyo (Weekend Shift) | Support Delivery | Tokyo, Japan | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - Toronto | Support Delivery | Ontario - Remote | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | a bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer - Toronto (Weekend Shift) | Support Delivery | Ontario - Remote | heading:you might thrive in this role if you | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer, Biosciences - San Francisco | Support Delivery | San Francisco | heading:requirements | EQUIVALENT_EXPERIENCE | research environments, scientific software, cloud platforms, APIs, or data-intensive workflows. - A degree or equivalent practical experience in a life sciences, computational, engineering, or other relevant technical field. |
| AI Support Engineer, Government - San Francisco, CA | Support Delivery | San Francisco | heading:requirements | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| AI Support Engineer, Government - Washington, D.C. | Support Delivery | Washington, DC | heading:requirements | EQUIVALENT_EXPERIENCE | - Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |
| Support Delivery Lead, Government | Support Delivery | Washington, DC | heading:requirements | EQUIVALENT_EXPERIENCE | A bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. - Experience supporting government, public-sector, regulated, or security-conscious customers and working through complex technical and organizational requirements. - Strong tech |
| Technical Program Manager, Strategic Initiatives | Technical Program Management | San Francisco | heading:you might thrive in this role if you | PHD | You might thrive in this role if you: - Possess an advanced degree in a hard science, with a PhD being advantageous, or a demonstrated track record of engineering expertise. - Have an extensive track record of successfully delivering high-profile, complex technical projects a |
| Senior Program Manager, Consumer Device Safety Operations | Trust & Safety | San Francisco | heading:requirements | EQUIVALENT_EXPERIENCE | arranty, returns, reverse logistics, or privacy-sensitive sensor and diagnostic data. - A technical degree or equivalent experience partnering closely with hardware, software, data, or systems engineering teams. - Experience with vendor operations, quality-assurance programs, regulated-product opera |
| Data Scientist, Inference Capacity Optimization | Workload | San Francisco | heading:qualifications | PHD; MASTERS | Qualifications - MS or PhD in Statistics, Computer Science, Operations Research, Applied Mathematics, Economics, or related quantitative discipline (or equivalent industry experience). - 5+ years of experie \|\| Qualifications - MS or PhD in Statistics, Computer Science, Operations Research, Applied Mathematics, Economics, or related quantitative discipline (or equivalent industry experience). - 5+ years of |
| Supply Chain Manager, Industrial Compute | Workload | San Francisco | heading:qualifications | BACHELORS; EQUIVALENT_EXPERIENCE | Qualifications - Bachelor's degree in Engineering, Supply Chain, Operations, Business, or equivalent practical experience. - 10+ years of experience leading technical supply chain, sourcing, manufacturing operation \|\| Qualifications - Bachelor's degree in Engineering, Supply Chain, Operations, Business, or equivalent practical experience. - 10+ years of experience leading technical supply chain, sourcing, manufacturing operations, or infrastructure delive… |

</details>

## 13. Compensation diagnostics

<details>
<summary>Salary components with interval preserved (657 rows)</summary>

| title | team | location | currency | interval | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| Research Engineer, AI for Chip Design | AI for Chip Design | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Software Engineer, AI for Chip Design | AI for Chip Design | San Francisco | USD | 1 YEAR | 266000.0 | 468000.0 |
| Account Associate - SF | Account Associates | San Francisco | USD | 1 YEAR | 108000.0 | 120000.0 |
| Sales Development Manager, Enterprise (AMER) | Account Associates | San Francisco | USD | 1 YEAR | 261000.0 | 305000.0 |
| Agency Partner, Ads Solutions | Ads Solutions | New York City | USD | 1 YEAR | 216000.0 | 273000.0 |
| Client Partner, Ads Solutions | Ads Solutions | San Francisco | USD | 1 YEAR | 239000.0 | 273000.0 |
| Client Partner, Ads Solutions - Travel | Ads Solutions | San Francisco | USD | 1 YEAR | 216000.0 | 273000.0 |
| Customer Success Manager, Ads Solutions (New York City) | Ads Solutions | New York City | USD | 1 YEAR | 176000.0 | 234000.0 |
| Customer Success Manager, Ads Solutions (San Francisco) | Ads Solutions | San Francisco | USD | 1 YEAR | 176000.0 | 234000.0 |
| Customer Success Manager, Ads Solutions (Seattle) | Ads Solutions | Seattle | USD | 1 YEAR | 176000.0 | 234000.0 |
| Partner Solutions Engineer, Ads Solutions - San Francisco | Ads Solutions | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Solutions Engineer, Ads Solutions - San Francisco | Ads Solutions | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Agent Post-Training Research | Agents | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Agent Post-Training, API & Power Users | Agents | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Agent Post-Training, Artifacts Research | Agents | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Agent Post-Training, Computer Use Research | Agents | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Agent Post-Training, Connectors Research | Agents | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Agent Post-Training, Context Research | Agents | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Agent Post-Training, Frontier Evals and Environments Research | Agents | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Agent Post-Training, Personality | Agents | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Research Engineer, Frontier Evals & Environments | Agents | San Francisco | USD | 1 YEAR | 295000.0 | 380000.0 |
| Researcher, Alignment | Alignment | San Francisco | USD | 1 YEAR | 295000.0 | 500000.0 |
| Researcher, Alignment CoT Monitorability | Alignment | San Francisco | USD | 1 YEAR | 295000.0 | 500000.0 |
| Researcher, Alignment Interpretability | Alignment | San Francisco | USD | 1 YEAR | 295000.0 | 500000.0 |
| Applied AI Software Engineer, GTM Growth Engineering | Applied AI | San Francisco | USD | 1 YEAR | 266000.0 | 405000.0 |
| Backend Software Engineer - Codex for Finance | Applied AI | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Engineering Manager, Core Experimentation | Applied AI | Seattle | USD | 1 YEAR | 510000.0 | 536000.0 |
| Full Stack Software Engineer - Codex for Finance | Applied AI | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Full Stack Software Engineer, Gov | Applied AI | Washington, DC | USD | 1 YEAR | 207000.0 | 385000.0 |
| Growth - Digital Marketing (Business) | Applied AI | San Francisco | USD | 1 YEAR | 239000.0 | 325000.0 |
| Growth - Digital Marketing (Consumer) | Applied AI | San Francisco | USD | 1 YEAR | 189000.0 | 265000.0 |
| Growth - Digital Marketing (Enterprise) | Applied AI | San Francisco | USD | 1 YEAR | 239000.0 | 325000.0 |
| Growth - Lifecycle Lead | Applied AI | San Francisco | USD | 1 YEAR | 239000.0 | 325000.0 |
| Growth - Lifecycle Lead (B2B) | Applied AI | San Francisco | USD | 1 YEAR | 239000.0 | 325000.0 |
| Software Engineer, Cooperative AI | Applied AI | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, GTM Growth Engineering | Applied AI | San Francisco | USD | 1 YEAR | 266000.0 | 405000.0 |
| Software Engineer, Native Learning Experiences | Applied AI | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Subject Matter Expert, Investment Banking | Applied AI | San Francisco | USD | 1 YEAR | 185000.0 | 205000.0 |
| Android Engineer, Ad Formats | Applied AI Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Android Engineer, Applied Foundations | Applied AI Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Android Engineer, ChatGPT ImageGen | Applied AI Engineering | San Francisco | USD | 1 YEAR | 185000.0 | 385000.0 |
| Android Engineer, ChatGPT Library Team | Applied AI Engineering | Seattle | USD | 1 YEAR | 185000.0 | 405000.0 |
| Android Engineer, Plugin Developer Platform | Applied AI Engineering | San Francisco | USD | 1 YEAR | 185000.0 | 385000.0 |
| Backend Software Engineer, Applied Foundations | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Backend Software Engineer, ChatGPT ImageGen | Applied AI Engineering | San Francisco | USD | 1 YEAR | 185000.0 | 305000.0 |
| ChatGPT Performance Engineer | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Data Engineer | Applied AI Engineering | San Francisco | USD | 1 YEAR | 235000.0 | 385000.0 |
| Data Engineer, Core Experimentation | Applied AI Engineering | Seattle | USD | 1 YEAR | 347000.0 | 385000.0 |
| Data Engineering Manager, Growth & Revenue | Applied AI Engineering | San Francisco | USD | 1 YEAR | 459000.0 | 536000.0 |
| Engineering Manager, ChatGPT Search Infrastructure | Applied AI Engineering | San Francisco | USD | 1 YEAR | 401000.0 | 445000.0 |
| Engineering Manager, ChatGPT Space | Applied AI Engineering | San Francisco | USD | 1 YEAR | 401000.0 | 445000.0 |
| Engineering Manager, Distillation & Detection Platform | Applied AI Engineering | San Francisco | USD | 1 YEAR | 400000.0 | 445000.0 |
| Engineering Manager, Library | Applied AI Engineering | Seattle | USD | 1 YEAR | 401000.0 | 445000.0 |
| Engineering Manager, MLE | Applied AI Engineering | San Francisco | USD | 1 YEAR | 500000.0 | 555000.0 |
| Founding Full Stack Software Engineer, Legal | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Frontend Software Engineer, Codex App | Applied AI Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Full Stack Software Engineer, ChatGPT Finances | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Full Stack Software Engineer, ChatGPT ImageGen | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Full Stack Software Engineer, Education | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Full Stack Software Engineer, Growth | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Full Stack Software Engineer, Product Explorations | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Full Stack Staff & Software Engineer, Consumer Monetization | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Full-Stack Engineer, ChatGPT Education & Learning | Applied AI Engineering | San Francisco | USD | 1 YEAR | 185000.0 | 490000.0 |
| Full-Stack Software Engineer, Applied Foundations | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Full-Stack Software Engineer, Emerging Products | Applied AI Engineering | San Francisco | USD | 1 YEAR | 295000.0 | 445000.0 |
| Machine Learning Engineer, Core Experimentation | Applied AI Engineering | Seattle | USD | 1 YEAR | 437000.0 | 485000.0 |
| Machine Learning Engineer, Monetization AI/ML | Applied AI Engineering | San Francisco | USD | 1 YEAR | 381000.0 | 555000.0 |
| Mobile / Full Stack Staff & Software Engineer, Consumer Monetization | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Product Manager, Technology Vertical | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Protection Scientist Engineer, Integrity | Applied AI Engineering | San Francisco | USD | 1 YEAR | 198000.0 | 425000.0 |
| Research Engineer, Retrieval & Search, Applied Engineering | Applied AI Engineering | San Francisco | USD | 1 YEAR | 293000.0 | 585000.0 |
| Senior Staff Software Engineer, Identity | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 405000.0 |
| Software Engineer, Ad Formats | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Ads Integrity | Applied AI Engineering | San Francisco | USD | 1 YEAR | 293000.0 | 385000.0 |
| Software Engineer, Ads Manager | Applied AI Engineering | Seattle | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, ChatGPT Infrastructure | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, ChatGPT Shopping | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Consumer Health | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Software Engineer, Enterprise Verticals | Applied AI Engineering | San Francisco | USD | 1 YEAR | 293000.0 | 325000.0 |
| Software Engineer, Financial Engineering | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Full-Stack - Core Experimentation | Applied AI Engineering | Seattle | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Habitat (Online Data) | Applied AI Engineering | Seattle | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Healthcare | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Software Engineer, Implicit Signals | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Infrastructure - Core Experimentation | Applied AI Engineering | Seattle | USD | 1 YEAR | 347000.0 | 385000.0 |
| Software Engineer, Integrity Foundations | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Localization | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Model Deployment- ChatGPT Engineering | Applied AI Engineering | London, UK | GBP | 1 YEAR | 194000.0 | 280000.0 |
| Software Engineer, Monetization Data Systems | Applied AI Engineering | Mountain View | USD | 1 YEAR | 293000.0 | 385000.0 |
| Software Engineer, Monetization Delivery | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Monetization ML Infrastructure | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Monetization Product & Platform | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Plugin Developer Platform | Applied AI Engineering | San Francisco | USD | 1 YEAR | 185000.0 | 490000.0 |
| Software Engineer, Plugin Ecosystem | Applied AI Engineering | San Francisco | USD | 1 YEAR | 185000.0 | 490000.0 |
| Software Engineer, Product Velocity | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Scaled Abuse | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Search Infrastructure | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Shop/Feed Ads | Applied AI Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Youth Well-Being | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Staff & Software Engineer, Payments & Billing, Consumer Monetization | Applied AI Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Tech Lead Manager, Education | Applied AI Engineering | San Francisco | USD | 1 YEAR | 401000.0 | 445000.0 |
| iOS Engineer, Applied Foundations | Applied AI Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Engineering Manager, Core Services | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 293000.0 | 385000.0 |
| Software Engineer - Privacy & Compliance | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, Build Systems / CI | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 185000.0 | 490000.0 |
| Software Engineer, Caching Infrastructure | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, ChatGPT Infrastructure | Applied AI Infrastructure | London, UK | GBP | 1 YEAR | 194000.0 | 280000.0 |
| Software Engineer, Cloud Infrastructure | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 230000.0 | 490000.0 |
| Software Engineer, Core Services | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, Database Systems | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Delivery / CD | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 210000.0 | 490000.0 |
| Software Engineer, Developer Productivity | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 210000.0 | 490000.0 |
| Software Engineer, Observability | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Resilience Engineering | Applied AI Infrastructure | San Francisco | USD | 1 YEAR | 230000.0 | 490000.0 |
| AI Systems Engineer, Codex Agents | Codex - Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Applied AI Engineer, Codex Core Agent | Codex - Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Full Stack Engineer, Enterprise Expansions | Codex - Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Full Stack Software Engineer, Agent Enablement | Codex - Engineering | San Francisco | USD | 1 YEAR | 255000.0 | 405000.0 |
| Full Stack Software Engineer, Codex | Codex - Engineering | San Francisco | USD | 1 YEAR | 255000.0 | 405000.0 |
| Full Stack Software Engineer, Cybersecurity Products | Codex - Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Full Stack Software Engineer, Sales Platform | Codex - Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 455000.0 |
| Product Engineer, Cyber | Codex - Engineering | San Francisco | USD | 1 YEAR | 255000.0 | 445000.0 |
| Product Engineer, Full Stack - Agents | Codex - Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Product Manager, Learning | Codex - Engineering | San Francisco | USD | 1 YEAR | 293000.0 | 385000.0 |
| Software Engineer, Cloud Agents | Codex - Engineering | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Codex Core Agents | Codex - Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, Codex Cyber | Codex - Engineering | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Codex Enterprise | Codex - Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, Enterprise Controls | Codex - Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, OpenAI Presence | Codex - Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Developer Experience Engineer, Cyber | Codex – Developer Experience | San Francisco | USD | 1 YEAR | 198000.0 | 335000.0 |
| Communications Manager, Monetization | Communications | San Francisco | USD | 1 YEAR | 297000.0 | 330000.0 |
| Internal Communications Lead, Enterprise & Growth | Communications | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Internal Communications, Enterprise & Growth | Communications | San Francisco | USD | 1 YEAR | 171000.0 | 190000.0 |
| Internal Communications, Research and Product | Communications | San Francisco | USD | 1 YEAR | 171000.0 | 190000.0 |
| Research Communications Manager | Communications | San Francisco | USD | 1 YEAR | 185000.0 | 205000.0 |
| Strategy & Systems Manager, Communications | Communications | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Business Development Lead, Compute Strategy | Compute | US - Remote | USD | 1 YEAR | 333000.0 | 370000.0 |
| Capacity Systems Software Engineer | Compute | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Community Engagement Lead, Ohio | Compute | US - Remote | USD | 1 YEAR | 176000.0 | 385000.0 |
| Data Center Compute, OpenHouse Savannah 2026 | Compute | US - Remote | USD | 1 YEAR | 125000.0 | 400000.0 |
| Data Center Hardware Quality & Reliability Engineer | Compute | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Development Lead | Compute | US - Remote | USD | 1 YEAR | 225000.0 | 385000.0 |
| Development Planner, Industrial Compute | Compute | US - Remote | USD | 1 YEAR | 225000.0 | 385000.0 |
| Economic Development Lead | Compute | US - Remote | USD | 1 YEAR | 176000.0 | 285000.0 |
| Infrastructure Operations & Sustainability Lead | Compute | US - Remote | USD | 1 YEAR | 223000.0 | 385000.0 |
| Infrastructure Sourcing Operations Lead | Compute | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Performance Modeling Engineer | Compute | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Performance Modeling Engineer ~2 | Compute | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Performance Modeling Lead | Compute | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Physical Network & Structured Cabling Engineer | Compute | San Francisco | USD | 1 YEAR | 257000.0 | 327000.0 |
| Site Operations Technician | Compute | San Francisco | USD | 1 YEAR | 157000.0 | 221000.0 |
| Software Engineer, Agent Infrastructure | Compute | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, Compute - Storage | Compute | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, Compute Infrastructure | Compute | San Francisco | USD | 1 YEAR | 230000.0 | 405000.0 |
| Software Engineer, Core Network Engineering | Compute | San Francisco | USD | 1 YEAR | 230000.0 | 342000.0 |
| Software Engineer, Workload Enablement | Compute | San Francisco | USD | 1 YEAR | 293000.0 | 385000.0 |
| Systems Generalist, GPT Infrastructure | Compute | San Francisco | USD | 1 YEAR | 293000.0 | 445000.0 |
| Technical Program Manager, Infrastructure Systems & Tooling | Compute | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Technical Program Manager, Manufacturing Operations | Compute | Singapore | SGD | 1 YEAR | 221000.0 | 258000.0 |
| Workload Porting & Performance Engineer | Compute | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Data Engineer, Hardware & Consumer Devices | Consumer Devices | San Francisco | USD | 1 YEAR | 295000.0 | 445000.0 |
| Engineering Manager, Multimodal (API) | Core Product & Platform \| API | San Francisco | USD | 1 YEAR | 401000.0 | 445000.0 |
| Full Stack Software Engineer, API Experience | Core Product & Platform \| API | New York City | USD | 1 YEAR | 266000.0 | 385000.0 |
| Machine Learning Engineer, API Multicloud | Core Product & Platform \| API | San Francisco | USD | 1 YEAR | 223000.0 | 423000.0 |
| Software Engineer, API Enterprise Controls | Core Product & Platform \| API | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, API Frontiers | Core Product & Platform \| API | New York City | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, API Multicloud | Core Product & Platform \| API | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, API Multimodal | Core Product & Platform \| API | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, API Safety | Core Product & Platform \| API | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Corporate Security GSOC Operator | Corporate Security | San Francisco | USD | 1 YEAR | 99000.0 | 110000.0 |
| Personnel Security Specialist | Corporate Security | San Francisco | USD | 1 YEAR | 126000.0 | 175000.0 |
| Senior Special Programs Security Manager (CSSO/CPSO) | Corporate Security | Washington, DC | USD | 1 YEAR | 158000.0 | 225000.0 |
| Creative Resource Manager, Business Marketing | Creative | San Francisco | USD | 1 YEAR | 287000.0 | 318000.0 |
| Analytics Engineer, GTM | Data Science | San Francisco | USD | 1 YEAR | 220000.0 | 335000.0 |
| Applied Data Science & Insights Leader - GTM Intelligence Solutions and Technical Success | Data Science | San Francisco | USD | 1 YEAR | 441000.0 | 515000.0 |
| Data Scientist, Ads Demand | Data Science | San Francisco | USD | 1 YEAR | 293000.0 | 515000.0 |
| Data Scientist, B2B Demand Generation, Growth & Measurement | Data Science | San Francisco | USD | 1 YEAR | 293000.0 | 385000.0 |
| Data Scientist, B2B Strategy & Intelligence | Data Science | San Francisco | USD | 1 YEAR | 347000.0 | 510000.0 |
| Data Scientist, Business | Data Science | San Francisco | USD | 1 YEAR | 345000.0 | 440000.0 |
| Data Scientist, Codex | Data Science | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Data Scientist, Core Experimentation | Data Science | Seattle | USD | 1 YEAR | 347000.0 | 385000.0 |
| Data Scientist, Cybersecurity | Data Science | US - Remote | USD | 1 YEAR | 263000.0 | 515000.0 |
| Data Scientist, Financial Engineering | Data Science | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Data Scientist, Infrastructure | Data Science | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Data Scientist, Platform and B2B Products | Data Science | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Data Scientist, Preparedness | Data Science | San Francisco | USD | 1 YEAR | 345000.0 | 385000.0 |
| Data Scientist, Product | Data Science | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Data Scientist, Real Estate & Workplace | Data Science | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Data Scientist, SMB Ads Growth | Data Science | San Francisco | USD | 1 YEAR | 293000.0 | 515000.0 |
| Data Scientist, Safety | Data Science | San Francisco | USD | 1 YEAR | 265000.0 | 380000.0 |
| Machine Learning Data Scientist, Forecasting | Data Science | San Francisco | USD | 1 YEAR | 340000.0 | 500000.0 |
| 3P Systems Architect | Datacenter Design | San Francisco | USD | 1 YEAR | 342000.0 | 555000.0 |
| CPU/Storage/PoP-WAN Program Manager | Datacenter Design | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Commissioning Program Manager, Infrastructure Delivery | Datacenter Design | San Francisco | USD | 1 YEAR | 177000.0 | 285000.0 |
| Commissioning Project Lead, Data Center Delivery | Datacenter Design | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Compute Infrastructure, Critical Facilities Manager | Datacenter Design | San Francisco | USD | 1 YEAR | 199000.0 | 302000.0 |
| Critical Facilities Lead, Compute Infrastructure | Datacenter Design | US - Remote | USD | 1 YEAR | 199000.0 | 302000.0 |
| Data Center Controls Network Engineer | Datacenter Design | San Francisco | USD | 1 YEAR | 257000.0 | 327000.0 |
| Data Center Infrastructure Electrical Engineer | Datacenter Design | San Francisco | USD | 1 YEAR | 257000.0 | 327000.0 |
| Data Center Infrastructure Engineering Program Manager (Network and Whitespace) | Datacenter Design | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Datacenter Networking Technician, AI Compute Deployment - Stargate | Datacenter Design | San Francisco | USD | 1 YEAR | 157000.0 | 302000.0 |
| Electrical Commissioning Lead | Datacenter Design | San Francisco | USD | 1 YEAR | 177000.0 | 285000.0 |
| Hardware Operations Engineer | Datacenter Design | San Francisco | USD | 1 YEAR | 157000.0 | 302000.0 |
| Industrial Compute | Datacenter Design | US - Remote | USD | 1 YEAR | 150000.0 | 300000.0 |
| Land Development & Due Diligence Lead | Datacenter Design | US - Remote | USD | 1 YEAR | 199000.0 | 327000.0 |
| Manufacturing Quality Engineer – Datacenter Infrastructure | Datacenter Design | San Francisco | USD | 1 YEAR | 207000.0 | 365000.0 |
| Mechanical Commissioning Lead | Datacenter Design | San Francisco | USD | 1 YEAR | 177000.0 | 285000.0 |
| Network Operations Engineer, AI Networking | Datacenter Design | San Francisco | USD | 1 YEAR | 157000.0 | 302000.0 |
| PCBA Manufacturing Engineer | Datacenter Design | Singapore | SGD | 1 YEAR | 171000.0 | 345000.0 |
| Powered Land Developer, Development & Power Projects | Datacenter Design | US - Remote | USD | 1 YEAR | 223000.0 | 385000.0 |
| Quality Engineer, Rack Infrastructure & Site Operations | Datacenter Design | Singapore | SGD | 1 YEAR | 171000.0 | 345000.0 |
| Strategic Sourcing Manager, Compute Infrastructure | Datacenter Design | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Strategic Sourcing Manager, Data Center Infrastructure, Electrical | Datacenter Design | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Strategic Sourcing Manager, Data Center Infrastructure, Mechanical | Datacenter Design | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Strategic Sourcing Manager, Data Center Infrastructure, Owner Furnished Equipment | Datacenter Design | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Software Engineer, Applied Emerging Talent (2027) | Emerging Talent | San Francisco | USD | 1 YEAR | 180000.0 | 180000.0 |
| Senior Employee Relations Partner | Employee Relations | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Member of Executive Operations | Executive Operations | San Francisco | USD | 1 HOUR | 62.98 | 110.58 |
| Member of Executive Operations, Seattle | Executive Operations | Seattle | USD | 1 HOUR | 62.98 | 86.54 |
| Accounting Manager | Finance | San Francisco | USD | 1 YEAR | 162000.0 | 180000.0 |
| Asset Compliance Program Lead, Hardware | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Business Systems Lead, Procure-to-Pay | Finance | San Francisco | USD | 1 YEAR | 272000.0 | 302000.0 |
| Contract Management Lead (Procurement) | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Corporate Development, Deal Lead | Finance | San Francisco | USD | 1 YEAR | 333000.0 | 370000.0 |
| Head of Sourcing Enablement & Delivery | Finance | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Head of Treasury Markets | Finance | San Francisco | USD | 1 YEAR | 266000.0 | 295000.0 |
| Lead Revenue Accounting, Technical (Strategic Partnerships) | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Lead, Corporate Technical Accounting and Strategic Transactions | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Lead, Revenue Accounting, Technical | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Lead, Technical Accounting (Compute Infrastructure) | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| M&A Finance Integration Lead | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Manager, Revenue Accounting | Finance | San Francisco | USD | 1 YEAR | 162000.0 | 180000.0 |
| Manager, Revenue Accounting, Technical (Strategic Commercial Deals) | Finance | San Francisco | USD | 1 YEAR | 162000.0 | 180000.0 |
| Manager, Technical & Operational Accounting | Finance | San Francisco | USD | 1 YEAR | 162000.0 | 180000.0 |
| Order Management & Billing Lead — Cloud Marketplaces & Partnerships | Finance | San Francisco | USD | 1 YEAR | 158000.0 | 205000.0 |
| Payroll Initiatives Lead | Finance | San Francisco | USD | 1 YEAR | 221000.0 | 245000.0 |
| Pricing Operations Lead | Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Pricing Strategist, GTM | Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Senior Manager, Accounts Payable - Compute | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Senior Manager, Extended Workforce Program | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Senior Manager, Financial Reporting | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Senior Manager, Technical Revenue Accounting, Ads | Finance | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Sr. Integrations Engineer, Supply Chain Technology | Finance | San Francisco | USD | 1 YEAR | 272000.0 | 302000.0 |
| Strategic Sourcing Lead, Professional Services – Human Data | Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Strategic Sourcing Leader, Professional Services | Finance | San Francisco | USD | 1 YEAR | 266000.0 | 295000.0 |
| Strategic Technology Negotiations Lead | Finance | San Francisco | USD | 1 YEAR | 234000.0 | 295000.0 |
| Tax Director, Business Advisory and Strategic Finance | Finance | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Full Stack Engineer, Fleet Scheduling | Fleet Clusters | San Francisco | USD | 1 YEAR | 230000.0 | 490000.0 |
| Software Engineer, Fleet Infrastructure | Fleet Clusters | San Francisco | USD | 1 YEAR | 230000.0 | 490000.0 |
| Software Engineer, Fleet Management | Fleet Clusters | San Francisco | USD | 1 YEAR | 230000.0 | 490000.0 |
| Software Engineer, GPU Infrastructure - HPC | Fleet Clusters | San Francisco | USD | 1 YEAR | 230000.0 | 490000.0 |
| Software Engineer, Research Developer Productivity | Fleet Clusters | San Francisco | USD | 1 YEAR | 230000.0 | 325000.0 |
| Deployment Lead, FDE - SF | Forward Deployed Engineering | San Francisco | USD | 1 YEAR | 230000.0 | 294000.0 |
| Deployment Lead, FDE- NYC | Forward Deployed Engineering | New York City | USD | 1 YEAR | 230000.0 | 294000.0 |
| Deployment Lead, Life Sciences- NYC | Forward Deployed Engineering | San Francisco | USD | 1 YEAR | 207000.0 | 294000.0 |
| Deployment Lead, Semiconductors- SF | Forward Deployed Engineering | San Francisco | USD | 1 YEAR | 200000.0 | 295000.0 |
| Forward Deployed Engineer (FDE) - SF | Forward Deployed Engineering | San Francisco | USD | 1 YEAR | 185000.0 | 300000.0 |
| Forward Deployed Engineer (FDE) - Seattle | Forward Deployed Engineering | Seattle | USD | 1 YEAR | 185000.0 | 300000.0 |
| Forward Deployed Engineer (FDE), Financial Services- NYC | Forward Deployed Engineering | New York City | USD | 1 YEAR | 185000.0 | 300000.0 |
| Forward Deployed Engineer (FDE), Healthcare - NYC | Forward Deployed Engineering | New York City | USD | 1 YEAR | 185000.0 | 300000.0 |
| Forward Deployed Engineer (FDE), Healthcare - SF | Forward Deployed Engineering | San Francisco | USD | 1 YEAR | 185000.0 | 300000.0 |
| Forward Deployed Engineer (FDE), Healthcare - Seattle | Forward Deployed Engineering | Seattle | USD | 1 YEAR | 185000.0 | 300000.0 |
| Forward Deployed Engineer (FDE), Legal-NYC | Forward Deployed Engineering | New York City | USD | 1 YEAR | 185000.0 | 300000.0 |
| Forward Deployed Engineer (FDE), Legal-SF | Forward Deployed Engineering | New York City | USD | 1 YEAR | 185000.0 | 300000.0 |
| Forward Deployed Software Engineer - NYC | Forward Deployed Engineering | New York City | USD | 1 YEAR | 153000.0 | 325000.0 |
| Forward Deployed Software Engineer - SF | Forward Deployed Engineering | San Francisco | USD | 1 YEAR | 185000.0 | 325000.0 |
| Forward Deployed Software Engineer - Seattle | Forward Deployed Engineering | Seattle | USD | 1 YEAR | 153000.0 | 325000.0 |
| Manager, Forward Deployed Engineering- NYC | Forward Deployed Engineering | New York City | USD | 1 YEAR | 302000.0 | 385000.0 |
| Full-Stack SWE, Data Acquisition (Foundations) | Foundations | San Francisco | USD | 1 YEAR | 295000.0 | 536000.0 |
| RE / RS - Foundations, Search | Foundations | San Francisco | USD | 1 YEAR | 380000.0 | 850000.0 |
| RE/RS, Data Understanding (MM) | Foundations | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Software Engineer - Data Aquisition (systems) | Foundations | San Francisco | USD | 1 YEAR | 295000.0 | 536000.0 |
| Software Engineer, Data Acquisition | Foundations | San Francisco | USD | 1 YEAR | 295000.0 | 536000.0 |
| Software Engineer, Foundations Search | Foundations | San Francisco | USD | 1 YEAR | 266000.0 | 455000.0 |
| Technical Program Manager, Foundations Data and Operations | Foundations | San Francisco | USD | 1 YEAR | 207000.0 | 285000.0 |
| Software Engineer, Frontier Systems - Power Management | Frontiers Clusters | San Francisco | USD | 1 YEAR | 295000.0 | 445000.0 |
| Software Engineer, Hardware Health | Frontiers Clusters | San Francisco | USD | 1 YEAR | 250000.0 | 445000.0 |
| HRBP, Consumer Devices | G&A | San Francisco | USD | 1 YEAR | 230000.0 | 260000.0 |
| Senior Technical Recruiter, Consumer Devices - Singapore | G&A | Singapore | SGD | 1 YEAR | 286000.0 | 380000.0 |
| Backend Software Engineer, GTM Innovation | GTM Innovation | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Agent Standards Architect, Global Affairs | Global Affairs | Washington, DC | USD | 1 YEAR | 171000.0 | 280000.0 |
| Applied Risk Standards Architect | Global Affairs | San Francisco | USD | 1 YEAR | 171000.0 | 280000.0 |
| US Congressional Lead | Global Affairs | Washington, DC | USD | 1 YEAR | 252000.0 | 280000.0 |
| US External Affairs Associate, Global Affairs | Global Affairs | Washington, DC | USD | 1 YEAR | 171000.0 | 280000.0 |
| GTM Strategy & Operations, Policy | Go To Market | San Francisco | USD | 1 YEAR | 239000.0 | 265000.0 |
| North America Vendor Lead, Ads | Growth | San Francisco | USD | 1 YEAR | 239000.0 | 239000.0 |
| ASIC Firmware Engineer, Modeling | Hardware | San Francisco | USD | 1 YEAR | 226000.0 | 445000.0 |
| ASIC Package SI/PI Engineer | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Advanced Packaging Reliability Engineer | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Component and Product Quality Engineer, Interconnects | Hardware | San Francisco | USD | 1 YEAR | 207000.0 | 365000.0 |
| Design Verification Engineer | Hardware | San Francisco | USD | 1 YEAR | 226000.0 | 445000.0 |
| GPT Infrastructure Lead | Hardware | San Francisco | USD | 1 YEAR | 293000.0 | 385000.0 |
| Hardware / Software CoDesign Engineer - 3P | Hardware | San Francisco | USD | 1 YEAR | 381000.0 | 485000.0 |
| Hardware Strategic Sourcing Manager, Optics | Hardware | San Francisco | USD | 1 YEAR | 226000.0 | 378000.0 |
| Hardware Systems Planning Lead (1P) | Hardware | San Francisco | USD | 1 YEAR | 257000.0 | 344000.0 |
| Hardware Tools Engineer | Hardware | San Francisco | USD | 1 YEAR | 225000.0 | 445000.0 |
| Host Systems Software Engineer | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Mechanical Engineer, Hardware Systems | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 455000.0 |
| Networking Operating System Firmware Engineer | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Physical Design Engineer | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Product Manufacturing Engineer - PCBA | Hardware | San Francisco | USD | 1 YEAR | 207000.0 | 365000.0 |
| RTL Design Engineer – Interconnect & Network Datapath | Hardware | San Francisco | USD | 1 YEAR | 225000.0 | 445000.0 |
| Rack Power Engineer | Hardware | San Francisco | USD | 1 YEAR | 287000.0 | 485000.0 |
| Signal Integrity Engineer | Hardware | San Francisco | USD | 1 YEAR | 225000.0 | 445000.0 |
| Software Engineer, AI accelerator Runtime | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, DevOps | Hardware | San Francisco | USD | 1 YEAR | 318000.0 | 485000.0 |
| Software Engineer, GPT Infrastructure | Hardware | San Francisco | USD | 1 YEAR | 293000.0 | 385000.0 |
| Software Engineer, Kernel Performance & AI Tooling | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Manufacturing Infrastructure | Hardware | San Francisco | USD | 1 YEAR | 310000.0 | 460000.0 |
| Software Engineer, Model Runtime | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Silicon Design Methodology | Hardware | San Francisco | USD | 1 YEAR | 225000.0 | 380000.0 |
| Supply Chain Operations Program Manager, AI Infrastructure | Hardware | San Francisco | USD | 1 YEAR | 177000.0 | 285000.0 |
| Supply Chain Program Manager (SCPM) - AI Infrastructure | Hardware | San Francisco | USD | 1 YEAR | 226000.0 | 285000.0 |
| Systems Software Engineer, Management Plane | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Systems Software Engineer, Security, First Party Hardware | Hardware | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Systems Software Engineer, Silicon Bringup | Hardware | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Tech Lead, Deployment & Operations — Custom Infrastructure | Hardware | San Francisco | USD | 1 YEAR | 342000.0 | 445000.0 |
| Wireless Regulatory Engineer - SAR | Hardware Engineering | Mountain View | USD | 1 YEAR | 318000.0 | 423000.0 |
| Program Manager, Human Data | Human Data | San Francisco | USD | 1 YEAR | 207000.0 | 230000.0 |
| Research Program Manager – Adversarial Model Research | Human Data | San Francisco | USD | 1 YEAR | 239000.0 | 328000.0 |
| Software Engineer, Research - Human Data | Human Data | San Francisco | USD | 1 YEAR | 295000.0 | 385000.0 |
| People Research Scientist | Human Resources | San Francisco | USD | 1 YEAR | 198000.0 | 220000.0 |
| Head of Employee Tech & Experience (ETX) | IT | San Francisco | USD | 1 YEAR | 313000.0 | 347000.0 |
| IT Audiovisual Operations Engineer | IT | San Francisco | USD | 1 YEAR | 187000.0 | 207000.0 |
| IT Support Specialist | IT | Seattle | USD | 1 HOUR | 60.58 | 108.17 |
| ITAV Deployment Engineer | IT | San Francisco | USD | 1 YEAR | 187000.0 | 207000.0 |
| ITAV Event Technical Producer | IT | San Francisco | USD | 1 YEAR | 240000.0 | 266000.0 |
| Senior Staff Software Engineer, Identity Infrastructure Engineering | IT | San Francisco | USD | 1 YEAR | 347000.0 | 510000.0 |
| Software Engineer, Inference - Multi Modal | Inference | San Francisco | USD | 1 YEAR | 295000.0 | 555000.0 |
| Software Engineer, Inference - Performance Optimization | Inference | San Francisco | USD | 1 YEAR | 266000.0 | 500000.0 |
| Software Engineer, Model Inference | Inference | San Francisco | USD | 1 YEAR | 266000.0 | 500000.0 |
| Abuse Investigator - Scams & Fraud | Intelligence & Investigations | US - Remote | USD | 1 YEAR | 158400.0 | 320000.0 |
| Child Safety Enforcement Specialist | Intelligence & Investigations | San Francisco | USD | 1 YEAR | 158400.0 | 220000.0 |
| Full Stack Engineer, Intelligence Systems | Intelligence & Investigations | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Fullstack Software Engineer, Child Safety Tools & Systems | Intelligence & Investigations | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Red Team Specialist - Cyber | Intelligence & Investigations | San Francisco | USD | 1 YEAR | 198000.0 | 320000.0 |
| Software Engineer, Accelerators | Kernels | San Francisco | USD | 1 YEAR | 295000.0 | 380000.0 |
| Associate General Counsel, Commercial – Infrastructure | Legal | San Francisco | USD | 1 YEAR | 381000.0 | 423000.0 |
| Counsel, Commercial | Legal | San Francisco | USD | 1 YEAR | 252000.0 | 280000.0 |
| Legal Contract Manager, Public Sector | Legal | Washington, DC | USD | 1 YEAR | 216000.0 | 240000.0 |
| Senior Counsel, AI Product (Enterprise/API) | Legal | San Francisco | USD | 1 YEAR | 330000.0 | 366000.0 |
| Senior Counsel, Commercial (Infrastructure) | Legal | San Francisco | USD | 1 YEAR | 330000.0 | 366000.0 |
| Senior Counsel, Corporate (M&A) | Legal | San Francisco | USD | 1 YEAR | 280000.0 | 350000.0 |
| Senior Counsel, Litigation & Regulatory | Legal | San Francisco | USD | 1 YEAR | 330000.0 | 366000.0 |
| Senior Product Counsel | Legal | San Francisco | USD | 1 YEAR | 330000.0 | 366000.0 |
| Engineering Manager, Rosalind Workbench | Life Sciences | San Francisco | USD | 1 YEAR | 401000.0 | 536000.0 |
| Software Engineer, Life Sciences | Life Sciences | San Francisco | USD | 1 YEAR | 347000.0 | 450000.0 |
| Education Content Marketing Lead | Marketing | San Francisco | USD | 1 YEAR | 333000.0 | 370000.0 |
| Enterprise Field Marketer | Marketing | San Francisco | USD | 1 YEAR | 227000.0 | 252000.0 |
| Executive Programs Lead, Americas | Marketing | San Francisco | USD | 1 YEAR | 287000.0 | 318000.0 |
| Global Head of Events | Marketing | San Francisco | USD | 1 YEAR | 361000.0 | 401000.0 |
| Growth Marketing Manager - Web & Organic, SMB Ads | Marketing | San Francisco | USD | 1 YEAR | 198000.0 | 219000.0 |
| Growth Marketing Manager, SMB Ads | Marketing | San Francisco | USD | 1 YEAR | 198000.0 | 219000.0 |
| Industry Product Marketing Manager | Marketing | San Francisco | USD | 1 YEAR | 221000.0 | 245000.0 |
| Integrated Marketing Lead, Brand & Policy | Marketing | San Francisco | USD | 1 YEAR | 287000.0 | 318000.0 |
| Integrated Marketing Manager, AI Impact | Marketing | San Francisco | USD | 1 YEAR | 287000.0 | 318000.0 |
| Integrated Marketing Manager, Hardware | Marketing | San Francisco | USD | 1 YEAR | 225000.0 | 250000.0 |
| Integrated Marketing Manager, Product & Model Launches | Marketing | San Francisco | USD | 1 YEAR | 287000.0 | 318000.0 |
| Lead, Ads Prospecting & Customer Intelligence | Marketing | San Francisco | USD | 1 YEAR | 287000.0 | 318000.0 |
| Lifecycle Marketing Manager, SMB Ads | Marketing | San Francisco | USD | 1 YEAR | 227000.0 | 252000.0 |
| Marketing Scientist | Marketing | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Partner Marketing Manager, Ads | Marketing | San Francisco | USD | 1 YEAR | 227000.0 | 252000.0 |
| Partner Marketing Manager, Technology Partners & ISVs | Marketing | San Francisco | USD | 1 YEAR | 287000.0 | 318000.0 |
| Product Communications Lead, Business | Marketing | San Francisco | USD | 1 YEAR | 297000.0 | 330000.0 |
| Product Marketing Lead, API Models & Research | Marketing | San Francisco | USD | 1 YEAR | 374000.0 | 415000.0 |
| Product Marketing Lead, ChatGPT Work | Marketing | San Francisco | USD | 1 YEAR | 284000.0 | 315000.0 |
| Product Marketing Manager, Advertising | Marketing | San Francisco | USD | 1 YEAR | 225000.0 | 250000.0 |
| Product Marketing Manager, Cybersecurity | Marketing | San Francisco | USD | 1 YEAR | 221000.0 | 245000.0 |
| Product Marketing Manager, IT Admin and Governance | Marketing | San Francisco | USD | 1 YEAR | 221000.0 | 245000.0 |
| SMB Innovation Sales & Strategy Lead | Marketing | San Francisco | USD | 1 YEAR | 227000.0 | 252000.0 |
| Safety Transparency Editor, Safety Systems | Marketing | San Francisco | USD | 1 YEAR | 220000.0 | 245000.0 |
| Scaled Programs Lead, SMB Ads | Marketing | San Francisco | USD | 1 YEAR | 287000.0 | 318000.0 |
| Senior Web Experience Strategist | Marketing | San Francisco | USD | 1 YEAR | 287000.0 | 318000.0 |
| Senior Webinar & Digital Events Strategist | Marketing | San Francisco | USD | 1 YEAR | 266000.0 | 295000.0 |
| Startup Content Marketing Manager | Marketing | San Francisco | USD | 1 YEAR | 198000.0 | 219000.0 |
| Model Policy Manager, Agentic Safety | Model Policy | San Francisco | USD | 1 YEAR | 207000.0 | 335000.0 |
| Model Policy Manager, Multimodal Safety | Model Policy | San Francisco | USD | 1 YEAR | 266000.0 | 335000.0 |
| Model Policy Manager, National Security | Model Policy | San Francisco | USD | 1 YEAR | 207000.0 | 335000.0 |
| Applied AI Architect, Government | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 234000.0 | 335000.0 |
| Applied AI Engineer, Cyber, Government | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 211000.0 | 302000.0 |
| Applied AI Engineer, Government | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 211000.0 | 302000.0 |
| Capture Manager, OpenAI for Government | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 221000.0 | 295000.0 |
| Cyber Enablement Lead, Gov | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 207000.0 | 230000.0 |
| Enablement Lead, Government | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 207000.0 | 295000.0 |
| Federal Account Director, National Security | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 261000.0 | 335000.0 |
| Forward Deployed Engineer, Gov | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 145800.0 | 280000.0 |
| Partnerships Operations Lead, OAI for Government | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 221000.0 | 266000.0 |
| Program Manager, Government Trusted Access | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 162000.0 | 240000.0 |
| Strategic Delivery Lead, Cyber | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 266000.0 | 370000.0 |
| Strategic Delivery Lead, Department of Energy & Science | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 266000.0 | 370000.0 |
| Strategy and Operations, OpenAI for Government | OpenAI for Gov | Washington, DC | USD | 1 YEAR | 221000.0 | 258000.0 |
| Head of Marketplace | Partnerships | New York City | USD | 1 YEAR | 400000.0 | 445000.0 |
| Partner Director, HCL, Wipro & Cognizant | Partnerships | San Francisco | USD | 1 YEAR | 380000.0 | 420000.0 |
| Partner Director, McKinsey Alliance | Partnerships | San Francisco | USD | 1 YEAR | 380000.0 | 420000.0 |
| Partner Director, PwC | Partnerships | San Francisco | USD | 1 YEAR | 380000.0 | 420000.0 |
| Workday Engineer | People | San Francisco | USD | 1 YEAR | 272000.0 | 302000.0 |
| Software Engineer, Full Stack (People Innovation) | People Innovation Labs | US - Remote | USD | 1 YEAR | 153000.0 | 385000.0 |
| People Research Data Scientist, AI Fairness & Bias | People Systems & Operations | San Francisco | USD | 1 YEAR | 198000.0 | 220000.0 |
| People Technology Analyst, Workday PATT & Benefits | People Systems & Operations | San Francisco | USD | 1 YEAR | 187000.0 | 266000.0 |
| Research Engineer / Research Scientist - Personal AGI, Memory | Post-training | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Research Engineer / Research Scientist - Personal AGI, Personalization | Post-training | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Research Engineer / Research Scientist, Health | Post-training | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Research Engineer / Research Scientist- Personal AGI (Post Training) | Post-training | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Research Engineer/Research Scientist - Personal AGI, North Stars | Post-training | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Research Engineer/Research Scientist- Personal AGI, Model Experience | Post-training | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Product Design Lead, Growth - Codex | Product Design | San Francisco | USD | 1 YEAR | 347000.0 | 405000.0 |
| Product Designer, Accessibility | Product Design | San Francisco | USD | 1 YEAR | 245000.0 | 310000.0 |
| Product Designer, Codex | Product Design | San Francisco | USD | 1 YEAR | 245000.0 | 310000.0 |
| Product Designer, Consumer Verticals | Product Design | San Francisco | USD | 1 YEAR | 245000.0 | 310000.0 |
| Product Designer, Engineering Acceleration | Product Design | Seattle | USD | 1 YEAR | 245000.0 | 310000.0 |
| Product Designer, Identity and Safety | Product Design | San Francisco | USD | 1 YEAR | 245000.0 | 310000.0 |
| Product Designer, Payments | Product Design | San Francisco | USD | 1 YEAR | 245000.0 | 310000.0 |
| Product Designer, Youth | Product Design | San Francisco | USD | 1 YEAR | 245000.0 | 310000.0 |
| Product Manager, API Agents | Product Management | San Francisco | USD | 1 YEAR | 293000.0 | 325000.0 |
| Product Manager, API Infrastructure | Product Management | San Francisco | USD | 1 YEAR | 325000.0 | 347000.0 |
| Product Manager, Core Models | Product Management | San Francisco | USD | 1 YEAR | 347000.0 | 490000.0 |
| Product Manager, Enterprise Identity | Product Management | San Francisco | USD | 1 YEAR | 347000.0 | 490000.0 |
| Product Manager, Financial Engineering | Product Management | San Francisco | USD | 1 YEAR | 293000.0 | 325000.0 |
| Product Manager, Financial Services | Product Management | San Francisco | USD | 1 YEAR | 401000.0 | 530000.0 |
| Product Manager, Multimodal Safety | Product Management | San Francisco | USD | 1 YEAR | 293000.0 | 325000.0 |
| Product Manager, Sensitive Deployments | Product Management | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Product Manager, Youth | Product Management | San Francisco | USD | 1 YEAR | 293000.0 | 385000.0 |
| Rosalind Life Sciences Product Manager | Product Management | San Francisco | USD | 1 YEAR | 347000.0 | 468000.0 |
| Platform Product Partnerships Lead | Product Partnerships | San Francisco | USD | 1 YEAR | 266000.0 | 370000.0 |
| Research Lead, Policy Communications | Product Policy | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Senior Product Policy Lead, Regulation | Product Policy | San Francisco | USD | 1 YEAR | 302000.0 | 335000.0 |
| Research Engineer/Research Scientist, RL/Reasoning | Reasoning | San Francisco | USD | 1 YEAR | 295000.0 | 445000.0 |
| Recruiter, AI/ML Research | Recruiting | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Recruiting Coordinator - Contract | Recruiting | San Francisco | USD | 1 HOUR | 57.0 | 70.0 |
| Senior Technical Recruiter, Engineering Leadership | Recruiting | US - Remote | USD | 1 YEAR | 172000.0 | 295000.0 |
| Senior Technical Sourcer, Applications Engineering | Recruiting | San Francisco | USD | 1 YEAR | 172000.0 | 240000.0 |
| Technical Recruiter | Recruiting | San Francisco | USD | 1 YEAR | 172000.0 | 240000.0 |
| Technical Sourcer, Research SWE | Recruiting | San Francisco | USD | 1 YEAR | 136800.0 | 240000.0 |
| AI Infrastructure Engineer, pAGI | Research | San Francisco | USD | 1 YEAR | 266000.0 | 500000.0 |
| Machine Learning Engineer, Multimodal Perception and Authentication | Research | San Francisco | USD | 1 YEAR | 342000.0 | 399000.0 |
| Research Engineer | Research | San Francisco | USD | 1 YEAR | 250000.0 | 445000.0 |
| Research Engineer / Research Scientist / AI Systems Engineer, RSI | Research | San Francisco | USD | 1 YEAR | 295000.0 | 445000.0 |
| Research Engineer, Codex | Research | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Research Scientist | Research | San Francisco | USD | 1 YEAR | 250000.0 | 445000.0 |
| Researcher, Synthetic RL | Research | San Francisco | USD | 1 YEAR | 295000.0 | 445000.0 |
| Senior Software Engineer - Research Platform, Consumer Devices | Research | San Francisco | USD | 1 YEAR | 293000.0 | 325000.0 |
| Research Program Manager | Research Program Management | San Francisco | USD | 1 YEAR | 239000.0 | 328000.0 |
| Research Program Manager, Data Acquisition | Research Program Management | San Francisco | USD | 1 YEAR | 239000.0 | 328000.0 |
| Research Program Manager, Governance | Research Program Management | San Francisco | USD | 1 YEAR | 239000.0 | 328000.0 |
| Research Program Manager, Human Data Campaigns | Research Program Management | San Francisco | USD | 1 YEAR | 239000.0 | 328000.0 |
| Actuator Design Engineer | Robotics | San Francisco | USD | 1 YEAR | 225000.0 | 423000.0 |
| Actuator Gear Design Engineer | Robotics | San Francisco | USD | 1 YEAR | 225000.0 | 423000.0 |
| Control Systems Software Engineer, Robotics | Robotics | San Francisco | USD | 1 YEAR | 380000.0 | 460000.0 |
| Electrical Engineer, Actuator Test Infrastructure | Robotics | San Francisco | USD | 1 YEAR | 225000.0 | 318000.0 |
| Electrical Engineer, Robotics | Robotics | San Francisco | USD | 1 YEAR | 287000.0 | 423000.0 |
| Engineering Technician, Actuators | Robotics | San Francisco | USD | 1 YEAR | 225000.0 | 318000.0 |
| Field Engineer | Robotics | San Francisco | USD | 1 YEAR | 225000.0 | 318000.0 |
| Inference Engineer, Robotics | Robotics | San Francisco | USD | 1 YEAR | 380000.0 | 380000.0 |
| Lead Safety Engineer, Robotics | Robotics | San Francisco | USD | 1 YEAR | 381000.0 | 423000.0 |
| Manufacturing Engineer, Motors & Actuators | Robotics | San Francisco | USD | 1 YEAR | 225000.0 | 318000.0 |
| Mechanical Design Engineer, Motor Design & Prototyping | Robotics | San Francisco | USD | 1 YEAR | 225000.0 | 318000.0 |
| Mechanical Engineer, Dynamometer and Actuator Testing Infrastructure | Robotics | San Francisco | USD | 1 YEAR | 225000.0 | 318000.0 |
| PCB Layout Engineer, Robotics | Robotics | San Francisco | USD | 1 YEAR | 318000.0 | 485000.0 |
| Prototyping Lab Technician, Robotics | Robotics | San Francisco | USD | 1 YEAR | 225000.0 | 295000.0 |
| Robotics Software Engineer | Robotics | San Francisco | USD | 1 YEAR | 255000.0 | 325000.0 |
| Software Engineer, Distributed Data Systems - Robotics | Robotics | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, ML Systems & Training Architecture | Robotics | San Francisco | USD | 1 YEAR | 295000.0 | 380000.0 |
| Technical Commodity Manager - Robotics | Robotics | San Francisco | USD | 1 YEAR | 157000.0 | 196000.0 |
| Technical Program Manager, Actuators | Robotics | San Francisco | USD | 1 YEAR | 207000.0 | 285000.0 |
| Technical Program Manager, Robotics Facilities | Robotics | San Francisco | USD | 1 YEAR | 207000.0 | 285000.0 |
| Software Engineer, Productivity - Inference Runtime | Runtime | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, Productivity - Model Performance | Runtime | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, Productivity - Networking | Runtime | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Technical Lead Manager - Training Runtime, Data(set) Movement | Runtime | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Training - Runtime Foundations Engineer | Runtime | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Training Performance Engineer | Runtime | San Francisco | USD | 1 YEAR | 295000.0 | 500000.0 |
| Training: ML Framework Engineer | Runtime | San Francisco | USD | 1 YEAR | 295000.0 | 500000.0 |
| Research Program Manager, Frontier Assurance | Safety Systems | San Francisco | USD | 1 YEAR | 239000.0 | 328000.0 |
| Researcher, Agent Safety, Oversight and System Mitigations | Safety Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Researcher, Agent Safety, Training and Evaluations | Safety Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Researcher, Frontier Cybersecurity Risks | Safety Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Researcher, Frontier Risk Mitigations | Safety Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Researcher, Interpretability | Safety Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Researcher, Multimodal Safety | Safety Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Researcher, Recursive Self-Improvement Safety | Safety Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Researcher, Robustness & Safety Training | Safety Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Researcher, Safety Oversight | Safety Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Researcher, Safety Training, National Security | Safety Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Software Engineer, AI Safety | Safety Systems | San Francisco | USD | 1 YEAR | 207000.0 | 385000.0 |
| Software Engineer, Safety Engineering | Safety Systems | San Francisco | USD | 1 YEAR | 207000.0 | 385000.0 |
| AWS Specialist Seller, Strategic Pursuits | Sales | San Francisco | USD | 1 YEAR | 302000.0 | 335000.0 |
| Account Director, Commercial | Sales | New York City | USD | 1 YEAR | 198000.0 | 220000.0 |
| Account Director, Digital Native Enterprise | Sales | San Francisco | USD | 1 YEAR | 234900.0 | 290000.0 |
| Account Director, Digital Native Large Enterprise | Sales | San Francisco | USD | 1 YEAR | 176000.0 | 350000.0 |
| Account Director, Digital Native New Business | Sales | San Francisco | USD | 1 YEAR | 189000.0 | 290000.0 |
| Account Director, Digital Natives Growth | Sales | San Francisco | USD | 1 YEAR | 189000.0 | 220500.0 |
| Account Director, Healthcare | Sales | San Francisco | USD | 1 YEAR | 189000.0 | 240000.0 |
| Account Director, Higher Education | Sales | San Francisco | USD | 1 YEAR | 305000.0 | 352000.0 |
| Account Director, Insurance | Sales | New York City | USD | 1 YEAR | 189000.0 | 240000.0 |
| Account Director, Large Enterprise | Sales | San Francisco | USD | 1 YEAR | 189000.0 | 240000.0 |
| Account Director, Life Sciences | Sales | San Francisco | USD | 1 YEAR | 189000.0 | 240000.0 |
| Account Director, Startups Expansion | Sales | San Francisco | USD | 1 YEAR | 378000.0 | 441000.0 |
| Strategic Pursuits Lead | Sales | San Francisco | USD | 1 YEAR | 302000.0 | 352000.0 |
| Data Center Design Engineer, Electrical | Scaling | San Francisco | USD | 1 YEAR | 257000.0 | 327000.0 |
| Data Center Infrastructure Architect | Scaling | San Francisco | USD | 1 YEAR | 257000.0 | 327000.0 |
| Hardware Engineer, Test | Scaling | San Francisco | USD | 1 YEAR | 177000.0 | 300000.0 |
| Product Manufacturing & Quality Engineer | Scaling | San Francisco | USD | 1 YEAR | 123000.0 | 285000.0 |
| Software Engineer, Data Infrastructure | Scaling | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Data Infrastructure - Research | Scaling | San Francisco | USD | 1 YEAR | 250000.0 | 380000.0 |
| Engineering Manager, Client Platform Engineering | Security | San Francisco | USD | 1 YEAR | 401000.0 | 445000.0 |
| Forward Deployed Security Engineer | Security | Washington, DC | USD | 1 YEAR | 266000.0 | 445000.0 |
| GRC Program Manager, Audit & Controls | Security | San Francisco | USD | 1 YEAR | 216000.0 | 252000.0 |
| GRC Technical Program Manager, Product Lifecycle Assurance | Security | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| IT Software Architect, SaaS Enablement and Governance | Security | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Network Engineer | Security | San Francisco | USD | 1 YEAR | 347000.0 | 510000.0 |
| Principal Security Engineer, Infrastructure Security | Security | US - Remote | USD | 1 YEAR | 401000.0 | 510000.0 |
| Principal Software Engineer, Infrastructure Security | Security | US - Remote | USD | 1 YEAR | 401000.0 | 510000.0 |
| Research Engineer, Privacy | Security | San Francisco | USD | 1 YEAR | 0.0 | 500000.0 |
| Security Engineer, Agent Security | Security | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Security Engineer, Application Security | Security | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Security Engineer, Application Security | Security | Seattle | USD | 1 YEAR | 266000.0 | 445000.0 |
| Security Engineer, Application Security | Security | New York City | USD | 1 YEAR | 266000.0 | 445000.0 |
| Security Engineer, Detection and Response | Security | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Security Engineer, Infrastructure Security | Security | US - Remote | USD | 1 YEAR | 266000.0 | 445000.0 |
| Security Program Manager | Security | US - Remote | USD | 1 YEAR | 129600.0 | 310000.0 |
| Senior Technical Program Manager - Security | Security | US - Remote | USD | 1 YEAR | 165400.0 | 285000.0 |
| Software Engineer, Host Assurance | Security | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Infrastructure Security | Security | US - Remote | USD | 1 YEAR | 266000.0 | 445000.0 |
| Software Engineer, Privacy Engineering | Security | San Francisco | USD | 1 YEAR | 230000.0 | 325000.0 |
| Software Engineer, Security Observability | Security | San Francisco | USD | 1 YEAR | 293000.0 | 325000.0 |
| Staff Security Reliability Engineer | Security | San Francisco | USD | 1 YEAR | 347000.0 | 510000.0 |
| Technical Threat Investigator, Threat Intel Engineering | Security | San Francisco | USD | 1 YEAR | 347000.0 | 510000.0 |
| Vendor Security Technical Program Manager | Security | US - Remote | USD | 1 YEAR | 231300.0 | 256500.0 |
| Android Systems Engineer, Consumer Devices | Software | San Francisco | USD | 1 YEAR | 266000.0 | 385000.0 |
| Backend Engineer, Consumer Devices | Software | San Francisco | USD | 1 YEAR | 293000.0 | 325000.0 |
| Camera Software Engineer, Consumer Devices | Software | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Connectivity Software Engineer, Consumer Devices | Software | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Firmware Engineer, RTOS, Consumer Devices | Software | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Lab Operations Engineer, Systems Integration \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 230000.0 | 290000.0 |
| Operating Systems Engineer \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 230000.0 | 342000.0 |
| Operating Systems Engineer, Connectivity & Networking \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Operating Systems Engineer, Linux Kernel \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Operating Systems Engineer, On-Device Inference \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Release Engineer \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 207000.0 | 365000.0 |
| Software Engineer, HSM Infrastructure Security, Consumer Devices | Software | San Francisco | USD | 1 YEAR | 347000.0 | 445000.0 |
| Software Engineer, Private Computing | Software | San Francisco | USD | 1 YEAR | 230000.0 | 385000.0 |
| Software Engineer, Quality & Developer Tools \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 207000.0 | 365000.0 |
| Software Security Architect, Operating Systems \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 268000.0 | 342000.0 |
| Staff PLM & Engineering Applications Engineer, Consumer Devices | Software | San Francisco | USD | 1 YEAR | 257000.0 | 285000.0 |
| System Performance Engineer, Consumer Devices | Software | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| System Software Engineer, Consumer Devices | Software | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Systems Integration Engineer, Build Systems \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 207000.0 | 365000.0 |
| Systems Integration Manager \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 290000.0 | 365000.0 |
| Systems Test Engineer, End-to-End Validation \| Consumer Devices | Software | San Francisco | USD | 1 YEAR | 230000.0 | 290000.0 |
| Business Lead, Special Situations | Special Situations | San Francisco | USD | 1 YEAR | 333000.0 | 370000.0 |
| Deal Lead, Special Situations | Special Situations | San Francisco | USD | 1 YEAR | 333000.0 | 401000.0 |
| Physical Engineering Business Lead (Special Situations) | Special Situations | San Francisco | USD | 1 YEAR | 333000.0 | 370000.0 |
| Director, Compute & Infrastructure FP&A | Strategic Finance | San Francisco | USD | 1 YEAR | 293000.0 | 385000.0 |
| Finance Manager - Hardware Consolidations | Strategic Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Hardware Finance Manager | Strategic Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Head of Finance - Data Centers | Strategic Finance | San Francisco | USD | 1 YEAR | 347000.0 | 385000.0 |
| Pricing Strategist | Strategic Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Strategic Finance Lead, Corporate Finance and Capital Strategy | Strategic Finance | San Francisco | USD | 1 YEAR | 293000.0 | 325000.0 |
| Strategic Finance, Ads | Strategic Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Strategic Finance, B2B Partnerships | Strategic Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Strategic Finance, B2B Product | Strategic Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Strategic Finance, Compute | Strategic Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Strategic Finance, International & Marketing | Strategic Finance | San Francisco | USD | 1 YEAR | 234000.0 | 325000.0 |
| Strategic Finance, Partnerships | Strategic Finance | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| GTM Strategy & Operations, Professional Services | Strategy & Operations | San Francisco | USD | 1 YEAR | 293000.0 | 325000.0 |
| Program Manager, Business Marketing | Strategy & Operations | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Software Engineer, Compute Foundations | Supercomputing | San Francisco | USD | 1 YEAR | 255000.0 | 490000.0 |
| Software Engineer, Compute Foundations Systems | Supercomputing | San Francisco | USD | 1 YEAR | 230000.0 | 490000.0 |
| Engineering Manager, Cooperative Systems | Support Automation | San Francisco | USD | 1 YEAR | 401000.0 | 445000.0 |
| Engineering Manager, Cooperative Systems | Support Automation | Seattle | USD | 1 YEAR | 400000.0 | 445000.0 |
| AI Support Engineer - San Francisco | Support Delivery | San Francisco | USD | 1 YEAR | 180000.0 | 260000.0 |
| AI Support Engineer - San Francisco (Weekend Shift) | Support Delivery | San Francisco | USD | 1 YEAR | 180000.0 | 260000.0 |
| AI Support Engineer - Toronto | Support Delivery | Ontario - Remote | CAD | 1 YEAR | 200000.0 | 290000.0 |
| AI Support Engineer, Biosciences - San Francisco | Support Delivery | San Francisco | USD | 1 YEAR | 180000.0 | 260000.0 |
| AI Support Engineer, Government - San Francisco, CA | Support Delivery | San Francisco | USD | 1 YEAR | 180000.0 | 260000.0 |
| AI Support Engineer, Government - Washington, D.C. | Support Delivery | Washington, DC | USD | 1 YEAR | 162000.0 | 234000.0 |
| Dedicated Support Engineer - San Francisco | Support Delivery | San Francisco | USD | 1 YEAR | 180000.0 | 260000.0 |
| Dedicated Support Engineering Lead | Support Delivery | San Francisco | USD | 1 YEAR | 284000.0 | 385000.0 |
| Senior Support Engineer - San Francisco | Support Delivery | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Senior Support Engineer - Toronto | Support Delivery | Ontario - Remote | CAD | 1 YEAR | 261000.0 | 290000.0 |
| Support Delivery Lead | Support Delivery | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Support Delivery Lead | Support Delivery | San Francisco | USD | 1 YEAR | 284000.0 | 315000.0 |
| Support Delivery Lead - Toronto | Support Delivery | Ontario - Remote | CAD | 1 YEAR | 297000.0 | 330000.0 |
| Support Delivery Lead, Ads | Support Delivery | San Francisco | USD | 1 YEAR | 284000.0 | 315000.0 |
| Support Delivery Lead, Government | Support Delivery | Washington, DC | USD | 1 YEAR | 284000.0 | 315000.0 |
| Support Program Manager, Support Delivery | Support Delivery | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Technical Program Manager, Support Delivery | Support Delivery | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Product Engagement Manager, User Operations | Support Operations | San Francisco | USD | 1 YEAR | 279000.0 | 310000.0 |
| Product Engagement Specialist, User Operations | Support Operations | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Strategy & Operations Programs, Support | Support Operations | San Francisco | USD | 1 YEAR | 216000.0 | 310000.0 |
| Support Operations Lead | Support Operations | San Francisco | USD | 1 YEAR | 279000.0 | 310000.0 |
| Support Program Manager, Partnerships | Support Operations | San Francisco | USD | 1 YEAR | 216000.0 | 310000.0 |
| Support Vendor Manager | Support Operations | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Technical Systems Program Manager, User Operations | Support Operations | San Francisco | USD | 1 YEAR | 216000.0 | 240000.0 |
| Software Engineer, Collective Communication | Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Software Engineer, Platform Systems | Systems | San Francisco | USD | 1 YEAR | 380000.0 | 500000.0 |
| Technical Program Manager, AI Safety & Safeguards | Technical Program Management | San Francisco | USD | 1 YEAR | 207000.0 | 445000.0 |
| Technical Program Manager, Applied API & Product | Technical Program Management | San Francisco | USD | 1 YEAR | 207000.0 | 445000.0 |
| Technical Program Manager, Applied Infrastructure | Technical Program Management | San Francisco | USD | 1 YEAR | 257000.0 | 445000.0 |
| Technical Program Manager, Cloud AI Partnerships | Technical Program Management | San Francisco | USD | 1 YEAR | 207000.0 | 445000.0 |
| Technical Program Manager, Compute Infrastructure | Technical Program Management | San Francisco | USD | 1 YEAR | 257000.0 | 335000.0 |
| Technical Program Manager, Developer Velocity | Technical Program Management | San Francisco | USD | 1 YEAR | 207000.0 | 445000.0 |
| Technical Program Manager, Enterprise | Technical Program Management | San Francisco | USD | 1 YEAR | 207000.0 | 445000.0 |
| Technical Program Manager, Model Deployment & Capacity | Technical Program Management | San Francisco | USD | 1 YEAR | 207000.0 | 445000.0 |
| Technical Program Manager, Multimodal | Technical Program Management | San Francisco | USD | 1 YEAR | 207000.0 | 445000.0 |
| Technical Program Manager, Partnerships | Technical Program Management | San Francisco | USD | 1 YEAR | 207000.0 | 230000.0 |
| Technical Program Manager, People Innovation Labs | Technical Program Management | San Francisco | USD | 1 YEAR | 257000.0 | 335000.0 |
| Technical Program Manager, Storage & Data Infrastructure | Technical Program Management | San Francisco | USD | 1 YEAR | 257000.0 | 445000.0 |
| Technical Program Manager, Strategic Initiatives | Technical Program Management | San Francisco | USD | 1 YEAR | 257000.0 | 445000.0 |
| Applied AI Architect | Technical Success | San Francisco | USD | 1 YEAR | 156600.0 | 276000.0 |
| Applied AI Architect | Technical Success | New York City | USD | 1 YEAR | 156600.0 | 276000.0 |
| Applied AI Architect, Digital Natives | Technical Success | San Francisco | USD | 1 YEAR | 221000.0 | 278000.0 |
| Applied AI Architect, Digital Natives (Strategics) | Technical Success | San Francisco | USD | 1 YEAR | 218000.0 | 278000.0 |
| Applied AI Architect, Enterprise | Technical Success | San Francisco | USD | 1 YEAR | 221000.0 | 276000.0 |
| Applied AI Architect, Healthcare & Life Sciences | Technical Success | San Francisco | USD | 1 YEAR | 221000.0 | 278000.0 |
| Applied AI Architect, Retail | Technical Success | San Francisco | USD | 1 YEAR | 217000.0 | 276000.0 |
| Applied AI Delivery Lead | Technical Success | San Francisco | USD | 1 YEAR | 234000.0 | 335000.0 |
| Applied AI Engineer, API Platform, Digital Natives | Technical Success | New York City | USD | 1 YEAR | 251000.0 | 278000.0 |
| Applied AI Engineer, API Platform, Digital Natives | Technical Success | San Francisco | USD | 1 YEAR | 251000.0 | 278000.0 |
| Applied AI Engineer, Agent Enablement | Technical Success | San Francisco | USD | 1 YEAR | 197000.0 | 280000.0 |
| Applied AI Engineer, Codex | Technical Success | San Francisco | USD | 1 YEAR | 211000.0 | 278000.0 |
| Applied AI Engineer, Cyber | Technical Success | San Francisco | USD | 1 YEAR | 211000.0 | 292000.0 |
| Applied AI Engineer, Enterprise | Technical Success | San Francisco | USD | 1 YEAR | 251000.0 | 278000.0 |
| Applied AI Engineer, Plugins | Technical Success | San Francisco | USD | 1 YEAR | 197000.0 | 280000.0 |
| Applied AI Engineer, Startups | Technical Success | San Francisco | USD | 1 YEAR | 211000.0 | 278000.0 |
| Demo Experience Engineer, Technical Success | Technical Success | San Francisco | USD | 1 YEAR | 234000.0 | 260000.0 |
| Early Access Deployment Engineer | Technical Success | San Francisco | USD | 1 YEAR | 250000.0 | 330000.0 |
| Manager, Applied AI Architect | Technical Success | San Francisco | USD | 1 YEAR | 280000.0 | 300000.0 |
| Manager, Applied AI Engineering (Codex) | Technical Success | San Francisco | USD | 1 YEAR | 302000.0 | 335000.0 |
| Manager, Applied AI Engineering (Digital Natives) | Technical Success | San Francisco | USD | 1 YEAR | 302000.0 | 335000.0 |
| Manager, Applied AI Engineering (Enterprise) | Technical Success | New York City | USD | 1 YEAR | 251000.0 | 335000.0 |
| Manager, Applied AI Engineering (Startups) | Technical Success | San Francisco | USD | 1 YEAR | 302000.0 | 335000.0 |
| Partner Applied AI Engineer | Technical Success | San Francisco | USD | 1 YEAR | 197000.0 | 278000.0 |
| Technical Program Manager, Global Programs — Applied AI Engineering | Technical Success | San Francisco | USD | 1 YEAR | 251000.0 | 280000.0 |
| Compensation Business Partner, GTM | Total Rewards | San Francisco | USD | 1 YEAR | 180000.0 | 260000.0 |
| Researcher, Training | Training | San Francisco | USD | 1 YEAR | 300000.0 | 600000.0 |
| Researcher, Training - London | Training | London, UK | GBP | 1 YEAR | 170000.0 | 445000.0 |
| Consumer Device Safety & Risk Operations Specialist, User Safety & Risk Operations | Trust & Safety | San Francisco | USD | 1 YEAR | 252000.0 | 335000.0 |
| Cyber Operations Lead, Critical Harm Operations | Trust & Safety | San Francisco | USD | 1 YEAR | 252000.0 | 335000.0 |
| Cyber Operations Strategist, Critical Harm Operations | Trust & Safety | Ontario - Remote | CAD | 1 YEAR | 140000.0 | 188000.0 |
| Device Safety & Risk Operations Specialist, User Safety & Risk Operations | Trust & Safety | San Francisco | USD | 1 YEAR | 252000.0 | 335000.0 |
| Regulatory Operations Analyst, User Safety & Risk Operations | Trust & Safety | San Francisco | USD | 1 YEAR | 252000.0 | 280000.0 |
| Safety Response Operations Lead | Trust & Safety | San Francisco | USD | 1 YEAR | 252000.0 | 280000.0 |
| Senior Operations Analyst, User Safety & Risk Operations | Trust & Safety | San Francisco | USD | 1 YEAR | 252000.0 | 280000.0 |
| Senior Program Manager, Consumer Device Safety Operations | Trust & Safety | San Francisco | USD | 1 YEAR | 252000.0 | 335000.0 |
| Senior Support Specialist, Ads | Trust & Safety | Ontario - Remote | CAD | 1 YEAR | 170000.0 | 188000.0 |
| Senior Support Specialist, Ads | Trust & Safety | San Francisco | USD | 1 YEAR | 189000.0 | 280000.0 |
| Trust & Safety Ads Operations Analyst, Programs | Trust & Safety | San Francisco | USD | 1 YEAR | 252000.0 | 280000.0 |
| User Safety & Risk Operations Analyst - Global Response (Weekend Shift) | Trust & Safety | San Francisco | USD | 1 YEAR | 189000.0 | 210000.0 |
| Data Scientist, Inference Capacity Optimization | Workload | San Francisco | USD | 1 YEAR | 293000.0 | 325000.0 |
| Software Engineer, Infrastructure - Analytics Platform | Workload | San Francisco | USD | 1 YEAR | 266000.0 | 445000.0 |
| Supply Chain Manager, Industrial Compute | Workload | San Francisco | USD | 1 YEAR | 205000.0 | 335000.0 |
| Technical Program Manager, Infrastructure Strategy & Delivery Operations | Workload | San Francisco | USD | 1 YEAR | 185000.0 | 285000.0 |
| Global Transportation Programs, Senior Manager | Workplace | San Francisco | USD | 1 YEAR | 203000.0 | 225000.0 |
| Senior Manager, EHS - Robotics | Workplace | San Francisco | USD | 1 YEAR | 203000.0 | 225000.0 |
| Senior Manager, Occupancy Planning & Workplace Strategy | Workplace | San Francisco | USD | 1 YEAR | 203000.0 | 225000.0 |

</details>

## 14. Data-quality summary

| current_roles | missing_description | missing_workplace_type | missing_is_remote | missing_primary_location | missing_published_at |
| --- | --- | --- | --- | --- | --- |
| 815 | 0 | 256 | 256 | 0 | 0 |

## 15. Exact SQL catalog

### current_roles

```sql
SELECT
                ashby_id, title, team, department, employment_type,
                display_location, published_at, is_listed, is_remote,
                workplace_type, career_url, job_url, apply_url,
                description_plain, present_in_html, present_in_api, source_status
            FROM roles
            WHERE present_in_api = 1
            ORDER BY team, title, ashby_id
```

### secondary_locations

```sql
SELECT ashby_id, location_index, location
            FROM api_secondary_locations
            ORDER BY ashby_id, location_index
```

### compensation_components

```sql
SELECT ashby_id, component_index, compensation_type, interval,
                   currency_code, min_value, max_value
            FROM api_compensation_components
            ORDER BY ashby_id, component_index
```

### source_status_counts

```sql
SELECT source_status, COUNT(*) AS roles
            FROM roles
            GROUP BY source_status
            ORDER BY source_status
```

### team_counts

```sql
SELECT team, COUNT(*) AS roles
            FROM roles
            WHERE present_in_api = 1
            GROUP BY team
            ORDER BY roles DESC, team
```

### primary_location_counts

```sql
SELECT COALESCE(display_location,'NULL') AS location, COUNT(*) AS roles
            FROM roles
            WHERE present_in_api = 1
            GROUP BY display_location
            ORDER BY roles DESC, location
```

### work_arrangement_counts

```sql
SELECT COALESCE(CAST(is_remote AS TEXT),'NULL') AS is_remote,
                   COALESCE(workplace_type,'NULL') AS workplace_type,
                   COUNT(*) AS roles
            FROM roles
            WHERE present_in_api = 1
            GROUP BY is_remote, workplace_type
            ORDER BY roles DESC
```

### data_quality

```sql
SELECT
                COUNT(*) AS current_roles,
                SUM(CASE WHEN description_plain IS NULL OR TRIM(description_plain)='' THEN 1 ELSE 0 END) AS missing_description,
                SUM(CASE WHEN workplace_type IS NULL THEN 1 ELSE 0 END) AS missing_workplace_type,
                SUM(CASE WHEN is_remote IS NULL THEN 1 ELSE 0 END) AS missing_is_remote,
                SUM(CASE WHEN display_location IS NULL OR TRIM(display_location)='' THEN 1 ELSE 0 END) AS missing_primary_location,
                SUM(CASE WHEN published_at IS NULL THEN 1 ELSE 0 END) AS missing_published_at
            FROM roles
            WHERE present_in_api = 1
```

## 16. What this report still does not claim

- A high evidence-overlap count does not prove qualification.
- A remote location field does not prove Utah eligibility unless the posting evidence supports it.
- Relocation assistance does not prove the employer will fund every up-front cost or allow delayed relocation.
- An experience-year mention is not automatically a hard requirement unless the qualification language says so.
- Sales-context terms are not automatic exclusions; strong sales-function evidence is separated from context.
- The deep-review pool is a bounded investigation set, not the final application list.
