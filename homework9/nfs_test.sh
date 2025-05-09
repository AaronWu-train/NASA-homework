#!/usr/bin/env bash
set -euo pipefail

USAGE="$(basename "$0") <mode> [arguments...]

Modes:
  single   <output_file> <log_file>
  parallel <hosts_file> <prefix> <log_dir>

Examples:
  # Single Mode
  ./nfs_test.sh single /mnt/nfs-share/test.dd single.log

  # Parallel mode
  ./nfs_test.sh parallel hosts.txt nfs_test perflogs
"

if [[ $# -lt 1 ]]; then
    echo "$USAGE" >&2
    exit 1
fi

mode=$1
shift

run_single() {
    local outfile=$1 logfile=$2
    mkdir -p "$(dirname "$logfile")"
    echo "Start Single Mode."
    echo "outfile: $outfile logfile: $logfile"
    echo "Waiting..."
    {
        echo "=== Writing ==="
        echo
        /usr/bin/time -v dd if=/dev/zero of="$outfile" bs=1G count=1 oflag=direct
        echo
        echo "=== Reading ==="
        echo
        /usr/bin/time -v dd if="$outfile" of=/dev/null bs=1G count=1 iflag=direct
    } &>"$logfile"
    echo "Results saved to $logfile"
}

run_parallel() {
    local hosts_file=$1 prefix=$2 logdir=$3
    mkdir -p "$logdir"/out "$logdir"/err

    # pssh 自動併發到 hosts_file 裡的 user@host
    parallel-ssh -h "$hosts_file" -P -A -t 600 \
        -o "$logdir"/out -e "$logdir"/err \
        "/usr/bin/time -v dd if=/dev/zero of=/mnt/nfs-share/${prefix}-\$(hostname)-\$(whoami).dd bs=1G count=1 oflag=direct && \
     /usr/bin/time -v dd if=/mnt/nfs-share/${prefix}-\$(hostname)-\$(whoami).dd of=/dev/null bs=1G count=1 iflag=direct"

    echo "Parallel runs dispatched."
    echo "  stdout logs: $logdir/out/"
    echo "  stderr logs: $logdir/err/"
}

case "$mode" in
single)
    if [[ $# -ne 2 ]]; then
        echo "Error: single mode needs 2 args" >&2
        echo "$USAGE" >&2
        exit 1
    fi
    run_single "$1" "$2"
    exit 0
    ;;
parallel)
    if [[ $# -ne 3 ]]; then
        echo "Error: parallel mode needs 3 args" >&2
        echo "$USAGE" >&2
        exit 1
    fi
    run_parallel "$1" "$2" "$3"
    exit 0
    ;;
*)
    echo "Error: unknown mode '$mode'" >&2
    echo "$USAGE" >&2
    exit 1
    ;;
esac
