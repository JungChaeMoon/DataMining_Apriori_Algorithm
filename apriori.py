# -*- coding: utf-8 -*-
"""
Date: Created on 2017-10-14 09:44am Thursday  
Author: zhaopace@foxmail.com
Description: 
    An Effectively Python Implementation of Apriori Algorithm for Finding Frequent 
    Sets and Association Rules   

"""

from collections import defaultdict
import csv
import os
from pathlib import Path


class Apriori(object):
    def __init__(self, minSupp, minConf):

        self.minSupp = minSupp #최소 지지도와
        self.minConf = minConf  #최소 신뢰도를 입력받음

    def fit(self, filePath):
        """ Run the apriori algorithm, return the frequent *-term sets. 
        """
        # Initialize some variables to hold the tmp result
        transListSet  = self.getTransListSet(filePath)   # get transactions (list that contain sets)
        itemSet       = self.getOneItemSet(transListSet)# get 1-item set

        itemCountDict = defaultdict(int)         # key=candiate k-item(k=1/2/...), value=count
        freqSet       = dict()                   # a dict store all frequent *-items set

        self.transLength = len(transListSet)     # number of transactions
        self.itemSet     = itemSet

        # Get the frequent 1-term set
        freqOneTermSet = self.getItemsWithMinSupp(transListSet, itemSet,
                                                  itemCountDict, self.minSupp)

        # Main loop
        k = 1
        currFreqTermSet = freqOneTermSet
        while currFreqTermSet != set():
            freqSet[k] = currFreqTermSet  # save the result
            k += 1
            currCandiItemSet = self.getJoinedItemSet(currFreqTermSet, k) # get new candiate k-terms set
            currFreqTermSet  = self.getItemsWithMinSupp(transListSet, currCandiItemSet,
                                                        itemCountDict, self.minSupp) # frequent k-terms set


        #
        self.itemCountDict = itemCountDict
        self.freqSet       = freqSet
        return itemCountDict, freqSet

    def getSpecRules(self, filePath, rhs):
        """ Specify a right item, construct rules for it
        """
        filePath = os.path.join(filePath, 'dataset-price.csv')

        filePath2 = Path(filePath).parent
        filePath2 = os.path.join(filePath2, 'dataset-quantity.csv')

        ItemPriceListSet = {}

        with open(filePath, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for item, price in reader:
                ItemPriceListSet.update({item: price})

        transListSet = defaultdict(int)

        temp = set()
        temp2 = ''

        transaction = defaultdict(int)
        tranlist = []

        with open(filePath2, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for line in reader:
                for term in line:
                    if term.isdigit():
                        transListSet[temp] += int(term)
                    else:
                        temp = (frozenset([term]))

        with open(filePath2, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for line in reader:
                transaction = defaultdict(int)
                for term in line:
                    if term.isdigit():
                        transaction[frozenset([temp2])] = int(term)
                    else:
                        temp2 = term
                tranlist.append(transaction)

        if rhs not in self.itemSet:
            print('Please input a term contain in the term-set !')
            return None

        rules = dict()
        for key, value in self.freqSet.items():
            for item in value:
                count = 0
                tran_count = 0
                element = ''
                if rhs.issubset(item) and len(item) > 1:
                    item_supp = self.getSupport(item)
                    item = item.difference(rhs)
                    for element in item:
                        element = element
                        count = count + transListSet[frozenset([element])]

                    for line in tranlist:
                        if frozenset([element]) in line:
                            for key, value in line.items():
                                if rhs == key:
                                    tran_count += value

                    conf = item_supp / self.getSupport(item)
                    conf = conf*float(tran_count)/float(count)
                    if conf >= self.minConf:
                        rules[item] = conf
        price_rules = defaultdict(int)

        for key, value in rules.items():
            for item, price in ItemPriceListSet.items():
                if item in rhs:
                    price_rules[key] += float(value)*float(price)

        return rules, price_rules

    def getSupport(self, item):
        """ Get the support of item """
        return self.itemCountDict[item] / self.transLength

    def getJoinedItemSet(self, termSet, k):
        return set([term1.union(term2) for term1 in termSet for term2 in termSet
                    if len(term1.union(term2))==k])

    def getOneItemSet(self, transListSet):

        itemSet = set()
        for line in transListSet:
            for item in line:
                itemSet.add(frozenset([item]))
        return itemSet

    def getTransListSet(self, filePath):

        filePath = os.path.join(filePath, 'dataset-quantity.csv')
        transListSet = []
        with open(filePath, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for line in reader:
                transset = set()
                for term in line:
                    if term.isdigit():
                        continue
                    transset.add(term)
                transListSet.append(transset)
        return transListSet

    def getItemsWithMinSupp(self, transListSet, itemSet, freqSet, minSupp):

        itemSet_  = set()
        localSet_ = defaultdict(int)
        for item in itemSet:
            freqSet[item]   += sum([1 for trans in transListSet if item.issubset(trans)])
            localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])

        # Only conserve frequent item-set 
        n = len(transListSet)
        for item, cnt in localSet_.items():
            itemSet_.add(item) if float(cnt)/n >= minSupp else None

        return itemSet_

    def getItemPriceListSet(self, filePath):  #제품별 가격을 dictionary로 선언하여 key value로 담아준다

        filePath = os.path.join(filePath, 'dataset-price.csv')

        ItemPriceListSet = {}

        with open(filePath, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for item, price in reader:
                ItemPriceListSet.update({item: price})

        return ItemPriceListSet
