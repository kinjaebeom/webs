var express = require('express');
var router = express.Router();

router.get('/', function(req, res){//앞에 posts가 생략되어있음 즉 posts/이거임
    res.render('index', {title:'게시판', pageName:'posts/list.ejs'});
});

router.get('/insert', function(req, res){
    res.render('index', {title:'글쓰기', pageName:'posts/insert.ejs'});
});
router.get('/playground', function(req, res){//앞에 posts가 생략되어있음 즉 posts/이거임
    res.render('index', {title:'놀이터여', pageName:'posts/playground.ejs'});
});
router.get('/read', function(req, res, next){//앞에 posts가 생략되어있음 즉 posts/이거임
    const id = req.query.id;
    res.render('index', {title:'게시글정보', pageName:'posts/read.ejs',id});
});


module.exports = router;