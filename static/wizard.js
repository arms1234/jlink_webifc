


function wizard(string)
{
	
	 var doc_height = $(document).height();
	 var doc_width  = $(document).width();
	 var step = 0;
	 var num_steps = 5;

	 $("body").append("<div class='wizard_overlay' id='wizard__owerlay'></div>");

	 $(".wizard_overlay").css("height", doc_height).css("width", doc_width).fadeIn(50);


	 $("body").append("<div class='wizard_outer'></div>");

	 $(".wizard_outer").append("<div class='wizard_inner'></div>");

	 $(".wizard_inner").append("<div class='wizard_content'></div>");

	 $(".wizard_inner").append("<hr noshade>");
	 $(".wizard_inner").append("<div class='wizard_buttons'></div>");

    $(".wizard_outer").css("left", ( $(window).width()  - $(".wizard_outer").width() ) / 2+$(window).scrollLeft() + "px");
    $(".wizard_outer").css("top",  ( $(window).height() - $(".wizard_outer").height() ) / 2 + "px");
        
    $(".wizard_outer").fadeIn(50);  
	 
	 $(".wizard_buttons").append("<button id='next_btn' value='Next'>Next</button>"); 	 
	 $(".wizard_buttons").append("<button id='prev_btn' value='Prev'>Prev</button>");

	 $("#prev_btn").hide(); 

	 $(".wizard_content").html(string);

	 $("#prev_btn").click(function()
    {
        if(step == 0)
	     {
		 $("#prev_btn").hide(); 
	     }
        else
	     {
		 step--;
		 $(".wizard_content").html(step);

	     }

	 });

	 $("#next_btn").click(function()
	 {
	     if(step < num_steps)
	     {
		 $("#prev_btn").show(); 
		 $("#next_btn").html("Next");
   	 step++;
		 $(".wizard_content").html(step);
	     }
	     else
	     {
		 $("#next_btn").html("Finish");

	     }

	 });

}

