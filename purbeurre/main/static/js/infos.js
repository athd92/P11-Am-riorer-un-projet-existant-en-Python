$("#mail").click(function () {
  let entry = {
    aliment_id: $("#aliment_id").text(),
  };
  console.log("ENTRY : " + entry.aliment_id);
  $.ajax({
    type: "POST",
    url: `${window.origin}/send_infos/`,
    data: {
      aliment_id: entry.aliment_id,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    beforeSend: function () {
      console.log("before");
      $("#mail").hide();
      $("#sending").show();
    },
    complete: function () {
      console.log("after");
      $("#sending").hide();
    },

    success: function (data, textStatus) {
      console.log("SUCCESS AJAX");
      $("#sent").show();
      $("#sent").click(false);
    },
    error: function (e) {
      $("#sent").hide();
      console.log("Ajax request failed: " + e);
      $("#error").show();
    },
  });
});
