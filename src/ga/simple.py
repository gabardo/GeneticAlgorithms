'''
Created on Jan 7, 2011

This module defines the data structures for a simple genetic algorithm
    Goldberg, David. (1989). Genetic Algorithms in Search, 
    Optimization and Machine Learning. Appendix Chapter 3 

Classes:

Chromosome - an artificial chromosome (bit string) extends ga.common.Chromosome
   by adding and unsigned int to represent the value of the chromosome as well
   as the code that manages it.
SimpleGeneticAlgorithm  - a simple tripartite algorithm

Functions:

population - initializes the old population for the Simple genetic algorithm

Exceptions:


@author: Val Hendrix (val.hendrix@me.com)
'''

from __future__ import division
import ga
from ga.common import GeneticAlgorithm,Individual

__version__ = '0.1'
__author__ = "Val Hendrix (val.hendrix@me.com)"
__date__ = 'Jan 7, 2011'
__url__ = 'https://github.com/valreee/GeneticAlgorithms'


def population(self):
    """
       Creates the initial population for the Simple genetic algoirthm.
       This function expects a SimpleGeneticAlgorithm instance or at 
       least an object with the following attributes
       
       popsize - size of the population
       lchrom - size of the chromosime
       random - a PRNG
       decode(chrom) - a function for decoding the chromosime
       oldpop - the old population array to create
       
    """
    for j in range(self.popsize):
        ''' initial population generation '''
        chrom = Chromosome()
        for j1 in range(self.lchrom):
            chrom[j1] = self.random.flip(0.5)
        x = self.decode(chrom)
        parent1 = 0
        parent2 = 0
        xsite = 0
        self.oldpop[j]=Individual(chrom, self.lchrom, x, None, parent1, parent2, xsite) 
        self.oldpop[j].fitness = self.objfunction(self.oldpop[j])

class Chromosome(ga.common.Chromosome):
    ''' An artificial chromosomve '''
    
    
    
    def __init__(self):
        ''' Constructor 
            
            Populations the chromosomes alleles to the length
        '''
        super(Chromosome, self).__init__()
        self.uint = 0
            
    
    def __setitem__(self, key, item): 
        """
           Set the allele representing the key with the item
            >>> chrom=Chromosome()
            >>> chrom[1]=True
        """
        
        if(key >= len(self.alleles) or item != self.alleles[key]):
            if item:
                self.uint += pow(2, key)
            elif key < len(self.alleles):
                self.uint -= pow(2, key)
        super(Chromosome, self).__setitem__(key,item)
       
    def __str__(self):
        s = ""
        for i in range(len(self.alleles)-1,-1,-1):
            s += '1' if self.alleles[i] else '0' 
        return s
   
        


    
class SimpleGeneticAlgorithm(GeneticAlgorithm):
    ''' 
        A simple genetic algorithm (SGA) as defined
        in Goldberg, David. (1989). Genetic Algorithms in Search
        Optimization & Machine Learning.
    '''
    
    def __init__(self, random, popsize=30, lchrom=30, maxgen=10, pcross=.6, pmutation=.033,verbose=False):
        ''' Constructor 
            Initializes the population with random individuals
        '''
        self.lchrom=lchrom
        self.coef = pow(2,lchrom)-1   # coefficient to normalize the domain 2^30-1  where 30 is the string size
        
        # set the anonymous population function
        self.initializePop= lambda: population(self)
        
        super(SimpleGeneticAlgorithm,self).__init__(random, popsize, maxgen, pcross, pmutation,verbose)             
                    
    
    def crossover(self, indiv1, indiv2):
        '''Cross two parent strings, place in two child strings
           using one-point crossover '''
        indivc1=Individual(chrom=Chromosome())
        indivc2=Individual(chrom=Chromosome())
        child1=indivc1.chrom
        child2=indivc2.chrom
        parent1=indiv1.chrom
        parent2=indiv2.chrom
            
        j = 0
        if self.random.flip(self.pcross):                   # Do flip with p(cross)
            jcross = self.random.rnd(0, self.lchrom - 1)    # Cross between 0 and l-1
            self.ncross += 1                                # Increment crossover counter
        else:
            jcross = self.lchrom
        
        # First exchange, 1 to 1 and 2 to 2
        for j in range(jcross):
            child1[j] = parent1[j]
            child2[j] = parent2[j]
            
        # Second Exchange, 1 to 2 and 2 to 1
        if jcross != self.lchrom:
            for j in range(jcross, self.lchrom):
                child1[j] = parent2[j]
                child2[j] = parent1[j]
        return jcross,indivc1,indivc2
            
    def mutate(self, i,chrom):
        ''' 
            Mutate and allele with pmutation, count number
            of mutations
        '''
        mutate = self.random.flip(self.pmutation)   #Flip biased coin
        if mutate:
            self.nmutation += 1
            chrom[i]=False if chrom[i] else True

    
    def decode(self, chrom):
        '''
        Decode string as unsigned binary integer
        '''
        return chrom.uint
    
    def objfunction(self, individual):
        ''' Fitness function - f(x) = x**n '''
        x=individual.x
        n = 10
        return pow(float(x) / self.coef, n)
    
    
            
            
    
            
   
                
    
        
        
    
        
    
        
