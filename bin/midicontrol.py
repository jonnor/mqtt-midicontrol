#!/usr/bin/env python2

import mido
import gevent
import msgflo

import sys, os, json, logging

def serialize_midi(msg):
    return msg.dict()

class MidiInput(msgflo.Participant):
  def __init__(self, role):
    d = {
      'component': 'midicontrol/Input',
      'label': 'Sends input from a MIDI device',
      'inports': [
        { 'id': 'open', 'type': 'string', 'hidden': True },
      ],
      'outports': [
        { 'id': 'raw', 'type': 'object' },
      ],
    }
    msgflo.Participant.__init__(self, d, role)

  def open(self, devicename):
    device = find_input(devicename)

    self.inport = inport = mido.open_input(device)
    def read_inport():
        while inport:
            for m in inport.iter_pending():
                raw = serialize_midi(m)
                self.send('raw', raw)
    gevent.spawn(read_inport)

  def process(self, inport, msg):
    if inport == 'open':
        name = msg.data
        self.open(name)
        #self.ack(msg)
        #self.send('raw', {'opened': name})

def find_input(want):
    device = None
    available = mido.get_input_names()
    for name in available:
        if want.lower() in name.lower():
            device = name
    return device

def main():
    msgflo.main(MidiInput)

if __name__ == '__main__':
    main()
