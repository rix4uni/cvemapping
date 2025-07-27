#!/usr/bin/env python3

from lib.core.enums import PRIORITY
__priority__ = PRIORITY.NORMAL

def dependencies():
  pass

def tamper(payload, **kwargs):
  if payload:
    payload = payload.replace('.dbo', '')
    
  return payload
