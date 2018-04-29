# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    "*** YOUR CODE HERE ***"
    """
    collect counts for each feature in trainingData
    get smoothed p(F)s using k values
    add up differences
    """

    kpList = []
    kCounter = 0

    """
    for k in kgrid:
        kpList.append(trainingData)

    for kC in range(0, len(kpList)):
        for dC in range(0, len(kpList[kC])):
            for feature in kpList[kC][dC]:
                kpList[kC][dC][feature]+=kgrid[kC]
    """

    blankCounters = {}
    for feature in trainingData[0]:
        blankCounters[feature] = 0

    for k in kgrid:
        kpList.append({"0":blankCounters, "1":blankCounters, "2":blankCounters, "3":blankCounters, "4":blankCounters, "5":blankCounters, "6":blankCounters, "7":blankCounters, "8":blankCounters, "9":blankCounters})

    numLabel = {"0":0.0, "1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0}

    for k in range(len(kpList)):
        for datum in range(len(trainingData)):
            label = str(trainingLabels[datum])
            numLabel[label]+=1
            for f in trainingData[datum]:
                kpList[k][label][f] += trainingData[datum][f]

    for k in range(len(kpList)):
        for label in kpList[k]:
            for feature in kpList[k][label]:
                #print kpList[k][label][feature]
                kpList[k][label][feature] = (kpList[k][label][feature]+kgrid[k])/(numLabel[label]+kgrid[k])
                print kpList[k][label][feature]

    print "NICK TEST STARTS HERE"
    #print kgrid
    #print kpList[0]["0"]
    #print trainingData
    #print trainingLabels
    #print validationData
    #print validationLabels
    print "NICK TEST ENDS HERE"

    #set later
    self.probabilities = None
    self.labelProbabilities = {"0":0, "1":0.0, "2":0.0, "3":0.0, "4":0.0, "5":0.0, "6":0.0, "7":0.0, "8":0.0, "9":0.0}
    for label in self.labelProbabilities:
        self.labelProbabilities[label] = float(numLabel[label])/float(len(trainingData))

    print self.labelProbabilities

    #util.raiseNotDefined()
        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    logJoint = util.Counter()
    
    "*** YOUR CODE HERE ***"
    pY = util.Counter 

    for label in self.legalLabels:
    	logJoint[label] = math.log(self.labelProbabilities[label])
    	for feat, value in datum.items
    	    if value > 0:
                logJoint[label] += math.log(self.probabilities[feat,label])
            else:
                logJoint[label] += math.log(1-self.probabilities[feat,label])

        return logJoint
    
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    for feat in self.features:
        featuresOdds.append((self.probabilities[feat, label1]/self.probabilities[feat, label2], feat))
       
    featuresOdds.sort(reverse = true)

    tempList = []

    for i in range(100):
    	tempList.append(featuresOdds[i])

    featuresOdds = list(tempList)

    

    return featuresOdds
    

    
      
