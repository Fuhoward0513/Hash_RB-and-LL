from poissonDraw import drawDistribution
import matplotlib.pyplot as plt
import pickle

# LFX = []
# LambdaY = []
# for LF in range(1, 400, 5):
#     expX, expP, normX, normY, poissonX, poissonY, Lambda, rootType = drawDistribution(loadFactor=LF, drawing=False)
#     LFX.append(LF)
#     LambdaY.append(Lambda)

# with open("LFX.txt", "wb") as fp:   #Pickling
#     pickle.dump(LFX, fp)
# with open("LambdaY.txt", "wb") as fp:   #Pickling
#     pickle.dump(LambdaY, fp)

with open("LFX.txt", "rb") as fp:   #Unpickling
    LFX = pickle.load(fp)
with open("LambdaY.txt", "rb") as fp:   #Unpickling
    LambdaY = pickle.load(fp)


plt.title("Lambda vs. load factor")
plt.xlabel("load factor")
plt.ylabel("Lambda")
plt.plot(LFX,LambdaY,'rs')
plt.show()