import random

# Just 100 names
_names = ['Isabel', 'Churchill', 'Ponchartrain', 'Ithaca', 'Potts', 'Fairchild', 'MacMahon', 'Magellanic',
          'Gambia', 'Greenfield', 'Cassiopeia', 'Cicero', 'Montrachet', 'Schroeder', 'Ektachrome', 'Goode',
          'Samuelson', 'Seville', 'Culbertson', 'Toledo', 'Carbone', 'Salvatore', 'Gottfried', 'Johannes',
          'Caruso', 'Ammerman', 'Bigelow', 'Schultz', 'Sanborn', 'Royce', 'Synge', 'Philip', 'Colombo',
          'Diogenes', 'Rhine', 'Adriatic', 'Pollard', 'Nostradamus', 'Dixie', 'Lima', 'Buchanan', 'Burroughs',
          'Amtrak', 'Politburo', 'Pennsylvania', 'Kimball', 'Comanche', 'Sault', 'Clarendon', 'Fiske', 'Johnsen',
          'Granville', 'Mohammed', 'Jonas', 'Cupid', 'Moghul', 'Alicia', 'Leigh', 'Teledyne', 'Smucker', 'Gino',
          'Cetus', 'Katmandu', 'Bloomfield', 'Kowalski', 'Honshu', 'Algenib', 'Oakley', 'Hyades', 'Sara',
          'Steinberg', 'Stockholm', 'Lao', 'Carl', 'Cornell', 'Elmer', 'Medici', 'Stevenson', 'Cassius', 'Baku',
          'Allentown', 'Orion', 'Hibernia', 'Gloria', 'Madagascar', 'Anheuser', 'Lucian', 'Eng', 'Coronado',
          'Fallopian', 'Daniel', 'Whittier', 'Purdue', 'Hetty', 'Galway', "I've", 'Romania', 'Havilland',
          'Canaan', 'Austin']


def random_name() -> str:
    return random.choice(_names)
