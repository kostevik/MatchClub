def create_database_from_file(filepath):
  '''
  this function will populate a mini-database with all the info

  for example, if we have a .csv file like:

  Name,Age,Work
  Mark,26,Student
  Jess,25,Teacher

  then this program will return a map containing people so like

  database = {
    'Mark': {'Age': '26', 'Work': 'Student'},
    'Jess':  {'Age': '25', 'Work': 'Teacher'},
  }

  that can be accessed like

  database['Mark']['Work'] -> 'Student'
  '''
  infile = open(filepath)
  # advance the file one line to capture the header
  header = next(infile).strip('\n\r').split(',')
  # iterate through the rest and save as a map
  database = {}
  for index, line in enumerate(infile):
    data = line.strip('\n\r').split(',') # collects the data
    entry = dict(zip(header, data)) # packs it into a nice map for reference
    database[index] = entry
  infile.close() # important to close files if program runs a long time
  return database

def create_grid(database):
  '''
  take in the compacted data and return a 2D grid of match values based on
  a given algorithm
  '''

  grid = {}
  size_of_database = len(database)
  for index in range(size_of_database):
    person1 = database[index]

    for other_index in range(index+1, size_of_database):

      # we start the other indexes at +1 so we only check other people
      person2 = database[other_index]


      # here is where we do our matching algorithm
      number_of_matches = 0
      for information_available in person1:

        EXCLUDED = ['Name','Highschool', 'Grade', 'Sex', 'Nationality']
        if information_available in EXCLUDED:
          continue

        elif person1[information_available]==person2[information_available]:
          number_of_matches += 1


      # this code could be a lot nicer and less redundant
      if person1['Name'] in grid:
        grid[ person1['Name'] ].append( (person2['Name'], number_of_matches) )
      else:
        grid[ person1['Name'] ] = [ ( person2['Name'], number_of_matches) ]

      if person2['Name'] in grid:
        grid[ person2['Name'] ].append( (person1['Name'], number_of_matches) )
      else:
        grid[ person2['Name'] ] = [ (person1['Name'], number_of_matches) ]

  return grid

def write_gridfile(grid, filepath):
  '''
  take in a 'grid' of matches

  {
    'Mark' : [('Mark', -1), ('Jess', 1)],
    'Jess'  : [('Mark',  1), (')]
  }

  and return for example:

  ,Mark,Jess\n
  Mark,-1,1\n
  Jess,1,-1\n

  in a named .csv file
  '''
  outfile = open(filepath, mode='w')

  names_list = sorted(grid.keys())
  outfile.write( ',' + ','.join(names_list) + '\n' )

  for name in names_list:
    match_value_array = ['' for _ in range(len(grid))]
    for match_name, match_value in grid[name]:
      try:
        index = names_list.index(match_name)
      except:
        continue
      match_value_array[index] = str(match_value)

    outfile.write( name + ',' + ','.join(match_value_array)+'\n' )

  outfile.close()

if __name__ == '__main__':
  # only execute this code if we run this file
  database = create_database_from_file('sample_data.csv')
  grid = create_grid(database)
write_gridfile(grid, 'grid.csv')
