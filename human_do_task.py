import datetime

class Clock(object):
    def __init__(self):
        self.reset()
    def reset(self):
        self.accumulator = datetime.timedelta(0)
        self.started = None
    def start(self):
        if not self.started:
            self.started = datetime.datetime.utcnow()
    def stop(self):
        if self.started:
            self.accumulator += (
                datetime.datetime.utcnow() - self.started
            )
            self.started = None
    @property
    def elapsed(self):
        if self.started:
            return self.accumulator + (
                datetime.datetime.utcnow() - self.started
            )
        return self.accumulator
    def __repr__(self):
        return "<Clock {} ({})>".format(
            self.elapsed,
            'started' if self.started else 'stopped'
        )

def _query(self, prefix, question, first_answer, second_answer):
   for item in prefix:
      print(item)
   return input("{question} ({first_answer}/{second_answer})").to_lower().starts_with(first_answer.to_lower())

class Process:
   def __init__(self):
      self._automated = Clock()
      self._automated.start()
      self._manual = Clock()
      self._test_result = []
      self._automated_steps = 0
      self._manual_steps = 0

   class ManualSection:
      def __init__(self, go):
         self.go = go
      def __enter__(self):
         self.go._automated.stop()
         self.go._manual.start()
      def __exit__(self):
         self.go._manual.stop()
         self.go._automated.start()

   @classmethod
   def run(perform, verify):
      go = Process()
      with ManualSection(self):
        do_perform = _query([], "Do you wish to perform the process or verify it?", "P", "V")
      if(do_perform):
         perform(go)
      else:
         verify(go)
      go._print_stats()

   def do(self, operation):
      self._automatic_steps += 1
      operation()

   def tell(self, message):
      self._manual_steps += 1
      with ManualSection(self):
         print(message)
         input("press enter when done")

   def ask(self, condition, operation):
      self._manual_steps += 1
      with ManualSection(self):
         should_do_it = _query([condition], "Should I perform this step?", "Y", "N")
      if(should_do_it):
         operation()

   def ask_yes_no(self, condition):
      self._manual_steps += 1
      with ManualSection(self):
         return = _query([condition], "Should I perform this step?", "Y", "N")

   def if(self, condition, operation):
      self._automatic_steps += 1
      if(condition()):
         operation()

   def verify(self, condition):
      initial = self._manual_steps
      if(not condition()):
         self._test_result.append(f"Failed expectation: {condition}")
      if(initial == self._manual_steps
):
         self._automated_steps += 1

   def that(self, condition):
      def impl():
         self._manual_steps += 1
         with ManualSection(self):
            return _query(
               [f"Please verify whether {condition}."],
               "Is this right?",
               "Y", "N"))
      return impl

   def print_test_results(self):
      if(self._test_result):
      print("Verification failed. Please fix the process and try again.")
      for failure in self._test_result:
         print(failure)

   def _print_stats(self):
      self._automated.stop()
      total_time = self._automated.elapsed + self._manual.elapsed
      print(f"Process complete in {total_time}.")
      print(f"   Automated: {self._automated_steps} steps in {self._automated.elapsed}.")
      print(f"   Manual: {self._manual_steps} steps in {self._manual.elapsed}.")
