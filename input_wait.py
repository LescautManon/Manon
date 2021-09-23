import msvcrt
import time
import sys

# prompt = 'Enter answer: '
prompt = ""


# def timed_input(caption, timeout=5, _delay=0.02):
def timed_input(caption, timeout, _delay=0.04):
    def echo(c):
        sys.stdout.write(c)
        sys.stdout.flush()

    echo(caption)
    _input = []
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        prompt_t = '\r{:.1f}| {}{}'.format(start - time.monotonic() + timeout, prompt, ''.join(_input))
        print(prompt_t, end='')
        if msvcrt.kbhit():
            c = msvcrt.getwch()
            if ord(c) == 13:
                # echo('\r\n')
                break
            elif ord(c) == 8:   # backspace
                print('\r{}'.format(' ' * len(prompt_t)), end='')
                _input = _input[:-1]
                continue

            _input.append(c)
            echo(c)
        time.sleep(_delay)
    if _input:
        return ''.join(_input)


# v = timed_input()
