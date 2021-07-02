from poissonDraw import drawDistribution
import matplotlib.pyplot as plt
import pickle

LFX = []
LambdaY = []
for LF in range(0, 305, 5):
    expX, expP, normX, normY, poissonX, poissonY, Lambda = drawDistribution(loadFactor=LF, drawing=False)
    LFX.append(LF)
    LambdaY.append(Lambda)

with open("LFX.txt", "wb") as fp:   #Pickling
    pickle.dump(LFX, fp)
with open("LambdaY.txt", "wb") as fp:   #Pickling
    pickle.dump(LambdaY, fp)

plt.title("Lambda vs. load factor")
plt.xlabel("load factor")
plt.ylabel("Lambda")
plt.plot(LFX,LambdaY,'rs')
# plt.legend()
plt.show()