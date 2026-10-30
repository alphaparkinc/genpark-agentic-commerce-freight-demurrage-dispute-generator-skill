# Ocean Freight Demurrage OSRA-22 Dispute Dismissal Generator Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Ocean Shipping Reform Act (OSRA-22) detention invoice validator, port appointment unavailability dispute generator, and FMC § 41104 charge dismissal packet compiler. Built for GenPark (https://www.genpark.ai).

## Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## MCP Tools Exposed
- `audit_demurrage_appointment_unavailability`: Prove container demurrage fees were unlawfully assessed during periods when marine terminal had zero truck gate appointments.
- `generate_fmc_inaccurate_invoice_charge_complaint`: Generate formal FMC 46 C.F.R. § 541 complaint seeking full dismissal and statutory civil penalties against ocean carrier.

## Installation & Usage
```bash
python -m genpark_agentic_commerce_freight_demurrage_dispute_generator_skill.server --test
```
