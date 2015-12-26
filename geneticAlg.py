##By Richard Zhou
##An attempt to imitate genetic algorithm based on a binary chromosome.
##  More information and inspiration can be found at
##  www.ai-junkie.com/ga/intro/gat1.html

import random

class chromosome:
    """A string of N binary 0/1s, with each 4 digit section
    representing a digit from 0-9 or a basic operator. It discards
    any nonsense statements and outputs the value the binary DNA
    represents after it is evaluated."""

    #all chromosomes have these attributes
    dnaSegment = ["0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101"]
    dnaSymbol =  [   "0",   "1",   "2",   "3",   "4",   "5",   "6",   "7",   "8",   "9",   "+",   "-",   "*",   "/"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["+", "-", "*", "/"]

    def __init__(self, targetVal, dnaLength = 36, inherit = ""):
        self.dna = ""
        self.targetValue = targetVal
        self.dnaLength = dnaLength
        #if it is not a child
        if inherit == "":
            for i in range(0, self.dnaLength):
                self.dna += str(random.getrandbits(1))
        #if its already initialized
        else:
            self.dna = inherit

        #convert to symbols
        self.translated = ""
        for i in range(0, self.dnaLength // 4):
            segment = self.dna[i*4:(i+1)*4]
            for k in range(0,14):
                if chromosome.dnaSegment[k] == segment:
                    self.translated += chromosome.dnaSymbol[k]
                    break

    def __str__(self):
        #print its chromosome
        print(self.dna)
        
        #print its information
        print(self.translated)

        #print its value
        print(self.evaluate())

        #print its fitness
        print(self.fitness())

        #return newline to keep python happy
        return "\n"

    def getDna(self):
        """Returns a string copy of the binary DNA genome."""
        #We are going to use this for breeding purposes
        return self.dna
    
    def evaluate(self):
        """Evaluates the binary DNA to give a numerical value"""
        
        self.wantNum = True  #This bool checks if the next value should be a number or an operator
        self.cleanDna = ""   #This string is the dna with the gibberish removed
        self.currVal = 0     #This is the running total of the DNA
        self.currSymbol = 0  #This is for running computation, default to addition index
        
        for i in self.translated:
            #if the char is not gibberish
            if self.wantNum and i in chromosome.numbers:
                self.cleanDna += i
                self.wantNum = not self.wantNum
            elif not self.wantNum and i in chromosome.symbols:
                self.cleanDna += i
                self.wantNum = not self.wantNum

        #if the last char is a symbol which is gibberish
        if self.cleanDna[-1] in ["+","-","*","/"]:
            self.cleanDna = self.cleanDna[0:len(self.cleanDna) - 1]

        #This part computes the cleaned up string
        for i in self.cleanDna:
            if i in chromosome.numbers:
                if self.currSymbol == 0:
                    self.currVal += int(i)
                elif self.currSymbol == 1:
                    self.currVal -= int(i)
                elif self.currSymbol == 2:
                    self.currVal *= int(i)
                elif self.currSymbol == 3:
                    if not int(i):  #in case we divide by zero
                        i = 1
                    self.currVal //= int(i)
            elif i in chromosome.symbols:
                for k in range(0,4):
                    if chromosome.symbols[k] == i:
                        self.currSymbol = k
                        break
                    
        #return our computed value
        return self.currVal

    def fitness(self):
        """Returns the fitness value of the chromosome as a float."""
        if self.evaluate() == self.targetValue:
            return 0
        else:
            #return float((1 / (self.evaluate() - self.targetValue)))
            return abs(self.evaluate() - self.targetValue)

#########################################################################################

class population:
    """This simulates the amount of organisms breeding and its genetic changes to
    attempt to obtain the value we give it."""

    def __init__(self, targetVal, dnaLength = 36, orgNum = 500, crossoverRate = 0.75, mutationRate = 0.001):
        self.targetVal = targetVal
        self.dnaLength = dnaLength
        self.orgNum = orgNum
        self.crossoverRate = crossoverRate
        self.mutationRate = mutationRate
        self.pond = []
        for i in range(0, self.orgNum):
            self.pond.append(chromosome(self.targetVal, self.dnaLength))
        #optional to sort by fitness but I've decided not to

    def breed(self, index1, index2):
        """Creates the organism from the pond creatures at index1 and index2."""
        #get the creatures' DNA to crossover/mutate
        dna1 = self.pond[index1].getDna()
        dna2 = self.pond[index2].getDna()
        dna3 = ""

        #decide whether crossover
        if random.random() <= self.crossoverRate:
            #crossover is splicing dna1 and dna2 together at the splice point
            splicePoint = random.randint(1, len(dna1) - 2)
            dna3 = dna1[0:splicePoint+1] + dna2[splicePoint+1:len(dna2)]
        else:
            #if there is no crossover we set it equal to dna1
            dna3 = dna1

        #give any possible mutations
        for j in dna3:
            if random.random() <= self.mutationRate:
                j = not j

        #return the actual organism, not the DNA
        return chromosome(self.targetVal, self.dnaLength, dna3)

    def find(self):
        """Finds the chromosome with the DNA that evaluates to the target value."""
        self.found = False      #Will stop loop if found, can leave to be always running
        while not self.found:   #Every pass is 1 generation
            for i in range(0, self.orgNum):
                index1 = random.randint(0, self.orgNum - 1)
                index2 = random.randint(0, self.orgNum - 1)
                #if they are the same, then it is asexual reproduction

                #breed the two organisms into a third and remove the worst one
                newOrg = self.breed(index1, index2)
                self.pond.append(newOrg)
                self.pond.remove(max([self.pond[index1], self.pond[index2], newOrg], key = chromosome.fitness))
                print(min([self.pond[index1], self.pond[index2], newOrg], key = chromosome.fitness))

                #if we found the given number, finish program
                if not min([self.pond[index1], self.pond[index2], newOrg], key = chromosome.fitness).fitness():
                    self.found = True
                    break


f = population(31)
f.find()
