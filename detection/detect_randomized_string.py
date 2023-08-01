from detection.detection_engine import DetectionEngine
import re

class DetectRandomizedString(DetectionEngine):
    def __init__(self, weight):
        super().__init__(weight)
        self.name="randomized_string"

    def run_detection(self,source_context):
        try:
            #detect randomized string like this; ELidMQDtIk
            randomized_string_count = 0.0
            names = []

            # Extract variables
            variable_pattern = re.compile(r"\$[a-zA-Z0-9_-]+[=.:)({} ]", re.IGNORECASE)
            variables = re.findall(variable_pattern, source_context.source)

            # Extract functions
            function_pattern = re.compile(r"function [a-zA-Z0-9_-]+[{ (]", re.IGNORECASE)
            functions = re.findall(function_pattern, source_context.source)

            # Create a list of variables
            for name in variables:
                variable = name[:-1].strip()
                names.append(variable[1:].lower())

            # Create a list of functions
            for name in functions:
                function = name[:-1].strip()
                names.append(function[8:].strip().lower())
            names = list(set(names))

            # Check if names qualify as randomized strings
            for name in names:
                if len(name) < 5:
                    continue
                if 0.3 > self.vowel_rate(name):
                    randomized_string_count += 1

            length = len(names)

            if(length <= 10 or randomized_string_count / length < 0.45):
                self.result = 0
                self.score = 0
                return
            
            self.result = randomized_string_count / length
                
            self.score = self.result * self.weight

        except Exception as e:
            # Handle any errors that occur during the detection process
            print("{0}:{1}".format(self.name,e))
            self.result = 0
            self.score = 0
            self.error = str(e)

    @staticmethod
    def vowel_rate(string):
        """
        Calculate the rate of vowels in a string.
        """
        total_vowel = sum(ch in 'aeiouy' for ch in string)
        return float(total_vowel) / float(len(string))
