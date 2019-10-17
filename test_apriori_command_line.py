# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 10:05:45 2018

@author: zbj
"""

from optparse import OptionParser    # parse command-line parameters
from apriori import Apriori
from pathlib import Path

if __name__ == '__main__':
    
    # Parsing command-line parameters
    optParser = OptionParser()
    optParser.add_option('-f', '--file',
                         dest='filePath',
                         help='Input a csv file',
                         type='string',
                         default=None)  # input a csv file

    optParser.add_option('-s', '--minSupp',
                         dest='minSupp',
                         help='Mininum support',
                         type='float',
                         default=0.10)  # mininum support value
                         
    optParser.add_option('-c', '--minConf', dest='minConf',
                         help='Mininum confidence',
                         type='float',
                         default=0.40)  # mininum confidence value    
                         
    optParser.add_option('-r', '--rhs', dest='rhs',
                         help='Right destination',
                         type='string',
                         default=None)  # 

    (options, args) = optParser.parse_args()       
        
    # Get two important parameters
    filePath = options.filePath
    minSupp  = options.minSupp
    minConf  = options.minConf
    rhs      = frozenset([options.rhs])
    print("""Parameters: \n - filePath: {} \n - mininum support: {} \n - mininum confidence: {} \n - rhs: {}\n""".\
          format(filePath,minSupp,minConf, rhs))

    # Run and print
    objApriori = Apriori(minSupp, minConf)
    itemCountDict, freqSet = objApriori.fit(filePath)
    for key, value in freqSet.items():
        print('frequent {}-term set:'.format(key))
        print('-'*20)
        for itemset in value:
            print(list(itemset))
        print()

    # Return rules with regard of `rhs`

    rules, conf_rules = objApriori.getSpecRules(filePath, rhs)

    print('-'*20)
    print('rules refer to {}'.format(list(rhs)))
    print('제품 연관도 기댓값')
    for key, value in rules.items():
        print('{} -> {}: {}'.format(list(key), list(rhs), value))
    print('-'*20)
    print('rules refer to {}'.format(list(rhs)))
    print('물품에 따른 수익')
    for key, value in conf_rules.items():
        print('{} -> {}: {}'.format(list(key), list(rhs), value))