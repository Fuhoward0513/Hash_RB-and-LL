可能要做的事情：
- [ ] Experiments
- [ ] Discussion
- [ ] Conclusion
- [ ] 包好repo，寫使用說明
- [ ] Demo影片
- [ ] 有空的話，可以寫個小網站讓大家查詢英文單字
- [ ] 再看一下Mark還有什麼要求




# 深入探討jdk1.8版本HashMap機制之效能分析

:star: java的HashMap處理hash collision的機制原為在衝突的bucket中添加Linked List，但在jdk1.8改版後，若Linked List太長，則改為使用Red Black Tree。然而，在這樣的機制下HashMap的效能真的變好了嗎？這是幾乎沒有前人懷疑過的，但卻相當重要的，因為牽扯到的人所有HashMap使用者的效能。我們很好奇於是展開了一系列的研究，最後發現了許多有趣的東西，準備與你們分享！


:fire: 我們仿照java的source code使用python自己實作完全同樣功能的HashMap，在本專題中，我們使用370,000個英文單字作為資料集，並對HashMap進行一系列理論與實驗數據分析，在實驗結果裡意外發現許多好玩的事情，下面我們將帶您深入java HashMap的世界，期望您閱讀完後受益良多。
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
:ab: 除此之外，在本次資料集中我們使用的是英文單字，我們用作其單字本身作為key代入hash function中，我們所使用的hash function為：

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

:triangular_flag_on_post: 至此我們已經準備好了實驗所需的工具，接下來只要將data set一個一個map進table中，table會根據參數`load factor`, `TREEIFY_THRESHOLD`決定何時該resize？以及何時該將過長的Linked List轉換成RB Tree？所以下面我們設想了多種情況進行實驗和理論分析，除了探討「load factor對bucket內平均長度的影響」、「load factor對RB Tree轉換率的影響」外，我們還會著重觀察在不同參數設定下的HashMap，其「建立map所需時間」以及「search item所需時間」來進行分析。



## :bar_chart: Experiments & Discussion

### 	:mag_right: Probability of Hash Collision
> :bulb: Note: 在實驗開始前，會有一些先備知識以及我們共同的語言需要您先理解，希望您能好好閱讀完，非常感謝！

我們可以看到java中的HashMap在達一定填充量時有自動擴容的功能，也就是說，table會永遠維持一定比例的填充量，這個比例由`load factor`控制。回想HashMap擴容的機制為
> 當table中的總元素數量大於`table size * load factor`時，table會double sized.

`load factor`越大代表`table size * load factor`也越大，也就代表元素總數量越不容易超過`table size * load factor`，也就意味著table不容易產生resize，導致table size較小，table的每個bucket都被填充的機率也就較大。舉極端的例子而言，假設load factor極小(趨近於0)，table每新增一個元素就進行擴容，那麼此table一定相當稀疏。

然而對我們來說，hash collision的碰撞機率其實相當重要，為什麼呢？因為若碰撞機率大，bucket後面所串接的元素也會越多，那麼`TREEIFY_THRESHOLD`的設置也就相當重要。倘若今天`load factor`很小，導致碰撞機率極小，結果bucket後面只有1~2個元素，但是`TREEIFY_TRESHOLD`卻設為10，那這樣配置下的treeify機制形同虛設。換句話說，如果我們能知道`load factor`配置下的碰撞機率，我們就能大概知道bucket後面串接了多少元素，也就大概知道`TREEIFY_THRESHOLD`要設置為多少才有機會產生treeify行為。

:question: 所以問題來了，我們該怎麼從`load factor`得知碰撞機率？在回答這個問題之前，我們直接進行實驗，下面我們在給定的load factor下，建立一個HashMap，`TREEIFY_THRESHOLD`在這裡並不重要，因為我們只是要觀察bucket後面串接的元素數量，不管其為Linked List或Red Black Tree。接著直接往HashMap插入370,000筆英文單字，最後統計table中bucket串接元素數量(以下統稱bucket長度)的個數，舉例來說：bucket長度為100的有53個，長度為105的有46個，長度為87的有33個…，最後將其表示為機率的形式，即可得出一類似機率密度函數的圖：
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

簡單來說，bucket後面串接的元素數量其實可以用`Poisson Distribution`來描述，在這裡就不詳說Poisson Distribution的原理。但此情境確實符合Poisson Distribution的情境，為了驗證這個機率分布是否是Poisson Distribution，我們重新做一次實驗，因為在Poisson Distribution中我們需要計算factorial，故這次僅插入50,000個英文單字，接著將實驗結果的bucket內元素數量做加權平均，得到：
>Experimental weighted average of 'nodes in bins': 6.103515625<br>

將這個值作為Poission Distribution $P\left( x \right) = \frac{{e^{ - \lambda } \lambda ^x }}{{x!}}$ 中的$\lambda$ (Possion Distribution中的peak所在的x值)，我們將之繪在同張圖上，可得：
>`input nodes`: 50,000<br>
>`load factor`: 10 <br>
![](https://i.imgur.com/RIJqLVn.png)

奇蹟似地吻合了！

這個結果其實給我們巨大的幫助。我們有以下兩個結論：
1. Poisson Distribution中的$\lambda$可以作為我們實驗結果中bucket串接的元素平均數量的期望值
2. $\lambda$本身的意義可以解讀為hash collision發生的期望值

綜合以上兩點，我們可以推論出：
>:heavy_check_mark: hash collision的機率 = bucket串接元素的平均數量

這個式子乍看下非常直觀，但我們認為其有價值的地方在於HashMap是會不斷進行size的變動的(依據`load factor`的不同，resize的頻率也不同)，且其bucket中元素的分布也會不停分散變動，在這樣動態的情境下，元素平均數量還能趨近於穩定的分布，甚至，不受`load factor`所影響(可見下圖不同`load factor`的實驗)！我們認為相當有趣。

![](https://i.imgur.com/ivxwteq.png)


### 	:mag_right: Load Factor & Probability of Hash Collision $\lambda$

:bulb: 在上一節我們看到bucket中元素數量的分布成Poisson Distribution，且元素數量的平均值可以做為Poisson Distribution中的$\lambda$ (其peak所在的x值)，可視為hash collision的機率。然而，我們卻還沒解答這個$\lambda$與`load factor`的關係，在這一章節我們將來討論這個問題。

前面我們已經討論過，`load factor`應與$\lambda$ (你可以視為碰撞機率，或bucket內平均元素數量)為正相關。從上圖也能看出來，隨著`load factor`越來越大，$\lambda$(Poisson Distribution的peak所在x值)也越大，但尚未看出明顯的關係，於是我們建立多個HashMap，每次都插入10,000個英文單字，每次都記錄其`load factor`與$\lambda$，將之繪在同張圖上，可得$\lambda$與`load factor`關係圖：

![](https://i.imgur.com/ImcqfHE.png)

我們可以從圖中直接觀察出來，$\lambda$與`load factor` 同時擁有線性和步階的關係。我們知道`load factor`越大，越不容易resize。此結果相當合理，在`load factor`跨越一個階段後，HashMap沒有發生resize，故累積了相較之下兩倍的元素在bucket裡面，元素平均數量兩倍，$\lambda$也因此兩倍。

:heavy_check_mark: 到此總算解決了我們一開始問的問題：
>能不能從`load factor`就大概知道bucket內元素長度為何，我們就能知道該將`TREEIFY_THRESHOLD`設為多少。
>
儘管我們沒有得到明確的equation。但我們可以用上圖做為查表工具，查出對應load factor的元素平均長度，著實夠用了。因此，在之後的實驗中，我們會加入TREEIFY_THRESHOLD的變因進去，情況會變得更複雜，而為了不要讓HashMap裡全是Linked List或全是RB Tree，我們會先參考對應HashMap的$\lambda$為多少，再將`TREEIFY_THRESHOLD`設為附近範圍的值，以便我們做「HashMap裡同時有Linked List以及RB Tree」情況的分析。


### 	:mag_right: Time to Construct HashMap
#### (1) Load Fator

`load factor` 是影響 Construct HashMap 一個重要變數之一，因為當 HashMap 內元素數量大於 table_size* `load factor`時 HashMap 會進行resize(table_size變為原本的2倍)，因此可以知道當 `load factor` 越小時 resize 的頻率會上升，因此 index collision 的機率會下降， HashMap 每個 bucket 內所串聯的元素數量會相少，因此整個 HashMap 的結構會由較多的 Linked list 所組成。

相反的，當 `load factor` 越大時 resize 的頻率會下降，因此 index collision 的機率會上升， HashMap 每個 bucket 內所串聯的元素數量會相對較多，整個 HashMap 的結構可能會由較多的 RB Tree 所組成。

:bulb:`Note: TREEIFY_THRESHOLD會影響一個bucket裡面元素是為Linked List或RB Tree的機率，所以在這個實驗中我們把它設為定值，如此便可以有「當串聯元素越多，越有可能有RB Tree」的結論，以利我們做接下來的分析。關於TREEIFY_THRESHOLD更詳細的分析可見下節。`

而由時間複雜度來看的話:

1. link list insertion in HashMap is O(1)
2. RB Tree insertion in HashMap is O(logN)

因此理論上而言，若在 `TREEIFY_THRESHOLD` 固定的情況下，當`load factor` 越小時，table裡有較多Linked List，因為插入時間為O(1)，Construct HashMap 的時間應該較短; 相反的，當`load factor` 越大時，table裡有較多RB Tree，因為插入時間需要O(logN)，Construct HashMap 的時間應該較長。

為了驗證這件事，我們將`TREEIFY_THRESHOLD`設為定值(=4)，在一定的`load factor`下建立100個HashMap，分別插入100, 200, 300,..., 10000個點，每次都記錄建立HashMap的時間。接著切換不同`load factor`= 0.75、1.5、3、6 做一樣的實驗，最後將Construct HashMap 所需時間相對於內部元素數量的關係繪製成圖:

![](https://i.imgur.com/Lj8e23X.png)

由上圖可以發現確實當要創建一個越大的 HashMap ，`load factor`越大所需要的時間越多，也因此證明了上面所述的猜測。

然而，在這樣的配置下，我們想確認不同的`load factor`、`node num`，會構建出怎樣的table建構，換句話說，有多少bucket是Linked List，多少是Reb Black Tree？於是我們繪出與上圖很類似的圖(`TREEIFY_THRESHOLD`同為4)，只有縱軸從時間改成「RBTree與Linked List出現的數量比例」，越大代表紅黑樹的比例越多：

![](https://i.imgur.com/phsLjzm.png)

這張圖相當有趣，首先，在任何x(InsertNodeNum)都有「`load factor`越大，紅黑樹越多」，符合我們上述的猜測，且成長曲縣是凹向上，這個部分相當有趣但我們還沒深究其原因。另外我們可以看到單一`load factor`都會有不連續的斷點。這些斷點合理推論是出現在HashMap Resize的時候。有趣的是，在這裡不同顏色的曲線會接上彼此的斷點，合理推論原因是因為這裡的`load factor`皆是2倍成長(0.75, 1.5, 3, 6)，故才會有這樣剛好有趣的現象。
#### (2) Treeify Threshold
`TREEIFY_THRESHOLD`也是影響 Construct HashMap 一個重要變數之一，當 bucket 內的 linked List 長度大於 `TREEIFY_THRESHOLD`時，會進行 `Treeify()` 將 bucket 內元素由 Linked List 結構轉為 RB Tree 結構。

因此我們猜測，當`load factor`固定的情況下，可以分為下面兩種狀況:
1. `TREEIFY_THRESHOLD`越小，隨著插入的元素增加，bucket 內linked list 長度大於`TREEIFY_THRESHOLD`的機率會相對較高，因此HashMap 會較為頻繁的進行`Treeify()`，而每次`Treeify()`所需的時間為 O(NlogN)，並且變為 RB Tree 結構後，插入新元素時的時間 O(logN)，會比原本的 Linked List 結構的 O(1) 還要來的大，因此 Construct HashMap 的時間應該較長。
2. `TREEIFY_THRESHOLD`越大，bucket 內linked list 長度大於`TREEIFY_THRESHOLD`的機率會相對較低，因此進行 `Treeify()`的頻率會較低，除此之外插入新元素的時間為 O(1)，相較於 RB Tree 結構的 O(logN)來的小，也因此 Construct HashMap 的時間應該較短。

為了驗證這個猜測，我們將`load factor`設為定值(=1)，在一定的`TREEIFY_THRESHOLD`下建立100個HashMap，分別插入100, 200, 300,..., 10000個點，每次都記錄建立HashMap的時間。接著切換不同`TREEIFY_THRESHOLD`= 1, 2, 4, 8 做一樣的實驗，最後將Construct HashMap 所需時間相對於內部元素數量的關係繪製成圖:

![](https://i.imgur.com/SEsn1kF.png)

由上圖可以發現確實當要創建一個越大的 HashMap ，當`TREEIFY_THRESHOLD`越小所需要的時間越多，也因此證明了上面所述的猜測。

### :mag_right: Average Searching Time
HashMap 的 Searching Time 的效率與整個 HashMap 的結構有很大的關係，由上述簡介可以知道 HashMap 是由 Linked List 和 RB TREE 結構組成的，因此 HashMap 的結構可以大致分為三類:
1. bucket全為Linked List
2. bucket全為RB TREE
3. bucket有 Linked List 以及 RB TREE

若以時間複雜度來看:
1. Linked List Searching in HashMap is O(N)
2. RB TREE Searching in HashMap is O(logN)
3. (Linked List + RB TREE) in HashMap Time is O(N)

由上面的時間複雜度來看，我們可以推知當table全為 RB TREE 時，HashMap的 Searching Time 的效率應該為最高的，而 Linked List 和 (Linked List + RB TREE) 效率應該是差不多的，但可能 (Linked List + RB TREE)會稍微好一點點。

因此為了驗證我們的想法，我們希望藉由調整決定 HashMap 結構的參數: `load factor`和`TREEIFY_THRESHOLD` ，找出 Linked List、RB TREE、(Linked List + RB TREE)三種不同結構的 HashMap，並讓他們搜尋一樣的字典(10000個單字)來比較三者之間 Searching Time 效率的差別。

#### (1) 實驗一:
我一開始的做法是先給定一個`load factor`，接著我會選定 4 個不同`TREEIFY_THRESHOLD`來產生出 4 種不同的 HashMap 結構，分別搜尋100, 200, 300,..., 10000個單字，並將其平均的搜尋時間與搜尋字數做成圖。

我做了四次測試，`load factor`分別設置為: 1、10、100、300，而每次測試 4 個`TREEIFY_THRESHOLD`皆為: 1、2、4、8，最後我得到了下面四張結果圖:

![](https://i.imgur.com/f0wVrTB.jpg)


由`load factor`=1、10 可以發現，其實四種結構的 Average Searching Time 是差不多的，幾乎是互相重疊，而到`load factor`=100、300 可以發現四種結構隨著搜尋資料變多，Average Searching Time有上下震盪的情形產生，但趨勢依然相同。


因此我們將插入10000個單字時，`load factor` 相對於 HashMap 裡的平均元素長度: λ 作圖(如下圖)，發現我們設置的`load factor`=10、100、300 所對應的 λ值都大於我們所設置的`TREEIFY_THRESHOLD`(=1、2、4、8)，<br>

:bangbang:因此推知我們上面做的四次測試的HashMap 結構幾乎皆為 RB TREE	:bangbang:
也因此四種不同`TREEIFY_THRESHOLD`計算出的 Average Searching Time 幾乎是重疊的。

而 `load factor`=100、300 在搜尋越多單字時 Average Searching Time 有上下震盪的現象，若由時間複雜度來看，RB TREE Search in HashMap is O(logN)，若`load factor` 越大時，擴容頻率會降低，因此 index collision 的頻率就會變高，bucket 內的元素長度會變大，也就是 N 會變大，Searching 所花費的時間會增加。因此當隨著搜尋單字量越大，Average Searching Time 也會隨著增加。

但當 HashMap 內的元素數量大於 `load factor`*table_size，會進行擴容， table_size 會變為原先的 2 倍，並將所有元素重新hash進 HashMap內，因此原先的 RB TREE 結構會被改變，且理想狀況下 lamda會縮小，所以 Average Searching Time 下降，最終往復發生產生上下震盪的情況。
![](https://i.imgur.com/E895g1J.jpg)


#### (2) 實驗二:
鑒於上次 HashMap 的結構未有明顯的差異，這次我依照 λ 與 `load factor` 圖來挑選我的`load factor`與`TREEIFY_THRESHOLD`:
選擇 `load factor` 後，參照它所對應的 λ值、以及該 λ值上下各取一個值，共三個值作為我的`TREEIFY_THRESHOLD`。

![](https://i.imgur.com/yGmNXcf.png)

在我們的猜測中，三個`TREEIFY_THRESHOLD`值分別會對應以下結構:
1. `TREEIFY_THRESHOLD` = λ: 因為`TREEIFY_THRESHOLD`剛好在 λ 附近，因此他高機率會是 (Linked List + RB TREE) 的結構。
2. `TREEIFY_THRESHOLD` > λ: 因為`TREEIFY_THRESHOLD`大於 λ 附近，因此該 HashMap Treeify的機率較低，因此此結構高機率會是全為 Linked List 的結構。
3. `TREEIFY_THRESHOLD` < λ: 因為`TREEIFY_THRESHOLD`小於 λ 附近，因此該 HashMap Treeify的機率較高，因此此結構高機率會是全為 RB TREE 的結構。

接著我們用上述方法做了三組測試: 

a. `load factor`=50, `TREEIFY_THRESHOLD`=20、40、80 (因由上圖看出`load factor`=50對應$\lambda$=40)

![](https://i.imgur.com/jBKDaVn.png)

b. `load factor`=100, `TREEIFY_THRESHOLD`=40、80、120 (因由上圖看出`load factor`=100對應$\lambda$=80)

![](https://i.imgur.com/cSgtdrG.png)

c. `load factor`=150, `TREEIFY_THRESHOLD`=80、160、240 (因由上圖看出`load factor`=150對應$\lambda$=160)

![](https://i.imgur.com/vKIG5Ec.png)

由上面三個結果可以清楚看出，當`TREEIFY_THRESHOLD` > λ 時，Average Searching Time 的效率明顯是比 `TREEIFY_THRESHOLD` = λ 和`TREEIFY_THRESHOLD` < λ 時還要來的好的。

並且可以發現當`TREEIFY_THRESHOLD` = λ 和`TREEIFY_THRESHOLD` < λ 時，它們的 Average Searching Time 也是相較靠近的，但`TREEIFY_THRESHOLD` = λ 的效率依然會比 `TREEIFY_THRESHOLD` < λ的情況下還要好一點。

因此這個測試符合我們的預期:
#### 資料結構:
1. `TREEIFY_THRESHOLD` = λ: (Linked List + RB TREE) 的結構。
2. `TREEIFY_THRESHOLD` > λ:  Linked List 的結構。
3. `TREEIFY_THRESHOLD` < λ:  RB TREE 的結構。

#### 時間複雜度:
1. `TREEIFY_THRESHOLD` = λ: O(N) + O(logN) = O(N)
2. `TREEIFY_THRESHOLD` > λ: O(N)
3. `TREEIFY_THRESHOLD` < λ: O(logN)














### 






## :bulb: Conclusion




## Contribution & 專題結論
:bulb: 在本次專題中，從題目的發想、資料結構實作、想各種不同情況的實驗、做數據分析、結果與理論分析等等都是由我們自己討論、腦力激盪出來的。對於其他網站的參考最多僅在HashMap原始碼解釋。對於此專題主要有下列2個結論：

1. :large_orange_diamond: 我們都認為這是不錯且重要的題目，幾乎沒有人做這樣的研究(也許真的是太枯燥了)，大部分研究java HashMap都只是在做原始碼解釋，沒有像我們對其參數設定做深入的理論研究、繪圖等等。儘管我們不是做有趣的生活化的主題，但在某種層面上我想我們應該還算「有創意」，況且還算做出有點結果，應該能算對開源有些貢獻。

    我們有看到不少人對java HashMap的這部分帶有疑問，尤其是Poisson Distribution的部分，難過的是，看到他們在網路上發文，卻沒有人幫他們解惑。經過這次專題研究，我們很希望能將這篇文章貼在解答下方，一定能讓他們滿意。

2. :large_orange_diamond: 我們一致認為這題目相當困難，其一是較少先人的相關參考資料。其二是其牽扯到的變因太多，要同時顧慮到這麼多種可能，又要將結果繪製在2D圖上，很看重我們的選擇參數去做實驗的能力。

Division of labour：

* B06502028 莊立楷
    > - HashMap implementation
    > - Hash Collision, $\lambda$, and `load factor` analysis.
    > - Report
* B06502018 傅子豪
    > - Red Black Tree implementation
    > - Time Analysis of HashMap in different `load factor`, `TREEIFY_THRESHOLD`, `input node numbers`
    > - Report 
    