if (typeof jQuery === 'undefined') {
  throw new Error('Cart\'s JavaScript requires jQuery')
}

$(document).ready(function (){
  ColorSelected($(".colorlist:first").attr("id"));
})

function ColorSelected(color_id){
  $("#"+color_id).addClass("selected").siblings("span").removeClass("selected");
  $(".sizelist").each(function (){
    $(this).removeClass("selected").addClass("disabled");
  });
  var title = $("#"+color_id).attr("title");
  var first = false;
  $(".inventorylist."+title).each(function (){
    var size = $(this).data("size");
    $(".sizelist"+"."+size).removeClass("disabled");
    if (!first){
      first = true;
      SizeSelected($(".sizelist"+"."+size).attr("id"));
    }
  });

}

function SizeSelected(size_id){
  /*
  if ($("#"+color_id).hasClass("selected")){
    $("#"+color_id).removeClass("selected");
  }else{

  }
  */
  $("#"+size_id).addClass("selected").siblings("span").removeClass("selected");
  var size = $("#"+size_id).attr("title");
  var color = $(".colorlist.selected").attr("title");
  $("."+color+"."+size).addClass("CurrentInvent").siblings("input").removeClass("CurrentInvent");
  var price = parseFloat($("."+color+"."+size).data("price"))
  $("#product_price").html(price);
  $("#market_price").html(parseInt(price/50 + 1) * 70);
  var stock = $("."+color+"."+size).data("stock");
  $("#product_inventory_1").html(stock);
  $("#product_inventory_2").html(stock);
  $("#deliv_fee").html($("."+color+"."+size).data("fee"))
  $("#spec-img").attr("src",$("."+color+"."+size).data("img"));
  CountModified();
}


function CountAdd(){
  $(".client_item_count")[0].value++;
  CountModified();
}

function CountMin(){
  $(".client_item_count")[0].value--;
  CountModified();
}


function CountModified(){
  var count = parseInt($(".client_item_count")[0].value);
  var max = parseInt($(".CurrentInvent").data("stock"));

  if (isNaN(count) || count < 1){
    count = 1;
  }
  if (count > max){
    count = max;
  }
  $(".client_item_count")[0].value = count.toString();
}

function AddToCart(){
  var item = new Object();
  itemid = $(".CurrentInvent").data("id");
  itemcount= parseInt($(".client_item_count")[0].value);
  $.post(
    "/eweb/cart/",
    {commend:"AddItem",
    id:itemid,
    count:itemcount},
    function (data, status){
      if (data.Status == "Error"){
        alert("添加失败");
      }else if (data.Status == "Success"){
        alert("添加成功");
      }
    },
    "json");
}


function Settle(){
  var items = new Array();
  var count = 0;
  var item = new Object();
  item.ID = $(".CurrentInvent").data("id");
  item.COUNT = parseInt($(".client_item_count")[0].value);
  items[count] = item;
  ++count;

  $.post(
    "/eweb/cart/",
    {commend:"Settle",
    itemlist:JSON.stringify(items),
    Count:count},
    function (data)
    {
      if (data.Status == "Error"){
        alert(data.Reason);
        location.reload();
      }else if (data.Status == "Success"){
        location.href="/eweb/cartstep2/";
      }
    },
    "json");
}
