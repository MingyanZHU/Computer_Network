<br/>
<br/>
<center> 
<img src="https://raw.githubusercontent.com/1160300314/Figure-for-Markdown/master/hit/hit_logo.png">
</center>
<br/>
<br/>
<center> <font size = 7> 
计算机网络 <br/>
课程实验报告 </font></center>
<br/>
<br/>
<br/>
<center>
<table width="800px" height="600px" border="1px">
      <tr>
      <td rowspan="1" colspan="1">实验名称</td>
      <td rowspan="1" colspan="7">HTTP代理服务器的设计与实现</td>
      </tr>
      <tr>
      <td rowspan="1" colspan="1">姓名</td>
      <td rowspan="1" colspan="3">朱明彦</td> 
      <td rowspan="1" colspan="1">院系</td>
      <td rowspan="1" colspan="3">计算机科学与技术学院</td>
      </tr>
      <tr>
      <td rowspan="1" colspan="1">班级</td>
      <td rowspan="1" colspan="3">1603109</td>
      <td rowspan="1" colspan="1">学号</td>
      <td rowspan="1" colspan="3">1160300314</td>
      </tr>
      <tr>
      <td rowspan="1" colspan="1">任课教师</td>
      <td rowspan="1" colspan="3">李全龙</td>
      <td rowspan="1" colspan="1">指导教师</td>
      <td rowspan="1" colspan="3">李全龙</td>
      </tr>
      <tr>
      <td rowspan="1" colspan="1">实验地点</td>
      <td rowspan="1" colspan="3">格物213</td>
      <td rowspan="1" colspan="1">实验时间</td>
      <td rowspan="1" colspan="3">2018年10月27日</td>
      </tr>
      <tr>
      <td rowspan="2"> 实验课表现</td> 
      <td colspan="2" rowspan="1">出勤、表现得分(10)</td>
      <td colspan="1" rowspan="1">  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
      <td colspan="1" rowspan="2">实验报告得分(40)</td>
      <td colspan="1" rowspan="2">  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
      <td colspan="1" rowspan="2">实验总分</td>
      <td colspan="1" rowspan="2">  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
      </tr>
      <tr>
      <td colspan="2" rowspan="1">操作结果得分(50)</td>
      <td colspan="1" rowspan="1"> &nbsp; &nbsp;</td>
      </tr>
      <tr>
      <td colspan="8" rowspan="1"> <center>教师评语</center></td>
      </tr>
      <tr>
      <td colspan="8" rowspan="16"> </td>
      </tr>
      </table>
</center>
<br/><br/>
<br/>
<br/>
<br/>
<center><img src="https://raw.githubusercontent.com/1160300314/Figure-for-Markdown/master/hit/HIT_CS_logo.png"></center>

<div STYLE="page-break-after: always;"></div>
<!-- 此处用于换行 -->

# 实验目的
熟悉并掌握Socket网络变成的过程与技术；深入理解HTTP协议，掌握HTTP代理服务器的基本工作原理；掌握HTTP代理服务器设计用于变成实现的基本技能。
# 实验内容
- 设计并实验一个基本HTTP代理服务器。要求在制定端口(例如8080)接收来自客户的HTTP请求并且根据其中的URL地址访问该地址所指向的HTTP服务器(原服务器)，接收HTTP服务器的相应报文，并将相应报文转发给对应的客户进行浏览。
- 设计并实现一个支持Cache功能的HTTP代理服务器。要求能缓存原服务器相应的对象，并能够通过修改请求报文(添加`if-modified-since`头部行)，向原服务器确认缓存对象是否是最新版本。
- 扩展HTTP代理服务器，支持网站过滤，允许/不允许访问某些网站。
- 扩展HTTP代理服务器，支持用户过滤，支持/不支持某些用户访问外部网站。
- 扩展HTTP代理服务器，支持网站引导，将用户对某个网站的访问引导至一个模拟网站(钓鱼)。
# 实验过程
<!-- 以文字描述、实验结果截图等形式阐述实验过程，必要时可附相应代码截图或以附件形式提交 -->
## Socket编程的客户端和服务器端的主要步骤

## HTTP代理服务的基本原理
本次实验中实现的HTTP代理服务器，主要是通过转发源主机的HTTP请求报文至目的服务器，并且将接收到的HTTP相应报文，再次转发到源主机上实现的。
## HTTP代理服务器的程序流程图
<!-- TODO LaTeX实现？ -->
## 实现HTTP代理服务器的关键技术及解决方案
### 1.解析HTTP请求报文
解析HTTP的请求报文主要是解析HTTP的头部行，在这里我们使用`\r\n`对整个请求报文进行划分，得到的就是每一个头部行的信息。
```python
headers = message.split('\r\n') # 其中message为proxy接收到的全部请求报文
```
其中最为重要的就是头部行的第一行，即**Request Line**，标注着method、URL和协议的版本号，并使用1个空格进行划分，如下：
```html
GET http://jwts.hit.edu.cn/resources/css/common/ydy.css HTTP/1.1
```
可以通过解析Request Line获得目的服务器的URL。
### 2.实现请求报文和响应报文的转发
在proxy的实现中主要涉及了3种socket，分别为：
1. 代理服务器用于处理TCP请求的socket，在本次实验中，将这个socket的端口绑定在12138端口；
2. 用于直接与源主机连接的socket，用于接受来自源主机的HTTP请求报文和从proxy将HTTP的响应报文转发至源主机，对于源主机的TCP请求，在一个线程中开启1个此种socket用于处理；
3. 其三为proxy代源主机与目的主机进行连接的socket，主要负责将源主机的HTTP请求转发发送至其目的主机，并获取从目的主机返回的HTTP响应报文。
# 实验结果
采用演示截图、文字说明等方式，给出本次实验的实验结果
# 问题讨论
对实验过程中的思考问题进行讨论或回答
# 心得体会
结合实验过程和结果给出实验的体会和收获
