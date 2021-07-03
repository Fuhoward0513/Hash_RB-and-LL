可能要做的事情：
- [ ] Experiments
- [ ] Discussion
- [ ] Conclusion
- [ ] 包好repo，寫使用說明
- [ ] Demo影片
- [ ] 有空的話，可以寫個小網站讓大家查詢英文單字
- [ ] 再看一下Mark還有什麼要求




# Deep Into HashMap

:bulb: 深入探討在jdk1.8版本中的HashMap，其hash collision機制：在bin中擴展成Linked List或Red Black Tree。在閱讀過官方的原始碼後，**我們好奇是否可以有更好的參數設定來使效能更好？** 這是幾乎沒有前人做過的，於是我們仿照java的source code使用python實作完全同樣功能的HashMap，接著使用370,000個英文單字作為資料集map進hash table中，同時測試與jdk1.8官方設定中不同的參數，以理論和實驗數據分析HashMap效能。
<br><br>

## :orange_book: Introduction & More about HashMap
在開始前，我們先來簡單了解一下jdk1.8的HashMap (以下統稱HashMap) 是怎麼運作的？
<br>參考以下概念圖：

![](https://i.imgur.com/WaeVbPl.png)


透過閱讀官方source code，我們整理出HashMap中主要且重要的幾個觀念：
> :heavy_check_mark: hash table會隨著元素增多而自動進行擴容。<br>
> :heavy_check_mark: hash collision的機制為「在碰撞的bin後面接成Linked List」。<br>
> :heavy_check_mark: hash collision進階機制為「若Linked List太長，轉換成Red Black Tree(以下統稱treeify)」。 <br>

然而其中可探討以及有趣的部份也不少，也是本次專題我們要深入討論的部分，例如：
<b>

:large_orange_diamond: 為何要擴容？擴容的時機點為何？<br>
:large_orange_diamond: 為何要進行treeify？又Linked List太長的標準為何？

</b>

其實這些問題官方都有自己的詮釋與參數設定：<br>
* `load factor`: 設定為`0.75`。當table中的總元素數量大於`table size * load factor`時，table進行擴容。擴容方式為將table直接擴充一倍，並將table中所有元素重新hash一遍，以讓它們能分布在新擴充出的格子裡。
* `TREEIFY_THRESHOLD`: 設定為`8`。當Linked List的長度大於等於`TREEIFY_THRESHOLD`時，將Linked List裡元素結構直接改成Red Black Tree。

閱讀到這裡後我們的第一個想法為：為何這些參數的值是這樣？我們可以理解`TREEIFY_THRESHOLD`不能太大，因為這樣永遠都無法轉換成Red Black Tree，若Linked List太長，搜尋效率就只能是較慢的O(N)。但也不能太小，因為這樣會太頻繁地轉換Red Black Tree，影響建立Map的效率。另外，`load factor`決定table何時要double size，所以也會影響到Linked List的長度。因此，我們認為應該會有一個較好的參數組合(`TREEIFY_THRESHOLD`, `load factor`)來使建立map的效率較好，且同時搜尋時間也能較快，在本次專題報告中，我們會先簡述自己實作HashMap的過程，接著我們會不斷改變這幾個變因，實測不同參數下的效能分析。




## Table of Contents

## :hammer: Data Structure Implementation
### :clipboard: HashMap Implementation
原則上我們仿照jdk1.8版本的HashMap的邏輯重建python版的HashMap，將之簡化後可以參考以下這個流程圖：([圖片來源](https://blog.csdn.net/u011240877/article/details/53358305#hashmap-%E5%9C%A8-jdk-18-%E4%B8%AD%E6%96%B0%E5%A2%9E%E7%9A%84%E6%93%8D%E4%BD%9C-%E6%A0%91%E5%BD%A2%E7%BB%93%E6%9E%84%E4%BF%AE%E5%89%AA-split ))
![](https://i.imgur.com/FB0iMd0.png)
然而在我們實作的HashMap中，還是有幾點與官方不同:
1. 我們並未設置`UNTREEIFY_THRESHOLD`，也就是說，在table進行resize的時候，若bucket(table中的元素)中是RB Tree，我們直接將Tree中的所有節點pop出來，重新對它們進行hash分配。反之，官方則是有特殊的`split()`來處理resize時RB Tree的修剪。
2. 我們並未在節點儲存`hash`屬性，所以在table resize的時候，我們使用每個節點的`key`屬性重新計算hash value。反之，官方則有這個屬性，方便其rehash時不用重新計算hash value，只要將其分配原地或2倍長度後的bucket的位置即可(因為resize是將table直接double size，故節點要嘛是在同位置，要嘛是兩倍index後的位置)。
3. 我們額外建立一個Red Black Tree的class建立實體放在table的bucket裡。官方則只是在HashMap程式碼中嵌入TreeNode和實作RB Tree的主要運算函式。

依照jdk1.8的邏輯，our `putValue()` method in class `HashMap`:
 ```python+=
 def putValue(self, newNode):
        hashValue = self.hashCode(newNode.value)
        root = self.hashTable[hashValue]
        if(root == None): # empty space
            self.hashTable[hashValue] = newNode
            self.incrementTotal()
        else: # Already somebody there.
            if(isinstance(root, RBTree)): # if it's a tree, addtreeVal
                root.insert(self.LL2TreeNode(newNode))
                self.incrementTotal()
            elif(root.value == newNode.value): # if exact same key, override.
                self.hashTable[hashValue] = newNode
            else: # it's LL.
                binCount = 0
                while(root!=None):
                    if(root.next == None):
                        root.next = newNode
                        self.incrementTotal()
                        binCount += 1
                        if(binCount >= self.TREEIFY_THRESHOLD):
                            self.treeifyBin(hashValue)
                        break
                    if(root.next.value == newNode.value): # if exact same key, override.
                        root.next = newNode
                        break
                    binCount += 1
                    root = root.next

        threshold = self.getTableSize() * self.loadFactor
        if(self.totalElement > threshold):
            self.tableResize()
```
除此之外，在本次資料集中我們使用的是英文單字，我們用作其單字本身作為key代入hash function中，我們所使用的hash function為：

***hash value*** $=s[0]\cdot31^{n-1} + s[1]\cdot31^{n-2} + \cdots + s[n-1]$

其中`s`為單字字串，`s[i]`為單字中第i個位置的字元的ASCII值，`n`為單字長度。最後將算得`hash value` 去mod table size即可得到其在table該存放的index位置，code如下：
```python+=
def hashCodeString(self, key):
    hashValue = 0
    for char in key:
        hashValue = hashValue * 31 + ord((char))
    return hashValue % self.getTableSize()
```

### :evergreen_tree: Red Black Tree Implementation
這次我們紅黑樹並未使用 Python 提供的套件，而是使用手刻的方式。
因應 HashMap 這次寫了 `search()`、`insert()`、`delete()`三種函式，但`delete()` 在最後的實作中並未使用到。使用時機為當bucket裡面的Linked List長度超過`TREEIFY_THRESHOLD`時，將Linked List內的節點一一`insert`進新建立的RB Tree實體。當使用者在查找元素的時候，如果發現在table上對應的hash value的bin的根節點是RB Tree的話，啟用`search`，達到O(logN)的查找速率。

至此我們已經準備好了實驗所需的工具，接下來只要將data set一個一個map進table中，table會根據參數`load factor`, `TREEIFY_THRESHOLD`決定何時該resize？以及何時該將過長的Linked List轉換成RB Tree？所以下面我們設想了多種情況進行實驗和理論分析，除了探討「load factor對bucket內平均長度的影響」、「load factor對RB Tree轉換率的影響」外，我們還會著重觀察在不同參數設定下的HashMap，其「建立map所需時間」以及「search item所需時間」來進行分析。



## :bar_chart: Experiments

### Probability of Hash Collision
我們可以看到java中的HashMap在達一定填充量時有自動擴容的功能，也就是說，table會永遠維持一定比例的填充量，這個比例由`load factor`控制。回想HashMap擴容的機制為
> 當table中的總元素數量大於`table size * load factor`時，table會double sized.

`load factor`越大代表`table size * load factor`也越大，也就代表元素總數量越不容易超過`table size * load factor`，也就意味著table不容易產生resize，導致table size較小，table的每個bucket都被填充的機率也就較大。舉極端的例子而言，假設load factor極小(趨近於0)，table每新增一個元素就進行擴容，那麼此table一定相當稀疏。

然而對我們來說，hash collision的碰撞機率其實相當重要，為什麼呢？因為若碰撞機率大，bucket後面所串接的元素也會越多，那麼`TREEIFY_THRESHOLD`的設置也就相當重要。倘若今天`load factor`很小，導致碰撞機率極小，結果bucket後面只有1~2個元素，但是`TREEIFY_TRESHOLD`卻設為10，那這樣配置下的treeify機制形同虛設。換句話說，如果我們能知道`load factor`配置下的碰撞機率，我們就能大概知道bucket後面串接了多少元素，也就大概知道`TREEIFY_THRESHOLD`要設置為多少才有機會產生treeify行為。

所以問題來了，我們該怎麼從`load factor`得知碰撞機率？在回答這個問題之前，我們直接進行實驗，下面我們在給定的load factor下，建立一個HashMap，`TREEIFY_THRESHOLD`在這裡並不重要，因為我們只是要觀察bucket後面串接的元素數量，不管其為Linked List或Red Black Tree。接著直接往HashMap插入370,000筆英文單字，最後統計table中bucket串接元素數量(以下統稱bucket長度)的個數，舉例來說：bucket長度為100的有53個，長度為105的有46個，長度為87的有33個…，最後將其表示為機率的形式，即可得出一類似機率密度函數的圖：
>`input nodes`: 370,000<br>
>`load factor`: 10
> ![](https://i.imgur.com/Xg9hs1J.png)

可以看到結果其實發人省思，我們可以觀察到:
1. 就算插入了370,000個點，HashMap也能讓每個bucket所串接的元素在0~18個點左右。
2. 其分布結果非常類似常態分佈

對於它非常類似常態分佈的結果，我很好奇，在找尋眾多資料後，我們在官方source code的某一處註解看到下列訊息：
> Ideally, under random hashCodes, the frequency of
nodes in bins follows a Poisson distribution (http://en.wikipedia.org/wiki/Poisson_distribution) with a parameter of about 0.5 on average for the default resizing threshold of 0.75, although with a large variance because of resizing granularity. Ignoring variance, the expected occurrences of list size k are (exp(-0.5) * pow(0.5, k) / factorial(k)). The first values are:<br>
>0:    0.60653066<br>
>1:    0.30326533<br>
>2:    0.07581633<br>
>3:    0.01263606<br>
>4:    0.00157952<br>
>5:    0.00015795<br>
>6:    0.00001316<br>
>7:    0.00000094<br>
>8:    0.00000006<br>
>more: less than 1 in ten million<br>

簡單來說，bucket後面串接的元素數量其實可以用`Poisson Distribution`來描述，在這裡就不詳說Poisson Distribution的原理。但確實如此，為了驗證這個機率分布是否是Poisson Distribution，我們重新做一次實驗，因為在Poisson Distribution中我們需要計算factorial，故這次僅插入50,000個英文單字，接著將實驗數據結果做加權平均，得到：
>Experimental weighted average of 'nodes in bins': 6.103515625<br>

將這個值作為Poission Distribution $P\left( x \right) = \frac{{e^{ - \lambda } \lambda ^x }}{{x!}}$ 中的$\lambda$，我們將之繪在同張圖上，可得：
>`input nodes`: 50,000<br>
>`load factor`: 10 <br>
![](https://i.imgur.com/RIJqLVn.png)

奇蹟似地吻合了！


### Time to Construct HashMap
#### (1) Load Fator
![](https://i.imgur.com/PatosmL.png =455x300)

`load factor` 是影響 Construct HashMap 一個重要變數之一，因為當 HashMap 內元素數量大於 table_size* `load factor`時 HashMap 會進行resize(table_size變為原本的2倍)，因此可以知道當 `load factor` 越小時 resize 的頻率會上升，因此 index collision 的機率會下降， HashMap 每個 bucket 內所串聯的元素數量會相少，因此整個 HashMap 的結構會由較多的 Linked list 所組成。

相反的，當 `load factor` 越大時 resize 的頻率會下降，因此 index collision 的機率會上升， HashMap 每個 bucket 內所串聯的元素數量會相對較多，整個 HashMap 的結構可能會由較多的 RB Tree 所組成。

:bulb:`Note: TREEIFY_THRESHOLD會影響一個bucket裡面元素是為Linked List或RB Tree的機率，所以在這個實驗中我們把它設為定值，如此便可以有「當串聯元素越多，越有可能會RB Tree」的結論，以利我們做接下來的分析。關於TREEIFY_THRESHOLD更詳細的分析可見下節。`

而由時間複雜度來看的話:

1. link list insertion in HashMap is O(1)
2. RB Tree insertion in HashMap is O(logN)

因此理論上而言，若在 `TREEIFY_THRESHOLD` 固定的情況下，當`load factor` 越小時，table裡有較多Linked List，因為插入時間為O(1)，Construct HashMap 的時間應該較短; 相反的，當`load factor` 越大時，table裡有較多RB Tree，因為插入時間需要O(logN)，Construct HashMap 的時間應該較長。

為了驗證這件事，我們將`TREEIFY_THRESHOLD`設為定值(=4)，在一定的`load factor`下建立100個HashMap，分別插入100, 200, 300,..., 10000個點，每次都記錄建立HashMap的時間。接著切換不同`load factor`= 0.75、1.5、3、6 做一樣的實驗，最後將Construct HashMap 所需時間相對於內部元素數量的關係繪製成圖:

![](https://i.imgur.com/Lj8e23X.png)

由上圖可以發現確實當要創建一個越大的 HashMap ，`load factor`越大所需要的時間越多，也因此證明了上面所述的猜測。

#### (2) Treeify Threshold
`TREEIFY_THRESHOLD`也是影響 Construct HashMap 一個重要變數之一，當 bucket 內的 linked List 長度大於 `TREEIFY_THRESHOLD`時，會進行 `Treeify()` 將 bucket 內元素由 Linked List 結構轉為 RB Tree 結構。

因此我們猜測，當`load factor`固定的情況下，可以分為下面兩種狀況:
1. `TREEIFY_THRESHOLD`越小，隨著插入的元素增加，bucket 內linked list 長度大於`TREEIFY_THRESHOLD`的機率會相對較高，因此HashMap 會較為頻繁的進行`Treeify()`，而每次`Treeify()`所需的時間為 O(NlogN)，並且變為 RB Tree 結構後，插入新元素時的時間 O(logN)，會比原本的 Linked List 結構的 O(1) 還要來的大，因此 Construct HashMap 的時間應該較長。
2. `TREEIFY_THRESHOLD`越大，bucket 內linked list 長度大於`TREEIFY_THRESHOLD`的機率會相對較低，因此進行 `Treeify()`的頻率會較低，除此之外插入新元素的時間為 O(1)，相較於 RB Tree 結構的 O(logN)來的小，也因此 Construct HashMap 的時間應該較短。

為了驗證這個猜測，我們將`load factor`設為定值(=1)，在一定的`TREEIFY_THRESHOLD`下建立100個HashMap，分別插入100, 200, 300,..., 10000個點，每次都記錄建立HashMap的時間。接著切換不同`TREEIFY_THRESHOLD`= 1, 2, 4, 8 做一樣的實驗，最後將Construct HashMap 所需時間相對於內部元素數量的關係繪製成圖:

![](https://i.imgur.com/SEsn1kF.png)

由上圖可以發現確實當要創建一個越大的 HashMap ，當`TREEIFY_THRESHOLD`越小所需要的時間越多，也因此證明了上面所述的猜測。

### Average Searching Time
一個 HashMap 的 Searching Time



### 






## :book: Discussion
## :bulb: Conclusion

## :bulb: What is My-sweety?
It's a productivity app built for lazybones and those who suffer from procrastination. Users only need to tell Sweety two things:<br>
<b>
<br>:large_orange_diamond:1. What are your to-do events? (including deadline, priority, total needed time, etc.)
<br>:large_orange_diamond:2. What is your daily available time in a week?

</b>

With these information, our scheduling algorithm will arrange your segmented events to different days optimally.
In addition, we also provide progress and diligence analysis so that you can clearly see what you've done so far.

<br>

## :date: Why My-sweety ?

We've seen lots of productivity apps with calendar and todo-list functions. However, it's rare to find apps that can do auto-scheduling. Our goal is, by helping users schedule the events optimally in advance, <b>to force them to be aware of the total amounts of undone tasks, so that they won't misestimate the remaining time to work hard. </b> 
<br><br>
Also, with all stuffs and statistics displayed in clear chart and graph, users get to evaluate their own performances.
So we'll confidently say these are the advantages of our app:
<b>

:heavy_check_mark: Optimal Scheduling <br>
:heavy_check_mark: Schedule Visualization <br>
:heavy_check_mark: Workloads Clearly Showed <br>
:heavy_check_mark: Progress Evaluation and Supervision <br>
</b>

<br>

## :hammer: Packages/Tools for building My-sweety
In this app, we come up with functions and ideas by ourselves. We also develop our own scheduling algorithm. But for the css style, we benefit a lot from open source. For example, `nivo` provides a wonderful chart/graph, and `mixamo` gives us vigorous 3D model and animations. Last but not least, Material UI is also a big helper. Check out all the packages and tools we've used:
+ Frontend
  - ReactJS
  - React Router
  - Three
  - React Three Fiber
  - React Three Drei
  - React Draggable
  - React Icons
  - Material UI
  - Axios
  - Jwt Decode
  - [nivo](https://nivo.rocks/)
  - [mixamo](https://www.mixamo.com/) (with [blender](https://www.blender.org/) & [gltfjsx](https://github.com/pmndrs/gltfjsx))
+ Backend
  - Express
  - nodemon
  - cors
  - jwt
  - mongoose
  - bcrypt
  - babel
  - mongoDB



# Getting Started
## Installation
1. **Clone the repository**
    ```shell=
    git clone https://github.com/Eric8808/wp1092.git
    ```
    ##### _:bulb:<font color=#F00078>The project is located at </font><font color=#A23400>`wp1092/final/my-sweety`</font>_
2. **Install node.js**  (If you have installed node.js, you can skip the step.) 
    * download from https://nodejs.org/en/
    * version "14.17.1" has been verified working fine.

3. **Install nvm**  (If you have installed nvm, you can skip the step.)
    * download from https://github.com/coreybutler/nvm-windows/releases/download/1.1.7/nvm-setup.zip
    * installation
    ```shell=
    nvm install 10.16.0
    nvm use 10.16.0
    ```
4. **Install yarn**  (If you have installed yarn, you can skip the step.)
    ```shell=
    npm install --global yarn
    ```
5. **Install the dependencies for the project**
    > go to the project directory (wp1092/final/my-sweety)
    ```shell=
    cd frontend
    yarn install
    ```
    ```shell=
    cd ../backend
    yarn install
    ```

6. **Start the project**
    > go to the project directory (wp1092/final/my-sweety)
    * open one terminal
    ```shell=
    yarn server
    ```
    :bulb:`note: We have prepared .env file for you, so you can directly run the server to connect to our mongoDB.`
    * open another terminal
    ```shell=
    yarn start
    ```

## Tutorial
If you haven't watched our demo video, go watch it and you'll know how easy to use our app:
>https://youtu.be/QRcVlVdssIo 
<br>

Alternatively, the following tutorial can help you navigate through our app:
<br>
Let's get started!

After running `yarn server` and `yarn start` in the project directory, if everything works fine, you'll see a home page like this. Then, simply click the phone button in the top center to continue.
![](https://i.imgur.com/YfLiNRK.png)

### Login Page
![](https://i.imgur.com/xgTacG1.png)
* Sign in/up your own account 
<br>(check out the author of the css style: https://www.florin-pop.com/)
<br>:bulb:`note: When signing up, since we are letting everyone to use our mongoDB right now, the username you typed may have been used. In such situation, please use another username to sign up.`
### Main Page
#### :calendar: Schedule Mode
![](https://i.imgur.com/Ahr9W6D.png)
#### 1. Adjust your daily available time.
Change the number under the calender.
#### 2. Add the tasks.
Press the `"Add"` button on the top to add a task in the TODO list. And you need to give some information about the task.
* Task name  
* Priority : `the order we schedule the task for you`
* Total time : `the time you need to complete the task`
* Separate : `the number of segments you want to break the task into` 
* Deadline  

:bulb:<b>note: please make sure </b>`Separate` <b>divides</b> `Total time`.

(You can add multiple tasks in the TODO list.)
#### 3. Schedule
Press the `"Schedule"` button. And we will schedule all the tasks in the TODO list. Your tasks will be moved to the "Scheduled List".

---

#### Follow the steps 1~3 above, your schedule will be filled. Next, you can adjust the schedule.
![](https://i.imgur.com/Ia2kZt6.png)
* You can switch to another week using the arrows next to the dates.
* If you have completed any task, you can click it in the schedule and click ``"COMPLETED"`` in the pop up dialog. This will turn the task color into green.
* You can also remove the task by clicking it and click ``"REMOVE"``. 

<img src="https://i.imgur.com/TIS6JAt.png" width=70%>

* Click the tasks in the TODO/Scheduled list to show the information about it.
* The little boxes in the scheduled list show the rate of completion.  
(The green ones mean `completed`, and the red ones mean `uncompleted`)  
#### :zap: Additional feature:  If you didn't complete all tasks today, the undone tasks will be moved to the TODO list when you login tomorrow. At that time, feel free to schedule them again.  

---

#### :chart_with_upwards_trend: Evaluation mode
After adding several tasks and completing several segments in the schedule. Let's see how diligent you are this week and how far you've moved forward!

By clicking the mode-switching button in the bottom left, we can enter `Evaluation Mode`.
![](https://i.imgur.com/jIUnJ2l.png)

Then you'll see a dashboard composed of several charts in the page, like this:
![](https://i.imgur.com/SQ4gsJW.png)
In this page, feel free to browse and check your personal statistics. More specifically, you'll find 3 main components here:

:large_blue_diamond: Scheduled list composition (top left)<br>
:large_blue_diamond: Total completed rate (top right)<br>
:large_blue_diamond: Plot of `Available Time` and `Completed segments` for the past 7 days (bottom)<br>

Looking at these evaluation results, users get to realize how diligent they've been so far. Conversely, if the completion rate is low and only small amounts of segments had been completed, it's a good opportunity for users to reflect on themselves.


### Almost the End
So far we've gone through the main functions of our app. Other functions such as signing out, deleting account, error handling, and login authentication are, in my opinion, pretty trivial, so we'll not elaborate too much about them! By the way, the triggered animations of Sweety are all different when clicking different things. Feel free to try these additional functions!

# More about My-sweety
## 3D Model Rendering
In fact, our initial app was just a scheduling app. Then, we thought that it'll be more interesting and vigorous for the app to have a virtual assistant, just like Sweety! Thanks to [mixamo](https://www.mixamo.com/), we got a cool character and animations. However, we still need to do some preprocessing and write some code to embedded a 3D model into our app. Following the [tutorial](https://codeworkshop.dev/blog/2021-01-20-react-three-fiber-character-animation/?fbclid=IwAR1nMbHYSuauk2POh57G2vpFaDFsMfA8nVgyRZEMF-oczUHxl1_IJQ8IhKQ ) here: 

1. We first use a open-source 3D computer graphics software [blender](https://www.blender.org/) to stash animations to our character. Then we export it as a gltf file.
![](https://i.imgur.com/ilpJ4GU.png)

2. Then use a package called [gltfjsx](https://github.com/pmndrs/gltfjsx) to generate jsx related file based on the given gltf file. The result will be something like this: 
```javascript=+
import React, { useRef } from 'react'
import { useGLTF, useAnimations } from '@react-three/drei'

export default function Model(props) {
  const group = useRef()
  const { nodes, materials, animations } = useGLTF('/girl.gltf')
  const { actions } = useAnimations(animations, group)
  return (
    <group ref={group} {...props} dispose={null}>
      <group rotation={[Math.PI / 2, 0, 0]} scale={[0.01, 0.01, 0.01]}>
        <primitive object={nodes.Hips} />
        <skinnedMesh
          geometry={nodes.Girl_Body_Geo.geometry}
          material={materials.Girl01_Body_MAT1}
          skeleton={nodes.Girl_Body_Geo.skeleton}
        />
        <skinnedMesh
          geometry={nodes.Girl_Brows_Geo.geometry}
          material={materials.Girl01_Brows_MAT1}
          skeleton={nodes.Girl_Brows_Geo.skeleton}
        />
        <skinnedMesh
          geometry={nodes.Girl_Eyes_Geo.geometry}
          material={materials.Girl01_Eyes_MAT1}
          skeleton={nodes.Girl_Eyes_Geo.skeleton}
        />
        <skinnedMesh
          geometry={nodes.Girl_Mouth_Geo.geometry}
          material={materials.Girl01_Mouth_MAT1}
          skeleton={nodes.Girl_Mouth_Geo.skeleton}
        />
      </group>
    </group>
  )
}

useGLTF.preload('/girl.gltf')
```

3. Next, use `react-three-fiber` to add a Canvas, Camera,and Light component to contain the given 3D model. Finally, with `useEffect` and `useRef`, we get to switch different animations among the model.


## Scheduling Algorithm
This is an algorithm which can turn all the added tasks into a well-arranged schedule. 
> **Input**:
> 
>   1. Tasks to be scheduled
>   
>   2. The time periods that is currently occupied by previously scheduled tasks.
>
>   3. The user's weekly available time

> **Output**: 
> 
> 1. A new schedule

Each input task has the following properties: _Name, Priority, Needtime, Separate, Deadline_.

When the backend server gets a calculation request, it calls our scheduling algorithm. The way we take `priority` into account is that we sort the tasks by their priorities in advance, which will make the subsequent permutation always arrange the high-priority task to an earlier date. Then, we basically use brute force to permute all possible events order. For each way of permutation, distribute them into different days. So far we just get a possible schedule. However, for each possible schedule, we set some rules to determine if it's legitimate. The rules are as follows: 

**Rules**
> * not legitimate if the any event exceeds the deadline.
> * not legitimate if the any event is repeated in one day.
> * not legitimate if the total working hours exceed the available time on that day.

Once a possible schedule is determined as legitimate, we will push it into an array. However, as the number of events goes even higher, the algorithm could spend too much time and memory. Therefore, we set a threshold of the length of that array. Once over the threshold, we stop calculating any possible schedule.

Right now we only have few information from users to do optimization. In the future, we hope to include more personal traits to do calculation, such as personality or week preference. Therefore, to evaluate a schedule, we temporily set a performance indicator like this:

**the pseudo code which calculates the performance indicator**
```javascript=+
let performance = 0
for days in schedule
    for event in days
        performance += day.date - events.dealine
    end
end
```
In this code, the `performance` measures how early the event is done. To make sure the tasks are arranged earlier so as to prevent procrastination, `performance` should be as large as possible. Luckily, in the permutation stage, we arrange events into schedule from present to future. So it's highly possible that the generated schedule already has a pretty good `performance`. As mentioned earlier, the schedules in the limited array, say 100 schedules, are relatively good.  We finally choose a schedule that has the highest `performance` among the 100 relatively good schedules to be the winner, that is, the output schedule of this algorithm. 


## :evergreen_tree: File Tree

:books:my-sweety                           
├─ :open_file_folder:backend                          
│  ├─ :open_file_folder:src                           
│  │  ├─ :open_file_folder:models                     
│  │  │  └─ :green_book:User.js                 
│  │  ├─ :open_file_folder:routes                     
│  │  │  ├─ :open_file_folder:api                     
│  │  │  │  ├─ :green_book:account.js           
│  │  │  │  ├─ :green_book:data.js              
│  │  │  │  ├─ :orange_book:index.js        
│  │  │  └─ :orange_book:index.js                
│  │  ├─ :green_book:main.js                    
│  │  ├─ :green_book:mongo.js                   
│  │  └─ :green_book:schedule.js                
│  └─ :ledger:package.json            
├─ :open_file_folder:frontend                                     
│  ├─ :open_file_folder:src                           
│  │  ├─ :open_file_folder:Components                 
│  │  │  ├─ :green_book:AddDialog.js            
│  │  │  ├─ :green_book:CalenderDates.js        
│  │  │  ├─ :green_book:CalenderDrawer.js       
│  │  │  ├─ :green_book:CalenderPopUpWindow.js  
│  │  │  ├─ :green_book:model3D.js              
│  │  │  ├─ :green_book:ModePanel.js            
│  │  │  ├─ :green_book:SignOutPanel.js         
│  │  │  ├─ :green_book:SignOutPopUpWindow.js   
│  │  │  ├─ :green_book:sweety.js               
│  │  │  └─ :green_book:TaskDialog.js           
│  │  ├─ :open_file_folder:containers                 
│  │  │  ├─ :open_file_folder:LoginPage               
│  │  │  │  ├─ :art:login.css            
│  │  │  │  ├─ :blue_book:LoginCard.js         
│  │  │  │  ├─ :blue_book:LoginPage.js         
│  │  │  │  └─ :blue_book:SweetyLoginPage.js   
│  │  │  ├─ :open_file_folder:mainPage                
│  │  │  │  ├─ :open_file_folder:EvalutationMode      
│  │  │  │  │  ├─ :green_book:EvalChart.js      
│  │  │  │  │  ├─ :green_book:EvalPie.js        
│  │  │  │  │  └─ :green_book:Evaluation.js     
│  │  │  │  ├─ :blue_book:Calender.js          
│  │  │  │  ├─ :blue_book:Calender_old.js      
│  │  │  │  ├─ :blue_book:Header.js            
│  │  │  │  ├─ :blue_book:Panel.js             
│  │  │  │  ├─ :blue_book:ScheduledList.js     
│  │  │  │  └─ :blue_book:TodoList.js          
│  │  │  ├─ :globe_with_meridians:api.js                  
│  │  │  ├─ :orange_book:App.js                  
│  │  │  └─ :orange_book:Authenticate.js         
│  │  ├─ :open_file_folder:hooks                      
│  │  │  ├─ :closed_book:useCalender.js          
│  │  │  ├─ :closed_book:useDisplayStatus.js     
│  │  │  └─ :closed_book:useTodoList.js          
│  │  ├─ :art:App.css               
│  │  ├─ :art:index.css                  
│  │  ├─ :orange_book:index.js           
│  └─ :ledger:package.json                 
└─ :ledger:package.json     


## Contribution
Oftentimes, we debug together, so for the following division of labor, we'll just list the "main parts" that each of us are responsible for.

* B06502028 莊立楷
    > - 前後端資料傳送 & DB
    > - 登入&登出系統
    > - 前端 display message
    > - 前端 home page, login page UI
    > - 前端 evaluation mode UI
    > - 前端 schedule mode 各種UI: todolist, scheduled list, popupWindow, mode switching 
    > - 3D model, animations製作與render
    > - README
    > - Demo影片
    > - FB貼文
* B06502155 陳冠綸
    > * 設計前端 UI 與各個component的互動
    > * TODO list 和 scheduled list 的增減
    > * 控制 schedule的available time 
    > * 將後端傳回的schedule 資料經過處理後 render到前端
    > * schedule上的事件標示為完成或是移除
    > * schedule 日期切換
    > * 處理前端會遇到的error情況
    > * 將網站 deploy 到 heroku
    > * README
* B07502003 馮其安
    > * schedule 排程設計
    > * schedule 傳送與接收
    > * 將schedule事件回歸todolist
    > * 刪除空events與更新畫面
    > * 3D model 加入頁面
    > * 將排程合併並更新
    > * 各種exception處理
    > * installation 測試
    > * README
    