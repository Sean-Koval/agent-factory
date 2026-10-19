# agent-factory-bots (code repo, template)

The factory's own code, all of it company-side: the hangar image this company runs, the plugins it adds, and the
Symphony bot. Nothing here changes hangar; it builds on hangar's released image and its plugin surface.

```text
Dockerfile                    FROM ghcr.io/sean-koval/hangar@sha256:…, plus plugins/ and the team harness's environments
plugins/
  requirements.txt            every plugin the image installs, pinned
  hangar-example-bump/        a deliverer: points a kustomize overlay at the image a change set built
team-harness/                 git submodule: the company's fork of the team harness, at a reviewed commit
symphony-bot/                 copied from agent-factory examples/symphony-bot, with this company's config.yaml
```

## Build and pin

CI builds the image on every merge to `main` and tags it with the merge commit
(`registry.example.com/agent-factory/hangar:<merge sha>`). The factory's change-set profile
(`agent-factory-deploy/policy/changesets/agent-factory.yaml`) waits for that tag (`image-ready`), then its deliverer,
`example-kustomize-bump` from `plugins/hangar-example-bump`, opens the deploy PR that pins the new digest in
`overlays/dev`. Prod is a person copying that digest.

## Plugins

A plugin is a Python package with a `hangar.plugins` entry point whose object has `name`, `api =
"hangar.plugin/v1"`, a `Settings` model and `register(host, settings)`; `register` calls `host.add_door`,
`add_notifier`, `add_tracker` or `add_deliverer`. Installing one does nothing until `HANGAR_PLUGINS.enable` names it in
the deploy repo, and a bad setting stops hangar from starting rather than running half-configured. Secrets in
settings are credential names only. A sign-in plugin (`hangar-<company>-auth`, for your IdP) would live here too.

## The Symphony bot

Copy `examples/symphony-bot/` from agent-factory into `symphony-bot/`, fill in `config.yaml` (pod, bot account,
hangar URL, credential names) and deploy it as its own Deployment next to hangar. It needs a hangar token with the
relay scope and the webhook key `bot-hook-key` (both from your secret manager). Its tests run with the stdlib only:
`python -m unittest discover -s symphony-bot/tests`.
