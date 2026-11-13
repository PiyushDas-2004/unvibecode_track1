"""Run a command, tee its output to a log, and record wall time + peak child RSS.
Usage: python measure.py LOGFILE -- cmd args...
"""
import resource, subprocess, sys, time, datetime
log = sys.argv[1]; cmd = sys.argv[sys.argv.index('--') + 1:]
start = time.monotonic(); t0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
with open(log, 'w') as f:
    f.write(f"# started_utc: {t0}\n# command: {' '.join(cmd)}\n")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in p.stdout:
        f.write(line); f.flush()
    rc = p.wait()
    wall = time.monotonic() - start
    rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    f.write(f"\n# exit_code: {rc}\n# wall_seconds: {wall:.1f}\n# peak_child_rss_kb: {rss}\n")
print(f"exit={rc} wall={wall:.1f}s peak_rss_kb={rss}")
