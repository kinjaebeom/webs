var express = require('express');
var router = express.Router();

/* GET 도서검색 page. */
router.get('/', function(req, res, next) { //기본주소로 / 이렇게만 적으면 이제 북 서치ejs로 가겠끔 설정. app.js에 app.use('/books', require('./routes/books')); 설정
  res.render('index', { title: '도서검색', pageName: 'books/search.ejs' }); //랜더링 하겠다는 뜻. index니깐 ejs파일을 불러옴
});
//장바구니 페이지 이동
router.get('/cart', function(req, res){
  res.render('index', {title:'장바구니', pageName:'books/cart.ejs'});
});
module.exports = router;

// var express = require('express');: 코드의 첫 줄에서는 Express 프레임워크를 가져옵니다. require 함수를 사용하여 Node.js 모듈 시스템에서 Express를 가져옵니다. 
// Express는 Node.js 웹 애플리케이션을 구축하기 위한 강력한 프레임워크로, HTTP 요청 및 응답 처리를 단순화하는 데 사용됩니다.

