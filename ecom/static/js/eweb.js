
 $(document).ready(function(){
 /*     $('#hrand1').click(function(){
         $.ajax({
             type: "GET",
             url: "/eweb/showproduct",
             data: {username:$(".col-lg-6").text(), content:$(".hidden").text()},
             dataType: "json",
             success: function(result){
                         $('.pro-list-show li').empty();   //清空resText里面的所有内容
                        var html = ''; 
                        html+='hello'
                         $.each(data, function(commentIndex, comment){
                               html += '<div class="comment"><h6>' + comment['username']
                                         + ':</h6><p class="para"' + comment['content']
                                         + '</p></div>';
                         });
                         $('.pro-list-show li').html(html);
                      }
         });
    });*/
      $("#hrand1").click(function(){
        var a = $("#hrand1").text();
        $.get("/eweb/showproduct",{'a':a}, function(ret){
            $('.pro-list-show li').html(ret)
        })
      });
      $("#select1 .select-all").click(function(){
        var a = $("#select1 .select-all").text();
        $.get("/eweb/showproduct",{'a':a}, function(ret){
            $('.pro-list-show li').html(ret)
        })
      });

            $("#hrand2").click(function(){
        var a = $("#hrand2").text();
        $.get("/eweb/showproduct",{'a':a}, function(ret){
            $('.pro-list-show li').html(ret)
        })
      });
                  $("#hrand3").click(function(){
        var a = $("#hrand3").text();
        $.get("/eweb/showproduct",{'a':a}, function(ret){
            $('.pro-list-show li').html(ret)
        })
      });
    });
/*$(document).ready(function() { 
$(".select1 li").click(function(){
    alert("Text: " + $(".alert-sm").text());
  });
});*/

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
  $("#selectA").live("click", 
  function() { 
    $(this).remove(); 
    $("#select1 .select-all").addClass("selected").siblings().removeClass("selected"); 
  }); 
  $("#selectB").live("click", 
  function() { 
    $(this).remove(); 
    $("#select2  .select-all ").addClass("selected").siblings().removeClass("selected"); 
  }); 
    $("#selectC").live("click", 
  function() { 
    $(this).remove(); 
    $("#select3 .select-all").addClass("selected").siblings().removeClass("selected"); 
  }); 

$(".item-filter li").live("click", 
    function () { 
        if ($(".alert-sm b ").length > 1) { 
            $(".select-no").hide(); 
        } else { 
            $(".select-no").show(); 
        } 
    });  

 });



//库存联动页面



