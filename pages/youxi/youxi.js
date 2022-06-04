Page({
data:{
  array1:[],
  id:0,//赋初始值必须的
  mima:0,
  showModal:false,//弹窗显示
  time:0,
  chaoshi:false//用于判断是否超时
},
onLoad(){
  //个人信息的存储
  //建立用户类
  function Users(id,passwords,score,time){
    this.id=id;
    this.passwords=passwords;
    this.score=score;
    this.time=time;
  }
  //用户信息存储
  //玩家信息的导入
  let that=this;
  var array=[];//数组用于存储申请的值作为中间量
  wx.request({
    url: 'http://localhost:3000/onLoad',
    method: 'GET',
    data: {},
    header: {
      'content-type': 'application/x-www-form-urlencoded'
    },
    success(res) {
      console.log(res.data.data)
      //完成对于用户名密码的录入
      for(let i=0;i<res.data.data.length;i++){
        array[i]=new Users(res.data.data[i].ID,res.data.data[i].code,0,0)//01等八进制文字禁止使用
    };
    //绑定信息到data中
    that.setData({
      array1:array
    })
    console.log("绑定好的array1",array);
  }
  });
},

huoQu() {
  var array2=this.data.array1;//给array赋值
  //信息的请求和导入
  let that = this;
//玩耍时间、积分的导入
  wx.request({
    url: 'http://localhost:3000/huoQu',
    method: 'GET',
    data: {},
    header: {
      'content-type': 'application/x-www-form-urlencoded'
    },
    success(res) {
      console.log(res.data.data);
      //嵌套循环用于更新游戏积分还有时间
      for(let i=0;i<array2.length;i++){
        for(let j=0;j<res.data.data.length;j++){
          if(array2[i].id==res.data.data[j].playtime_ID){
          array2[i].time=res.data.data[j].playtime;
          if(array2[i].score<res.data.data[j].score){
            array2[i].score=res.data.data[j].score
            }
          }
        }
      };
    }
  });

 //冒泡排序开始 ,将不同用户积分排序
 for(let a=0;a<array2.length-1;a++){
  for(let b=0;b<array2.length-1-a;b++){
     if(array2[b].score<array2[b+1].score){ 
       let temp=array2[b];//进行必要的时间更新
       array2[b]=array2[b+1];
       array2[b+1]=temp;
       //console.log("temp",temp);
       //console.log("排序后array2",array2);
      }

  }
 }
 console.log("更新完得知",array2)
 //数据绑定
 this.setData({
   array1:array2
 })

}
,
yonghuming(e){
this.setData({
  id:e.detail.value
})
console.log("e.detail.value",e.detail.value)
},
mima(e){
  this.setData({
    mima:e.detail.value
  })
  console.log("e.detail.value",e.detail.value)
  },
  //登录并进行时间显示提醒
denglu(){
var id=this.data.id
var mima=this.data.mima
var array2=this.data.array1
console.log("array2[0].time",array2[0].time)
var dl;
for(let i=0;i<array2.length;i++){
  if(array2[i].id==id&&array2[i].passwords==mima){
    dl=i;
    console.log(array2[dl].time);
   break;
  }
  else {dl=-1}
}
if(dl!=-1){
  this.setData({
    showModal: true,
    time:array2[dl].time
  })
  //判断是否超时
  if(dl!=-1&&array2[dl].time>=2){
    this.setData({
      chaoshi:true
    })
  }
  else{
      this.setData({
        chaoshi:false
      })}
   
var a=this.data.showModal//用于显示弹窗
console.log("a",a)
}

//console.log("dl",dl)
},
//关闭弹窗
hidepopup: function () {
  this.setData({
    showModal: false
  })}
})
