

if (typeof jQuery === 'undefined') {
  throw new Error('Cart\'s JavaScript requires jQuery')
}

$(document).ready(
  GetCartItems()
)
var Item = {
  createNew: function(ItemID,ProductID,Name,Color,Size,Price,ImageUrl,DelivFee,Stock,Count,AddTime){
    var item = {};
    item._id = ItemID;
    item._productId = ProductID;
    item._name = Name;
    item._color = Color;
    item._size = Size;
    item._price = Price;
    item._image = ImageUrl;
    item._delivFee = DelivFee;
    item._stock = Stock;
    item._count = Count;
    item._addTime = AddTime;
    return item;

  }
}
/*
"_ItemID":,
"_ProductID":,
"_Name":,
"_Color":,
"_Size":,
"_Price":,
"_Image":,
"_DelivFee"
"_Stock":,
"_Count":,
"_AddTime":,
*/
function GetCartItems(){
  $.get(
    "/eweb/cart/",
    {commend:"GetCartItems"},
    function (cart, status){
      var count = cart.Count;
      if (count <= 0){
        $("#cart_empty").show();
      } else{
        $("#cart_has_content").show();
        var items = new Array();
        for (var i = 0; i < count; ++i){
          var item = Item.createNew(
            cart.Contents[i].ItemID,
            cart.Contents[i].ProductID,
            cart.Contents[i].Name,
            cart.Contents[i].Color,
            cart.Contents[i].Size,
            cart.Contents[i].Price,
            cart.Contents[i].Image,
            cart.Contents[i].DelivFee,
            cart.Contents[i].Stock,
            cart.Contents[i].Count,
            cart.Contents[i].AddTime);
          items.push(item);
        }
        DisplayCart(items);
      }

    },
    "json");
}

function AppendItem(item){
  str = '';
  str +='<tr class="cart_item" id="cart_item_'+item._id+'">';
//隐藏信息
  str +=  '<input type="hidden" class="ui-unit-id" value="'+item._id+'">';
  str +=  '<input type="hidden" class="ui-unit-price" value="'+item._price+'">';
  str +=  '<input type="hidden" class="ui-unit-stock" value="'+item._stock+'">';
//checkbox
  str +=  '<td width="5%" class="tr-list">';
  str +=    '<form>';
  str +=      '<div>';
  str +=        '<label><input class="checkbox" type="checkbox" /></label>';
  str +=      '</div>';
  str +=    '</form>';
  str +=  '</td>';
//image和描述
  str +=  '<td width="45%" class="tr-list">';
  str +=    '<a href="../good/'+ item._productId +'"><img class="pull-left" alt="'+item._name+'" src="'+item._image+'" /></a>';
  str +=    '<div class="summary blue-font"><a href="../good/'+ item._productId +'">'+ item._name+'</a></div>';
  str +=  '</td>';
//总额
  str +=  '<td width="21%" class="tr-list"><b class="orange-font">￥ <span class="item-price">'+ item._price*item._count +' </span></b></td>';
//数量
  str +=  '<td width="21%" class="tr-list">';
  str +=    '<span class="ui-spinner">';
  str +=      '<input autocomplete="off" class="ui-unit-count" maxlength="13" onkeyup="this.value=this.value.replace(/\D/gi,\'\')" onafterpaste="this.value=this.value.replace(/\D/g,\'\')" onchange="CountModified(\'cart_item_'+item._id+'\')" type="text" value="'+item._count+'" aria-valuenow="0" />';
  str +=      '<a class="ui-spinner-button ui-spinner-up" onclick="javascript:CountAdd(\''+item._id+'\')" tabindex="-1"><span class="ui-icon">▲</span></a>';
  str +=      '<a class="ui-spinner-button ui-spinner-down" onclick="javascript:CountMin(\''+item._id+'\')" tabindex="-1"><span class="ui-icon">▼</span></a>';
  str +=    '</span>';
  str +=  '</td>';
//删除操作
  str +=  '<td width="8%" class="tr-list bule-font"><a href="javascript:DeleteItem(\''+item._id+'\')" >删除</a></td>';

  str +='</tr>';
  $("#cart_list").append(str);
}

function CountAdd(id){
  $("#cart_item_"+id+" .ui-unit-count")[0].value++;
  CountModified(id);
}

function CountMin(id){
  $("#cart_item_"+id+" .ui-unit-count")[0].value--;
  CountModified(id);
}

function UpdateCartStore(itemid, count){
  $.post(
    "/eweb/cart/",
    {commend:"UpdateCartItem",
    ItemId:itemid,
    ItemCount:count},
    function (data, status){
      //alert(status);
    },
    "json");
}

function DeleteItem(id){
  UpdateCartStore(id, 0);
  $("#cart_item_"+id).remove();
  UpdateTotalPrice();
  alert("Delete");
}

function Settle(){
  var items = new Array();
  var count = 0;

  $(".cart_item").each(
    function (){
      var item = new Object();
      item.ID = $(this).find(".ui-unit-id")[0].value;
      item.COUNT = $(this).find(".ui-unit-count")[0].value;
      //items[count] = "["+item.ID+","+item.COUNT+"]";
      items[count] = item;
      ++count;
    }
  );

  $.post(
    "/eweb/cart/",
    {commend:"Settle",
    itemlist:JSON.stringify(items),
    Count:count},
    function (data)
    {
      if (data.Status == "Error")
      {
        alert(data.Reason);
        location.reload();
      }else if (data.Status == "Success"){
        location.href="/eweb/cartstep2/";
      }
    },
    "json");
  alert(JSON.stringify(items));
}


function CountModified(id){
  var count = parseInt($("#cart_item_"+id+" .ui-unit-count")[0].value);
  var max = parseInt($("#cart_item_"+id+" .ui-unit-stock")[0].value);
  var price = parseFloat($("#cart_item_"+id+" .ui-unit-price")[0].value);
  if (isNaN(count) || count < 1){
    count = 1;
  }
  if (count > max){
    count = max;
  }
  $("#cart_item_"+id+" .ui-unit-count")[0].value = count.toString();
  $("#cart_item_"+id+" .item-price").html(price*count);
  UpdateCartStore(id, count);
  UpdateTotalPrice();
}

function UpdateTotalPrice(){
  var total = 0;
  var HasItems = false;
  $("#cart_list .cart_item").each(
    function(){
      HasItems = true;
      total += parseFloat($(this).find(".item-price").text());
    }
  );
  if (HasItems){
    $(".total-price").html(" "+total+"元");
  }else{
    $("#cart_empty").show();
    $("#cart_has_content").hide();
  }
}

function DisplayCart(items){

  for (var i = 0; i < items.length; ++i){
    for (var j = i + 1; j < items.length; ++j){
      if (items[j]._addTime > items[i]._addTime){
        var tmp = items[i];
        items[i] = items[j];
        items[j] = tmp;
      }
    }
    AppendItem(items[i]);
  }
  UpdateTotalPrice();
}

