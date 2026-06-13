---
layout: default
title: Testing: running your first job
---

Before submitting any work, verify that the cluster is healthy and all nodes are visible to
the scheduler.

## Check cluster status

From the login node, run:

```bash
sinfo
```

You should see your compute node listed as `idle`:

```text
PARTITION        AVAIL  TIMELIMIT  NODES  STATE NODELIST
pixiecluster*       up   infinite      1   idle pixie02
```

If the node shows `down` or `unknown`, check that `slurmd` is running on the compute node:

```bash
ssh pixie02 systemctl status slurmd
```

## Submit a minimal batch job

Create a file called `hello.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=hello
#SBATCH --output=hello-%j.out
#SBATCH --ntasks=1

echo "Hello from $(hostname) at $(date)"
```

Submit it:

```bash
sbatch hello.sh
```

Slurm will print a job ID, e.g. `Submitted batch job 1`.

## Check job status

```bash
squeue
```

While the job is running you will see it listed. Once it completes the queue will be empty.
Check the output file (replace `1` with your job ID):

```bash
cat hello-1.out
```

Expected output:

```text
Hello from pixie02 at Fri Jun 13 10:00:00 BST 2026
```

The hostname should be your compute node, not the login node.

## Run an interactive job

For debugging it is often useful to get a shell directly on a compute node:

```bash
srun --pty bash
```

Your prompt will change to reflect the compute node hostname. Type `exit` to return to the
login node.

## Test the shared filesystem

Jobs can read and write to `/sharedfs` from any node. Verify this round-trips correctly:

```bash
#!/bin/bash
#SBATCH --job-name=sharedfs-test
#SBATCH --output=sharedfs-%j.out
#SBATCH --ntasks=1

echo "written by $(hostname)" > /sharedfs/test.txt
cat /sharedfs/test.txt
```

After the job completes, confirm the file is visible from the login node:

```bash
cat /sharedfs/test.txt
```

## Test a multi-node job

If you have more than one compute node, verify that Slurm can span them:

```bash
#!/bin/bash
#SBATCH --job-name=multinode
#SBATCH --output=multinode-%j.out
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=2

srun hostname
```

The output file should contain one line per node.
