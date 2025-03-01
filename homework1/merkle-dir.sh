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

build() {
    case $1 in
        '--output')
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

    if [[ -z "$output" ]] || [[ -z "$directory" ]]; then
        echo "$usage"
        exit 1
    fi

    if [[ ! -d $directory ]] || [[ ! -f $output ]]; then
        echo "$usage"
        exit 1
    fi
}

gen_proof() {
    case $1 in
        '--output')
            output_file="$2"
            shift 2
            ;;
        '--tree')
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

    # loss options or argument
    if [[ -z "$output_file" ]] || [[ -z "$tree_file" ]] || [[ -z "$argument" ]]; then
        echo "$usage"
        exit 1
    fi

    # file1 exist and not regular file
    if [[ -e $output_file ]] && [[ ! -f $output_file ]]; then
        echo "$usage"
        exit 1
    fi

    # file2 not regular file
    if [[ ! -f $tree_file ]]; then
        echo "$usage"
        exit 1
    fi
}

verify_proof() {
    case $1 in
        '--proof')
            proof="$2"
            shift 2
            ;;
        '--root')
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

    # loss options or argument
    if [[ -z "$proof" ]] || [[ -z "$root" ]] || [[ -z "$argument" ]]; then
        echo "$usage"
        exit 1
    fi

    if [[ -f "$proof" ]] || [[ -f "$argument" ]]; then
        echo "$usage"
        exit 1
    fi

    if [[ ! "$root" =~ ^([A-F0-9]+|[a-f0-9]+)$ ]]; then
        echo "$usage"
        exit 1 
    fi
}

## main function: check args
# if: no subcommand
if [[ $# -lt 1 ]]; then
    echo "$usage"
    exit 1 
fi

# else: handle subcommand or -h / --help 
case "$1" in
    '-h'|'--help')
        echo "$usage"
        if [[ $# -lt 2 ]]; then
            exit 0;
        else
            exit 1;
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

