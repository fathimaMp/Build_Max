$(document).ready(function() {
  function fetchworkers(work) {
        $.ajax({
            type: "GET",
            url: "/get_workers/",
            data: { 'work': work },
            dataType: "json",
            success: function (data) {
                $("#worker").empty();
                console.log(data)
                for (var i = 0; i < data.length; i++) {
                    $("#worker").append("<option value='" + data[i].workerId__workerId + "'>" + data[i].workerId__First_Name + " " + data[i].workerId__Last_Name + "</option>");
                    $("#wages").val(data[i].Wage)
                }
            },
            error: function (xhr, status, error) {
                console.log("yyyyy");
            }
        });
    }

    $("#id_workId").on("change", function() {
        var selectedWork = $(this).val();
        fetchworkers(selectedWork);
    });

    // Initialize the worker dropdown based on the default work selection
    fetchworkers($("#id_workId").val());
});

