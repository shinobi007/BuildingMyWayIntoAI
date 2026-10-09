# ProofLoop Role Deep Analysis Report v0.16

Generated: `2026-10-08T05:22:56.215589+00:00`  
Baseline: `C:\Users\psychoGanon\Desktop\BuilidingMyWayIntoAI\Day1\proofloop_role_analysis_report_v0_15.json`  
Database: `C:\Users\psychoGanon\Desktop\BuilidingMyWayIntoAI\Day1\proofloop_enriched.db`  
Database access: **read-only**

## Purpose

This is the second-stage role analysis. v0.15 established the 815-role landscape, location/sales/technical classifications, and the first deep-review pool. v0.16 moves from role-level signals to **qualification-by-qualification evidence mapping**. It is designed to be used *with* v0.15 when choosing the final top five; it does not choose those five automatically.

## Baseline validation

| baseline_battery | baseline_roles | database_current_roles | role_ids_exact_match | sqlite_integrity |
| --- | --- | --- | --- | --- |
| ProofLoop Role Selection Transparency Battery v0.15 | 815 | 815 | True | ok |
## Methodology guardrails

- This layer consumes the v0.15 report instead of replacing it.
- The final top five are NOT selected by this script.
- Strong sales classifications are excluded from the candidate seed.
- Non-US/jurisdiction-mismatch roles are not promoted into the decision pool.
- Qualifications are extracted only from exact line-level headings; ordinary prose containing words like requirements no longer starts a qualifications section.
- Resume programming-language entries are treated as skill claims, not proof of years of production software engineering.
- Major gap means current evidence does not establish a posted expectation; it is not a claim that the skill cannot be learned.
- Location paths preserve remote-now, remote-needs-confirmation, relocation-supported, and onsite/location-dependency as separate states.
- Decision bands are rule-based and transparent; they are not an opaque numeric fit score.

## Candidate funnel

- Baseline current roles: **815**
- Roles entering deep requirement analysis: **224**
- Decision-review pool emitted: **30**

### Decision bands

| band | roles |
| --- | --- |
| A_TOP5_REVIEW | 1 |
| B_SERIOUS_REVIEW | 48 |
| C_STRETCH_REVIEW | 122 |
| C_REQUIREMENTS_INCOMPLETE | 23 |
| D_BACKGROUND | 30 |

### Career lanes

| lane | roles |
| --- | --- |
| PRIMARY_SUPPORT_IT | 29 |
| ADJACENT_TECHNICAL | 63 |
| STRETCH_TECHNICAL | 132 |

### Location paths

| location_path | roles |
| --- | --- |
| RELOCATION_SUPPORTED | 135 |
| US_LOCATION_DEPENDENCY | 71 |
| REMOTE_NEEDS_CONFIRMATION | 10 |
| REMOTE_NOW_STRONG | 8 |

### Seniority burden

| seniority | roles |
| --- | --- |
| UNKNOWN | 113 |
| MODERATE | 26 |
| HIGH | 29 |
| LOW | 2 |
| VERY_HIGH | 54 |

## Decision-review pool

This is an ordered **manual review pool**, not a final ranking. Ordering is lexicographic and transparent: decision band → career lane → location path → fewer major/moderate gaps → lower seniority burden → more direct qualification matches.

| title | team | lane | title_alignment | location_path | workplace | relocation | office_days | sales | technical | seniority | max_years | direct_req | claimed_req | adjacent_req | major_gaps | moderate_gaps | gap_domains | salary | decision_band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Product Engagement Manager, User Operations | Support Operations | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | RELOCATION_SUPPORTED | Hybrid | YES | 3 | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | UNKNOWN |  | 3 | 0 | 0 | 1 | 0 | automation_workflows; process_improvement; product_management | USD 279000.0–310000.0 / 1 YEAR | A_TOP5_REVIEW |
| IT Support Specialist | IT | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | RELOCATION_SUPPORTED | OnSite | YES | 5 | NO_SALES_SIGNAL_FOUND | HIGH | UNKNOWN |  | 1 | 1 | 2 | 1 | 0 | audiovisual_event_technology | USD 60.58–108.17 / 1 HOUR | B_SERIOUS_REVIEW |
| Dedicated Support Engineer - San Francisco | Support Delivery | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | US_LOCATION_DEPENDENCY | Hybrid | NO |  | REVIEW_SALES_CONTEXT | HIGH | UNKNOWN |  | 5 | 0 | 0 | 1 | 1 | api_integrations; cloud_infrastructure; distributed_systems; troubleshooting_incidents | USD 180000.0–260000.0 / 1 YEAR | B_SERIOUS_REVIEW |
| ITAV Event Technical Producer | IT | PRIMARY_SUPPORT_IT | OTHER_TECHNICAL_ROLE | US_LOCATION_DEPENDENCY | OnSite | NO |  | NO_SALES_SIGNAL_FOUND | NONE_DETECTED | UNKNOWN |  | 4 | 0 | 0 | 1 | 1 | automation_workflows; production_system_ownership | USD 240000.0–266000.0 / 1 YEAR | B_SERIOUS_REVIEW |
| Security Program Manager | Security | ADJACENT_TECHNICAL | ADJACENT_PROGRAM_ROLE | REMOTE_NEEDS_CONFIRMATION | Hybrid | NO |  | NO_SALES_SIGNAL_FOUND | MEDIUM | MODERATE | 5 | 2 | 0 | 1 | 1 | 0 | mergers_acquisitions | USD 129600.0–310000.0 / 1 YEAR | B_SERIOUS_REVIEW |
| Technical Program Manager, Compute Infrastructure | Technical Program Management | ADJACENT_TECHNICAL | ADJACENT_PROGRAM_ROLE | RELOCATION_SUPPORTED |  | YES | 3 | NO_SALES_SIGNAL_FOUND | HIGH | MODERATE | 5 | 0 | 0 | 2 | 0 | 0 |  | USD 257000.0–335000.0 / 1 YEAR | B_SERIOUS_REVIEW |
| Technical Program Manager, Multimodal | Technical Program Management | ADJACENT_TECHNICAL | ADJACENT_PROGRAM_ROLE | RELOCATION_SUPPORTED |  | YES | 3 | NO_SALES_SIGNAL_FOUND | HIGH | UNKNOWN |  | 4 | 0 | 0 | 1 | 0 | ml_ai_engineering; uat_qa_bug | USD 207000.0–445000.0 / 1 YEAR | B_SERIOUS_REVIEW |
| Technical Program Manager, Developer Velocity | Technical Program Management | ADJACENT_TECHNICAL | ADJACENT_PROGRAM_ROLE | RELOCATION_SUPPORTED |  | YES | 3 | NO_SALES_SIGNAL_FOUND | MEDIUM | UNKNOWN |  | 1 | 0 | 2 | 1 | 0 | distributed_systems; technical_program_delivery; uat_qa_bug | USD 207000.0–445000.0 / 1 YEAR | B_SERIOUS_REVIEW |
| Technical Program Manager, Enterprise | Technical Program Management | ADJACENT_TECHNICAL | ADJACENT_PROGRAM_ROLE | RELOCATION_SUPPORTED |  | YES | 3 | REVIEW_SALES_CONTEXT | MEDIUM | UNKNOWN |  | 1 | 0 | 2 | 1 | 0 | api_integrations; professional_software_engineering | USD 207000.0–445000.0 / 1 YEAR | B_SERIOUS_REVIEW |
| Senior Support Specialist, Ads | Trust & Safety | ADJACENT_TECHNICAL | DIRECT_ROLE_FAMILY | US_LOCATION_DEPENDENCY | Hybrid | NO |  | REVIEW_SALES_CONTEXT | MEDIUM | HIGH | 6 | 4 | 1 | 0 | 0 | 0 |  | USD 189000.0–280000.0 / 1 YEAR | B_SERIOUS_REVIEW |
| Technical Program Manager, People Innovation Labs | Technical Program Management | ADJACENT_TECHNICAL | ADJACENT_PROGRAM_ROLE | US_LOCATION_DEPENDENCY | Hybrid | NO |  | NO_SALES_SIGNAL_FOUND | MEDIUM | HIGH | 7 | 2 | 0 | 1 | 0 | 0 |  | USD 257000.0–335000.0 / 1 YEAR | B_SERIOUS_REVIEW |
| Technical Systems Program Manager, User Operations | Support Operations | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | RELOCATION_SUPPORTED | Hybrid | YES |  | REVIEW_SALES_CONTEXT | MEDIUM | VERY_HIGH | 8 | 4 | 0 | 2 | 0 | 0 |  | USD 216000.0–240000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Support Operations Lead | Support Operations | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | RELOCATION_SUPPORTED | Hybrid | YES | 3 | REVIEW_SALES_CONTEXT | MEDIUM | VERY_HIGH | 10 | 2 | 0 | 0 | 1 | 0 | people_management | USD 279000.0–310000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Product Engagement Specialist, User Operations | Support Operations | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | RELOCATION_SUPPORTED | Hybrid | YES | 3 | NO_SALES_SIGNAL_FOUND | MEDIUM | VERY_HIGH | 8 | 2 | 0 | 0 | 1 | 1 | product_management; technical_program_delivery | USD 216000.0–240000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Support Delivery Lead | Support Delivery | PRIMARY_SUPPORT_IT | OTHER_TECHNICAL_ROLE | RELOCATION_SUPPORTED | Hybrid | YES | 3 | REVIEW_SALES_CONTEXT | MEDIUM | VERY_HIGH | 10 | 1 | 0 | 0 | 1 | 1 | professional_software_engineering; technical_support | USD 234000.0–260000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Support Delivery Lead | Support Delivery | PRIMARY_SUPPORT_IT | OTHER_TECHNICAL_ROLE | RELOCATION_SUPPORTED | Hybrid | YES | 3 | REVIEW_SALES_CONTEXT | MEDIUM | VERY_HIGH | 8 | 1 | 0 | 0 | 1 | 1 | professional_software_engineering; technical_support | USD 284000.0–315000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Senior Support Engineer - San Francisco | Support Delivery | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | RELOCATION_SUPPORTED |  | YES | 3 | NO_SALES_SIGNAL_FOUND | HIGH | VERY_HIGH | 8 | 2 | 0 | 0 | 2 | 3 | distributed_systems; threat_intelligence_ir; troubleshooting_incidents | USD 234000.0–260000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Senior Staff Software Engineer, Identity Infrastructure Engineering | IT | PRIMARY_SUPPORT_IT | SPECIALIST_ENGINEERING_STRETCH | RELOCATION_SUPPORTED | Hybrid | YES | 3 | NO_SALES_SIGNAL_FOUND | HIGH | VERY_HIGH | 10 | 1 | 0 | 0 | 3 | 1 | cloud_infrastructure; distributed_systems; identity_device_management; professional_software_engineering; python_scripting | USD 347000.0–510000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Head of Employee Tech & Experience (ETX) | IT | PRIMARY_SUPPORT_IT | OTHER_TECHNICAL_ROLE | US_LOCATION_DEPENDENCY | Hybrid | NO |  | NO_SALES_SIGNAL_FOUND | MEDIUM | UNKNOWN |  | 0 | 0 | 0 | 0 | 0 |  | USD 313000.0–347000.0 / 1 YEAR | C_STRETCH_REVIEW |
| AI Support Engineer, Biosciences - San Francisco | Support Delivery | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | US_LOCATION_DEPENDENCY | Hybrid | NO |  | NO_SALES_SIGNAL_FOUND | HIGH | VERY_HIGH | 8 | 6 | 1 | 1 | 0 | 0 |  | USD 180000.0–260000.0 / 1 YEAR | C_STRETCH_REVIEW |
| AI Support Engineer - San Francisco | Support Delivery | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | US_LOCATION_DEPENDENCY |  | NO |  | REVIEW_SALES_CONTEXT | HIGH | VERY_HIGH | 8 | 4 | 1 | 0 | 0 | 0 |  | USD 180000.0–260000.0 / 1 YEAR | C_STRETCH_REVIEW |
| AI Support Engineer - San Francisco (Weekend Shift) | Support Delivery | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | US_LOCATION_DEPENDENCY |  | NO |  | REVIEW_SALES_CONTEXT | HIGH | VERY_HIGH | 8 | 4 | 1 | 0 | 0 | 0 |  | USD 180000.0–260000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Strategy & Operations Programs, Support | Support Operations | PRIMARY_SUPPORT_IT | OTHER_TECHNICAL_ROLE | US_LOCATION_DEPENDENCY |  | NO |  | REVIEW_SALES_CONTEXT | MEDIUM | VERY_HIGH | 8 | 2 | 0 | 0 | 0 | 0 |  | USD 216000.0–310000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Support Program Manager, Partnerships | Support Operations | PRIMARY_SUPPORT_IT | ADJACENT_PROGRAM_ROLE | US_LOCATION_DEPENDENCY |  | NO |  | REVIEW_SALES_CONTEXT | MEDIUM | VERY_HIGH | 8 | 0 | 0 | 1 | 0 | 0 |  | USD 216000.0–310000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Engineering Manager, Cooperative Systems | Support Automation | PRIMARY_SUPPORT_IT | SPECIALIST_ENGINEERING_STRETCH | US_LOCATION_DEPENDENCY | Hybrid | NO |  | NO_SALES_SIGNAL_FOUND | MEDIUM | VERY_HIGH | 12 | 2 | 0 | 0 | 0 | 1 |  | USD 401000.0–445000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Engineering Manager, Cooperative Systems | Support Automation | PRIMARY_SUPPORT_IT | SPECIALIST_ENGINEERING_STRETCH | US_LOCATION_DEPENDENCY | Hybrid | NO |  | NO_SALES_SIGNAL_FOUND | MEDIUM | VERY_HIGH | 12 | 2 | 0 | 0 | 0 | 1 |  | USD 400000.0–445000.0 / 1 YEAR | C_STRETCH_REVIEW |
| IT Audiovisual Operations Engineer | IT | PRIMARY_SUPPORT_IT | OTHER_TECHNICAL_ROLE | US_LOCATION_DEPENDENCY | Hybrid | NO |  | NO_SALES_SIGNAL_FOUND | MEDIUM | MODERATE | 5 | 6 | 0 | 1 | 2 | 1 | api_integrations; audiovisual_event_technology; datacenter_facilities; hardware_electrical; troubleshooting_incidents | USD 187000.0–207000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Senior Technical Program Manager - Security | Security | ADJACENT_TECHNICAL | ADJACENT_PROGRAM_ROLE | REMOTE_NOW_STRONG | Remote | NO |  | NO_SALES_SIGNAL_FOUND | MEDIUM | MODERATE | 5 | 0 | 0 | 0 | 2 | 0 | security_engineering; technical_program_delivery | USD 165400.0–285000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Vendor Security Technical Program Manager | Security | ADJACENT_TECHNICAL | ADJACENT_PROGRAM_ROLE | REMOTE_NOW_STRONG | Remote | NO |  | NO_SALES_SIGNAL_FOUND | HIGH | UNKNOWN |  | 2 | 0 | 3 | 2 | 1 | api_integrations; identity_device_management; security_engineering; security_vendor_risk; vendor_management | USD 231300.0–256500.0 / 1 YEAR | C_STRETCH_REVIEW |
| Technical Threat Investigator, Threat Intel Engineering | Security | ADJACENT_TECHNICAL | SPECIALIST_ENGINEERING_STRETCH | REMOTE_NOW_STRONG | Remote | YES |  | NO_SALES_SIGNAL_FOUND | HIGH | UNKNOWN |  | 2 | 1 | 0 | 3 | 1 | offensive_security; threat_intelligence_ir; troubleshooting_incidents | USD 347000.0–510000.0 / 1 YEAR | C_STRETCH_REVIEW |

## Benchmark roles carried forward from v0.15

| title | team | lane | title_alignment | location_path | workplace | relocation | office_days | sales | technical | seniority | max_years | direct_req | claimed_req | adjacent_req | major_gaps | moderate_gaps | gap_domains | salary | decision_band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IT Support Specialist | IT | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | RELOCATION_SUPPORTED | OnSite | YES | 5 | NO_SALES_SIGNAL_FOUND | HIGH | UNKNOWN |  | 1 | 1 | 2 | 1 | 0 | audiovisual_event_technology | USD 60.58–108.17 / 1 HOUR | B_SERIOUS_REVIEW |
| Dedicated Support Engineer - San Francisco | Support Delivery | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | US_LOCATION_DEPENDENCY | Hybrid | NO |  | REVIEW_SALES_CONTEXT | HIGH | UNKNOWN |  | 5 | 0 | 0 | 1 | 1 | api_integrations; cloud_infrastructure; distributed_systems; troubleshooting_incidents | USD 180000.0–260000.0 / 1 YEAR | B_SERIOUS_REVIEW |
| Technical Systems Program Manager, User Operations | Support Operations | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | RELOCATION_SUPPORTED | Hybrid | YES |  | REVIEW_SALES_CONTEXT | MEDIUM | VERY_HIGH | 8 | 4 | 0 | 2 | 0 | 0 |  | USD 216000.0–240000.0 / 1 YEAR | C_STRETCH_REVIEW |
| AI Support Engineer - San Francisco | Support Delivery | PRIMARY_SUPPORT_IT | DIRECT_ROLE_FAMILY | US_LOCATION_DEPENDENCY |  | NO |  | REVIEW_SALES_CONTEXT | HIGH | VERY_HIGH | 8 | 4 | 1 | 0 | 0 | 0 |  | USD 180000.0–260000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Vendor Security Technical Program Manager | Security | ADJACENT_TECHNICAL | ADJACENT_PROGRAM_ROLE | REMOTE_NOW_STRONG | Remote | NO |  | NO_SALES_SIGNAL_FOUND | HIGH | UNKNOWN |  | 2 | 0 | 3 | 2 | 1 | api_integrations; identity_device_management; security_engineering; security_vendor_risk; vendor_management | USD 231300.0–256500.0 / 1 YEAR | C_STRETCH_REVIEW |
| Technical Threat Investigator, Threat Intel Engineering | Security | ADJACENT_TECHNICAL | SPECIALIST_ENGINEERING_STRETCH | REMOTE_NOW_STRONG | Remote | YES |  | NO_SALES_SIGNAL_FOUND | HIGH | UNKNOWN |  | 2 | 1 | 0 | 3 | 1 | offensive_security; threat_intelligence_ir; troubleshooting_incidents | USD 347000.0–510000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Applied AI Engineer, Enterprise | Technical Success | ADJACENT_TECHNICAL | SPECIALIST_ENGINEERING_STRETCH | REMOTE_NEEDS_CONFIRMATION | Hybrid | YES | 3 | REVIEW_SALES_CONTEXT | HIGH | UNKNOWN |  | 4 | 0 | 0 | 2 | 0 | javascript_scripting; ml_ai_engineering; professional_software_engineering; python_scripting | USD 251000.0–278000.0 / 1 YEAR | C_STRETCH_REVIEW |
| Early Access Deployment Engineer | Technical Success | ADJACENT_TECHNICAL | SPECIALIST_ENGINEERING_STRETCH | RELOCATION_SUPPORTED | Hybrid | YES | 3 | REVIEW_SALES_CONTEXT | HIGH | MODERATE | 4 | 1 | 0 | 1 | 3 | 0 | cloud_infrastructure; enterprise_customer_delivery; javascript_scripting; ml_ai_engineering; production_system_ownership; professional_software_engineering; python_scripting; technical_customer_communication; uat_qa_bug; web_frontend | USD 250000.0–330000.0 / 1 YEAR | C_STRETCH_REVIEW |

## Major gap domains across the deep candidate set

| domain | roles_or_mentions |
| --- | --- |
| professional_software_engineering | 38 |
| hardware_electrical | 27 |
| troubleshooting_incidents | 26 |
| ml_ai_engineering | 26 |
| api_integrations | 21 |
| distributed_systems | 19 |
| uat_qa_bug | 18 |
| production_system_ownership | 17 |
| threat_intelligence_ir | 16 |
| cloud_infrastructure | 14 |
| datacenter_facilities | 12 |
| automation_workflows | 11 |
| enterprise_customer_delivery | 11 |
| python_scripting | 10 |
| security_engineering | 10 |
| technical_program_delivery | 8 |
| data_science_statistics | 8 |
| identity_device_management | 8 |
| javascript_scripting | 6 |
| documentation_training | 6 |
| people_management | 4 |
| vendor_management | 4 |
| technical_customer_communication | 4 |
| fraud_abuse_investigations | 4 |
| product_management | 3 |
| audiovisual_event_technology | 3 |
| technical_support | 3 |
| offensive_security | 3 |
| sql_data | 2 |
| process_improvement | 1 |
| mergers_acquisitions | 1 |
| security_vendor_risk | 1 |
| web_frontend | 1 |
| ticketing_itsm | 1 |

## Parser diagnostics

The qualification parser now requires an exact line-level heading. This specifically fixes the v0.15 failure mode where the word `requirements` inside ordinary prose could be mistaken for a Qualifications heading.

| method | roles |
| --- | --- |
| line_heading:YOU MIGHT THRIVE IN THIS ROLE IF YOU: | 33 |
| not_found | 23 |
| line_heading:You might thrive in this role if you have: | 25 |
| line_heading:You Might Thrive in This Role If You | 2 |
| line_heading:You might thrive in this role if you | 6 |
| line_heading:You might thrive in this role if you: | 69 |
| line_heading:YOU MIGHT THRIVE IN THIS ROLE IF YOU | 15 |
| line_heading:YOU MIGHT THRIVE IN THIS ROLE IF: | 2 |
| line_heading:Qualifications | 12 |
| line_heading:YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE: | 8 |
| line_heading:YOU MIGHT THRIVE IN THIS ROLE IF YOU HAVE | 3 |
| line_heading:What We’re Looking For | 1 |
| line_heading:You’ll thrive in this role if you: | 11 |
| line_heading:You Might Thrive in This Role If You: | 5 |
| line_heading:You might thrive in this role if you have | 1 |
| line_heading:You might thrive in this role if: | 2 |
| line_heading:Qualifications: | 2 |
| line_heading:You'll thrive in this role if you: | 1 |
| line_heading:You’ll Thrive In This Role If You | 1 |
| line_heading:YOU’LL THRIVE IN THIS ROLE IF YOU | 2 |

## Detailed candidate dossiers

### Product Engagement Manager, User Operations — Support Operations

- **Decision band:** `A_TOP5_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: 3; relocation: yes
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `NONE_DETECTED`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=3, claimed-skill=0, adjacent=0, major gaps=1, moderate gaps=0
- **Salary:** USD 279000.0–310000.0 / 1 YEAR
- **Why this band:** 1 major currently-unproven requirement area(s); 3 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

- Lead a team coordinating product launches across internal and external teams, ensuring seamless execution and support readiness. - Set the team’s strategy and priorities, translate them into clear goals and quality standards, and allocate capacity to deliver against them. - Build a high-performing team through ongoing coaching, feedback, development, and performance management. - Build out a Voice of the User program with scalable feedback loops between support, Product, and Engineering pre and post launch, so customer insights inform product development and strategy. - Advocate for users by representing their needs and pain points in product and engineering discussions. - Partner with Product, Engineering, Marketing, and Operations to align on launch goals and timelines. - Monitor post-launch performance and gather support data to assess product impact and inform improvements. - Document and standardize launch procedures to make them repeatable and scalable. - Identify launch risks and propose solutions that minimize disruption to customers. - Report on feedback-loop performance, including key insights, trends, and recommendations for the product roadmap.

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_support |  | Have experience leading product enablement or launch-readiness functions at scale, particularly in a customer support environment. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Have shipped tooling or automations that reduced manual work and scaled beyond a single team (workflows, dashboards, scripted automation, lightweight pipelines)." |
| MAJOR_GAP | POSTED_EXPECTATION |  | automation_workflows, process_improvement, product_management |  | Have experience in product management with automation and tool development, using metrics and feedback to improve decisions and processes. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Build strong cross-functional relationships with Product, Engineering, and Operations teams. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are passionate about customer advocacy and can translate customer feedback into strategic product insights. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are highly organized and able to manage multiple projects with competing deadlines. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Communicate technical concepts and customer pain points clearly to diverse audiences. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Take ownership of initiatives from ideation through implementation and post-launch analysis. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in a fast-paced environment with shifting priorities. |

**Major currently-unproven requirements**

- Have experience in product management with automation and tool development, using metrics and feedback to improve decisions and processes.

**Posted qualifications with direct work-evidence overlap**

- Have experience leading product enablement or launch-readiness functions at scale, particularly in a customer support environment.
- Have shipped tooling or automations that reduced manual work and scaled beyond a single team (workflows, dashboards, scripted automation, lightweight pipelines)."
- Communicate technical concepts and customer pain points clearly to diverse audiences.

**Apply:** https://jobs.ashbyhq.com/openai/bbf8d3b8-2f8f-49f8-9f35-73c7847647f7/application

### IT Support Specialist — IT

- **Decision band:** `B_SERIOUS_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** Seattle / Washington, DC, San Francisco, London, UK
- **Work arrangement:** OnSite; office days: 5; relocation: yes
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `HIGH`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=1, claimed-skill=1, adjacent=2, major gaps=1, moderate gaps=0
- **Salary:** USD 60.58–108.17 / 1 HOUR
- **Why this band:** 1 major currently-unproven requirement area(s); 1 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

- Improve Support Systems and Processes: Collaborate with cross-functional teams to identify opportunities for improvement, support the creation and maintenance of repeatable workflows (such as onboarding and device imaging), and contribute innovative ideas during IT team meetings. - Collaborate across OpenAI: Work closely with cross-functional teams (Security, Facilities, People Ops, etc.) to ensure seamless employee experiences. Clearly articulate issues, potential solutions, and timelines to both technical and non-technical stakeholders. - Act as Frontline IT Support: Serve as the primary point of contact for troubleshooting hardware, software, and network issues, ensuring prompt and reliable resolution of employee requests. - Manage Vendors and Equipment: Coordinate with vendors for procurement, repairs, and maintenance while managing hardware and software inventories to maintain secure, up-to-date, and standardized systems.

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | crm_saas, identity_device_management | Azure, Google Workspace, Intune, Jamf, Microsoft 365, Windows, macOS | Have strong technical expertise in macOS (with a working knowledge of Windows as a plus), identity and device management (e.g., Azure AD, Jamf, Intune), and enterprise collaboration tools like Google Workspace, Office 365, Slack, and Atlassian products. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Demonstrate excellent written and verbal communication skills, ensuring clarity and professionalism in both internal and external interactions. |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents, identity_device_management | macOS | Excel at troubleshooting and problem-solving within Mac and macOS environments, ensuring smooth operations for users. |
| MAJOR_GAP | POSTED_EXPECTATION |  | audiovisual_event_technology |  | Have experience orchestrating high-production all-hands events, managing the AV and technical aspects to ensure successful outcomes. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | process_improvement |  | Are highly driven and motivated, with a proactive approach to problem solving and continuous improvement. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Exhibit precision and attention to detail in your work, consistently delivering high-quality results. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Possess a customer-first mindset and the ability to clearly articulate technical details to diverse audiences. |
| CLAIMED_SKILL_MATCH | PREFERRED |  | automation_workflows, process_improvement, python_scripting, vendor_management |  | Are proactive in process improvement and vendor management, with added value in mentoring junior team members, automating workflows via scripting or low-code tools, and managing IT projects as a bonus. |

**Major currently-unproven requirements**

- Have experience orchestrating high-production all-hands events, managing the AV and technical aspects to ensure successful outcomes.

**Posted qualifications with direct work-evidence overlap**

- Are highly driven and motivated, with a proactive approach to problem solving and continuous improvement.

**Apply:** https://jobs.ashbyhq.com/openai/49ae54dc-3d33-4107-8112-63fac1ee86ca/application

### Dedicated Support Engineer - San Francisco — Support Delivery

- **Decision band:** `B_SERIOUS_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: not detected; relocation: no
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `HIGH`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=5, claimed-skill=0, adjacent=0, major gaps=1, moderate gaps=1
- **Salary:** USD 180000.0–260000.0 / 1 YEAR
- **Why this band:** 1 major currently-unproven requirement area(s); 5 qualification item(s) map to direct work evidence; Location remains a material dependency

**Responsibilities excerpt**

- Work directly with Premium Support customers to troubleshoot their most complex technical issues, including API failures, integration challenges, authentication errors, unexpected product behavior, performance degradation, and production incidents. - Provide end-to-end technical ownership by analyzing logs and system behavior, reproducing errors, testing hypotheses, and isolating the likely failure domain. Where possible, you’ll identify the root cause before escalating to Engineering; where that is not possible, you’ll provide a clear hypothesis and the evidence needed to accelerate Engineering’s investigation. - Become a trusted expert on OpenAI’s products and systems, serving as a critical escalation point and a technical backstop for our most strategic customers. - Own the customer-specific response to high-impact incidents. You’ll assess severity and business impact, initiate the appropriate response path, coordinate cross-functional responders, maintain clear ownership, and ensure issues move through mitigation, resolution, and post-incident follow-through. - Communicate clearly and proactively during periods of uncertainty, providing accurate updates to customer technical…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_support, troubleshooting_incidents |  | Have significant experience in Support Engineering, Solutions Engineering, Solutions Architecture, or another role involving hands-on diagnosis of complex production issues. |
| MAJOR_GAP | POSTED_EXPECTATION |  | troubleshooting_incidents, api_integrations, distributed_systems, cloud_infrastructure | REST APIs | Have expert-level troubleshooting skills and a strong track record of resolving ambiguous technical problems across APIs, distributed systems, cloud infrastructure, and enterprise integrations. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents, api_integrations, uat_qa_bug | REST APIs | Are comfortable working with logs, metrics, traces, API requests, authentication flows, and customer-provided code or configurations to understand system behavior and test hypotheses. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents, technical_customer_communication |  | Have experience leading or playing a central role in customer-impacting incidents, including severity assessment, technical coordination, stakeholder communication, root-cause analysis, and post-incident follow-through. |
| MODERATE_GAP | POSTED_EXPECTATION |  | troubleshooting_incidents, automation_workflows, python_scripting, javascript_scripting | JavaScript/TypeScript, Python | Can write code or scripts to reproduce issues, interrogate systems, automate repetitive work, and improve internal tools. Experience with Python, JavaScript, or similar languages is valuable. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Can communicate complex technical issues clearly to engineers, customer technical teams, business stakeholders, and senior leaders—especially when information is incomplete or evolving. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Build strong, high-trust relationships with customers and cross-functional partners while maintaining clear and scalable ownership boundaries. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Look beyond the immediate issue to identify patterns, improve the system, and prevent the same problem from recurring. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in ambiguity, update quickly as new information emerges, and are willing to learn whatever is needed to get the job done. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bring a humble, team-first mindset, strong judgment, and a genuine eagerness to help both customers and colleagues succeed. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_support |  | Are excited to use OpenAI’s products, agents, and emerging AI capabilities to transform how technical support operates at scale. |

**Major currently-unproven requirements**

- Have expert-level troubleshooting skills and a strong track record of resolving ambiguous technical problems across APIs, distributed systems, cloud infrastructure, and enterprise integrations.

**Posted qualifications with direct work-evidence overlap**

- Have significant experience in Support Engineering, Solutions Engineering, Solutions Architecture, or another role involving hands-on diagnosis of complex production issues.
- Are comfortable working with logs, metrics, traces, API requests, authentication flows, and customer-provided code or configurations to understand system behavior and test hypotheses.
- Have experience leading or playing a central role in customer-impacting incidents, including severity assessment, technical coordination, stakeholder communication, root-cause analysis, and post-incident follow-through.
- Can communicate complex technical issues clearly to engineers, customer technical teams, business stakeholders, and senior leaders—especially when information is incomplete or evolving.
- Are excited to use OpenAI’s products, agents, and emerging AI capabilities to transform how technical support operates at scale.

**Apply:** https://jobs.ashbyhq.com/openai/2348230a-295f-434d-9b16-653e01ddbd0b/application

### ITAV Event Technical Producer — IT

- **Decision band:** `B_SERIOUS_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `OTHER_TECHNICAL_ROLE`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** OnSite; office days: not detected; relocation: no
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `NONE_DETECTED`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=4, claimed-skill=0, adjacent=0, major gaps=1, moderate gaps=1
- **Salary:** USD 240000.0–266000.0 / 1 YEAR
- **Why this band:** 1 major currently-unproven requirement area(s); 4 qualification item(s) map to direct work evidence; Location remains a material dependency

**Responsibilities excerpt**

- Lead technical production for complex internal, hybrid, and distributed events from early planning and scoping through rehearsal, live delivery, and debrief. - Align Internal Comms, Marketing, Brand Experience, and Workplace on audience goals, requirements, scope, dependencies, and decision owners. Turn ambiguous or competing needs into an agreed production plan and readiness criteria. - Configure and operate live audio, video switching, cameras, playback, conferencing, streaming, and recording systems for the agreed production. - Integrate the run of show across sites and lead multiple crews globally for all-company events. Align technical cues, rehearsals, content handoffs, schedules, and contingencies with partner teams to deliver one cohesive event. - Lead rehearsals and validate the complete audience experience, including remote contribution, playback, recording, and tested backup paths. - Independently prioritize technical production tradeoffs and lead risk reviews and incident response. Resolve ambiguity within your scope, and seek guidance for complex situations or decisions owned by event, staffing, budget, or engineering partners. - Build reusable production plans, sho…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Experience leading complex live or hybrid productions across multiple teams, from ambiguous requirements through rehearsal, delivery, and debrief. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents |  | Advanced expertise in multiple live-production domains, such as audio, video, conferencing, streaming, or AV-over-IP, and the ability to diagnose complex interactions across the complete signal path. |
| MAJOR_GAP | POSTED_EXPECTATION |  | automation_workflows, production_system_ownership |  | Experience configuring and operating professional production systems and creating reusable show files or control workflows. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents |  | Practical AV-over-IP and networking knowledge sufficient to troubleshoot live media, timing, and connectivity with engineering partners. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Experience independently resolving ambiguous production problems, setting detailed plans, and prioritizing tradeoffs while seeking guidance when complexity or decision authority requires it. |
| MODERATE_GAP | POSTED_EXPECTATION |  | troubleshooting_incidents, uat_qa_bug, threat_intelligence_ir |  | Demonstrated ownership of rehearsals, technical readiness, failover testing, and calm incident response for high-priority productions. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Ability to lead crews and influence partner teams without reporting authority, with clear boundaries for content, brand, budget, staffing, and engineering decisions. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Experience working with communications, marketing, brand or creative experience, Workplace, and technical partners on complex events, including sensitive planning and late changes. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Experience building reusable production frameworks and validated AI workflows, guiding team adoption, and mentoring peers or junior staff with measurable improvements in their capability. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Experience with multi-space or multi-location productions and sensitive executive events is a plus. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Experience with systems such as Q-SYS, Dante, Ross, Vizrt, or comparable production platforms is a plus. |

**Major currently-unproven requirements**

- Experience configuring and operating professional production systems and creating reusable show files or control workflows.

**Posted qualifications with direct work-evidence overlap**

- Advanced expertise in multiple live-production domains, such as audio, video, conferencing, streaming, or AV-over-IP, and the ability to diagnose complex interactions across the complete signal path.
- Practical AV-over-IP and networking knowledge sufficient to troubleshoot live media, timing, and connectivity with engineering partners.
- Experience working with communications, marketing, brand or creative experience, Workplace, and technical partners on complex events, including sensitive planning and late changes.
- Experience building reusable production frameworks and validated AI workflows, guiding team adoption, and mentoring peers or junior staff with measurable improvements in their capability.

**Apply:** https://jobs.ashbyhq.com/openai/d089cc3e-e81e-42b7-be77-23bbc9d02431/application

### Security Program Manager — Security

- **Decision band:** `B_SERIOUS_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `ADJACENT_PROGRAM_ROLE`
- **Location path:** `REMOTE_NEEDS_CONFIRMATION` — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** US - Remote / New York City, Seattle, Washington, DC, San Francisco
- **Work arrangement:** Hybrid; office days: not detected; relocation: no
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `MODERATE`; max explicit years detected: 5
- **Requirement evidence:** direct=2, claimed-skill=0, adjacent=1, major gaps=1, moderate gaps=0
- **Salary:** USD 129600.0–310000.0 / 1 YEAR
- **Why this band:** 1 major currently-unproven requirement area(s); 2 qualification item(s) map to direct work evidence; Potential US-remote path needs confirmation

**Responsibilities excerpt**

- Own Security & IT M&A programs, including supporting System Operations and other engineering teams in defining and performing timely diligence assessments, and scoping, planning, and executing acquisition integrations. Carry the work through Day 1 readiness, onboarding of people and systems, post-close priorities, and handoff to ongoing owners. - Partner with Corporate Development, IT, Infrastructure, Application, Legal, Privacy, Security, GRC, Corporate Security and other teams to understand cross-functional requirements and navigate tradeoffs. Make responsibilities and decision rights clear while bringing in the right experts for technical and risk judgments. - Learn partner teams’ workflows and identify missed dependencies, bottlenecks, duplicated effort, and risks that could slow an integration or weaken its outcome. Address recurring problems at their source. - Establish scalable frameworks and processes to support core programs, including defining durable program goals and core measures of success. Build useful intake paths, playbooks, onboarding checklists, decision points, and handoff standards that teams adopt in practice. - Use AI and automation to organize information…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are an empathetic communicator and leader who is able to influence a variety of cross-functional and executive audiences, and build durable trust with partners. |
| ADJACENT_MATCH | POSTED_EXPECTATION | 5 | technical_program_delivery |  | Have 5+ years of experience leading complex cross-functional programs, with a proven record of successful partnership in security, IT, infrastructure, privacy, trust, product risk, or other technical domains. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have carried programs from an ambiguous starting point through execution and lasting ownership. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Have built a new program, workflow, or operating model yourself and can show how you earned adoption and improved results. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are curious about how teams work in practice and can find the underlying issue behind a missed handoff or recurring exception. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Have used AI or automation to improve a real workflow and can explain what changed, how people adopted it, and where human judgment remains necessary. |
| MAJOR_GAP | POSTED_EXPECTATION |  | mergers_acquisitions |  | Have experience in Mergers & Acquisitions or related areas. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in high-trust environments, bring rigor and systems thinking to ambiguity, and operate with a bias for aligned execution over org boundaries. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are structured, detail-oriented, and rigorous in ensuring quality, accountability, and durable delivery. |

**Major currently-unproven requirements**

- Have experience in Mergers & Acquisitions or related areas.

**Posted qualifications with direct work-evidence overlap**

- Have built a new program, workflow, or operating model yourself and can show how you earned adoption and improved results.
- Have used AI or automation to improve a real workflow and can explain what changed, how people adopted it, and where human judgment remains necessary.

**Apply:** https://jobs.ashbyhq.com/openai/6fd50ace-941b-4559-992f-e53f9b76c9a0/application

### Technical Program Manager, Compute Infrastructure — Technical Program Management

- **Decision band:** `B_SERIOUS_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `ADJACENT_PROGRAM_ROLE`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** unspecified; office days: 3; relocation: yes
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `HIGH`
- **Seniority burden:** `MODERATE`; max explicit years detected: 5
- **Requirement evidence:** direct=0, claimed-skill=0, adjacent=2, major gaps=0, moderate gaps=0
- **Salary:** USD 257000.0–335000.0 / 1 YEAR
- **Why this band:** Explicit relocation assistance

**Responsibilities excerpt**

- Lead end-to-end delivery of both New Compute SKUs and large-scale GPU clusters across an external partner ecosystem while supporting capacity planning for training and inference. - Ability to contextually drive multi-threaded bring-up programs spanning hardware, networking, power, and cooling—owning plans, dependencies, and critical paths. - Interface with chip providers to derisk long-term onboarding to new hardware platforms by working across kernels, comms, hardware, and scheduling engineering teams. - Build and operationalize program mechanisms (roadmaps, milestones, risk registers, runbooks) that make delivery predictable at massive scale. - Partner with engineering to improve cluster turn-up reliability, repeatability, and automation, reducing time-to-serve for new capacity. - Support network operations and end-to-end physical and logical bring-up of OpenAI network Points-of-Presence (PoPs), including on-site deployment, rack cabling, and close collaboration with engineering teams. - Coordinate cross-functional readiness (security, finance, operations, product/research stakeholders) to ship production-ready compute. - Manage integration and handoffs across teams and partne…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Possess a degree in a hard science, or have a demonstrated track record of engineering expertise. |
| ADJACENT_MATCH | POSTED_EXPECTATION | 5 | technical_program_delivery, enterprise_customer_delivery |  | Have 5+ years of experience in program management for major projects including capital projects or hyperscaler infrastructure deployment. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Demonstrate the ability to serve as the go-to person solely responsible for driving and delivering complex projects. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are comfortable managing cross-functional and cross-company teams; experience driving information and decision hygiene. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have an extensive track record of successfully delivering high-profile, technical projects against tight deadlines. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are technically adept and have effectively partnered with engineering or fundamental research teams of the highest caliber. |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | vendor_management |  | Have experience interfacing with and leading external vendors including engineering firms, equipment suppliers, and/or construction firms. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have expertise in designing and implementing simple, scalable processes that solve complex problems. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have experience managing complicated dependencies such as logistics and/or supply chains. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are relentlessly resourceful and thrive in ambiguous, fast-paced environments. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are interested in and thoughtful about the impacts of AGI. |

**Apply:** https://jobs.ashbyhq.com/openai/8fb1615c-34bf-47c4-a1d1-b7b2f836bbd3/application

### Technical Program Manager, Multimodal — Technical Program Management

- **Decision band:** `B_SERIOUS_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `ADJACENT_PROGRAM_ROLE`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** unspecified; office days: 3; relocation: yes
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `HIGH`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=4, claimed-skill=0, adjacent=0, major gaps=1, moderate gaps=0
- **Salary:** USD 207000.0–445000.0 / 1 YEAR
- **Why this band:** 1 major currently-unproven requirement area(s); 4 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

- Build a system for mining production conversations and product signals to identify representative multimodal workflows, user needs, and failure modes. - Establish and maintain evaluations for the highest-priority multimodal behaviors and use cases, with clear coverage, quality standards, and ownership. - Package production signals into decision-ready data and evaluations that research teams can use to improve model behavior. - Measure whether model, prompt, configuration, and product changes produce meaningful improvements in multimodal evaluations and user outcomes. - Close gaps between research and production environments, including system prompts, sampling behavior, multimodal configurations, inference differences, and other sources of parity drift. - Create a repeatable process for reproducing product failures with research partners and validating fixes in the shipped experience. - Lead multimodal capacity planning by forecasting demand, translating it into GPU and serving needs, and managing headroom and reallocation tradeoffs for voice and image-generation workloads. - Improve the tooling and operating processes used to plan, launch, and operate multimodal capabilities as …

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MAJOR_GAP | POSTED_EXPECTATION |  | uat_qa_bug, ml_ai_engineering |  | Have led technically complex programs across machine learning, multimodal products, model evaluation, data pipelines, inference, capacity, or large-scale product infrastructure. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | uat_qa_bug |  | Can move fluently between user-facing product behavior and the underlying model, evaluation, configuration, serving, and capacity systems. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | uat_qa_bug |  | Have built mechanisms that convert production signals into prioritized evaluations, data, engineering work, and measurable product improvements. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Can reason credibly about GPU demand, serving constraints, latency, reliability, quality, and launch tradeoffs. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents |  | Have closed research-to-production gaps and can drive structured debugging and validation across teams with different environments and incentives. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Turn manual or fragmented workflows into scalable tooling, clear ownership, and durable operating practices. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Lead effectively across research, engineering, product, operations, Human Data, and external partners without relying on direct authority. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Communicate crisply, make ambiguity tractable, and use metrics and evidence to drive decisions. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in ambiguous, scaling environments and can bring order to complex cross-functional work without losing pace. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Care about OpenAI's mission and about expanding responsible access to advanced AI systems. |

**Major currently-unproven requirements**

- Have led technically complex programs across machine learning, multimodal products, model evaluation, data pipelines, inference, capacity, or large-scale product infrastructure.

**Posted qualifications with direct work-evidence overlap**

- Can move fluently between user-facing product behavior and the underlying model, evaluation, configuration, serving, and capacity systems.
- Have built mechanisms that convert production signals into prioritized evaluations, data, engineering work, and measurable product improvements.
- Have closed research-to-production gaps and can drive structured debugging and validation across teams with different environments and incentives.
- Turn manual or fragmented workflows into scalable tooling, clear ownership, and durable operating practices.

**Apply:** https://jobs.ashbyhq.com/openai/9b017213-6467-413f-b72c-59678c5d8bae/application

### Technical Program Manager, Developer Velocity — Technical Program Management

- **Decision band:** `B_SERIOUS_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `ADJACENT_PROGRAM_ROLE`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** unspecified; office days: 3; relocation: yes
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=1, claimed-skill=0, adjacent=2, major gaps=1, moderate gaps=0
- **Salary:** USD 207000.0–445000.0 / 1 YEAR
- **Why this band:** 1 major currently-unproven requirement area(s); 1 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

- Own the cross-functional roadmap for improving local development, CI, testing, build workflows, and release infrastructure. - Create a durable intake and prioritization mechanism for developer friction, using evidence to focus teams on the highest-impact improvements. - Lead programs that improve deployment speed and safety, including pre-merge confidence, progressive rollout, release guardrails, rollback readiness, and post-deploy validation. - Improve the reliability and predictability of release trains across ChatGPT backend services, web, mobile, and desktop platforms. - Partner with platform, infrastructure, reliability, engineering acceleration, and observability teams to reduce deployment-related incidents and regressions. - Increase visibility into what is shipping when, and make cross-platform dependencies and launch risks clear to engineers, product managers, and launch owners. - Define and operationalize metrics for developer productivity, build and test health, deployment throughput, release reliability, and engineering velocity. - Drive adoption of automation, observability, release orchestration, and scalable developer tooling, with clear ownership and sustained op…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MAJOR_GAP | POSTED_EXPECTATION |  | uat_qa_bug, technical_program_delivery, distributed_systems |  | Have led complex technical programs spanning developer infrastructure, CI/CD, build and test systems, release engineering, or distributed systems. |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | automation_workflows, enterprise_customer_delivery |  | Can engage deeply with engineers on workflow architecture, deployment systems, rollout risk, observability, and operational tradeoffs. |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | enterprise_customer_delivery |  | Have delivered measurable improvements in developer velocity, deployment throughput, release reliability, or engineering efficiency. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Know how to turn fragmented ownership and recurring manual work into durable mechanisms, standards, and tooling with strong adoption. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Use data and qualitative evidence to prioritize work, define useful metrics, and distinguish real productivity gains from local optimization. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Lead effectively across platform and product teams, resolve ambiguity, and keep multi-team execution moving without direct authority. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Use metrics to guide decisions, identify bottlenecks, and demonstrate measurable improvements in throughput, predictability, or reliability. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Communicate with precision and can move comfortably between technical detail, operational execution, and executive-level decisions. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in ambiguous, scaling environments and can bring order to complex cross-functional work without losing pace. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Care about OpenAI's mission and about expanding responsible access to advanced AI systems. |

**Major currently-unproven requirements**

- Have led complex technical programs spanning developer infrastructure, CI/CD, build and test systems, release engineering, or distributed systems.

**Posted qualifications with direct work-evidence overlap**

- Communicate with precision and can move comfortably between technical detail, operational execution, and executive-level decisions.

**Apply:** https://jobs.ashbyhq.com/openai/ad958934-fd89-4033-8b13-1a4871d8073c/application

### Technical Program Manager, Enterprise — Technical Program Management

- **Decision band:** `B_SERIOUS_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `ADJACENT_PROGRAM_ROLE`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** unspecified; office days: 3; relocation: yes
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=1, claimed-skill=0, adjacent=2, major gaps=1, moderate gaps=0
- **Salary:** USD 207000.0–445000.0 / 1 YEAR
- **Why this band:** 1 major currently-unproven requirement area(s); 1 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

- Drive technical strategy and execution for enterprise product and AI workflow initiatives, from design through implementation, launch, customer rollout, and iteration. - Partner with engineering teams to influence architectural direction, interface definitions, and implementation tradeoffs across full-stack products, APIs, integrations, and shared platform systems. - Translate enterprise customer requirements into actionable product priorities across AI-powered workflows, agent experiences, integrations, permissions, data access, evaluations, identity, security, governance, and deployment readiness. - Represent the needs of enterprise buyers, IT administrators, security teams, business leaders, developers, and end users in product and technical decisions. - Identify adoption barriers, competitive gaps, and opportunities to make OpenAI products easier for organizations to evaluate, purchase, deploy, manage, and scale. - Balance near-term customer needs and delivery commitments with long-term platform direction, technical quality, and responsible deployment. - Coordinate enterprise launch readiness, including security and operational requirements, customer-facing dependencies, esc…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | technical_program_delivery |  | Have a strong track record leading complex technical programs across enterprise software, cloud platforms, developer products, or AI systems. |
| MAJOR_GAP | POSTED_EXPECTATION |  | api_integrations, professional_software_engineering | REST APIs | Bring strong technical acumen across several of the following areas: full-stack product systems, client technologies, API development, scalable architecture, and enterprise integrations, with a track record of influencing architectural direction and technical decisions. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Understand enterprise requirements such as SSO, SCIM, role-based access control, audit logging, data residency, compliance, and administrative controls. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Understand how enterprises evaluate, buy, deploy, and govern software, including the different priorities of buyers, administrators, security teams, developers, and end users. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Can connect technical architecture, hands-on problem-solving, customer conversations, and strategic decisions, connecting implementation details to product direction and business outcomes. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | uat_qa_bug |  | Bring strong product judgment across modern AI systems, including agents, connectors, tool use, retrieval or context, evaluations, and the tradeoffs across reliability, latency, cost, safety, and user experience. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Exercise sound judgment in ambiguous environments and can bring structure to complex work without slowing teams down. |
| ADJACENT_MATCH | PREFERRED |  | identity_device_management, enterprise_customer_delivery |  | Experience leading enterprise software launches involving security, identity, compliance, or deployment readiness is preferred. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Communicate clearly, build trust across functions, and influence decisions without relying on formal authority. |

**Major currently-unproven requirements**

- Bring strong technical acumen across several of the following areas: full-stack product systems, client technologies, API development, scalable architecture, and enterprise integrations, with a track record of influencing architectural direction and technical decisions.

**Posted qualifications with direct work-evidence overlap**

- Bring strong product judgment across modern AI systems, including agents, connectors, tool use, retrieval or context, evaluations, and the tradeoffs across reliability, latency, cost, safety, and user experience.

**Apply:** https://jobs.ashbyhq.com/openai/a4981ed2-331a-4927-a95f-fabb64c9c799/application

### Senior Support Specialist, Ads — Trust & Safety

- **Decision band:** `B_SERIOUS_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: not detected; relocation: no
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `HIGH`; max explicit years detected: 6
- **Requirement evidence:** direct=4, claimed-skill=1, adjacent=0, major gaps=0, moderate gaps=0
- **Salary:** USD 189000.0–280000.0 / 1 YEAR
- **Why this band:** 4 qualification item(s) map to direct work evidence; Location remains a material dependency

**Responsibilities excerpt**

- Own advertiser cases from initial intake through resolution, including complex or sensitive Ads Trust & Safety escalations; investigate whether issues stem from policy, review operations, product behavior, tooling, or another dependency, then communicate clear next steps and follow through. - Develop deep expertise across advertiser workflows, ads policies, enforcement processes, review systems, and support tooling. - Build a detailed view of advertiser friction by combining ticket themes, escalation patterns, quality findings, and service metrics to prioritize improvements and identify emerging experience or safety gaps. - Turn frontline learnings into clearer help content, stronger playbooks, better routing and escalation criteria, improved knowledge management and quality standards, and self-service opportunities. - Partner with Product, Policy, Engineering, Legal, Data Science, and Go To Market teams to resolve recurring issues, surface advertiser feedback, and scale durable solutions. - Drive operational excellence through AI-assisted workflows and automation that reduce manual effort, improve team efficiency, and elevate support quality. - Support readiness for new ads for…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| DIRECT_MATCH | POSTED_EXPECTATION | 6 | technical_support |  | Have 6+ years of experience in customer support, user operations, ads operations, Trust & Safety, risk operations, escalations, or a related field, including ownership of high-impact customer or advertiser cases. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bring strong investigative judgment and can translate ambiguous signals into policy support, operational gaps, product defects, and expected behavior |
| DIRECT_MATCH | POSTED_EXPECTATION |  | uat_qa_bug |  | Can synthesize data trends, feedback, QA findings, and service metrics into clear priorities and system improvement while maintaining strong judgment and safeguards |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Have improved support processes, knowledge bases, escalation workflows, routing systems, or quality programs. |
| CLAIMED_SKILL_MATCH | POSTED_EXPECTATION |  | api_integrations, automation_workflows, python_scripting | Python, REST APIs | Are comfortable using AI and emerging technologies (i.e. Codex, ChatGPT, OpenAI API, etc.) and/or code (e.g. Python) to automate repetitive tasks and integrating tools |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Build trust with cross-functional partners, communicate clearly and empathetically with advertisers and internal teams, and drive action without formal authority. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in ambiguity, learn quickly, manage competing priorities, and bring a humble, service-oriented mindset. |
| DIRECT_MATCH | PREFERRED |  | automation_workflows |  | Bonus: Understand advertiser workflows, ads ecosystems, policy enforcement, account reviews, or ads safety operations. |

**Posted qualifications with direct work-evidence overlap**

- Have 6+ years of experience in customer support, user operations, ads operations, Trust & Safety, risk operations, escalations, or a related field, including ownership of high-impact customer or advertiser cases.
- Can synthesize data trends, feedback, QA findings, and service metrics into clear priorities and system improvement while maintaining strong judgment and safeguards
- Have improved support processes, knowledge bases, escalation workflows, routing systems, or quality programs.
- Bonus: Understand advertiser workflows, ads ecosystems, policy enforcement, account reviews, or ads safety operations.

**Apply:** https://jobs.ashbyhq.com/openai/f21b387c-617b-4473-9e84-2fbfa89c27a9/application

### Technical Program Manager, People Innovation Labs — Technical Program Management

- **Decision band:** `B_SERIOUS_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `ADJACENT_PROGRAM_ROLE`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: not detected; relocation: no
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `HIGH`; max explicit years detected: 7
- **Requirement evidence:** direct=2, claimed-skill=0, adjacent=1, major gaps=0, moderate gaps=0
- **Salary:** USD 257000.0–335000.0 / 1 YEAR
- **Why this band:** 2 qualification item(s) map to direct work evidence; Location remains a material dependency

**Responsibilities excerpt**

- Independently lead complex, high-priority technical programs from early planning through launch, adoption, and ongoing iteration. - Partner with product and engineering leadership to translate strategy and team objectives into clear, executable plans. - Establish program structures, decision-making forums, operating cadences, and accountability across multiple teams. - Align product, design, engineering, data, operations, and other stakeholders around priorities, responsibilities, and delivery plans. - Partner closely with engineering leads to manage technical dependencies, sequencing, delivery risks, and launch readiness. - Identify gaps in strategy or execution, develop recommendations, and drive the decisions needed to move work forward. - Anticipate risks and blockers, clarify tradeoffs, resolve disagreements, and escalate decisions when needed. - Own communication, enablement, change management, and rollout strategies for new products and workflows. - Lead post-launch user engagement through onboarding, training, office hours, hands-on support, and other programs that drive adoption. - Build trusted relationships with users and create an environment where they provide frequ…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| ADJACENT_MATCH | POSTED_EXPECTATION | 7 | technical_program_delivery |  | Have 7+ years of experience in technical program management, product operations, or a similar role leading complex software initiatives. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have independently led multiple high-impact programs involving several technical and business teams. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have helped take new software products from early planning through launch, adoption, and rapid iteration toward product-market fit. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are energized by working directly with users and willing to provide hands-on support while a product is still new. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Know how to build trust with users, ask good questions, and get candid feedback about what is and is not working. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Can identify patterns across qualitative feedback, usage data, and operational signals and turn them into actionable recommendations. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | api_integrations |  | Have strong technical fluency and can partner with engineers on architecture, integrations, data dependencies, security, reliability, and delivery tradeoffs. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have led significant operational or organizational change alongside technical product delivery. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Can influence senior leaders, drive difficult decisions, and build alignment across teams with competing priorities. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Identify and address strategic or execution gaps without waiting for detailed direction. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Communicate clearly and directly across technical teams, operational partners, users, and executives. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Can move comfortably between organizational strategy and detailed, hands-on execution |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bring structure to fast-moving work without adding unnecessary process. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are curious about how AI can change the way organizations operate and how people work. |

**Posted qualifications with direct work-evidence overlap**

- Have strong technical fluency and can partner with engineers on architecture, integrations, data dependencies, security, reliability, and delivery tradeoffs.
- Communicate clearly and directly across technical teams, operational partners, users, and executives.

**Apply:** https://jobs.ashbyhq.com/openai/87ef8476-e930-47ed-abc2-a1bedcc074fb/application

### Technical Systems Program Manager, User Operations — Support Operations

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: not detected; relocation: yes
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 8
- **Requirement evidence:** direct=4, claimed-skill=0, adjacent=2, major gaps=0, moderate gaps=0
- **Salary:** USD 216000.0–240000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 4 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

- Own and drive CRM systems initiatives across support - Partner with senior business stakeholders and engineering teams to identify operational pain points, define scalable solutions, evaluate technical tradeoffs, and execute across Salesforce and adjacent platforms - Align cross-functional stakeholders including Revenue Operations, Support Delivery, Risk, Engineering, Data, Legal, and Enterprise Platform teams while driving prioritization and execution - Help operationalize AI-native workflows by defining and building scalable automation, orchestration, agentic workflows, and human-in-the-loop processes in partnership with cross-functional teams

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| ADJACENT_MATCH | POSTED_EXPECTATION | 8 | technical_program_delivery |  | You have 8+ years of experience driving high-impact technical programs in a program management, technical program management or adjacent role |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_support, automation_workflows, crm_saas |  | Strong understanding of CRM workflows customer systems supporting user operations or support organizations |
| DIRECT_MATCH | POSTED_EXPECTATION |  | crm_saas |  | Experience working across CRM systems, routing engines, and adjacent systems |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | technical_program_delivery |  | Proven ability to drive complex cross-functional initiatives from discovery and stakeholder alignment through execution and operationalization |
| DIRECT_MATCH | POSTED_EXPECTATION |  | api_integrations, crm_saas | REST APIs, Salesforce | Strong technical fluency across APIs, integrations, event-driven architectures, enterprise SaaS ecosystems, and Salesforce platform capabilities |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Experience partnering closely with Engineering, Revenue Operations, Security, and Enterprise Platform teams |
| DIRECT_MATCH | POSTED_EXPECTATION |  | uat_qa_bug |  | Experience operating within SOX/SOC2-controlled environments with strong understanding of SDLC, QA, release management, and operational governance |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Strong written and verbal communication skills with the ability to clearly communicate priorities, tradeoffs, risks, and execution plans |

**Preferred / bonus items**

| classification | domains | requirement |
| --- | --- | --- |
| DIRECT_MATCH | api_integrations | Ability to independently reason through technical system design, integration dependencies, and operational tradeoffs alongside engineering teams |
| UNCLASSIFIED_REQUIREMENT |  | Experience working within AI-native, high-growth, or highly ambiguous operating environments |
| UNCLASSIFIED_REQUIREMENT |  | Exposure to global support operations |
| UNCLASSIFIED_REQUIREMENT |  | Ability to operate scrappily and iteratively while maintaining a strong bias toward scalability, governance, and long-term maintainability |

**Posted qualifications with direct work-evidence overlap**

- Strong understanding of CRM workflows customer systems supporting user operations or support organizations
- Experience working across CRM systems, routing engines, and adjacent systems
- Strong technical fluency across APIs, integrations, event-driven architectures, enterprise SaaS ecosystems, and Salesforce platform capabilities
- Experience operating within SOX/SOC2-controlled environments with strong understanding of SDLC, QA, release management, and operational governance

**Apply:** https://jobs.ashbyhq.com/openai/e1b8fd3a-315c-4480-9105-98228093d429/application

### Support Operations Lead — Support Operations

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: 3; relocation: yes
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 10
- **Requirement evidence:** direct=2, claimed-skill=0, adjacent=0, major gaps=1, moderate gaps=0
- **Salary:** USD 279000.0–310000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 1 major currently-unproven requirement area(s); 2 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

- Lead and evolve organizational design for our frontline operations across partner and vendor management, coaching teams to expand automation and deliver measurable capacity gains. - Lead multi-site partner management, including commercial ownership, capacity planning and workforce management, QBRs, and performance recovery. - Own end-to-end service governance for partner and vendor teams, including automation rate, cost to serve, first-response time, productivity, and quality. - Set standards for how work gets done at scale, replacing one-off fixes with reusable systems. - Upskill teams and partner with Automation Engineering, Support Engineering, and Fraud & Risk to embed LLM-powered tools into frontline workflows.

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| DIRECT_MATCH | POSTED_EXPECTATION | 10,4 | automation_workflows |  | Have 10+ years of experience in support operations including 4+ years leading senior individual contributors with a strong track record of coaching, driving accountability, and improving performance and automation adoption at scale. |
| MAJOR_GAP | POSTED_EXPECTATION |  | people_management |  | Are comfortable managing a team while staying hands-on in solving ambiguous operational problems. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are fluent in operational data and technical collaboration, able to define metrics, interpret dashboards, design experiments, and partner with engineering and data teams to turn ambiguous support problems into scalable systems. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Think in systems, using process design, data, tooling, and automation to reduce manual work and create durable capacity. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Can partner credibly with technical teams and translate support needs into clear requirements, owning problem definition, adoption, change management, and operational outcomes. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are energized by building structure in a high-growth environment where the support model, tooling, and partner strategy are still evolving. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have scaled support operations through organizational design and tooling in a high-growth technology company without compromising quality. |

**Major currently-unproven requirements**

- Are comfortable managing a team while staying hands-on in solving ambiguous operational problems.

**Posted qualifications with direct work-evidence overlap**

- Have 10+ years of experience in support operations including 4+ years leading senior individual contributors with a strong track record of coaching, driving accountability, and improving performance and automation adoption at scale.
- Think in systems, using process design, data, tooling, and automation to reduce manual work and create durable capacity.

**Apply:** https://jobs.ashbyhq.com/openai/c7f26e3d-7345-44a6-8e5a-3599679bfe9e/application

### Product Engagement Specialist, User Operations — Support Operations

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: 3; relocation: yes
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 8
- **Requirement evidence:** direct=2, claimed-skill=0, adjacent=0, major gaps=1, moderate gaps=1
- **Salary:** USD 216000.0–240000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 1 major currently-unproven requirement area(s); 2 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

- Design, build, and own scalable systems for launch readiness, feedback capture, triage, synthesis, and routing. - Coordinate product launches across internal User Operations teams and external third party teams to ensure seamless execution and support readiness. - Develop and implement scalable feedback loops between support teams and product/engineering teams, ensuring customer insights are integrated into product development and strategy. - Serve as the voice of the user, advocating for their needs and pain points in product and engineering discussions. - Collaborate with cross-functional teams (e.g., Product, Engineering, Marketing, and Operations) to align on product launch goals and timelines. - Lead efforts to document and standardize launch procedures, ensuring they are easily repeatable and scalable as the product line grows. - Monitor post-launch performance, gathering data from support teams to evaluate product impact and inform future improvements. - Identify potential risks and challenges during product rollouts, proposing solutions to mitigate disruptions to customer service. - Regularly report on the performance of the feedback loop, including key insights, trends,…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| DIRECT_MATCH | POSTED_EXPECTATION | 8 | technical_support |  | Have 8+ years of experience in product launch coordination, especially within a customer support environment (internal and/or external). |
| MAJOR_GAP | POSTED_EXPECTATION |  | technical_program_delivery, product_management |  | Bring product management, technical program management, or similarly hands-on experience taking ambiguous problems from discovery through delivery and adoption. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Enjoy working cross-functionally and are skilled at building relationships with Product, Engineering, and Operations teams. |
| MODERATE_GAP | POSTED_EXPECTATION |  | api_integrations, automation_workflows, python_scripting, professional_software_engineering | REST APIs | Are technically fluent in areas such as APIs, integrations, data flows, analytics, automation, or lightweight scripting, even if you are not a software engineer. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are passionate about customer advocacy and have experience translating customer feedback into strategic product insights. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are highly organized and able to manage multiple projects with competing deadlines. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Have excellent communication skills, with the ability to clearly articulate technical concepts and customer pain points to diverse audiences. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are proactive and take ownership of initiatives, from ideation through to implementation and post-launch analysis. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are comfortable working in a fast-paced environment where priorities can shift quickly. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have a data-driven mindset, using metrics and feedback to guide decision-making and optimize processes. |

**Major currently-unproven requirements**

- Bring product management, technical program management, or similarly hands-on experience taking ambiguous problems from discovery through delivery and adoption.

**Posted qualifications with direct work-evidence overlap**

- Have 8+ years of experience in product launch coordination, especially within a customer support environment (internal and/or external).
- Have excellent communication skills, with the ability to clearly articulate technical concepts and customer pain points to diverse audiences.

**Apply:** https://jobs.ashbyhq.com/openai/2a799206-4716-4f26-8aef-372ed6b8df8f/application

### Support Delivery Lead — Support Delivery

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `OTHER_TECHNICAL_ROLE`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: 3; relocation: yes
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 10
- **Requirement evidence:** direct=1, claimed-skill=0, adjacent=0, major gaps=1, moderate gaps=1
- **Salary:** USD 234000.0–260000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 1 major currently-unproven requirement area(s); 1 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

_Not cleanly extracted._

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MAJOR_GAP | POSTED_EXPECTATION | 10 | technical_support, professional_software_engineering |  | Have 10+ years of experience in technical support engineering or software engineering |
| MODERATE_GAP | PREFERRED | 5 | technical_support, professional_software_engineering |  | Have 5+ years of experience leading technical support engineering or software engineering teams, ideally in high-scale or fast-paced environments |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have experience leading highly skilled engineering teams and are comfortable empowering senior ICs while setting a clear technical and operational direction. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bring deep technical experience in application development or infrastructure, paired with a strong instinct for operational systems and customer reliability. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are a strong cross-functional partner with a proven ability to influence engineering and product roadmaps through support-driven insights. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Take an automation-first approach and have a track record of implementing tooling or processes that scale support impact through AI and systems thinking. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in ambiguous environments and balance strategic leadership with a willingness to get into technical details when needed. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are energized by customer impact and excel at building trust with strategic accounts during critical issues or periods of transformation. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are mission-driven, collaborative, and operate with high integrity and humility. |

**Major currently-unproven requirements**

- Have 10+ years of experience in technical support engineering or software engineering

**Posted qualifications with direct work-evidence overlap**

- Take an automation-first approach and have a track record of implementing tooling or processes that scale support impact through AI and systems thinking.

**Apply:** https://jobs.ashbyhq.com/openai/2e645639-3362-42f7-b0b9-e99380c48d29/application

### Support Delivery Lead — Support Delivery

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `OTHER_TECHNICAL_ROLE`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: 3; relocation: yes
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 8
- **Requirement evidence:** direct=1, claimed-skill=0, adjacent=0, major gaps=1, moderate gaps=1
- **Salary:** USD 284000.0–315000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 1 major currently-unproven requirement area(s); 1 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

_Not cleanly extracted._

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MAJOR_GAP | POSTED_EXPECTATION | 8 | technical_support, professional_software_engineering |  | Have 8+ years of experience in technical support engineering or software engineering |
| MODERATE_GAP | PREFERRED | 4 | technical_support, professional_software_engineering |  | Have 4+ years of experience leading technical support engineering or software engineering teams, ideally in high-scale or fast-paced environments |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have experience leading highly skilled engineering teams and are comfortable empowering senior ICs while setting a clear technical and operational direction. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bring deep technical experience in application development or infrastructure, paired with a strong instinct for operational systems and customer reliability. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are a strong cross-functional partner with a proven ability to influence engineering and product roadmaps through support-driven insights. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Take an automation-first approach and have a track record of implementing tooling or processes that scale support impact through AI and systems thinking. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in ambiguous environments and balance strategic leadership with a willingness to get into technical details when needed. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are energized by customer impact and excel at building trust with strategic accounts during critical issues or periods of transformation. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are mission-driven, collaborative, and operate with high integrity and humility. |

**Major currently-unproven requirements**

- Have 8+ years of experience in technical support engineering or software engineering

**Posted qualifications with direct work-evidence overlap**

- Take an automation-first approach and have a track record of implementing tooling or processes that scale support impact through AI and systems thinking.

**Apply:** https://jobs.ashbyhq.com/openai/76583c87-78ea-4886-906d-81b0a9c05bfe/application

### Senior Support Engineer - San Francisco — Support Delivery

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** unspecified; office days: 3; relocation: yes
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `HIGH`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 8
- **Requirement evidence:** direct=2, claimed-skill=0, adjacent=0, major gaps=2, moderate gaps=3
- **Salary:** USD 234000.0–260000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 2 major currently-unproven requirement area(s); 2 qualification item(s) map to direct work evidence; Explicit relocation assistance

**Responsibilities excerpt**

- Be among the foremost technical and troubleshooting experts for our API platform at OpenAI. You are the last line of defense before the core Engineering team. - Proactively identify and implement opportunities to scale support operations by leveraging automation and advancements in AI technologies. Contribute to shaping the future of technical support in an AI-driven era. - Configure and use advanced monitoring and alerting workflows to proactively detect customer impacting issues in real time. - In partnership with engineering, contribute to reliability reviews and preparedness for new features, launches, or strategic customer requirement updates. Ensure that operational readiness (monitoring, alerting, and fallback plans) is in place for any such changes. - Design and refine incident response processes and documentation across strategic customers, engineering and support teams. - Analyze operational metrics and incident RCAs to identify areas for improvement. Proactively recommend and implement enhancements to monitoring dashboards, alert configurations, and support workflows. - Provide support coverage during holidays and weekends based on business needs.

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MODERATE_GAP | POSTED_EXPECTATION |  | professional_software_engineering |  | Have a Bachelor’s degree in Computer Science or a related field. A strong software engineering foundation is important for this role’s success. |
| DIRECT_MATCH | POSTED_EXPECTATION | 8 | troubleshooting_incidents |  | Have 8+ years of experience in technical operations roles such as SRE/NOC, designing monitoring systems and resolving production issues in fast-paced and mission-critical environments. A strong track record of troubleshooting complex technical problems at the systems level. |
| MAJOR_GAP | POSTED_EXPECTATION |  | distributed_systems |  | Have deep familiarity with modern monitoring, alerting, and observability practices. Hands‑on experience setting up or managing metrics, logging, and tracing for distributed systems (e.g., understanding of SLIs/SLOs, alert tuning, dashboard creation). |
| MAJOR_GAP | POSTED_EXPECTATION |  | troubleshooting_incidents, threat_intelligence_ir |  | Have proven experience leading incident response for high‑severity outages or service disruptions. Able to perform real‑time incident coordination, root cause analysis, and drive follow‑ups (post‑mortems, action items) to prevent recurrence. Knowledge of industry best practices for incident management and fault diagnosis. |
| MODERATE_GAP | POSTED_EXPECTATION |  | automation_workflows, python_scripting, professional_software_engineering | Python | Have strong skills in scripting or software engineering (e.g., Python or similar) to automate repetitive tasks and integrate tools. |
| MODERATE_GAP | POSTED_EXPECTATION |  | sql_data, distributed_systems, cloud_infrastructure |  | Have solid understanding of cloud infrastructure and distributed systems fundamentals. Comfortable working with cloud services, load balancers, databases, and containerized applications. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents, technical_customer_communication |  | Are effective at working cross‑functionally in a high‑trust environment. Strong communication skills to explain technical issues and resolutions to both engineering and non‑technical stakeholders. You can coordinate efforts across teams and are comfortable providing updates in the midst of an ongoing incident. #LI-NM2 |

**Major currently-unproven requirements**

- Have deep familiarity with modern monitoring, alerting, and observability practices. Hands‑on experience setting up or managing metrics, logging, and tracing for distributed systems (e.g., understanding of SLIs/SLOs, alert tuning, dashboard creation).
- Have proven experience leading incident response for high‑severity outages or service disruptions. Able to perform real‑time incident coordination, root cause analysis, and drive follow‑ups (post‑mortems, action items) to prevent recurrence. Knowledge of industry best practices for incident management and fault diagnosis.

**Posted qualifications with direct work-evidence overlap**

- Have 8+ years of experience in technical operations roles such as SRE/NOC, designing monitoring systems and resolving production issues in fast-paced and mission-critical environments. A strong track record of troubleshooting complex technical problems at the systems level.
- Are effective at working cross‑functionally in a high‑trust environment. Strong communication skills to explain technical issues and resolutions to both engineering and non‑technical stakeholders. You can coordinate efforts across teams and are comfortable providing updates in the midst of an ongoing incident. #LI-NM2

**Apply:** https://jobs.ashbyhq.com/openai/5431666c-530b-49c0-b67e-32477f9eaf5e/application

### Senior Staff Software Engineer, Identity Infrastructure Engineering — IT

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `SPECIALIST_ENGINEERING_STRETCH`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: 3; relocation: yes
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `HIGH`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 10
- **Requirement evidence:** direct=1, claimed-skill=0, adjacent=0, major gaps=3, moderate gaps=1
- **Salary:** USD 347000.0–510000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 3 major currently-unproven requirement area(s); 1 qualification item(s) map to direct work evidence; Explicit relocation assistance; Specialist engineering/research/security title is outside the strongest documented work-history lane

**Responsibilities excerpt**

- Lead the architecture, development, and operation of identity infrastructure that spans cloud platforms, internal systems, and critical engineering services. - Design and evolve systems for authentication, authorization, access governance, auditability, and policy enforcement with a strong focus on reliability, scalability, and secure-by-default design. - Build foundational infrastructure and platform capabilities that are broadly used across engineering, research, and security teams. - Improve the reliability, observability, performance, and operational maturity of identity infrastructure that supports mission-critical systems and workflows. - Lead ambiguous, high-impact technical initiatives across security, infrastructure, and engineering teams, driving alignment and execution across multiple stakeholders. - Partner closely with engineers, researchers, and security teams to build scalable access patterns and infrastructure that enable rapid development while maintaining strong security boundaries and operational rigor. - Raise the engineering bar through strong technical judgment, thoughtful system design, operational excellence, and long-term ownership of critical infrastruc…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MAJOR_GAP | POSTED_EXPECTATION | 10 | professional_software_engineering |  | 10+ years building and operating large-scale infrastructure, platform, or backend systems. |
| MAJOR_GAP | POSTED_EXPECTATION |  | identity_device_management, distributed_systems, cloud_infrastructure |  | Deep experience with cloud infrastructure, identity systems, distributed systems, and infrastructure-as-code. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Experience leading complex technical initiatives across teams and driving architecture in ambiguous environments. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | api_integrations |  | Experience building security-critical systems involving authentication, authorization, access governance, privileged access, or policy enforcement. |
| MAJOR_GAP | POSTED_EXPECTATION |  | python_scripting, professional_software_engineering | Python | Strong software engineering fundamentals with experience in Go, Rust, Python, or similar languages. |
| MODERATE_GAP | POSTED_EXPECTATION |  | troubleshooting_incidents, identity_device_management, cloud_infrastructure |  | Ability to debug across code, cloud infrastructure, identity systems, networking, and operations. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | High bar for reliability, security, auditability, and operational rigor in mission-critical systems. This role is based in San Francisco, CA. We use a hybrid work model of three days in the office per week and offer relocation assistance to new employees. |

**Major currently-unproven requirements**

- 10+ years building and operating large-scale infrastructure, platform, or backend systems.
- Deep experience with cloud infrastructure, identity systems, distributed systems, and infrastructure-as-code.
- Strong software engineering fundamentals with experience in Go, Rust, Python, or similar languages.

**Posted qualifications with direct work-evidence overlap**

- Experience building security-critical systems involving authentication, authorization, access governance, privileged access, or policy enforcement.

**Apply:** https://jobs.ashbyhq.com/openai/72a58872-70e2-4340-a259-e9bea3596883/application

### Head of Employee Tech & Experience (ETX) — IT

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `OTHER_TECHNICAL_ROLE`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: not detected; relocation: no
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=0, claimed-skill=0, adjacent=0, major gaps=0, moderate gaps=0
- **Salary:** USD 313000.0–347000.0 / 1 YEAR
- **Why this band:** Location remains a material dependency

**Responsibilities excerpt**

- Lead the next stage of ETX’s global growth across Helpdesk, SysOps, Logistics and AV, with a shared strategy and accountability for employee outcomes. - Continually elevate the employee experience through research and design, directing investment to simplify entire user journeys, remove unnecessary effort and amplify what employees can accomplish. - Accelerate ETX’s agent-led and customer-zero work as capabilities advance: continually challenge which workflows need to exist, extend what agents can own end to end and evolve the operating model to deliver measurable amplification. - Develop leaders who earn trust, grow others and sustain an environment where people feel valued, take pride in their work and enjoy working together. Give people meaningful ownership and opportunities to stretch and grow, with clear priorities and sustainable workloads. - Scale global services to support company growth, with clear commitments to reliability, security, responsiveness, and effective controls. Measure performance through employee effort, service quality, and time to resolution. - Shape priorities and investment with leadership across the company, accelerating execution across functions wi…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have led global organizations through growth and transformation, with measurable improvements in employee experience and reliability. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Start with what employees need. Use research and design to challenge assumptions and remove unnecessary work. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Rethink how the organization works as AI advances, expanding what agents can own and delivering measurable amplification. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Build leadership teams that help people grow, own meaningful work and enjoy working together. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Set direction and investment priorities with leadership across the company. Own execution, adoption and lasting results. THE IMPACT YOU’LL HAVE You’ll help people at OpenAI do their most ambitious work. You’ll compound the impact of ETX’s agent-led work, turning advances in AI into measurable amplification, giving people back time and making technology simp… |

**Apply:** https://jobs.ashbyhq.com/openai/4aa1dcbf-166a-4538-ae4e-08cf39c7ff23/application

### AI Support Engineer, Biosciences - San Francisco — Support Delivery

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: not detected; relocation: no
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `HIGH`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 8
- **Requirement evidence:** direct=6, claimed-skill=1, adjacent=1, major gaps=0, moderate gaps=0
- **Salary:** USD 180000.0–260000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 6 qualification item(s) map to direct work evidence; Location remains a material dependency

**Responsibilities excerpt**

- Work directly with Rosalind and life sciences customers, taking ownership of complex technical and operational support cases from intake through resolution. - Serve as a critical escalation point and final line of defense for complex technical issues, partnering closely with customers and Engineering teams to troubleshoot, resolve, and proactively prevent recurring problems while leveraging scripting and emerging AI capabilities to improve internal tooling and automate operational workflows - Support customer workflows across ChatGPT, Codex, and the OpenAI API, including questions about tool access, environment constraints, reproducibility, product behavior, and responsible model usage. - Build bioscience-aware intake flows, diagnostic procedures, routing logic, escalation paths, playbooks, response templates, and internal and customer-facing knowledge content. - Determine whether an issue requires technical support, workflow enablement, scientific consultation, solutions architecture, product feedback, or another specialized response, and route it to the appropriate owner without losing context or accountability. - Coordinate complex escalations across Product, Engineering, For…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| ADJACENT_MATCH | POSTED_EXPECTATION | 8 | technical_support, troubleshooting_incidents, technical_customer_communication, enterprise_customer_delivery |  | Have 8+ years of experience in technical support, support engineering, escalations, technical account management, solutions operations, product operations, incident management, or a related customer-facing technical role. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Bring meaningful familiarity with life sciences disciplines or workflows, such as computational biology, bioinformatics, genomics, transcriptomics, drug discovery, or related fields. |
| DIRECT_MATCH | EXPLICIT_REQUIREMENT |  | automation_workflows |  | Can rapidly understand and triage questions involving scientific tools and workflows while recognizing when specialized scientific expertise is required. |
| DIRECT_MATCH | PREFERRED | 8 | technical_support |  | Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. |
| CLAIMED_SKILL_MATCH | POSTED_EXPECTATION |  | api_integrations, automation_workflows, python_scripting | Python, REST APIs | Are comfortable using emerging technologies (ie. Codex, ChatGPT, OpenAI API, etc.) to script or engineer code (e.g., Python) for automating repetitive tasks and integrating tools. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents, crm_saas |  | Have expert-level SaaS troubleshooting skills with the ability to rapidly understand new technologies and complex concepts. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents |  | Demonstrate polished enterprise communication: calm with high-stakes customers during live incident calls and proven experience building strong relationships with customers and cross-functional partners to drive resolution to complex issues. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Exceptional critical thinker and problem solver with the ability to clearly communicate complex technical issues to both customers and internal teams. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in ambiguity, adapt rapidly to change, continuously learn, and proactively seek opportunities for growth. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bring a humble, team first mindset, a genuine eagerness to help others, and the curiosity to quickly learn whatever knowledge is needed to help both your teammates and our customers succeed. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |

**Preferred / bonus items**

| classification | domains | requirement |
| --- | --- | --- |
| UNCLASSIFIED_REQUIREMENT |  | Experience supporting software, data, or AI products used in regulated or security-sensitive scientific environments. |
| DIRECT_MATCH | api_integrations, automation_workflows | Experience working with computational research environments, scientific software, cloud platforms, APIs, or data-intensive workflows. |
| UNCLASSIFIED_REQUIREMENT |  | A degree or equivalent practical experience in a life sciences, computational, engineering, or other relevant technical field. |

**Posted qualifications with direct work-evidence overlap**

- Bring meaningful familiarity with life sciences disciplines or workflows, such as computational biology, bioinformatics, genomics, transcriptomics, drug discovery, or related fields.
- Can rapidly understand and triage questions involving scientific tools and workflows while recognizing when specialized scientific expertise is required.
- Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments.
- Have expert-level SaaS troubleshooting skills with the ability to rapidly understand new technologies and complex concepts.
- Demonstrate polished enterprise communication: calm with high-stakes customers during live incident calls and proven experience building strong relationships with customers and cross-functional partners to drive resolution to complex issues.
- Exceptional critical thinker and problem solver with the ability to clearly communicate complex technical issues to both customers and internal teams.

**Apply:** https://jobs.ashbyhq.com/openai/759dd316-cbe9-4e73-af57-808502568b29/application

### AI Support Engineer - San Francisco — Support Delivery

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** unspecified; office days: not detected; relocation: no
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `HIGH`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 8
- **Requirement evidence:** direct=4, claimed-skill=1, adjacent=0, major gaps=0, moderate gaps=0
- **Salary:** USD 180000.0–260000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 4 qualification item(s) map to direct work evidence; Location remains a material dependency

**Responsibilities excerpt**

_Not cleanly extracted._

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| DIRECT_MATCH | PREFERRED | 8 | technical_support |  | Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. |
| CLAIMED_SKILL_MATCH | POSTED_EXPECTATION |  | api_integrations, automation_workflows, python_scripting | Python, REST APIs | Are comfortable using emerging technologies (ie. Codex, ChatGPT, OpenAI API, etc.) to script or engineer code (e.g., Python) for automating repetitive tasks and integrating tools. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents, crm_saas |  | Have expert-level SaaS troubleshooting skills with the ability to rapidly understand new technologies and complex concepts. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents |  | Polished enterprise communication and are calm with high-stakes customers during live incident calls |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Proven experience building strong relationships with customers and cross-functional partners to drive resolution to complex issues. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Exceptional critical thinker and problem solver with the ability to clearly communicate complex technical issues to both customers and internal teams. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in ambiguity, adapt rapidly to change, continuously learn, and proactively seek opportunities for growth. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bring a humble, team first mindset, a genuine eagerness to help others, and the curiosity to quickly learn whatever knowledge is needed to help both your teammates and our customers succeed. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |

**Posted qualifications with direct work-evidence overlap**

- Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments.
- Have expert-level SaaS troubleshooting skills with the ability to rapidly understand new technologies and complex concepts.
- Polished enterprise communication and are calm with high-stakes customers during live incident calls
- Exceptional critical thinker and problem solver with the ability to clearly communicate complex technical issues to both customers and internal teams.

**Apply:** https://jobs.ashbyhq.com/openai/1a979fd4-1bce-484e-a416-aed2810677a6/application

### AI Support Engineer - San Francisco (Weekend Shift) — Support Delivery

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `DIRECT_ROLE_FAMILY`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** unspecified; office days: not detected; relocation: no
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `HIGH`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 8
- **Requirement evidence:** direct=4, claimed-skill=1, adjacent=0, major gaps=0, moderate gaps=0
- **Salary:** USD 180000.0–260000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 4 qualification item(s) map to direct work evidence; Location remains a material dependency

**Responsibilities excerpt**

_Not cleanly extracted._

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| DIRECT_MATCH | PREFERRED | 8 | technical_support |  | Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments. |
| CLAIMED_SKILL_MATCH | POSTED_EXPECTATION |  | api_integrations, automation_workflows, python_scripting | Python, REST APIs | Are comfortable using emerging technologies (ie. Codex, ChatGPT, OpenAI API, etc.) to script or engineer code (e.g., Python) for automating repetitive tasks and integrating tools. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents, crm_saas |  | Have expert-level SaaS troubleshooting skills with the ability to rapidly understand new technologies and complex concepts. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents |  | Polished enterprise communication and are calm with high-stakes customers during live incident calls |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Proven experience building strong relationships with customers and cross-functional partners to drive resolution to complex issues. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Exceptional critical thinker and problem solver with the ability to clearly communicate complex technical issues to both customers and internal teams. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in ambiguity, adapt rapidly to change, continuously learn, and proactively seek opportunities for growth. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bring a humble, team first mindset, a genuine eagerness to help others, and the curiosity to quickly learn whatever knowledge is needed to help both your teammates and our customers succeed. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bachelor’s degree in Computer Science, Computer Engineering, another relevant technical field, or equivalent practical experience. |

**Posted qualifications with direct work-evidence overlap**

- Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, ideally within high-growth tech startups or other fast-paced environments.
- Have expert-level SaaS troubleshooting skills with the ability to rapidly understand new technologies and complex concepts.
- Polished enterprise communication and are calm with high-stakes customers during live incident calls
- Exceptional critical thinker and problem solver with the ability to clearly communicate complex technical issues to both customers and internal teams.

**Apply:** https://jobs.ashbyhq.com/openai/99f823a1-66ec-44bd-ba30-d3645aa49d74/application

### Strategy & Operations Programs, Support — Support Operations

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `OTHER_TECHNICAL_ROLE`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** unspecified; office days: not detected; relocation: no
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 8
- **Requirement evidence:** direct=2, claimed-skill=0, adjacent=0, major gaps=0, moderate gaps=0
- **Salary:** USD 216000.0–310000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 2 qualification item(s) map to direct work evidence; Location remains a material dependency

**Responsibilities excerpt**

- Drive the ideation and operationalization of new support systems, processes, and programs. - Collaborate with leaders to identify, evaluate, and prioritize new strategic and operational initiatives, ensuring alignment with company goals and unique organizational objectives - Work with product, engineering, and data teams to uncover and address key operational challenges and growth/scaling opportunities within the support organization, such as automation, process optimization, and enhanced self-service options. - Deep dive into the critical drivers of our support operations and identifying opportunities for optimization and innovation. - Partner with other members of the go-to-market organization, product, and partnerships to launch new initiatives – helping think through strategic impacts, executing on operational components, and driving change management.

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| DIRECT_MATCH | EXPLICIT_REQUIREMENT | 5,8,5 | technical_customer_communication |  | Have 8+ years of experience in operations, strategy, and consulting, with at least 5 years of experience building and leading customer-facing operations. You have a history of high impact work in a technical environment. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are non-traditional – this role will require leveraging technology and concepts that are not yet established in the world (some of which you will produce yourself). |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents |  | Are comfortable operating at all altitudes – discussing strategy and vision with executives, and troubleshooting operations with individual contributors. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have extensive experience in taking end-to-end ownership of large, ambiguous problems, and breaking them down into clear, actionable plans. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have direct experience engaging with executives and senior leaders to influence and drive strategic decisions. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are highly analytical, with strong skills in data modeling and operational forecasting to drive insights and decision-making. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Possess excellent communication and collaboration skills and are skilled in influencing stakeholders across all levels of the organization. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in chaos, and relentlessly drive program structure to enable the team. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have a passion for technology, AI, and customer service, and are enthusiastic about the transformative impact of AI on business and society. |

**Posted qualifications with direct work-evidence overlap**

- Have 8+ years of experience in operations, strategy, and consulting, with at least 5 years of experience building and leading customer-facing operations. You have a history of high impact work in a technical environment.
- Are comfortable operating at all altitudes – discussing strategy and vision with executives, and troubleshooting operations with individual contributors.

**Apply:** https://jobs.ashbyhq.com/openai/9747412d-a23d-48ba-bddd-ad1247c360f5/application

### Support Program Manager, Partnerships — Support Operations

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `ADJACENT_PROGRAM_ROLE`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** unspecified; office days: not detected; relocation: no
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 8
- **Requirement evidence:** direct=0, claimed-skill=0, adjacent=1, major gaps=0, moderate gaps=0
- **Salary:** USD 216000.0–310000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; Location remains a material dependency

**Responsibilities excerpt**

- Lead support readiness for new and existing cloud and strategic partnerships, including launch planning, operational design, and ongoing program execution. - Partner closely with Engineering, Product, go-to-market teams, and external partners to develop support models for technically complex products and integrations. - Define partner-specific customer journeys, support workflows, escalation paths, ownership models, and cross-company handoffs. - Identify operational and technical risks, align stakeholders on solutions, and drive improvements that strengthen the customer experience. - Establish clear success metrics and operating rhythms to monitor partnership health, launch readiness, and support performance. - Use AI and automation to improve partner-related support workflows and scale operations effectively.

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| ADJACENT_MATCH | POSTED_EXPECTATION | 8 | technical_program_delivery |  | Have 8+ years of experience in program management, support operations, partnerships, or related roles within a fast-paced technology environment. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have experience working closely with engineering teams to translate technical requirements into clear operational plans. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have experience with cloud platforms, cloud-provider partnerships, or technically complex enterprise products. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are comfortable navigating ambiguity and driving alignment across internal teams and external partners. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Can move between strategic planning and hands-on execution while maintaining a strong focus on customer outcomes. |
| UNCLASSIFIED_REQUIREMENT | EXPLICIT_REQUIREMENT |  |  |  | Have experience in cybersecurity or life sciences; this background is a plus but not required. |

**Apply:** https://jobs.ashbyhq.com/openai/66b7c776-aa50-4e86-aec1-5c8e07868522/application

### Engineering Manager, Cooperative Systems — Support Automation

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `SPECIALIST_ENGINEERING_STRETCH`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: not detected; relocation: no
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 12
- **Requirement evidence:** direct=2, claimed-skill=0, adjacent=0, major gaps=0, moderate gaps=1
- **Salary:** USD 401000.0–445000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 2 qualification item(s) map to direct work evidence; Location remains a material dependency; Specialist engineering/research/security title is outside the strongest documented work-history lane

**Responsibilities excerpt**

- Lead and grow a small team building applied AI systems for internal operations - Design and build AI-powered automation systems in close proximity to customers - Stay hands-on in architecture and implementation across the full stack - Develop evolving systems spanning developer tools, automation platforms, knowledge graphs, and data systems - Deploy systems directly to internal users and close customers to iterate rapidly based on real-world feedback - Engage frequently with scaled workforces to understand needs and validate solutions - Create systems for visibility and learning in hybrid workforces - Partner with product, research, and ops teams daily

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| UNCLASSIFIED_REQUIREMENT | EXPLICIT_REQUIREMENT | 7,12,3 |  |  | Have 12+ years of experience in engineering, including 3+ years of experience in engineering management, and at least 7 years as an IC engineer |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are a hands-on builder who enjoys operating across the stack |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have deep experience applying AI, and are ready to experiment with frontier approaches |
| MODERATE_GAP | POSTED_EXPECTATION |  | professional_software_engineering |  | Bring strong technical judgment across systems design, infrastructure, and full-stack development |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Have built developer tools, internal platforms, or workflow automation systems |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Enjoy frequent interaction with customers and thrive in feedback-driven development loops |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are comfortable with ambiguity and excited to operate in a rapidly evolving space |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Have experience in operationally complex environments (e.g., logistics, support systems, internal tooling, warehouse automation, etc.) |

**Posted qualifications with direct work-evidence overlap**

- Have built developer tools, internal platforms, or workflow automation systems
- Have experience in operationally complex environments (e.g., logistics, support systems, internal tooling, warehouse automation, etc.)

**Apply:** https://jobs.ashbyhq.com/openai/241154df-ab1a-4dfa-8b18-66e087d1e636/application

### Engineering Manager, Cooperative Systems — Support Automation

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `SPECIALIST_ENGINEERING_STRETCH`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** Seattle / none
- **Work arrangement:** Hybrid; office days: not detected; relocation: no
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `VERY_HIGH`; max explicit years detected: 12
- **Requirement evidence:** direct=2, claimed-skill=0, adjacent=0, major gaps=0, moderate gaps=1
- **Salary:** USD 400000.0–445000.0 / 1 YEAR
- **Why this band:** Very high posted seniority burden; 2 qualification item(s) map to direct work evidence; Location remains a material dependency; Specialist engineering/research/security title is outside the strongest documented work-history lane

**Responsibilities excerpt**

- Lead and grow a small team building applied AI systems for internal operations - Design and build AI-powered automation systems in close proximity to customers - Stay hands-on in architecture and implementation across the full stack - Develop evolving systems spanning developer tools, automation platforms, knowledge graphs, and data systems - Deploy systems directly to internal users and close customers to iterate rapidly based on real-world feedback - Engage frequently with scaled workforces to understand needs and validate solutions - Create systems for visibility and learning in hybrid workforces - Partner with product, research, and ops teams daily

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| UNCLASSIFIED_REQUIREMENT | EXPLICIT_REQUIREMENT | 7,12,3 |  |  | Have 12+ years of experience in engineering, including 3+ years of experience in engineering management, and at least 7 years as an IC engineer |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are a hands-on builder who enjoys operating across the stack |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have deep experience applying AI, and are ready to experiment with frontier approaches |
| MODERATE_GAP | POSTED_EXPECTATION |  | professional_software_engineering |  | Bring strong technical judgment across systems design, infrastructure, and full-stack development |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Have built developer tools, internal platforms, or workflow automation systems |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Enjoy frequent interaction with customers and thrive in feedback-driven development loops |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are comfortable with ambiguity and excited to operate in a rapidly evolving space |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Have experience in operationally complex environments (e.g., logistics, support systems, internal tooling, warehouse automation, etc.) |

**Posted qualifications with direct work-evidence overlap**

- Have built developer tools, internal platforms, or workflow automation systems
- Have experience in operationally complex environments (e.g., logistics, support systems, internal tooling, warehouse automation, etc.)

**Apply:** https://jobs.ashbyhq.com/openai/817c523c-59b2-4206-ae52-7dd6d36090b4/application

### IT Audiovisual Operations Engineer — IT

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `PRIMARY_SUPPORT_IT`; title alignment: `OTHER_TECHNICAL_ROLE`
- **Location path:** `US_LOCATION_DEPENDENCY` — US office location, but remote/relocation terms are not conclusive
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: not detected; relocation: no
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `MODERATE`; max explicit years detected: 5
- **Requirement evidence:** direct=6, claimed-skill=0, adjacent=1, major gaps=2, moderate gaps=1
- **Salary:** USD 187000.0–207000.0 / 1 YEAR
- **Why this band:** 2 major currently-unproven requirement area(s); 6 qualification item(s) map to direct work evidence; Location remains a material dependency

**Responsibilities excerpt**

- Set up, configure, administer, and maintain conference room AV, video conferencing, background music, digital signage, and other ITAV-owned systems. - Resolve vendor escalations that require internal administrative access or technical expertise, owning diagnosis, remediation, and verification of service restoration. - Manage assigned ITAV installation and commissioning scope for office builds, refreshes, and moves, adds, and changes using established standards, and verify that completed systems are ready for ongoing operation. - Serve as the technical bridge between vendors and ITAV Engineering, providing clear diagnostic evidence and escalating issues that require changes to system designs or engineering standards. - Execute software updates, configuration changes, equipment replacements, and conferencing move/add/change requests using established standards and recovery procedures. - Validate operational readiness for new or upgraded systems, including configuration, monitoring, administrative access, documentation, and support handoffs. - Investigate recurring failures and work with ITAV Engineering to implement and validate lasting improvements. - Maintain runbooks and recove…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MAJOR_GAP | POSTED_EXPECTATION | 5 | troubleshooting_incidents, datacenter_facilities, hardware_electrical, audiovisual_event_technology |  | 5+ years of experience implementing and troubleshooting enterprise AV systems, including installation, commissioning, and working from technical designs; hands-on experience with Logitech, Cisco, QSYS and Google Meet conferencing hardware. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents |  | Hands-on expertise configuring, administering, and troubleshooting video conferencing platforms such as Google Meet, Zoom, and Microsoft Teams. |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents, vendor_management |  | Experience working with support vendors to diagnose escalated issues, perform administrative actions outside vendor permissions, and document verified resolutions. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Experience administering AV or workplace technology services, including configuration, monitoring, software updates, and recovery, as well as migrating video conferencing platforms. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents, basic_network_dns |  | Practical knowledge of enterprise networking, including IP addressing, VLANs, DNS, DHCP, and multicast, sufficient to diagnose AV connectivity and work effectively with Network Engineering. |
| MAJOR_GAP | POSTED_EXPECTATION |  | troubleshooting_incidents, api_integrations, hardware_electrical |  | Experience configuring and troubleshooting wayfinding and conference room booking hardware, software, and room-resource integrations. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents |  | Experience deploying and troubleshooting AV over IP, including Q-LAN, Dante, and NDI. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents |  | Experience configuring and troubleshooting systems in the Q-SYS control ecosystem. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | documentation_training |  | Experience applying AV build standards, validating system performance, and maintaining clear configuration and support documentation. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | ticketing_itsm |  | Experience using IT ticketing systems to prioritize technical escalations, communicate with users and partner teams, and meet agreed support expectations. |
| MODERATE_GAP | POSTED_EXPECTATION |  | automation_workflows, python_scripting, javascript_scripting, powershell_bash | Bash, JavaScript/TypeScript, Python | Experience using basic scripting, such as Bash, Lua, Python, or JavaScript, and AI or agentic workflows to automate repeatable work, validate results, handle failures, and document how others can operate it. |

**Major currently-unproven requirements**

- 5+ years of experience implementing and troubleshooting enterprise AV systems, including installation, commissioning, and working from technical designs; hands-on experience with Logitech, Cisco, QSYS and Google Meet conferencing hardware.
- Experience configuring and troubleshooting wayfinding and conference room booking hardware, software, and room-resource integrations.

**Posted qualifications with direct work-evidence overlap**

- Hands-on expertise configuring, administering, and troubleshooting video conferencing platforms such as Google Meet, Zoom, and Microsoft Teams.
- Practical knowledge of enterprise networking, including IP addressing, VLANs, DNS, DHCP, and multicast, sufficient to diagnose AV connectivity and work effectively with Network Engineering.
- Experience deploying and troubleshooting AV over IP, including Q-LAN, Dante, and NDI.
- Experience configuring and troubleshooting systems in the Q-SYS control ecosystem.
- Experience applying AV build standards, validating system performance, and maintaining clear configuration and support documentation.
- Experience using IT ticketing systems to prioritize technical escalations, communicate with users and partner teams, and meet agreed support expectations.

**Apply:** https://jobs.ashbyhq.com/openai/0e76e8eb-cd22-43c8-a9d0-cc35a3b9cb08/application

### Senior Technical Program Manager - Security — Security

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `ADJACENT_PROGRAM_ROLE`
- **Location path:** `REMOTE_NOW_STRONG` — workplace_type=Remote and US - Remote appears in primary or secondary locations
- **Primary / secondary:** US - Remote / New York City, Seattle, Washington, DC, San Francisco
- **Work arrangement:** Remote; office days: not detected; relocation: no
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `MEDIUM`
- **Seniority burden:** `MODERATE`; max explicit years detected: 5
- **Requirement evidence:** direct=0, claimed-skill=0, adjacent=0, major gaps=2, moderate gaps=0
- **Salary:** USD 165400.0–285000.0 / 1 YEAR
- **Why this band:** 2 major currently-unproven requirement area(s); Strong current US-remote path

**Responsibilities excerpt**

- Drive execution of critical security and compliance programs such as vulnerability management, merger and acquisition security and integration, infrastructure hardening, and datacenter security management. You will need to deeply collaborate on technical architecture and resolve technical problems in partnership with engineering. - Partner with IT, Infrastructure, Application, Legal, Privacy, and Security teams to build scalable programs, and deliver critical security outcomes across multiple disciplines, including insider threat, information security, physical security, and information technology. - Establish scalable frameworks and build programs around critical security initiatives including vulnerability management, evidence collection, incident response coordination, supply chain risk management, and device security. - Track and enforce OpenAI’s privacy and security requirements by translating commitments into engineering milestones and driving their full implementation across systems. - Create and maintain program-level visibility across risk areas, security milestones, and cross-org dependencies—ensuring outcomes are delivered reliably and at high quality. - Communicate s…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are an empathetic communicator and leader—able to influence across technical and non-technical audiences, and build durable trust with partners. |
| MAJOR_GAP | POSTED_EXPECTATION | 5 | technical_program_delivery, security_engineering |  | Have 5+ years of experience leading complex technical programs focused on infrastructure security, data privacy, compliance, or enterprise platform capabilities. |
| MAJOR_GAP | POSTED_EXPECTATION |  | security_engineering |  | Are deeply fluent in the intersection of engineering systems, security controls, and regulatory expectations—and are able to bring clarity and structure across all three. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Thrive in high-trust environments, bring rigor and systems thinking to ambiguity, and operate with a bias for aligned execution over org boundaries. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Are structured, detail-oriented, and rigorous in ensuring quality, accountability, and durable delivery. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have a proven record of success driving highly cross-functional efforts across engineering, infrastructure, legal, compliance, and product stakeholders. |

**Major currently-unproven requirements**

- Have 5+ years of experience leading complex technical programs focused on infrastructure security, data privacy, compliance, or enterprise platform capabilities.
- Are deeply fluent in the intersection of engineering systems, security controls, and regulatory expectations—and are able to bring clarity and structure across all three.

**Apply:** https://jobs.ashbyhq.com/openai/c414f15f-60c4-40b5-a896-d2ad6c7f4415/application

### Vendor Security Technical Program Manager — Security

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `ADJACENT_PROGRAM_ROLE`
- **Location path:** `REMOTE_NOW_STRONG` — workplace_type=Remote and US - Remote appears in primary or secondary locations
- **Primary / secondary:** US - Remote / Seattle, San Francisco
- **Work arrangement:** Remote; office days: not detected; relocation: no
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `HIGH`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=2, claimed-skill=0, adjacent=3, major gaps=2, moderate gaps=1
- **Salary:** USD 231300.0–256500.0 / 1 YEAR
- **Why this band:** 2 major currently-unproven requirement area(s); 2 qualification item(s) map to direct work evidence; Strong current US-remote path

**Responsibilities excerpt**

- Own vendor security engagements from understanding the business need through scoping, assessment, decision, treatment, and reassessment when material facts change. Make assessment decisions independently and use judgment about when to involve peers, specialists, or leadership. Route formal exceptions and risk acceptance to the appropriate decision owners. - Understand vendor use cases, workflows, user journeys, data flows, identities, access, integrations, and supply-chain dependencies. Identify plausible attack paths and their consequences for OpenAI. - Assess relevant architectures, configurations, controls, logs, and operational practices. Test whether the evidence supports the security claims that matter to the engagement, and make gaps and uncertainty clear. - Develop practical treatments, including changes to the operating model, data exposure, access, architecture, vendor choice, controls, or containment. Drive implementation with the responsible owners and verify that the treatment works. - Build reusable security patterns with clear applicability, safeguards, evidence requirements, exceptions, and review triggers. - Work with Legal, Procurement, and vendors on security …

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MAJOR_GAP | POSTED_EXPECTATION |  | vendor_management, security_vendor_risk |  | Have independently assessed consequential third-party, supply-chain, or comparable security risks, and can apply that judgment to unfamiliar vendor technologies and operating models. |
| MAJOR_GAP | POSTED_EXPECTATION |  | api_integrations, identity_device_management, security_engineering | REST APIs | Understand security principles and controls, including data protection, access management, application security, prevention, detection, and response. Can reason about architecture, identity, APIs, data flows, logging, integrations, and whether controls work. |
| MODERATE_GAP | POSTED_EXPECTATION |  | security_vendor_risk |  | Know relevant frameworks and standards, including ISO 27001, NIST 800-53, and SOC 2, and can use them to inform an assessment of the actual engagement. |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | vendor_management |  | Have translated security findings and requirements into practical contractual positions with Legal, Procurement, and vendor representatives. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows, uat_qa_bug |  | Have delivered useful products or workflow improvements, tested expected behavior and failure cases, learned from users, and owned performance after launch. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | uat_qa_bug |  | Can use Codex or comparable AI-assisted development tools to build, run, inspect, and test working solutions. |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | technical_program_delivery |  | Have independently delivered cross-functional programs, turned ambiguity into technical requirements and plans, and adapted priorities to achieve measurable outcomes. Can judge when to build, use existing systems, or engage partners to resolve blockers. |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | vendor_management |  | Build constructive relationships with Security, Engineering, Product, Privacy, Legal, business teams, and vendors. Communicate complex security issues clearly in writing and conversation, including your recommendation, supporting evidence, and relevant tradeoffs. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Question assumptions, try thoughtful new approaches, investigate unfamiliar systems, and revise your judgment when new evidence changes the situation. |

**Major currently-unproven requirements**

- Have independently assessed consequential third-party, supply-chain, or comparable security risks, and can apply that judgment to unfamiliar vendor technologies and operating models.
- Understand security principles and controls, including data protection, access management, application security, prevention, detection, and response. Can reason about architecture, identity, APIs, data flows, logging, integrations, and whether controls work.

**Posted qualifications with direct work-evidence overlap**

- Have delivered useful products or workflow improvements, tested expected behavior and failure cases, learned from users, and owned performance after launch.
- Can use Codex or comparable AI-assisted development tools to build, run, inspect, and test working solutions.

**Apply:** https://jobs.ashbyhq.com/openai/3ae71c21-60dd-42b2-a913-58df05988976/application

### Technical Threat Investigator, Threat Intel Engineering — Security

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `SPECIALIST_ENGINEERING_STRETCH`
- **Location path:** `REMOTE_NOW_STRONG` — workplace_type=Remote and US - Remote appears in primary or secondary locations
- **Primary / secondary:** San Francisco / New York City, US - Remote
- **Work arrangement:** Remote; office days: not detected; relocation: yes
- **Sales classification:** `NO_SALES_SIGNAL_FOUND`
- **Technical core:** `HIGH`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=2, claimed-skill=1, adjacent=0, major gaps=3, moderate gaps=1
- **Salary:** USD 347000.0–510000.0 / 1 YEAR
- **Why this band:** 3 major currently-unproven requirement area(s); 2 qualification item(s) map to direct work evidence; Strong current US-remote path; Specialist engineering/research/security title is outside the strongest documented work-history lane

**Responsibilities excerpt**

- Conduct deep, end-to-end investigations into sophisticated threat actors interacting with OpenAI’s models, products, and broader ecosystem. - Think like an adversary — model attacker behavior, anticipate misuse patterns, and proactively hunt for, identify, and disrupt malicious activity. - Leverage internal telemetry, OSINT, vendor data, and in-house safety systems to produce high-confidence findings on adversarial use of our models in cyber operations, platform abuse, and threats targeting OpenAI. - Translate investigative findings into concrete improvements across detection, enforcement, intel, and safety pipelines. - Build tooling, scripts, automations, and agentic workflows that scale investigative throughput and reduce manual effort. - Prototype solutions in ambiguous and emerging problem spaces, including new product surfaces, novel attacker behaviors, and areas where existing coverage may be limited. - Partner closely with teams across Security, Safety Systems, Product Policy, and Integrity to operationalize findings and drive meaningful outcomes. - Produce clear, high-signal written outputs and recommendations that inform decision-making across technical and executive st…

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MAJOR_GAP | POSTED_EXPECTATION |  | troubleshooting_incidents, threat_intelligence_ir, offensive_security |  | Experience in threat intelligence, incident response, offensive security, or a closely related field. |
| MAJOR_GAP | POSTED_EXPECTATION |  | threat_intelligence_ir |  | Solid experience investigating sophisticated threat actors, including model misuse, platform abuse, or other adversarial activity in complex environments. |
| MAJOR_GAP | POSTED_EXPECTATION |  | threat_intelligence_ir |  | A strong understanding of adversary behavior, infrastructure, and tradecraft, and the ability to apply that understanding to proactive investigations. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Demonstrated ability to independently drive deep technical investigations from ambiguous signals through to clear, actionable findings. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Experience using AI to extend or accelerate investigative workflows. |
| CLAIMED_SKILL_MATCH | POSTED_EXPECTATION |  | automation_workflows, python_scripting |  | Strong scripting ability and comfort building lightweight automation, investigative tooling, or workflows that improve scale and repeatability. |
| MODERATE_GAP | POSTED_EXPECTATION |  | troubleshooting_incidents, sql_data, vendor_management, threat_intelligence_ir |  | Strong ability to leverage telemetry from diverse systems and vendors to drive investigations, including directly querying, extracting, and stitching together data where needed. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Strong written and verbal communication skills, especially the ability to translate technical investigations into high-signal outputs for diverse stakeholders. |
| UNCLASSIFIED_REQUIREMENT | EXPLICIT_REQUIREMENT |  |  |  | Comfort operating independently in ambiguous, fast-moving problem spaces with minimal oversight. This is a remote role with close collaboration required across teams in the US and UK. While the role is remote, regular in-person engagement with our San Francisco (SF) headquarters will be expected. Relocation assistance is available for candidates who wish to… |

**Major currently-unproven requirements**

- Experience in threat intelligence, incident response, offensive security, or a closely related field.
- Solid experience investigating sophisticated threat actors, including model misuse, platform abuse, or other adversarial activity in complex environments.
- A strong understanding of adversary behavior, infrastructure, and tradecraft, and the ability to apply that understanding to proactive investigations.

**Posted qualifications with direct work-evidence overlap**

- Experience using AI to extend or accelerate investigative workflows.
- Strong written and verbal communication skills, especially the ability to translate technical investigations into high-signal outputs for diverse stakeholders.

**Apply:** https://jobs.ashbyhq.com/openai/f01b7084-a68d-4e30-ace9-6b5e6d90c517/application


## Comparison benchmark dossiers

### Applied AI Engineer, Enterprise — Technical Success

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `SPECIALIST_ENGINEERING_STRETCH`
- **Location path:** `REMOTE_NEEDS_CONFIRMATION` — US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous
- **Primary / secondary:** San Francisco / New York City, US - Remote
- **Work arrangement:** Hybrid; office days: 3; relocation: yes
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `HIGH`
- **Seniority burden:** `UNKNOWN`; max explicit years detected: none
- **Requirement evidence:** direct=4, claimed-skill=0, adjacent=0, major gaps=2, moderate gaps=0
- **Salary:** USD 251000.0–278000.0 / 1 YEAR
- **Why this band:** 2 major currently-unproven requirement area(s); 4 qualification item(s) map to direct work evidence; Potential US-remote path needs confirmation; Specialist engineering/research/security title is outside the strongest documented work-history lane

**Responsibilities excerpt**

- Partner directly with enterprise customers to identify high-value opportunities and translate them into technical architectures, implementation plans, evaluation strategies, and measurable success criteria. - Design, build, and deploy AI systems that solve important customer problems and produce measurable business outcomes. - Work hands-on in code to build prototypes, evaluation harnesses, reference implementations, integrations, and production accelerators. - Make sound technical decisions across models, agents, retrieval, tools, data, reliability, observability, latency, cost, safety, security, and governance. - Diagnose complex implementation challenges, reproduce failures, test hypotheses, and drive blockers toward resolution. - Help customers progress from promising prototypes to reliable production systems, sustained adoption, and scaled impact. - Partner closely with customer engineering teams and OpenAI Product, Research, Engineering, Security, and go-to-market teams, translating deployment experience into high-signal product feedback. - Create reusable architectures, tooling, playbooks, and technical guidance that accelerate future enterprise deployments.

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MAJOR_GAP | POSTED_EXPECTATION |  | professional_software_engineering, ml_ai_engineering |  | Have a demonstrated track record of designing, building, and delivering AI or machine-learning systems in enterprise environments, including taking systems from prototype to production. Relevant backgrounds may include applied AI or ML engineering, forward-deployed engineering, software engineering, customer engineering, solutions architecture, or technical… |
| DIRECT_MATCH | POSTED_EXPECTATION |  | troubleshooting_incidents, uat_qa_bug |  | Can point to substantial personal contributions in code, architecture, evaluation, debugging, or production engineering—not only program or stakeholder management. |
| MAJOR_GAP | POSTED_EXPECTATION |  | python_scripting, javascript_scripting, ml_ai_engineering | JavaScript/TypeScript, Python | Are highly proficient in Python and comfortable working across an AI application stack; experience with JavaScript, TypeScript, or another relevant language is valuable. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Understand how to evaluate AI systems systematically using representative data, graders, production signals, and human judgment. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | api_integrations |  | Have navigated enterprise production requirements such as integrations, reliability, observability, security, privacy, data governance, performance, and cost. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | automation_workflows |  | Can connect technical decisions to customer workflows, adoption, and measurable business outcomes. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Communicate with clarity and credibility across hands-on engineers, technical leaders, security teams, product leaders, and executives. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Bring high agency, strong technical judgment, and end-to-end ownership in ambiguous environments. |
| UNCLASSIFIED_REQUIREMENT | EXPLICIT_REQUIREMENT |  |  |  | Learn quickly, challenge assumptions constructively, and collaborate with humility; experience in a particular industry or with OpenAI products is not required. |

**Major currently-unproven requirements**

- Have a demonstrated track record of designing, building, and delivering AI or machine-learning systems in enterprise environments, including taking systems from prototype to production. Relevant backgrounds may include applied AI or ML engineering, forward-deployed engineering, software engineering, customer engineering, solutions architecture, or technical consulting.
- Are highly proficient in Python and comfortable working across an AI application stack; experience with JavaScript, TypeScript, or another relevant language is valuable.

**Posted qualifications with direct work-evidence overlap**

- Can point to substantial personal contributions in code, architecture, evaluation, debugging, or production engineering—not only program or stakeholder management.
- Have navigated enterprise production requirements such as integrations, reliability, observability, security, privacy, data governance, performance, and cost.
- Can connect technical decisions to customer workflows, adoption, and measurable business outcomes.
- Communicate with clarity and credibility across hands-on engineers, technical leaders, security teams, product leaders, and executives.

**Apply:** https://jobs.ashbyhq.com/openai/01091aed-427d-4e10-8cdb-fb500cf55bb9/application

### Early Access Deployment Engineer — Technical Success

- **Decision band:** `C_STRETCH_REVIEW`
- **Career lane:** `ADJACENT_TECHNICAL`; title alignment: `SPECIALIST_ENGINEERING_STRETCH`
- **Location path:** `RELOCATION_SUPPORTED` — US office location with explicit relocation-assistance wording
- **Primary / secondary:** San Francisco / none
- **Work arrangement:** Hybrid; office days: 3; relocation: yes
- **Sales classification:** `REVIEW_SALES_CONTEXT`
- **Technical core:** `HIGH`
- **Seniority burden:** `MODERATE`; max explicit years detected: 4
- **Requirement evidence:** direct=1, claimed-skill=0, adjacent=1, major gaps=3, moderate gaps=0
- **Salary:** USD 250000.0–330000.0 / 1 YEAR
- **Why this band:** 3 major currently-unproven requirement area(s); 1 qualification item(s) map to direct work evidence; Explicit relocation assistance; Specialist engineering/research/security title is outside the strongest documented work-history lane

**Responsibilities excerpt**

- Engage deeply with strategic customers during the earliest alpha stages to understand their goals, workflows, technical constraints, and highest-value opportunities. - Translate emerging and ambiguous model capabilities into scoped use cases, working prototypes, and clear success criteria. - Prototype rapidly with customers, Product, and Research through experiment-driven iteration. - Design and support evaluations that reveal model behavior, solution quality, workflow impact, and failure modes. - Evaluate and troubleshoot based feedback across product, model behavior to determine patterns and gaps - Own early access program execution end to end, from customer onboarding and live experimentation through synthesis and launch decisions. - Align Research, Product, Engineering, GTM, Legal, Security, Marketing, and launch teams by communicating risks, tradeoffs, and recommendations clearly. - Codify architectures, evaluation methods, technical patterns, and program learnings into reusable playbooks that improve future deployments.

**Qualification-by-qualification evidence map**

| classification | strength | years | domains | technologies | requirement |
| --- | --- | --- | --- | --- | --- |
| MAJOR_GAP | POSTED_EXPECTATION | 4 | technical_customer_communication, professional_software_engineering, production_system_ownership |  | Have 4+ years of software engineering or equivalent technical experience, including meaningful customer-facing delivery and ownership of production systems. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Have a track record of rapidly turning ambiguous ideas into working prototypes and carrying the strongest approaches through to reliable solutions. Can demonstrate examples of systems thinking. |
| MAJOR_GAP | POSTED_EXPECTATION |  | python_scripting, javascript_scripting, web_frontend, enterprise_customer_delivery, cloud_infrastructure | JavaScript/TypeScript, Python | Be proficient in Python and/or JavaScript or TypeScript, comfortable across modern front-end and back-end development, and familiar with cloud deployment. |
| MAJOR_GAP | POSTED_EXPECTATION |  | uat_qa_bug, ml_ai_engineering |  | Bring practical AI and LLM depth, including experience reasoning about model behavior, designing evaluations, and building production-oriented AI applications. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Exercise strong product and customer judgment by identifying the highest-value problem, scoping the right experiment, separating signal from noise, and balancing speed with technical integrity. |
| UNCLASSIFIED_REQUIREMENT | POSTED_EXPECTATION |  |  |  | Own problems end to end, learn unfamiliar technical or domain concepts quickly, and impose useful structure without waiting for perfect information. |
| ADJACENT_MATCH | POSTED_EXPECTATION |  | enterprise_customer_delivery |  | Manage several high-stakes technical engagements at once while anticipating blockers, adapting plans, and maintaining momentum across customers and internal teams. |
| DIRECT_MATCH | POSTED_EXPECTATION |  | technical_customer_communication |  | Communicate complex ideas with clarity and empathy, challenge assumptions constructively, and build trust with technical and non-technical stakeholders. |

**Major currently-unproven requirements**

- Have 4+ years of software engineering or equivalent technical experience, including meaningful customer-facing delivery and ownership of production systems.
- Be proficient in Python and/or JavaScript or TypeScript, comfortable across modern front-end and back-end development, and familiar with cloud deployment.
- Bring practical AI and LLM depth, including experience reasoning about model behavior, designing evaluations, and building production-oriented AI applications.

**Posted qualifications with direct work-evidence overlap**

- Communicate complex ideas with clarity and empathy, challenge assumptions constructively, and build trust with technical and non-technical stakeholders.

**Apply:** https://jobs.ashbyhq.com/openai/ee6b7ece-ffcb-4546-8b4c-ef755ec21c14/application

