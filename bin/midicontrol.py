#!/usr/bin/env python2

import mido

def find_input(want):
    device = None
    available = mido.get_input_names()
    for name in available:
        if want.lower() in name.lower():
            device = name
    return device

def main():
    want = 'LPD8'
    device = find_input(want)

    with mido.open_input(device) as inport:
        print 'opened'
        for msg in inport:
            print(msg)

if __name__ == '__main__':
    main()
