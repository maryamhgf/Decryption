import random
import re
from collections import deque
from itertools import combinations 
from copy import deepcopy
from math import floor
from math import log
import os


class Decoder():
    
    def __init__(self, text):
        self.text = text
    
    
    alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r'
        , 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def fileToSet(self, data):
        fileset = re.sub("[^a-zA-Z]+", " ", data)
        return set(fileset.split(' '))
    
    def fileToSetFile(self, address):
        with open(address, 'r') as f:
            data = f.read()
        
        fileset = re.sub("[^a-zA-Z]+", " ", data)
        return set(fileset.split(' '))

    def getInitiallPopulation(self):
        randomSelect = random.sample(self.alphabets, 26)
        return dict(zip(randomSelect, self.alphabets))

    def mutation(self, child1, child2, maxMutatedGenes, minMutatedGenes, maxFitting, repeatation, 
            localMax, stuck, match, flags):
        select = random.uniform(0, 1)
        if(select >= 0.7 and not flags[0] and not flags[1] and not flags[2] and not(stuck)):
            return
        if(select >= 0.6 and flags[0]):
            return 
        if(select >= 0.8 and flags[1]):
            return
        if(select >= 1 and flags[2]):
            return
        whichChild = random.randint(1, 2)
        for keyIndex in range(2):
            if(keyIndex == 0):
                if(whichChild == 1 ):
                    continue
                key = child1
            elif(keyIndex == 1 ):
                if(whichChild == 2 ):
                    continue
                key = child2
            numOfMutatedGene = random.randint(min(minMutatedGenes, maxMutatedGenes), max(maxMutatedGenes, minMutatedGenes))
            if(stuck):
                numOfMutatedGene = random.randint(1, 7)
            if(flags[0]):
                numOfMutatedGene = random.randint(5, 8)
            if(flags[1]):
                numOfMutatedGene = random.randint(4, 8)
            if(flags[2]):
                numOfMutatedGene = random.randint(2, 4)
            mutatedAlphabets = random.sample(self.alphabets, numOfMutatedGene)
            #print("NUM OF MUTATED: ", numOfMutatedGene, "MutatedAlphabets: ", mutatedAlphabets)
            for letter in mutatedAlphabets:
                valueBeforMutation = key[letter]
                randomOffset = random.randint(-4, 4)
                if(repeatation):
                    randomOffset = random.randint(-3, 5)
                nextLetter = chr(ord(letter) + randomOffset).lower()
                while(not nextLetter.isalpha()):
                    randomOffset = random.randint(-4, 4)
                    if(repeatation):
                        randomOffset = random.randint(-3, 5) 
                    nextLetter = chr(ord(letter) + randomOffset).lower()
                key[letter] = key[nextLetter]
                key[nextLetter] = valueBeforMutation


    def calculatingFittinfForOneKey(self, key, globalLowerDict, encodedSet):
        #decoding:
        decoded = set()
        for word in encodedSet:
            listedWord = list(word)
            i = 0
            for letter in word:
                if(letter.isupper()):
                    listedWord[i] = key[letter.lower()]
                else:
                    listedWord[i] = key[letter]
                i = i + 1
            decoded.add("".join(listedWord))
        common = decoded.intersection(globalLowerDict)
        score = 0
        for word in common:
            score = score + len(word)
        return score
            
    def calculateFitting(self, population):
        encodedSet = self.fileToSet(self.text) 
        script_dir = os.path.dirname(__file__)
        globalAddress = script_dir + "/Attachment/global_text.txt"
        globalSet = self.fileToSetFile(globalAddress)
        globalSetLower = set(map(lambda x:x.lower(), globalSet))
        fitting = []
        for key in population:
            fittingScore = self.calculatingFittinfForOneKey(key, globalSetLower, encodedSet)
            fitting.append(fittingScore)
        return fitting

    def crossOver(self, parent1, parent2, crossOverProb, repeatation, localMAx, match, flags):
        randomProb = random.uniform(0, 1)
        if(randomProb <= crossOverProb):
            if(repeatation):
                randomSelect = random.randint(0, 2)
                if(localMAx):
                    randomSelect = random.randint(1, 2)
                if(match or flags[2] or flags[1]):
                    randomSelect = 1
                if(randomSelect == 0):
                    crossOverPoint1 = random.randint(3, 10)
                    crossOverPoint2 = random.randint(10, 20)
                    crossOverPoint3 = random.randint(20, 25)
                    child1 = {}
                    child2 = {}
                    for i in range(crossOverPoint1):
                        child1.update({self.alphabets[i] : parent1[self.alphabets[i]] })
                        child2.update({self.alphabets[i] : parent2[self.alphabets[i]]})
                    for i in range(crossOverPoint2 - crossOverPoint1):
                        child1.update({self.alphabets[i + crossOverPoint1] : parent2[self.alphabets[i + crossOverPoint1]] })
                        child2.update({self.alphabets[i + crossOverPoint1] : parent1[self.alphabets[i + crossOverPoint1]]})
                    for i in range(crossOverPoint3 - crossOverPoint2):
                        child1.update({self.alphabets[i + crossOverPoint2] : parent1[self.alphabets[i + crossOverPoint2]] })
                        child2.update({self.alphabets[i + crossOverPoint2] : parent2[self.alphabets[i + crossOverPoint2]]})
                    for i in range(26 - (crossOverPoint3) ):
                        child1.update({self.alphabets[i + crossOverPoint3] : parent2[self.alphabets[i + crossOverPoint3]] })
                        child2.update({self.alphabets[i + crossOverPoint3] : parent1[self.alphabets[i + crossOverPoint3]]})               
                    
                if(randomSelect == 1):
                    child1 = {}
                    child2 = {}
                    crossOverPoint = random.randint(10, 18)
                    if(localMAx):
                        crossOverPoint = random.randint(11, 15)
                    randomLength = 0
                    for i in range(crossOverPoint):
                        child1.update({self.alphabets[i] : parent1[self.alphabets[i]] })
                        child2.update({self.alphabets[i] : parent2[self.alphabets[i]]})
                    for i in range(randomLength):
                        child1.update({self.alphabets[i + crossOverPoint] : parent2[self.alphabets[i + crossOverPoint]]})
                        child2.update({self.alphabets[i + crossOverPoint] : parent1[self.alphabets[i + crossOverPoint]]})
                    for i in range(26 - (crossOverPoint + randomLength)):
                        child1.update({self.alphabets[i + crossOverPoint + randomLength] : parent2[self.alphabets[i + crossOverPoint + randomLength]]})
                        child2.update({self.alphabets[i + crossOverPoint + randomLength] : parent1[self.alphabets[i + crossOverPoint + randomLength]]})
            
                if(randomSelect == 2):
                    #Three Version:
                    crossOverPoint = random.randint(3, 21)
                    randomLength = random.randint(min(3, 25 - crossOverPoint), max(3, 25 - crossOverPoint))
                    if(localMAx):
                        crossOverPoint = 8
                        randomLength = 8
                    child1 = {}
                    child2 = {}
                    for i in range(crossOverPoint):
                        child1.update({self.alphabets[i] : parent1[self.alphabets[i]] })
                        child2.update({self.alphabets[i] : parent2[self.alphabets[i]]})
                    for i in range(randomLength):
                        child1.update({self.alphabets[i + crossOverPoint] : parent2[self.alphabets[i + crossOverPoint]]})
                        child2.update({self.alphabets[i + crossOverPoint] : parent1[self.alphabets[i + crossOverPoint]]})
                    for i in range(26 - (crossOverPoint + randomLength)):
                        child1.update({self.alphabets[i + crossOverPoint + randomLength] : parent1[self.alphabets[i + crossOverPoint + randomLength]]})
                        child2.update({self.alphabets[i + crossOverPoint + randomLength] : parent2[self.alphabets[i + crossOverPoint + randomLength]]})
            
            else:    
                #Three Version:
                crossOverPoint = random.randint(3, 21)
                randomLength = random.randint(min(3, 25 - crossOverPoint), max(3, 25 - crossOverPoint))
                child1 = {}
                child2 = {}
                for i in range(crossOverPoint):
                    child1.update({self.alphabets[i] : parent1[self.alphabets[i]] })
                    child2.update({self.alphabets[i] : parent2[self.alphabets[i]]})
                for i in range(randomLength):
                    child1.update({self.alphabets[i + crossOverPoint] : parent2[self.alphabets[i + crossOverPoint]]})
                    child2.update({self.alphabets[i + crossOverPoint] : parent1[self.alphabets[i + crossOverPoint]]})
                for i in range(26 - (crossOverPoint + randomLength)):
                    child1.update({self.alphabets[i + crossOverPoint + randomLength] : parent1[self.alphabets[i + crossOverPoint + randomLength]]})
                    child2.update({self.alphabets[i + crossOverPoint + randomLength] : parent2[self.alphabets[i + crossOverPoint + randomLength]]})
        
        else: 
            child1 = parent1
            child2 = parent2
        return child1, child2

    def getParent2(self, population, numOfParents, fitting, repeatation, generation, localMax):
        parents = []
        sortedFitting = deepcopy(fitting)
        sortedFitting.sort(reverse = True)
        seenIndices = set()
        seenNums = set()
        i = 0
        while len(parents) < numOfParents:
            if not(sortedFitting[i] in seenNums):
                indices = [ii for ii, x in enumerate(fitting) if x == sortedFitting[i]]
            else:
                i = i + 1
                continue
            seenNums.add(sortedFitting[i])
            for j in range(len(indices)):
                if not (indices[j] in seenIndices):
                    parents.append(population[indices[j]])
                    seenIndices.add(indices[j])
                    if(len(parents) >= numOfParents):
                        break
            i = i + 1
        return parents

    def pairing(self, matingPool, numOfParents):
        pairs = []
        i = 0
        while i <= (len(matingPool) - 2):
            if( not([matingPool[i], matingPool[i + 1]] in pairs)):
                pairs.append([matingPool[i], matingPool[i + 1]])
            i = i + 1

        return pairs


    def mating(self, pairs, crossOverP, minMutatedGenes, maxMutatedGenes, numberOfPopulation, 
            maxFitting, elitism, repeatation, localMax, stuck, match, flags):
        offspring = []
        flag = 0
        #Main childs:
        for pair in pairs:
            parent1 = pair[0]
            parent2 = pair[1]
            child1, child2 = self.crossOver(parent1, parent2, crossOverP, repeatation, localMax, match, flags)
            self.mutation(child1, child2, maxMutatedGenes, minMutatedGenes, maxFitting, repeatation
                    , localMax, stuck, match, flags)
            if(not child1 in offspring):
                offspring.append(child1)
            if(not child2 in offspring):
                offspring.append(child2)

        i = 0
        j = 0
        while(len(offspring) < numberOfPopulation ):
            if(j == 2):
                j = 0
            offspring.append(pairs[i][j])
            i = i + 1
            j = j + 1
            if(i >= len(pairs)):
                flag = 1
                break
            
        i = 0
        step = 1
        while(len(offspring) < numberOfPopulation and not(stuck)):
            parent1 = pairs[i][0]
            parent2 = pairs[i + step][0]
            child1, child2 = self.crossOver(parent1, parent2, crossOverP, repeatation, localMax, match, flags)
            self.mutation(child1, child2, maxMutatedGenes, minMutatedGenes, maxFitting, repeatation, 
                    localMax, stuck, match, flags)
            if(not child1 in offspring):
                offspring.append(child1)
            if(not child2 in offspring):
                offspring.append(child2)        
            i = i + 1
            if(i >= len(pairs) - 1):
                print("len(offspring) in break first::::::::", len(offspring))
                flag = 1
                break
        if(flag == 1):
            print("len(offspring) in AFTER break ::::::::", len(offspring))


        for i in range(floor(elitism * numberOfPopulation)):
            if( j == 2):
                j = 0
            if not pairs[i][j] in offspring:
                offspring.append(pairs[i][j])
            j = j + 1
        
        if(flags[1] or flags[2] or stuck):
            for i in range(20):
                parent1 = pairs[i+ random.randint(100, 300)][random.randint(0,1)]
                parent2 = pairs[i + random.randint(100, 300)][random.randint(0, 1)]
                child1, child2 = self.crossOver(parent1, parent2, crossOverP, repeatation, localMax, match, flags)
                self.mutation(child1, child2, maxMutatedGenes, minMutatedGenes, maxFitting,
                        repeatation, localMax, stuck, match, flags)
                if(not child1 in offspring):
                    offspring.append(child1)
                if(not child2 in offspring):
                    offspring.append(child2)        
                i = i + 1
                if(i >= len(pairs) - 1):
                    flag = 1
                    break

        return offspring

    def convert(self, key, data, maxFitiing):
            script_dir = os.path.dirname(__file__)
            decoddedAddress = script_dir + "/Attachment/decoded_text_Fitting"+ str(maxFitiing)+".txt"             
            decodedFile = open(decoddedAddress,"w+") 
            for letter in data:
                    if(not letter.isalpha()):
                            decodedFile.write(letter)
                            continue
                    else:
                            if(letter.isupper()):
                                    outLetter = key[letter.lower()].upper()

                            elif(letter.islower()):
                                    outLetter = key[letter.lower()]
                    decodedFile.write(outLetter)


    def decoder(self, numberOfPopulation, numberOfParents, numberOfGeneration, 
            maxMutatedGenes, minMutatedGenes, crossOverProb, n, elitism): 
        population = []
        initialMaxMutatedGens = maxMutatedGenes
        initialMinMutatedGens = minMutatedGenes
        initialCrossOverP = crossOverProb
        initialElitism = elitism
        while len(population) < numberOfPopulation:
            new = self.getInitiallPopulation()
            if not new in population:
                population.append(new)
        maxFittingPrevGenerarion = 0
        maxFittingPrevGenerarion1 = 0
        maxFittingPrevGenerarion2 = 0
        maxFittingPrevGenerarion3 = 0
        generation = 0
        encodedSet = self.fileToSet(self.text) 
        script_dir = os.path.dirname(__file__)
        globalAddress = script_dir + "/Attachment/global_text.txt"        
        globalSet = self.fileToSetFile(globalAddress)
        while True:
            print("GENERATION: ", generation)
            fitting2 = self.calculateFitting(population)
            print("MAXIMUM FITTING:::::::::::: ", max(fitting2), 
                    "INDEX:" , fitting2.index(max(fitting2)))
            maxFitiing = max(fitting2)
            repeatation = 0
            flag1 = 0
            flag2 = 0
            flag3 = 0
            maxMutatedGenes = initialMaxMutatedGens
            minMutatedGenes = initialMinMutatedGens
            crossOverProb = initialCrossOverP
            elitism = initialElitism
            localMax = 0
            stuck = 0
            match = 0
            flags = []
            #Write results:
            if(maxFitiing >= 1960):
                self.convert(population[fitting2.index(maxFitiing)], self.text, maxFitiing)
            #Write result:
            if(maxFitiing >= 1730):
                self.convert(population[fitting2.index(maxFitiing)], self.text, maxFitiing)
            
    
            if(maxFitiing == maxFittingPrevGenerarion and maxFittingPrevGenerarion1 == maxFittingPrevGenerarion 
                    and  maxFittingPrevGenerarion1 == maxFittingPrevGenerarion2 and maxFittingPrevGenerarion3 == maxFittingPrevGenerarion2):
                        stuck = 1 
                        elitism = 0.001
                        crossOverProb = 1

            if(maxFitiing == maxFittingPrevGenerarion and maxFittingPrevGenerarion1 == maxFittingPrevGenerarion 
                ):
                repeatation = 1
                crossOverProb = 1
                elitism = 0.008
                print("REPETEATION")
            #1:
            if(maxFitiing >= 1700 and maxFitiing < 1800):
                maxMutatedGenes = initialMaxMutatedGens + random.randint(6, 8)
                minMutatedGenes = initialMinMutatedGens + random.randint(-3, 5)
                flag1 = 1   
                if(not repeatation):
                    crossOverProb = 0.7
                print("LOCAL MAX")
            #2:
            if(maxFitiing >= 1800 and maxFitiing <= 1900):
                flag2 = 1
                crossOverProb = random.uniform(0.7, 1)
                elitism = random.uniform(0.005, 0.01)
            #3:
            if(maxFitiing >= 1900):
                flag3 = 1
                crossOverProb = 1
            if(maxFitiing >= 1920):
                match = 1
                crossOverProb = 1   
            flags.append(flag1)
            flags.append(flag2)
            flags.append(flag3)
            matingParents = self.getParent2(population,numberOfParents, fitting2, repeatation, generation, localMax)
            pairs = self.pairing(matingParents, numberOfParents)
            offspring = self.mating(pairs, crossOverProb, minMutatedGenes, maxMutatedGenes
                    , numberOfPopulation, maxFitiing, elitism, repeatation, localMax, stuck, match, flags)

            maxFittingPrevGenerarion3 = maxFittingPrevGenerarion2
            maxFittingPrevGenerarion2 = maxFittingPrevGenerarion1
            maxFittingPrevGenerarion1 = maxFittingPrevGenerarion
            maxFittingPrevGenerarion = maxFitiing       
            population = offspring
            generation = generation + 1

    def decode(self):
        numberOfPopulation = 2000
        numberOfParents = 1001
        numberOfGeneration = 450
        maxMutatedGenes = 11
        minMutatedGenes = 3 
        elitism = 0.01    
        n = 3
        crossOverProb = 0.8
        self.decoder(numberOfPopulation, numberOfParents, numberOfGeneration, 
                maxMutatedGenes, minMutatedGenes, crossOverProb, n, elitism)




d = open('E:/AI/Attachment/encoded_text.txt').read()
d = Decoder(d)
d.decode()