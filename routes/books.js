var express = require('express');
var router = express.Router();

/* GET 도서검색 page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: '도서검색', pageName: 'books/search.ejs' }); //랜더링 하겠다는 뜻. index니깐 ejs파일을 불러옴
});

module.exports = router;