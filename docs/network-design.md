# Network Routing Design

## Public Subnets
- Route `0.0.0.0/0` through the Internet Gateway (IGW).
- Used for internet-facing resources (e.g., ALB).

## Private Subnets (Current State)
- **Decision:** Isolated Subnet.
- No default route to the internet or NAT Gateway.
- **Reasoning:** The initial workload in the private subnet is a database tier. Databases do not require outbound internet access to function. This provides maximum network isolation and avoids unnecessary NAT Gateway costs.

## Future considerations
If application workloads are added to the private subnets and require external API access, a NAT Gateway will be introduced with explicit documentation of the cost and architectural trade-offs.