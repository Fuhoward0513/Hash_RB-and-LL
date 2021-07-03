可能要做的事情：
- [ ] Experiments
- [ ] Discussion
- [ ] Conclusion
- [ ] 包好repo，寫使用說明
- [ ] Demo影片




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

## :hammer: HashMap Implementation

原則上我們仿照jdk1.8版本的HashMap的邏輯重建python版的HashMap，將之簡化後可以參考以下這個流程圖：([圖片來源](https://blog.csdn.net/u011240877/article/details/53358305#hashmap-%E5%9C%A8-jdk-18-%E4%B8%AD%E6%96%B0%E5%A2%9E%E7%9A%84%E6%93%8D%E4%BD%9C-%E6%A0%91%E5%BD%A2%E7%BB%93%E6%9E%84%E4%BF%AE%E5%89%AA-split ))
![](https://i.imgur.com/FB0iMd0.png)
然而在我們實作的HashMap中，還是有幾點與官方不同:
1. 我們並未設置`UNTREEIFY_THRESHOLD`，也就是說，在table進行resize的時候，若bin中是RB Tree，我們直接將Tree中的所有節點pop出來，重新對它們進行hash分配。反之，官方則是有特殊的`split()`來處理resize時RB Tree的修剪。
2. 我們並未在節點儲存`hash`屬性，所以在table resize的時候，我們使用每個節點的`key`屬性重新計算hash value。反之，官方則有這個屬性，方便其rehash時不用重新計算hash value，只要將其分配原地或2倍長度後的bin的位置即可(因為resize是將table直接double size，故節點要嘛是在同位置，要嘛是兩倍index後的位置)。
3. 我們額外建立一個Red Black Tree的class建立實體放在table的bin裡。官方則只是在HashMap程式碼中嵌入TreeNode和並實作RB Tree的主要運算函式。


## :bar_chart: Experiments
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
    