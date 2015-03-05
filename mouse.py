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

# from pymouse import PyMouse
# from pykeyboard import PyKeyboard
# 
# MOUSE = PyMouse()
# KEYBOARD = PyKeyboard()

DELAY = 1.0 / 1024

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

  VX = event.deltaX()
  VY = event.deltaY()

  draw_screen(loc.x, loc.y)

def draw_screen(x=0, y=0):
  global VX
  global VY
  global MOUSEX
  global MOUSEY

  MOUSEX = x
  MOUSEY = y

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
  if (MOUSEX < 1 or MOUSE_X > WIDTH - 1):
    VX *= -1
  if (MOUSEY < 1 or MOUSE_Y > HEIGHT - 1):
    VY *= -1

  movemouse(MOUSEX + VX, MOUSEX + VY)

def main():
  app = NSApplication.sharedApplication()
  delegate = AppDelegate.alloc().init()
  NSApp().setDelegate_(delegate)
  AppHelper.runEventLoop()

main()



