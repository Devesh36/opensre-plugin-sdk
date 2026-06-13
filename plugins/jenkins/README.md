# opensre-plugin-jenkins

Bridged OpenSRE **jenkins** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `JENKINS_URL`

## Tools

- `get_jenkins_build_log`
- `get_jenkins_pipeline_stages`
- `list_jenkins_builds`
- `list_jenkins_jobs`
- `list_jenkins_running_builds`

## Install

```bash
pip install -e plugins/jenkins
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/jenkins
```
