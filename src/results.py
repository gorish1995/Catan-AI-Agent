from log import *
from play import *
from players import *
from collections import defaultdict
import sys 

def main():
  
    colors = ['orange', 'red', 'green', 'blue']

    # Changes to this may also require changes throughout the rest of the file
    possibleClasses = ['qAI', 'WeightedAI', 'qAI_improved', 'minimax']

    testName = sys.argv[1]
    baseClass = sys.argv[2]
    testClass = sys.argv[3]

    print(testName, baseClass, testClass)
    assert baseClass in possibleClasses and testClass in possibleClasses
  
    # Should take in a trained weights filename created via train.py as the 4th argument
    assert len(sys.argv) >= 5
    trainedWeightsLog = Log(sys.argv[4])

    # Set the baseline weights that we are comparing against. Can either be randomized or
    # defined by us
    
    # If we are using user-defined baseline weights, then pass -w as the fourth argument
    weightLogSpecified = len(sys.argv) == 7 and sys.argv[5] == '-w'

    # If the -w flag is set, then an argument should also be passed with the name
    # of the user-defined weight file
    if weightLogSpecified:
        print('weight log specified')
        baselineWeights = [Log(sys.argv[6])] * 4
    else:
        # Create new random weights for each of the baseline AIs
        # These will be randomized in players.py as we've been doing
        baselineWeights = [Log('BaselineAiWeightsLog%s.txt' % i) for i in range(4)]
        for i in range(4):
            baselineWeights[i].log_dict({'DELETE ME': -1})
  
    dump = Log(testName)
    dump.log('Test: ' + str(testName))
    dump.append('Base class: ' + str(baseClass))
    dump.append('Test class: ' + str(testClass))
    dump.append_dict(trainedWeightsLog.readDict())
    dump.append('\n')

    aggregateWins = 0
    aggregateGames = 0

    # Run the test player 100 times starting from each of the 4 different turn orders
    for i in range(4):
        
        print('i = ' + str(i))     
        
        def createPlayers():
            players = [] 
            
            # Initialize all 4 players of type 'base class'
            if baseClass == 'qAI':
                players = [qAI(j, str(j), colors[j], baselineWeights[j]) for j in range(4)]
            elif baseClass == 'WeightedAI':
                players = [WeightedAI(j, str(j), colors[j], baselineWeights[j]) for j in range(4)]
            elif baseClass == 'qAI_improved':
                players = [qAI_win(j, str(j), colors[j], baselineWeights[j]) for j in range(4)]
            elif baseClass == 'minimax':
                players = [qAI_minimax(j, str(j), colors[j], baselineWeights[j]) for j in range(4)]
                

            # Overwrite 1 player of type 'test class' to start in position i
            if testClass == 'qAI':
                players[i] = qAI(i, str(i), colors[i], trainedWeightsLog) 
            elif testClass == 'WeightedAI':
                players[i] = WeightedAI(i, str(i), colors[i], trainedWeightsLog) 
            elif testClass == 'qAI_improved':
                players[i] = qAI_win(i, str(i), colors[i], trainedWeightsLog) 
            elif testClass == 'minimax':
                players[i] = qAI_minimax(i, str(i), colors[i], trainedWeightsLog) 
            return players

        winners = {p:0 for p in range(4)}
        for _ in range(25):
            play = Play(createPlayers())
            play.main()
            
            for player in play.players:
                if player.score >= 10:
                    winners[player.turn_num] += 1
        print('updating aggregate wins')
        aggregateWins += winners[i]
        aggregateGames += 25 # Ignore that some games may not have had a winner
    
        dump.append('With starting position ' + str(i) + ':')
        dump.append_dict(winners)
        dump.append('\n')
    
    print('final logging')
    dump.append('\n')
    dump.append('Aggregate from each of 4 starting positions:')
    dump.append(str(aggregateWins) + ' wins')
    dump.append(str(aggregateGames) + ' games')
    dump.append(str(aggregateWins * 1.0 / aggregateGames) + ' win percentage for test class')

if __name__ == '__main__':
    main()
