
$(document).ready(function() { 
  $(".select1 li").click(function() { 
  $(this).addClass("selected").siblings().removeClass("selected"); 
    if ($(this).hasClass("select-all")) { 
      $("#selectA").remove(); 
    } else { 
      var copyThisA = $(this).clone(); 
      if ($("#selectA").length > 0) { 
        $("#selectA a").html($(this).text()); 
      } else { 
        $(".alert-sm b").append(copyThisA.attr("id", "selectA")); 
      } 
    } 
  });
  $(".select2 li").click(function() { 
  $(this).addClass("selected").siblings().removeClass("selected"); 
    if ($(this).hasClass("select-all")) { 
      $("#selectB").remove(); 
    } else { 
      var copyThisB = $(this).clone(); 
      if ($("#selectB").length > 0) { 
        $("#selectB a").html($(this).text()); 
      } else { 
        $(".alert-sm b").append(copyThisB.attr("id", "selectB")); 
      } 
    } 
  });
    $(".select3 li").click(function() { 
  $(this).addClass("selected").siblings().removeClass("selected"); 
    if ($(this).hasClass("select-all")) { 
      $("#selectC").remove(); 
    } else { 
      var copyThisC = $(this).clone(); 
      if ($("#selectC").length > 0) { 
        $("#selectC a").html($(this).text()); 
      } else { 
        $(".alert-sm b").append(copyThisC.attr("id", "selectC")); 
      } 
    } 
  });
  $("#selectA").on("click", 
  function() { 
    $(this).remove(); 
    $("#select1 .select-all").addClass("selected").siblings().removeClass("selected"); 
  }); 
  $("#selectB").on("click", 
  function() { 
    $(this).remove(); 
    $("#select2  .select-all ").addClass("selected").siblings().removeClass("selected"); 
  }); 
    $("#selectC").on("click", 
  function() { 
    $(this).remove(); 
    $("#select3 .select-all").addClass("selected").siblings().removeClass("selected"); 
  }); 

$(".item-filter li").on("click", 
    function () { 
        if ($(".alert-sm b").length > 1) { 
            $(".alert-sm b").hide(); 
        } else { 
            $(".alert-sm b").show(); 
        } 
    }); 
/* $(".list-body a").click(function() { 
    var a = $(this).html()
    $.getJSON('showproduct', {'a':a}, function(ret){
          $('#product-list').html(''); 
            $.each(ret, function(homepage,item){
            $('#product-list').append('<li><a href=""><img class="center-block"src="/static/images/'+item+'"></a><div class="summary"><a href="">'+item+'</a></div><div class="price"><b>1000</b></div><div class="list-show-eva"><i class="icon-main icon-eva-6"></i><a href="">北京有货</a></div><button type="button" class="btn btn-default btn-xs">加入购物车</button></li>')

         })
        });
  })*/
 });
