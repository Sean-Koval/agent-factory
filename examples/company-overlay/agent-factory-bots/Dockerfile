# The factory's hangar image: hangar's release by digest, this company's plugins, and the team harness's
# environments, each pinned. CI builds it on every merge and tags it with the merge commit; the deploy repo pins the
# result by digest (agent-factory-deploy overlays/*/kustomization.yaml).
FROM ghcr.io/sean-koval/hangar@sha256:HANGAR_IMAGE_DIGEST

# Company plugins (entry-point group hangar.plugins). Installed is not enabled: HANGAR_PLUGINS.enable names them.
COPY plugins/ /tmp/plugins/
RUN python -m pip install --no-cache-dir --no-deps -r /tmp/plugins/requirements.txt && rm -rf /tmp/plugins

# The company's fork of the team harness, as a git submodule pinned to a reviewed commit: the role environments and
# the work-default harness, listed in HANGAR_ENV_DIRS.
COPY team-harness/environments/ /opt/team-harness/environments/
COPY team-harness/harnesses/work-default/ /opt/team-harness/harnesses/work-default/
