from sys import argv
script, training_file, test_file = argv

def build_classifier(training_file):
  with open (training_file) as tfile:
    rows = tfile.readlines()
    print(len(rows))

build_classifier(training_file)
