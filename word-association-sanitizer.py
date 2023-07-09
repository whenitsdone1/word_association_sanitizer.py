


#Invalid download link for datasets outside of ipynb notebook
#To execute this code, please download the datasets from the following link or insert your own data

#!wget 'https://cloudstor.aarnet.edu.au/plus/s/W0aB5FYiwN1u5Ls/download' -O in.txt
#download datasets

class Word:
  def __init__(self,word):
    self.word = word
    self.count = 0
    self.neighbours = []
  #create word class and intialize some variables
  def increment(self):
    self.count += 1
  #create a function to increment the count when duplicate words are discovered
  def addneighbour(self, neighbour):
    if neighbour is None:
      self.neighbours.append("NULL")
    else:
      self.neighbours.append(neighbour.word)
  #if we find a neighbour add it to the neighbour list, else add NULL
  def __str__(self):
    return f"{self.word} (count: {self.count}, neighbours: {', '.join(self.neighbours)})"
  #return a string representation of the word objects
  def __lt__(self, other):
  #less than method for word objects
   return self.word < other.word
  def __le__(self, other):
   return self.word <= other.word
   #less than or equal to method for word objects

def read_data(file_path, lexicon_list): #read data from files
    with open(file_path) as f: #line is f
        for line in f:
            words = line.strip().split() #strip white spaces from words, and split words up
                                         #by whitespaces between them
            lexicon_list.extend(words)   #add words onto the lexicon list
    return lexicon_list
def read_cleaner(lexicon_list): #method for sanitizing  data in the dataset
    for i in range(len(lexicon_list)): #for length of the list
        word = lexicon_list[i] #add words as entries into the list
        stripped_word = word.strip() #strip any remaining whitespaces - maybe redundant
        new_word = "" #initalize a new word
        for char in stripped_word: #for each character in a word...
            if char.isalpha() or char.isspace(): #if its an alphabetic character or a space
                new_word += char.lower() #add to new-word, and make every letter lowercase
        if any(c.isalpha() or c.isspace() for c in new_word): #check if any characters in new_word are spaces or letters
            lexicon_list[i] = new_word #if true, add as an element in new_word
        else:
            lexicon_list[i] = "" #if false, add a whitespace instead
    return [word for word in lexicon_list if word != ""] #return the list again, with the words we just instantiated,
                                                         #as long as the word isn't solely whitespaces
def read_helper(lexicon_list):
    lexicon = {}  # initialize an empty dictionary instead of an empty list
    for word in lexicon_list:
        if word in lexicon:  # if the word is already in the dictionary
            lexicon[word].increment()  # just increment the count of the corresponding Word object
        else:  # if the word is not in the dictionary
            w = Word(word)  # create a new Word object
            lexicon[word] = w  # add the new Word object to the dictionary
    lexicon = list(lexicon.values()) #now convert the dictionary back into a list
    return lexicon

def merge(lexicon, left, mid, right):
    array = []

    left_idx = left
    right_idx = mid + 1

    #setup an array and define the indexes

    #merge elements till there is an empty array
    while left_idx <= mid and right_idx <= right:
        if type(lexicon[left_idx]) != Word:
            print(f"Error: element {left_idx} is not a Word object")
        elif type(lexicon[right_idx]) != Word:
            print(f"Error: element {right_idx} is not a Word object")
    #if there are any non-word objects encountered throw an error
        elif lexicon[left_idx] <= lexicon[right_idx]:
            array.append(lexicon[left_idx])
            left_idx += 1 #increment left index
        else:
            array.append(lexicon[right_idx])
            right_idx += 1 #increment right index
    #if left_idx is larger, add left to the array
    #else add right

    while left_idx <= mid:
        array.append(lexicon[left_idx])
        left_idx +=1
    while right_idx <= right:
        array.append(lexicon[right_idx])
        right_idx += 1
    #if one subarray is empty, add the other to the array

    for idx in range(left,right + 1):
        lexicon[idx] = array[idx - left]
   #assign contents of the newly sorted array to the original listg

def merge_sort(lexicon, first, last):
    if first < last:
    #only sort arrays with more than one element
        mid = (first + last) // 2
    #define mid
        merge_sort(lexicon, first, mid)
        merge_sort(lexicon, mid + 1, last)
        #sort left then right
        merge(lexicon, first, mid, last)
        #merge left & right

def find_neighbours(lexicon):
    length_table = {}
    for word_obj in lexicon:
        length = len(word_obj.word)
        if length in length_table:
            length_table[length].append(word_obj)
        else:
            length_table[length] = [word_obj]
    # create an empty dictionary, group word objects of the same length
    # together to avoid comparing each word to the entire list

    for word_list in length_table.values(): #create a list of words with the same length
        first = 0
        while first < len(word_list): #while we haven't traversed the entire list
            second = first + 1
            while second < len(word_list):
              #create two loops to iterate through and compare
              #an element with every other element of the list
                first_word = word_list[first]
                second_word = word_list[second]
                divergence = 0
                i = 0
                #intialize divergence var to count differences, i var to compare letters
                #choose words from dictionary
                while i < len(first_word.word): #while we haven't compared every letter
                    if first_word.word[i] != second_word.word[i]: #if there is a letter difference
                        divergence += 1 #increment divergence
                        if divergence > 1: #if more than one difference they are not neighbours
                            break
                    i += 1
                if divergence == 1: #if one difference, add them as neighbours
                    first_word.addneighbour(second_word)
                    second_word.addneighbour(first_word)
                second += 1 #compare first with the next word in the word_list
            if not word_list[first].neighbours:
                word_list[first].addneighbour(None) #if no neighbours, add NULL
            first += 1 #move on to the next word

def write_data(lexicon): #function to write data into a document
  with open("out.txt", "w") as f: #create out.txt and call it f
    counter = 0 #intalize a counter
    while counter < len(lexicon): #while we haven't added every word
     if counter != len(lexicon) - 1: #if this isn't the last word, make a new line
      f.write(str(lexicon[counter]) + "\n") #write a new word to the file and start a new line
      counter += 1
     else: #if this is the last word, don't make a new line
      f.write(str(lexicon[counter]))
      counter += 1 #increment the counter
#if-else clause prevents the word count from being incorrect due to extra line printing

def build_lexicon(input_filename, output_filename):
  #call existing functions
  lexicon_list = [] #intialize the list
  lexicon_list = read_data("in.txt", lexicon_list)
  lexicon_list = read_cleaner(lexicon_list)
  lexicon = read_helper(lexicon_list)
  merge_sort(lexicon, 0, len(lexicon) - 1)
  find_neighbours(lexicon)
  """
  lexicon = lexicon[::-1]
  for obj in lexicon:
   print(str(obj))""" #to reverse the list for testing the worst case - uncomment these lines

  write_data(lexicon)

#assessable cell
input_filename = 'in.txt'
output_filename = 'out.txt'
build_lexicon(input_filename, output_filename)    # You cannot modify this function call

#timing cell
import timeit

N_REPEATS = 2

input_filename = 'in.txt'
output_filename = 'out.txt'


total_execution_time = timeit.timeit(lambda: build_lexicon(input_filename, output_filename), globals=globals(), number=N_REPEATS)
average_time = total_execution_time / N_REPEATS

print(f'Average execution time: {average_time:.2f}s across {N_REPEATS} runs')