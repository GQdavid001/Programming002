
var express = require("express");
var querystring = require('querystring');
var mysql = require('mysql');
// post需要
var bodyParser = require("body-parser");

var app = express();

// post需要
app.use(bodyParser.urlencoded({ extended: true }));

// 跨域
app.all('*', function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
  res.header("X-Powered-By", ' 3.2.1');
  res.header("Content-Type", "application/json;charset=utf-8");
  next();
});

// 配置数据库信息
var connection = mysql.createConnection({
  host: 'localhost',
  port: '3306',
  user: 'root',
  password: '123456',
  database: 'daoru'
});

// 连接
connection.connect();

// 获取类型列表
//玩家获取
app.get("/onLoad", function (req, res) {
  var sql = 'select * from players';
  connection.query(sql , function (err, data) {
    if (err) {
      console.log(err);
    } else {
      var result = {
        "status": "200",
        "message": "success",
      }
      result.data = data;
      res.end(JSON.stringify(result));
    }
  });
});
//时间信息获取
app.get("/onPullDownRefresh", function (req, res) {
  var sql = 'select ID_score,score, playtime from scores	,playtime where ID_score=playtime_ID';
  connection.query(sql , function (err, data) {
    if (err) {
      console.log(err);
    } else {
      var result = {
        "status": "200",
        "message": "success",
      }
      result.data = data;
      res.end(JSON.stringify(result));
    }
  });
});
// 添加类型
app.post("/addType", function (req, res) {
  var params = [req.body.name];
  var sql = "INSERT INTO players(Id,name) VALUES(0,?)";
  connection.query(sql, params, function (err, data) {
    if (err) {
      res.end('error')
    } else {
      var result = {
        "status": "200",
        "message": 'success',
      }
      res.end(JSON.stringify(result))
    }
  });
});

app.listen(3000);
console.log('3000 running');
