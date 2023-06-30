$(function () {
    $("#id_avatar, #id_background_color").on("change", function () {
        $("#appearance-form").submit();
    });

    $(".select-default-avatar").on("click", function () {

        var imageName = $(this).data("avatar-name");
        console.log(imageName)
        $("#id_avatar_choice").val(imageName);
        $("#appearance-form").submit();
    });

    $(".random-default-avatar").on("click", function () {
        $("#id_avatar_draw").prop("checked", true);
        $("#appearance-form").submit();
    });
});


$(".klasa").each(function(){
  $(this).modalForm({
    formURL: $(this).data('form-url'), isDeleteForm: true
  });
});
