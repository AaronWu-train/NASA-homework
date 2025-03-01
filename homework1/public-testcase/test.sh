#!/usr/bin/env bash

usage() {
    cat <<EOF
Usage: $0 <script-to-test> <test-directory>

Arguments:
  <script-to-test>  Path to your merkle-dir.sh script.
  <test-directory>  Path to 1/, 2/, 3/, or 4/ in the same directory as this script.

Example:
  $0 ./merkle-dir.sh ${0%/*}/1
EOF
    exit 1
}

run_command(){
    local arg="$1"
    local output="$(echo -n "$arg" | sed -n 's/.*--output \([^ ]*\).*/\1/p')"

    echo -e "arg:\n$arg"
    echo "stdout:"
    read -a args_array <<< "$arg"
    $SCRIPT "${args_array[@]}" &
    local pid=$!

    (sleep $TIMEOUT && kill -0 $pid 2>/dev/null && kill $pid) &
    timeout_pid=$!

    wait $pid
    local exit_status=$?
    kill $timeout_pid 2>/dev/null
    echo -e "exit status:\n$exit_status"

    if test "$exit_status" -eq 0 && test -n "$output"; then
        echo "output_file:"
        cat "$output" 2>/dev/null || echo "ERROR: file not found"
    fi
}

if [[ $# -ne 2 ]]; then
    echo "ERROR: Incorrect number of arguments."
    usage
fi

TIMEOUT=60
TESTDIR="$2"
SCRIPT="$(realpath -m "$1" --relative-to "$TESTDIR")"
OLDPWD="$PWD"
cd "$TESTDIR"

input_file="input"
expected_output_dir="output"
output_dir="your_output"

if [ -d "$output_dir" ]; then
    echo "WARNING: Removing all files in $(realpath -m "$output_dir" --relative-to "$OLDPWD")..."
    rm -f "$output_dir"/*
else
    mkdir -p "$output_dir"
fi

test_group=""
declare -a group_names=()
declare -a scores=()
passed_tests=0
total_tests=0
testname=1

while IFS= read -r line; do
    if [[ -z "$line" ]]; then
        continue
    fi

    if [[ "$line" =~ ^#\ TEST\ GROUP:\ (.*) ]]; then
        if test -n "$test_group"; then
            scores+=("$passed_tests/$total_tests")
            group_names+=("$test_group")
        fi
        test_group="${BASH_REMATCH[1]}"
        passed_tests=0
        total_tests=0
        echo "=== Running Test Group: $test_group ==="
        continue
    fi

    arg="$line"
    output_file="$output_dir/$testname.out"
    output_file_expected="$expected_output_dir/$testname.out"

    echo -n "Test $(basename $TESTDIR)-$testname: "
    run_command "$arg" > "$output_file"

    if ! diff -q "$output_file" "$output_file_expected" >/dev/null 2>&1; then
        echo "FAILED"
        #diff "$output_file" "$output_file_expected"
    else
        echo "PASSED"
        ((passed_tests++))
    fi
    ((total_tests++, testname++))
done < "$input_file"

if test -n "$test_group"; then
    scores+=("$passed_tests/$total_tests")
    group_names+=("$test_group")
fi

echo "=== Result ==="
for i in "${!scores[@]}"; do
    echo "${group_names[$i]}: ${scores[$i]}"
done
