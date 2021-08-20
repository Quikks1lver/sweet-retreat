from typing import Union, Tuple

from color.Colors import Colors
from .Text import Text
from timing.ClockMethods import Clock_Methods

class Timed_Text():
   """
   Class w/state in order to render text for a given time span
   Each object can render one text chunk at a time
   """

   def __init__(self):
      """
      Creates an object to help with rendering text on a time interval
      """
      # for text
      self.text: str = ""
      self.font = None
      self.font_size: int = 0
      self.color = None
      self.location: Tuple[int, int] = None
      
      # timing
      self.time_interval: int = 0
      self.upper_threshold: int = 0

   def populate_timed_text_parameters(self, text: str, font, font_size: int, color: Union[Colors, Tuple[int, int, int]], location: Tuple[int, int], time_interval: int) -> None:
      """
      (re)populates state of the object to a new set of text
      :param text: text to be displayed
      :param font: Text.Font enum
      :param font_size: in pixels
      :param color: Colors.Color value or RGB tuple
      :param location: x, y tuple
      :param time_interval: time in seconds for text to be displayed
      """
      self.text = text
      self.font = font
      self.font_size = font_size
      self.color = color
      self.location = location

      self.time_interval = time_interval
      self.upper_threshold = Clock_Methods.get_current_time_in_seconds() + time_interval

   def run(self, screen):
      """
      This function needs to be called inside the main game loop in order for the text to be blit
      """
      if not Clock_Methods.is_past_this_time_in_seconds(self.upper_threshold):
         Text.render(screen, self.text, self.font, self.font_size, self.color, self.location)