from .poissonDraw import drawDistribution
import matplotlib.pyplot as plt

'''
In this file, we import "drawDistribution" module from poissonDraw. 
We want to know how "load factor" affects "lambda"(weighted average of distribution of bin of length, which is also the peak.). 
For each load factor, say 1 to 400 stepped by 5, we call "drawDistribution" to calculate the lambda at a single time of experiment. 
After conducting many times of experiments, we plot "lambda" to "load factor". Note that "lambda" is affected by "nodeNum" and "loadFactor", so here we fix the nodeNum to simplify the situation(of course you can test different nodeNum).
'''
def drawLFandLambda(nodeNum=10000):
    LFX = []
    LambdaY = []
    for LF in range(1, 400, 5):
        expX, expP, normX, normY, poissonX, poissonY, Lambda, rootType = drawDistribution(nodeNum=nodeNum,loadFactor=LF, drawing=False,TREEIFY_THRESHOLD=8)
        LFX.append(LF)
        LambdaY.append(Lambda)


    plt.title("Lambda vs. load factor")
    plt.xlabel("load factor")
    plt.ylabel("Lambda")
    plt.plot(LFX,LambdaY,'rs')
    plt.show()