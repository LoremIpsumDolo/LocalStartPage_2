$(document).ready(function () {

  var _total_news = $(".outer_news_wrapper").find(".news_wrapper").length;

  $('.legend_btn').click(function () {
    console.log(_total_news);
    //
    let current_value = parseInt($(this).attr("value"));
    let current_id = '#news_index_' + current_value;
    let next_id = "";
    let next_value = "";
    //
    if ( current_value === _total_news ) {
      console.log("last element");
      next_value = 1;
    } else {
      next_value = current_value + 1;
    }
    //
    next_id = '#news_index_' + next_value;
    let next_title = $(next_id).attr("title");
    //
    console.log(current_id, next_id, next_title);
    //
    $(this).attr("value", next_value);
    $(this).text(next_title + " >>");
    //
    $(current_id).toggleClass("no_display");
    $(next_id).toggleClass("no_display");
  });
});