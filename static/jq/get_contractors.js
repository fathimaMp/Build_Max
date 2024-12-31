$(document).ready(function() {
  function fetchcontractors(work) {
        $.ajax({
            type: "GET",
            url: "/get_contractors/",
            data: { 'work': work },
            dataType: "json",
            success: function (data) {
                $("#contractor").empty();
                console.log(data)
                for (var i = 0; i < data.length; i++) {
                    $("#contractor").append("<option value='" + data[i].ContractorId__ContractorId + "'>" + data[i].ContractorId__First_Name + " " + data[i].ContractorId__Last_Name + "</option>");
                    $("#Rate").val(data[i].Rate)
                }
            },
            error: function (xhr, status, error) {
                console.log("yyyyy");
            }
        });
    }

    $("#id_workId").on("change", function() {
        var selectedWork = $(this).val();
        fetchcontractors(selectedWork);
    });

    // Initialize the worker dropdown based on the default work selection
    fetchcontractors($("#id_workId").val());
});

