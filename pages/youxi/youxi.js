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
    function Users(id,passwords,name,score,time){
      this.id=id;
      this.passwords=passwords;
      this.name=name;
      this.score=score;
      this.time=time;
    }
    //用户信息存储
  var a1=new Users(1,123,"zhangsan",0,0)//01等八进制文字禁止使用
  var a2=new Users(2,123,"lisi",0,0)
  var a3=new Users(3,123,"wangwu",0,0)
  var a4=new Users(4,123,"zhaoliu",0,0)
  var a5=new Users(5,123,"hanqi",0,0)
  //绑定用户信息数据
  var arr=[a1,a2,a3,a4,a5]
  this.setData({
     array1:arr
  })
  //console.log(arr)
  },
  huoqu(){
  var u1={id:3,
    passwords:123,
    name:"wangwu",
    score:25,
    time:3}//对象初始化时，用:
    var array2=this.data.array1;//给array赋值
    //进行积分更新
  for(let i=0;i<array2.length;i++){
    if(array2[i].id==u1.id&&array2[i].passwords==u1.passwords){
      array2[i].time=u1.time;
      if(array2[i].score<u1.score){
        array2[i].score=u1.score
      }
    }
  }
  console.log(array2)
   //冒泡排序开始 ,将不同用户积分排序
   for(let i=0;i<array2.length-1;i++){
    for(let j=0;j<array2.length-1;j++){
    if(array2[j].score<array2[j+1].score){ 
      let temp=array2[j]//进行必要的时间更新
      array2[j]=array2[j+1]
      array2[j+1]=temp}
    }
   }
   //
   this.setData({
     array1:array2
   })
  },
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