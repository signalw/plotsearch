$(document).ready(function() {
  
  var curr_page = parseInt($("#page").text());

  if (curr_page <= 1) {
    $("#prev").prop('disabled', true);
  }

  if (curr_page > ($('#total').text()-1)/10) {
    $("#next").prop('disabled', true);
  }

  $("#prev").click(function(){
    $("#results-form").attr("action", "/results/p."+(curr_page-1));
    $("#results-form").submit();
  });

  $("#next").click(function(){
    $("#results-form").attr("action", "/results/p."+(curr_page+1));
    $("#results-form").submit();
  });

});
