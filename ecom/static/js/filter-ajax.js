 $(document).ready(function() { 
 $(".selected-1 a").click(function() { 
    var a = $(this).text()+'1'
    $.getJSON('showproduct', {'a':a}, function(ret){
          $('#product-list').html(''); 
            $.each(ret, function(homepage,item){
            $('#product-list').append('<li><a href=""><img class="center-block"src="/res/'+item['img']+'"></a><div class="summary"><a href="">'+item['name']+'</a></div><div class="price"><b>售价:'+item['price']+'</b></div><div class="list-show-eva"><i class="icon-main icon-eva-6"></i><a href="">北京有货</a></div><button type="button" class="btn btn-default btn-xs">加入购物车</button></li>')

         })
        });
  })
 $(".selected-2 a").click(function() { 
    var a = $(this).text()+'2'
    $.getJSON('showproduct', {'a':a}, function(ret){
          $('#product-list').html(''); 
            $.each(ret, function(homepage,item){
            $('#product-list').append('<li><a href=""><img class="center-block"src="/res/'+item['img']+'"></a><div class="summary"><a href="">'+item['name']+'</a></div><div class="price"><b>售价:'+item['price']+'</b></div><div class="list-show-eva"><i class="icon-main icon-eva-6"></i><a href="">北京有货</a></div><button type="button" class="btn btn-default btn-xs">加入购物车</button></li>')


         })
        });
  })
  $(".selected-3 a").click(function() { 
    var a = $(this).text()+'3'
    $.getJSON('showproduct', {'a':a}, function(ret){
          $('#product-list').html(''); 
            $.each(ret, function(homepage,item){
            $('#product-list').append('<li><a href=""><img class="center-block"src="/res/'+item['img']+'"></a><div class="summary"><a href="">'+item['name']+'</a></div><div class="price"><b>售价:'+item['price']+'</b></div><div class="list-show-eva"><i class="icon-main icon-eva-6"></i><a href="">北京有货</a></div><button type="button" class="btn btn-default btn-xs">加入购物车</button></li>')


         })
        });
  })

 $(".list-body a").click(function() { 
    var a = $(this).text()
    $.getJSON('showproduct', {'a':a}, function(ret){
          $('#product-list').html(''); 
            $.each(ret, function(homepage,item){
            $('#product-list').append('<li><a href=""><img class="center-block"src="/res/'+item['img']+'"></a><div class="summary"><a href="">'+item['name']+'</a></div><div class="price"><b>售价:'+item['price']+'</b></div><div class="list-show-eva"><i class="icon-main icon-eva-6"></i><a href="">北京有货</a></div><button type="button" class="btn btn-default btn-xs">加入购物车</button></li>')
              

         })
        });
  })
  });

