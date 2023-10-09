# Optimizing the cloning process using multiprocessing

## Usage
```
$ python3 single_thread.py
# OR
$ python3 single_thread.py [specify num_processes here]
```
## Summary of the cloning scripts
* Environment variables consist up **github username and token**, **name of parent repo of all cloned repo**, **error log file**, **hashes file**, **start and end date**
* First up the list of distinct_packages are created by the query "SELECT DISTINCT Package FROM Publish_Packages"
* Then for each package, first it checks whether it is cloned already. If not, then it checks if the URL for the vcs of the package exists. If it does and it contains the string "salsa.debian.org", it clones the repo.
* Multithreading is implemented using python's multiprocess module. I split the list of packages into sublists and ran the cloning processes on each sublist.

*Note*: The check for cloned repo using 'os.path.exists()' somehow doesn't work, so I use subprocess to execute 'ls' and check for the result code instead.

## Current results and observation
### As of October 9th
* Method of comparison: I **ran both scripts for 5 minutes**. single_thread.py has a built-in timer to stop at the 5 minute mark, while for the other I manually Ctrc+C after 5 minutes. For multi_process.py, I **ran with 4, 8, 16 scores**. I tested several times and **in the environment no repos were cloned previously**. I **measured the cloning speed using the result from the 'du -sh' command**. I **wasn't using git credentials** when testing this. Here's the result:

| Num_processes       | 1      | 4      | 8      |
|---------------------|--------|--------|--------|
| Size of clone_repos | ~650MB | ~3.6GB | ~5.3GB |

* Observation: Multithread does increase the cloning speed greatly. However, when I'm about to test for 16 processes I got 429 from server. It seems like the server has rate-limiting. This could be problematic if we're cloning a large number of repos continuosly.

## TO-DO
### As of October 9th
* Investigate the cause of 429 and rate-limiting rules on the server side.
* Implement remediation for 429 cases.
* Run the test for a longer interval to confirm previous conclusions.
