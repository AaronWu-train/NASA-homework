args=$(getopt -o "abo:" -l "input:" -- $*)
# you should not use `getopt abo: "$@"` since that would parse
# the arguments differently from what the set command below does.
if [ $? -ne 0 ]; then
    echo 'Usage: ...'
    exit 2
fi
set -- $args
# You cannot use the set command with a backquoted getopt directly,
# since the exit code from getopt would be shadowed by those of set,
# which is zero by definition.
while :; do
    case "$1" in
    -a | -b | --input)
        echo "flag $1 set"
        sflags="${1#-}$sflags"
        shift
        ;;
    -o)
        echo "oarg is '$2'"
        oarg="$2"
        shift
        shift
        ;;
    --)
        shift
        break
        ;;
    *)
        echo "WTF"
        exit 1
        ;;
    esac
done
echo "single-char flags: '$sflags'"
echo "oarg is '$oarg'"
