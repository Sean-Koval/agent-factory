# agent-factory-database (database repo): none in v1

The four-repo convention has a database repo for services with a schema of their own. The factory has none yet:
hangar keeps its state in one SQLite file on a persistent volume (one replica), backed up with `hangar admin backup`. So
the factory's own change-set profile (`agent-factory-deploy/policy/changesets/agent-factory.yaml`) has three roles:
infra, code and deploy.

When hangar moves to a managed database, this directory becomes that repo: migrations, a `make migrate-up test
migrate-down` verify against a database service in the sandbox (`role-database` in the team harness), and
`self_approval: never` in its repo policy. A service's database repo looks like that today; see
`policy/repos/example-service-db.yaml`.
