from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap

from AppKit import NSScreen

from time import sleep

DELAY = 1.0 / 1024

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

def main():
  fivelaps()

main()
