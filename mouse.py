#!/usr/bin/python2.6
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap

from Cocoa import *
from Foundation import *
from PyObjCTools import AppHelper

from AppKit import NSScreen

from time import sleep

import threading
import math

# from pymouse import PyMouse
# from pykeyboard import PyKeyboard
# 
# MOUSE = PyMouse()
# KEYBOARD = PyKeyboard()

DELAY = 1.0 / 10

class AppDelegate(NSObject):
  def applicationDidFinishLaunching_(self, aNotification):
    # keyboard
    NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSKeyDownMask, key_handler)

    # mouse
    NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSMouseMovedMask, mouse_handler)
    NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSLeftMouseDownMask, mouse_handler)
    NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSLeftMouseUpMask, mouse_handler)
    NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSRightMouseDownMask, mouse_handler)
    NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSRightMouseUpMask, mouse_handler)

def key_handler(event):
  print event.timestamp(), event.keyCode(), event.characters()

def mouse_handler(event):
  global VX
  global VY

  loc = event.locationInWindow()

  vx = event.deltaX()
  vy = event.deltaY()

  if (vx == 0):
    pass
  elif (vx < 0):
    VX = -math.log(-vx)
  else:
    VX = math.log(vx)

  if (vy == 0):
    pass
  elif (vy < 0):
    VY = -math.log(-vy)
  else:
    VY = math.log(vy)

  VX *= 4
  VY *= 4

  draw_screen(loc.x, loc.y)

def draw_screen(x=0, y=0):
  global VX
  global VY
  global MOUSEX
  global MOUSEY
  global WIDTH
  global HEIGHT

  MOUSEX = x
  MOUSEY = HEIGHT - y

  frame = NSScreen.mainScreen().frame()

  width = int(frame.size.width)
  height = int(frame.size.height)

  x = x / width
  y = y / height

  char_width = 14 * 4 - 2
  char_height = 12

  print "x: %04d y: %04d vx: %04.2f vy: %04.2f" % (MOUSEX, MOUSEY, VX, VY)
  print "=" * char_width
  for i in range(char_height):

    y0 = 1.0 - float(i + 1) / char_height
    y1 = 1.0 - float(i) / char_height

    if (y0 < y and y < y1):
      index = int(char_width * x)
      space = " " * index
      space += "^"
      space += " " * (char_width - index - 1)
    else:
      space = " " * char_width

    print "|" + space + "| %.4f %.4f %.4f" % (y0, y, y1)
  print "=" * char_width

def mouseEvent(type, posx, posy):
  theEvent = CGEventCreateMouseEvent(
              None, 
              type, 
              (posx,posy), 
              kCGMouseButtonLeft)
  CGEventPost(kCGHIDEventTap, theEvent)

def mousemove(posx,posy):
  mouseEvent(kCGEventMouseMoved, posx,posy);
  sleep(DELAY)

def mouseclick(posx,posy):
  # uncomment this line if you want to force the mouse 
  # to MOVE to the click location first (I found it was not necessary).
  #mouseEvent(kCGEventMouseMoved, posx,posy);
  mouseEvent(kCGEventLeftMouseDown, posx,posy);
  mouseEvent(kCGEventLeftMouseUp, posx,posy);

def follow_line(x0, y0, x1, y1, step=1):
  xstep = step
  if (x1 < x0):
    xstep *= -1

  ystep = step
  if (y1 < y0):
    ystep *= -1

  if (x0 == x1):
    x1 += 1

  if (y0 == y1):
    y1 += 1

  for x in range(x0, x1, xstep):
    for y in range(y0, y1, ystep):
      mousemove(x, y)

def follow_box(x0, y0, width, height, step=1):
  follow_line(x0, y0, width, y0)
  follow_line(width, y0, width, height)
  follow_line(width, height, x0, height)
  follow_line(x0, height, x0, y0)

def lap(scale=1):
  padding = 10
  frame = NSScreen.mainScreen().frame()

  width = int(frame.size.width)
  height = int(frame.size.height)

  width = int(width * scale)
  height = int(height * scale)

  follow_box(padding, padding, width - padding, height - padding)

def fivelaps():
   for i in range(5):
     scale = 1.0 / (i + 1)
     lap(scale)

MOUSEX = 700
MOUSEY = 450
VX = 0
VY = 0

frame = NSScreen.mainScreen().frame()

WIDTH = int(frame.size.width)
HEIGHT = int(frame.size.height)

def airhockey():
  global VX
  global VY
  global MOUSEX
  global MOUSEY
  global WIDTH
  global HEIGHT
  global mousemove
  global DELAY

  while (True):
    if (MOUSEX < 1):
      VX = abs(VX)
      MOUSEX = 0
      print "HOZ BOUNCE"
    if (MOUSEX > WIDTH - 2):
      MOUSEX = WIDTH
      VX = -abs(VX)
      print "HOZ BOUNCE"

    if (MOUSEY < 1):
      VY = abs(VY)
      MOUSEY = 0
      print "VERT BOUNCE"
    if (MOUSEY > HEIGHT - 2):
      MOUSEY = HEIGHT
      VY = -abs(VY)
      print "VERT BOUNCE"

    mousemove(MOUSEX + VX, MOUSEY + VY)


def main():
  thread = threading.Thread(target=airhockey)
  thread.start()

  app = NSApplication.sharedApplication()
  delegate = AppDelegate.alloc().init()
  NSApp().setDelegate_(delegate)
  AppHelper.runEventLoop()

main()
