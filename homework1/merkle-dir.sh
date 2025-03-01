#! /usr/bin/bash

usage='merkle-dir.sh - A tool for working with Merkle trees of directories.

Usage:
  merkle-dir.sh <subcommand> [options] [<argument>]
  merkle-dir.sh build <directory> --output <merkle-tree-file>
  merkle-dir.sh gen-proof <path-to-leaf-file> --tree <merkle-tree-file> --output <proof-file>
  merkle-dir.sh verify-proof <path-to-leaf-file> --proof <proof-file> --root <root-hash>

Subcommands:
  build          Construct a Merkle tree from a directory (requires --output).
  gen-proof      Generate a proof for a specific file in the Merkle tree (requires --tree and --output).
  verify-proof   Verify a proof against a Merkle root (requires --proof and --root).

Options:
  -h, --help     Show this help message and exit.
  --output FILE  Specify an output file (required for build and gen-proof).
  --tree FILE    Specify the Merkle tree file (required for gen-proof).
  --proof FILE   Specify the proof file (required for verify-proof).
  --root HASH    Specify the expected Merkle root hash (required for verify-proof).

Examples:
  merkle-dir.sh build dir1 --output dir1.mktree
  merkle-dir.sh gen-proof file1.txt --tree dir1.mktree --output file1.proof
  merkle-dir.sh verify-proof dir1/file1.txt --proof file1.proof --root abc123def456'

writable() {
    if [[ -d "$1" || -L "$1" ]]; then
        return 1
    fi
    if [[ ! -e "$1" || (-f "$1" && -w "$1") ]]; then
        return 0
    fi
    return 1
}

process_build() {
    mapfile -t files < <(find "$1" -type f | LC_COLLATE=C sort)
    printf "%s\n" "$(realpath -s --relative-to="$1" "${files[@]}")"

    printf "\n"

    arr=()
    for file in "${files[@]}"; do
        arr+=("$(sha256sum "$file" | awk '{print $1}')")
    done

    for ((i = 0; i < ${#arr[@]}; i++)); do
        if [[ $i -eq 0 ]]; then
            printf "%s" "${arr[$i]}"
        else
            printf ":%s" "${arr[$i]}"
        fi
    done
    printf "\n"

    while [[ ${#arr[@]} -gt 1 ]]; do
        newarr=()
        for ((i = 0; i < ${#arr[@]}; i += 2)); do
            local j=$((i + 1))
            if [[ $j -lt ${#arr[@]} ]]; then
                local tmp="${arr[$i]}${arr[$j]}"
                local tmpH
                tmpH="$(echo -n "$tmp" | xxd -r -p | sha256sum | awk '{print $1}')"
                [[ $i -gt 1 ]] && echo -n ":"
                printf "%s" "$tmpH"
                newarr+=("$tmpH")
            else
                newarr+=("${arr[$i]}")
            fi
        done
        printf "\n"
        arr=("${newarr[@]}")
    done
}

build() {
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
        '--output')
            if [[ "$#" -lt 2 ]]; then
                echo "$usage"
                exit 1
            fi
            output="$2"
            shift 2
            ;;
        *)
            if [[ -z "$directory" ]]; then
                directory="$1"
                shift
            else
                echo "$usage"
                exit 1
            fi
            ;;
        esac
    done

    if [[ -z "$output" || -z "$directory" ]]; then
        echo "$usage"
        exit 1
    fi

    if ! writable "$output"; then
        echo "$usage"
        exit 1
    fi

    if [[ ! -d "$directory" || -L "$directory" ]]; then
        echo "$usage"
        exit 1
    fi

    process_build "$directory" >"$output"
}

process_gen_proof() {
    leaf_path="$1"
    tree_file="$2"
    reading_first_part=true
    n=0

    while IFS= read -r line; do
        if [ -z "$line" ]; then
            reading_first_part=false

            if [[ -z "$pos" ]]; then
                return 1
            fi

            printf "leaf_index:%s,tree_size:%s\n" "$((pos + 1))" "$n"
            continue
        fi

        if $reading_first_part; then
            if [[ "$leaf_path" = "$line" ]]; then
                pos=$n
            fi
            n=$((n + 1))
        else
            IFS=":" read -ra parts <<<"$line"

            if [[ -n $tmp ]]; then
                parts+=("$tmp")
            fi

            if [[ $n -gt 1 && $((pos ^ 1)) -lt $n ]]; then
                echo "${parts[$((pos ^ 1))]}"
            fi
            if [[ $((n % 2)) -gt 0 ]]; then
                tmp="${parts[$((n - 1))]}"
            else
                tmp=""
            fi

            n=$(((n + 1) / 2))
            pos=$((pos / 2))
        fi
    done <"$tree_file"
    return 0
}

gen_proof() {
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
        '--output')
            if [[ "$#" -lt 2 ]]; then
                echo "$usage"
                exit 1
            fi
            output_file="$2"
            shift 2
            ;;
        '--tree')
            if [[ "$#" -lt 2 ]]; then
                echo "$usage"
                exit 1
            fi
            tree_file="$2"
            shift 2
            ;;
        *)
            if [[ -z "$argument" ]]; then
                argument="$1"
                shift
            else
                echo "$usage"
                exit 1
            fi
            ;;
        esac
    done

    # loss options or argument
    if [[ -z "$output_file" ]] || [[ -z "$tree_file" ]] || [[ -z "$argument" ]]; then
        echo "$usage"
        exit 1
    fi

    # file1 exist and not regular file
    if [[ -e $output_file && ! -f $output_file || -L $output_file ]]; then
        echo "$usage"
        exit 1
    fi

    # file2 not regular file
    if [[ ! -f $tree_file || -L $tree_file ]]; then
        echo "$usage"
        exit 1
    fi

    if ! process_gen_proof "$argument" "$tree_file" >"$output_file"; then
        echo "ERROR: file not found in tree"
        exit 1
    else
        exit 0
    fi
}

process_verify_proof() {
    leaf_file="$1"
    proof_file="$2"
    root_hash="$(echo "$3" | awk '{print tolower($0)}')"

    h="$(sha256sum "${leaf_file}" | awk '{print $1}')"

    while IFS= read -r line; do
        if [[ -z $FIRST_LINE ]]; then
            FIRST_LINE=48763
            k=$(echo "$line" | awk -F'[:,]' '{print $2}')
            n=$(echo "$line" | awk -F'[:,]' '{print $4}')
            k=$((k - 1))
            n=$((n - 1))
        else
            if [[ $n -eq 0 ]]; then
                echo "Verification Failed"
                exit 1
            fi

            if [[ $((k & 1)) -gt 0 || $k -eq $n ]]; then
                local tmp="${line}${h}"
                h="$(echo -n "$tmp" | xxd -r -p | sha256sum | awk '{print $1}')"
                while [[ $((k & 1)) -eq 0 ]]; do
                    k=$((k / 2))
                    n=$((n / 2))
                done
            else
                local tmp="${h}${line}"
                h="$(echo -n "$tmp" | xxd -r -p | sha256sum | awk '{print $1}')"
            fi
            k=$((k / 2))
            n=$((n / 2))
        fi
    done <"$proof_file"

    if [[ $n -eq 0 && "$h" = "${root_hash}" ]]; then
        echo "OK"
        exit 0
    else
        echo "Verification Failed"
        exit 1
    fi
}

verify_proof() {
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
        '--proof')
            if [[ "$#" -lt 2 ]]; then
                echo "$usage"
                exit 1
            fi
            proof="$2"
            shift 2
            ;;
        '--root')
            if [[ "$#" -lt 2 ]]; then
                echo "$usage"
                exit 1
            fi
            root="$2"
            shift 2
            ;;
        *)
            if [[ -z "$argument" ]]; then
                argument="$1"
                shift
            else
                echo "$usage"
                exit 1
            fi
            ;;
        esac
    done

    # loss options or argument
    if [[ -z "$proof" ]] || [[ -z "$root" ]] || [[ -z "$argument" ]]; then
        echo "$usage"
        exit 1
    fi

    if [[ ! -f "$proof" || ! -f "$argument" || -L "$proof" || -L "$argument" ]]; then
        echo "$usage"
        exit 1
    fi

    if [[ ! "$root" =~ ^([A-F0-9]+|[a-f0-9]+)$ ]]; then
        echo "$usage"
        exit 1
    fi

    process_verify_proof "$argument" "$proof" "$root"
}

## main function: check args
# if: no subcommand
if [[ $# -lt 1 ]]; then
    echo "$usage"
    exit 1
fi

# else: handle subcommand or -h / --help
case "$1" in
'-h' | '--help')
    echo "$usage"
    if [[ $# -lt 2 ]]; then
        exit 0
    else
        exit 1
    fi
    ;;
'build')
    shift
    build "$@"
    ;;
'gen-proof')
    shift
    gen_proof "$@"
    ;;
'verify-proof')
    shift
    verify_proof "$@"
    ;;
*)
    echo "$usage"
    exit 1
    ;;
esac
