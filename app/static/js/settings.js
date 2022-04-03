$(document).ready(function () {

  $(".setting_name_container").click(function () {
    $(this).parent().find(".setting_content_container").toggle("slow");
  });

  // EDIT
  $(".btn_edit").click(function () {
    toggle_vis($(this));

  });

  // SAVE
  $(".btn_save").click(function () {
    let setting_main_name = $(this).parent().parent().parent().find(".setting_name_container").text().trim();
    let type_wrapper = $(this).parent().parent().find(".setting_type_wrapper");
    var json_main = {};
    var json_data = {};

    $(type_wrapper).each(function () {

      let type_wrapper_name = $(this).find("legend").text().trim();
      let wrapper_content = $(this).find(".settings_content");

      json_data[type_wrapper_name] = loop_over_inputs(wrapper_content);

    });

    json_main[setting_main_name] = json_data;
    console.log(json_main);
    // if response is ok
    set_new_values($(this));
  });

  // CANCEL
  $(".btn_cancel").click(function () {
    let settings_content = $(this).parent().parent().find("input");
    $(settings_content).each(function () {
      $(this).val("");
    });
    toggle_vis($(this));
  });

});


function set_new_values(_this) {
  $(_this).parent().parent().parent().find(".setting_name_container").text().trim();
  let type_wrapper = $(_this).parent().parent().find(".setting_type_wrapper");

  $(type_wrapper).each(function () {

    let wrapper_content = $(this).find(".settings_content");

    $(wrapper_content).each(function () {

      let settings_input = $(this).find(".setting_value_input");
      let new_val

      if ( settings_input.val().length === 0 ) {
        new_val = settings_input.attr("placeholder")
      } else {
        new_val = settings_input.val();
      }
      $(this).find(".settings_content_value").text(new_val);
    });
  });
  toggle_vis(_this);
}


function toggle_vis(_this) {
  $(_this).parent().parent().find(".settings_content_value").toggle();
  $(_this).parent().parent().find(".setting_value_input").toggle();
  $(_this).parent().find(".setting_btn").toggle();
}


function loop_over_inputs(settings_content) {
  var response = {}

  $(settings_content).each(function () {
    let _key = $(this).find(".settings_content_key").text();
    let settings_input = $(this).find(".setting_value_input");
    let settings_value

    if ( settings_input.val().length === 0 ) {
      settings_value = settings_input.attr("placeholder")
    } else {
      settings_value = settings_input.val();
    }

    response[_key] = settings_value
  });

  return response;
}