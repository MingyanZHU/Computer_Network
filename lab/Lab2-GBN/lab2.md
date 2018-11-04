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
      <td rowspan="1" colspan="7">GBN协议的设计与实现</td>
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
      <td rowspan="1" colspan="3">2018年11月3日</td>
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

# 见doc格式报告 
# 实验目的
理解滑动窗口协议的基本原理；掌握GBN的工作原理；掌握基于UDP设计并实现一个GBN协议的过程与技术。
# 实验内容
- 基于UDP设计一个简单的GBN协议，实现单项可靠数据传输(服务器到客户的数据传输)
- 模拟引入数据包的丢失，验证所设计协议的有效性
- 改进所设计的GBN协议，支持双向数据传输
- 将所设计的GBN协议改进为SR协议
# 实验过程
### 1. GBN协议数据分组格式
在本次实验中使用的GBN数据分组格式为 
### 2. GBN确认分组格式

### 3. 协议两端程序流程图

### 4. 数据分组丢失验证模拟方法
在实验中模拟数据包丢失的方法，采取实验报告中的建议，对于接收端，接收到的数据帧，以一定的概率发送ACK报文(在实验中使用的概率为50%)，剩余的情况接收端不发送ACK即表现为ACK报文丢失。
### 5. 程序中实现的主要类(或函数)及其主要作用
在实验中主要类有4种，分为GBN协议的客户端、服务器端和SR协议的客户端、服务器端。其中由于GBN协议和SR协议都实现了全双工通信，所以客户端和服务器端都可以互相向对方发送数据，两边的实现是对称的，所以以`GBNClient`和`SRClient`为例进行说明。
`GBNClient`为GBN协议中的客户端实现，其中有`__send()`函数作为发送方时的主要功能，即从可用窗口中发送数据，以及接收并处理来自接收方发回的ACK报文。
`__receive()`函数主要的功能是作为接收方时，接收数据包，并以一定的概率回复ACK报文，在收到冗余ACK报文的时候丢弃回复带有`next_expected_num`的ACK报文。
# 实验结果
采用演示截图、文字说明等方式，给出本次实验的实验结果
# 问题讨论
对实验过程中的思考问题进行讨论或回答
# 心得体会
结合实验过程和结果给出实验的体会和收获
