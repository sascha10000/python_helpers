import signal
import os

'''
 Manages open file handlers and closes them on SIGINT or SIGTERM
'''
class GlobalFileHandler:
  class __Singleton:
    def __init__(self):
      signal.signal(signal.SIGINT, self.close_all)
      signal.signal(signal.SIGTERM, self.close_all)
      self.filehandlers = {}

    '''
    Append data to file
    :param data
    data to append
    :param file
    file to append the data
    '''
    def append(self, data, file):
      try:
       self.filehandlers[file].write(data)
      except KeyError:
       self.filehandlers[file] = open(file, "a+")
       self.filehandlers[file].write(data)

    '''
    :returns
    list of open file handles
    '''
    def handlers(self):
      return self.filehandlers

    '''
    Get a certain handle
    :param file
    file to get the handle for
    :returns
    the given file handle
    '''
    def getHandle(self, file):
      return self.filehandlers[file]

    '''
    Removes a file
    :param file
    file to remove
    :returns
    value indicating if file was deleted 
    '''
    def remove(self, file) -> bool:
      if self.exists(file):
        os.remove(file)
        return True

      return False

    '''
    Checks if file exists
    :param file
    file to check existence for
    :returns
    true if file exists
    '''
    def exists(self, file) -> bool:
      return os.path.exists(file)

    '''
    Closes all handles (is registered for some signals)
    '''
    def close_all(self):
      for handler in self.filehandlers:
        print("Closing " + handler + "!...")
        self.filehandlers[handler].close()
        print("File " + handler + " closed!")


  ### SINGLETON STUFF
  instance = None
  def __init__(self):
    if GlobalFileHandler.instance is None:
      GlobalFileHandler.instance = GlobalFileHandler.__Singleton()

  def __getattr__(self, name):
    return getattr(self.instance, name)
