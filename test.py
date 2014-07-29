import urllib2
response = urllib2.urlopen('http://propokertools.com/simulations')
html = response.read()

# Ids of Elements
# Hand 1: #h1
# Hand 2: #h2
# Board: #boardField
# Simulate: #pptbutton

