# Future AWS Architecture Plan

## Status

This is a future production plan, not an MVP build requirement. The locally hosted MVP must remain portable and must not require AWS services to run.

## Proposed production topology

- **Route 53:** DNS.
- **CloudFront + AWS WAF:** edge delivery and baseline request protection.
- **Application Load Balancer:** routes HTTPS traffic to the web service.
- **ECS on Fargate:** runs separate Django web, Celery worker, and Celery Beat services from the same versioned image.
- **Amazon ECR:** stores signed/versioned container images.
- **Amazon RDS for PostgreSQL:** Multi-AZ system of record, encryption, automated backups, and point-in-time recovery.
- **Amazon ElastiCache for Redis:** Celery broker and ephemeral coordination in private subnets.
- **AWS Secrets Manager:** Google, OpenAI, database, and application secrets with rotation procedures.
- **AWS KMS:** encryption keys for secrets, database, backups, logs, and application-level credential envelopes.
- **Amazon S3:** encrypted export/backup artifacts only when a product need is approved; do not use it as an uncontrolled email dump.
- **CloudWatch:** service logs, metrics, dashboards, and alarms.
- **AWS CloudTrail:** infrastructure control-plane audit.
- **Amazon SES:** only for a later approved notification capability; not part of the MVP.

## Network boundaries

- One VPC across at least two availability zones.
- Public subnets contain only the load balancer and required managed ingress.
- Django, workers, scheduler, RDS, and Redis run in private subnets.
- Security groups allow only required service-to-service paths.
- Database and Redis have no public ingress.
- NAT or controlled egress permits Google and selected model-provider APIs.
- Add VPC endpoints for supported AWS control-plane services where useful.

## Environments

- Separate AWS accounts or strongly isolated accounts/projects for development, staging, and production.
- Separate databases, queues, secrets, encryption keys, OAuth clients, and model credentials.
- No production email content in lower environments.
- Infrastructure defined as code before the first hosted environment.

## Deployment path

1. Containerize and verify the local topology.
2. Create infrastructure-as-code modules for network, data, compute, secrets, and observability.
3. Deploy an empty development environment.
4. Run migrations as a controlled one-off task.
5. Deploy web and worker services with health checks.
6. Validate OAuth callbacks, queue behavior, retention, deletion, and tenant isolation.
7. Create staging with synthetic email fixtures only.
8. Run security, restore, load, and failure tests.
9. Approve production readiness through a separate release gate.

## Scaling model

- Scale Django on request concurrency and latency.
- Scale workers on queue depth and job age.
- Keep exactly one active logical Beat scheduler or use a lease/leader mechanism.
- Apply per-workspace and per-provider rate limits.
- Separate queues by workload class before splitting services.
- Add read replicas or vector infrastructure only after measured need.

## Data protection and recovery

- Encrypt RDS, Redis, EBS/container scratch, S3, logs, and backups.
- Use point-in-time recovery for PostgreSQL.
- Define and test restore procedures before production.
- Ensure retention deletion propagates to active data and expires from backups according to documented backup lifecycle.
- Define target RPO/RTO before choosing final backup and Multi-AZ policy.
- Record administrative access and use short-lived credentials.

## Production gates

- Verified tenant-isolation tests
- Google OAuth production verification as applicable
- Privacy policy and data-processing disclosures
- Model-provider data-handling review
- Secrets rotation and incident runbooks
- Backup restoration exercise
- Load and queue recovery tests
- Dependency/container vulnerability checks
- Deletion and retention evidence
- Monitoring and on-call ownership

## Decisions deferred until hosting work begins

- AWS region and residency commitments
- ECS versus EKS; ECS/Fargate is the default unless requirements justify Kubernetes
- Exact RDS and Redis sizing
- Cross-region disaster recovery
- Observability vendor beyond CloudWatch
- Private model connectivity for on-prem or customer VPC deployments

