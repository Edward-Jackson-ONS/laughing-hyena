# Auto-updating a build and scheduling container execution
## Example of triggering a Cloud Build job using Cloud SDK
A build or rebuild of the docker image (stored in Artifact Registry) will be automatically triggered when code is pushed to the specified branch.

```bash
gcloud builds triggers create github \
--name=name-of-trigger \
--region=europe-west2 \
--repo-name=name-of-repo \
--repo-owner=name-of-repo-owner \
--branch-pattern=^main$ \
--build-config=Dockerfile \
--include-logs-with-status
```

`--name` is the name you wish to give your trigger job.
`--branch-pattern` is the branch name from which to build (with ^...$ regex bounds)

N.B. The trigger can be deleted as follows:
```bash
gcloud builds triggers delete name-of-trigger \
--region=europe-west2
```


## Example of scheduling a Cloud Run job using Cloud SDK

```bash
gcloud scheduler jobs create http name-of-schedule-job \
--location=europe-west2 \
--schedule='0 6 * * 2-6' \
--uri=https://europe-west2-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/project-name/jobs/cloud-run-job-name:run
```

`--uri` is the full URL of the Cloud Run job, exposing region, project name and Cloud Run job name.

Jobs can be paused and deleted as follows:

```bash
gcloud scheduler jobs pause name-of-schedule-job \
--location="europe-west2"

gcloud scheduler jobs delete name-of-schedule-job \
--location="europe-west2"
```