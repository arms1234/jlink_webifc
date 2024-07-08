
function apprise(string, args, callback)
{
	var default_args =
	{
		'confirm'		:	false, 		// Ok and Cancel buttons
		'verify'		:	false,		// Yes and No buttons
		'input'			:	false, 		// Text input (can be true or string for default text)
		'animate'		:	false,		// Groovy animation (can true or number, default is 400)
		'textOk'		:	'Ok',		// Ok button default text
		'textCancel'	:	'Cancel',	// Cancel button default text
		'textYes'		:	'Yes',		// Yes button default text
		'textNo'		:	'No',		// No button default text
		'prompt'        :   false,
		'select'        :   false

	};
	
	if(args) 
	{
		for(var index in default_args) 
			{ if(typeof args[index] == "undefined") args[index] = default_args[index]; } 
	}
	
	var aHeight = $(document).height();
	var aWidth = $(document).width();
	$('body').append('<div class="appriseOverlay" id="aOverlay"></div>');
	$('.appriseOverlay').css('height', aHeight).css('width', aWidth).fadeIn(100);
	$('body').append('<div class="appriseOuter"></div>');
	$('.appriseOuter').append('<div class="appriseInner"></div>');
	$('.appriseInner').append(string);
    $('.appriseOuter').css("left", ( $(window).width() - $('.appriseOuter').width() ) / 2+$(window).scrollLeft() + "px");
    $('.appriseOuter').css("top", ( $(window).height() - $('.appriseOuter').height() ) / 2 + "px");
    
    
    if(args)
	{
		if(args['animate'])
		{ 
			var aniSpeed = args['animate'];
			if(isNaN(aniSpeed)) { aniSpeed = 400; }
			$('.appriseOuter').css('top', '-200px').show().animate({top:"100px"}, aniSpeed);
		}
		else
			$('.appriseOuter').fadeIn(100); 
	}
	else
		$('.appriseOuter').fadeIn(100); 

    
    if(args)
    {
		if(args['input'])
    	{
			var input;

    		if(typeof(args['input'])=='string')
    			input = '<input type="text" class="aTextbox" t="aTextbox" value="'+args['input']+'" />';
    		else
				input = '<input type="text" class="aTextbox" t="aTextbox" />';

			if(typeof(args['prompt']) == 'string')
				input = '<div>' + args['prompt'] + input + '</div>';
			input = '<div class="aInput">'+input+'</div>';;

			$('.appriseInner').append(input)
			$('.aTextbox').focus();
    	}
    }

    
    $('.appriseInner').append('<div class="aButtons"></div>');
    if(args)
    {
		if(args['select'] && (typeof(args['select']) == 'object'))
		{
			var btns = args['select'];
			for(var i in btns)
				$('.aButtons').append('<button value="'+btns[i]+'">'+btns[i]+'</button>');
		}
		else if(args['confirm'] || args['input'])
		{ 
			$('.aButtons').append('<button value="ok">'+args['textOk']+'</button>');
			$('.aButtons').append('<button value="cancel">'+args['textCancel']+'</button>'); 
		}
		else if(args['verify'])
		{
			$('.aButtons').append('<button value="ok">'+args['textYes']+'</button>');
			$('.aButtons').append('<button value="cancel">'+args['textNo']+'</button>');
		}
		else
		    $('.aButtons').append('<button value="ok">'+args['textOk']+'</button>'); 
	}
    else
        $('.aButtons').append('<button value="ok">Ok</button>'); 
	

	$(document).keydown(function(e) 
	{
		if($('.appriseOverlay').is(':visible'))
		{
			if(e.keyCode == 13) 
				{ $('.aButtons > button[value="ok"]').click(); }
			if(e.keyCode == 27) 
				{ $('.aButtons > button[value="cancel"]').click(); }
		}
	});
	
	var aText = $('.aTextbox').val();
	if(!aText) { aText = false; }
	$('.aTextbox').keyup(function()
    	{ aText = $(this).val(); });
   
    $('.aButtons > button').click(function()
    {
    	$('.appriseOverlay').remove();
		$('.appriseOuter').remove();
    	if(callback)
    	{
			var wButton = $(this).attr("value");
			if(wButton=='ok')
			{ 
				if(args)
				{
					if(args['input'])
						callback(aText); 
					else
						callback(true); 
				}
				else
					callback(true); 
			}
			else if(wButton=='cancel')
				callback(false);
			else
				callback(wButton);
				 
		}
	});
}


function apprise_progress_box(string)
{
	
	var aHeight = $(document).height();
	var aWidth = $(document).width();
	$('body').append('<div class="appriseOverlay" id="aOverlay"></div>');
	$('.appriseOverlay').css('height', aHeight).css('width', aWidth).fadeIn(100);
	$('body').append('<div class="appriseOuter"></div>');
	$('.appriseOuter').append('<div class="appriseInner"></div>');
	$('.appriseInner').append(string);
    $('.appriseOuter').css("left", ( $(window).width() - $('.appriseOuter').width() ) / 2+$(window).scrollLeft() + "px");
    $('.appriseOuter').css("top", ( $(window).height() - $('.appriseOuter').height() ) / 2 + "px");
        
    $('.appriseOuter').fadeIn(100);

    //$('.appriseOuter').append('<div id="progressbar"></div>');
    //$('#progressbar').progressbar({value: 37});

    //.css('top', '100px')   
}




function apprise_progress_box_set_text(string)
{
    $('.appriseInner').empty();
    $('.appriseInner').append(string);
}

function apprise_close_progress_box()
{
    $('.appriseOverlay').remove();
	$('.appriseOuter').remove();
}

