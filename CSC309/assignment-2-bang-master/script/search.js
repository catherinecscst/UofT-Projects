//This is the url of yahoo whether api, we mainly use this to fetch data
var head = "https://query.yahooapis.com/v1/public/yql?q=";
var s_woeid = "select woeid from geo.places(1) where text=\"";
var s_AllDataOfWoeid = "select * from weather.forecast where woeid in (";
var tail = "\")&format=json";

//indicator of position in prediction, reset when input updates
var positionIndex=0;

//make search page
function makeSearch(){
	makeSearchStructure();
	makeSearchBody(makeSearchBodyDetail);
}

function makeSearchStructure(){
	$("#myTopnav").append("<div id=\"topnavBg\"></div>")
				  .append("<a href=\"#searchPage\">Search</a>")
				  .append("<a onclick=\"showAbout()\">About</a>");

	$("#searchPage").append("<h1>Weather Search</h1>")
					.append("<div id=\"searchBody\"></div>");	
}

function makeSearchBody(buildDetail){
	$("#searchBody").append("<input type=\"text\" id=\"searchTextField\" "
								+ "autocomplete=\"off\" data-country=\"\" "
								+"placeholder=\"City Name...\">")
					.append("<span id=\"searchButtonBg\"></span>");

	//when click searchTextField then select everything
	$("#searchTextField").click(function(){
		$("#searchTextField").select();
	});

	buildDetail();
}

function makeSearchBodyDetail(){
	$("#searchButtonBg").append("<input type=\"button\" id=\"searchButton\"" 
		+ "onclick=\"searchAction()\" value=\"Search\"/>");
}

//infomation in the won't change, unless user gives a valid input
function searchAction(){
	//user selected prediction
	var currentSelected = $(".city-autocomplete div")[positionIndex];
	var autoText = $(currentSelected).text();

	//set user selection to text filed
	$("#searchTextField").val(autoText);
	
	var searchInput = autoText;
	var url = head+s_AllDataOfWoeid+s_woeid+searchInput+tail;

	//avoid user search nothing
	if(searchInput.length == 0){
		alert("Nothing to search");
		return;
	}
	
	$.ajax({
		type: "GET",
		url: url,
		success: function(data){
			var results = data.query.results
			
			//case that fail to find a city's weather information
			if(results == null){
				alert("No weather information of this city");
				$("#searchTextField").val("");
				return;
			}

			results = data.query.results.channel;
			//after each search re-set all related view
			resetView();
			//buile following two parts for each search
			makeToday("#today",results);
			makeForcast("#forecast",results);
			
			//show user all information after first search
			activateSearchResult();
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) { 
	        alert("abnormal network connection"); 
	    } 
	});
}

function resetView(){
	$("#myTopnav").empty();
	$("#searchResult").empty();

	$("#myTopnav").append("<div id=\"topnavBg\"></div>")
				  .append("<a href=\"#searchPage\">Search</a>")
				  .append("<a href=\"#today\">Today</a>")
				  .append("<a href=\"#forecast\">Forecast</a>")
				  .append("<a onclick=\"showAbout()\">About</a>");

	$("#searchResult").append("<div id=\"today\"></div>")
					  .append("<div id=\"forecast\"></div>")
					  .append("<div id=\"clothing\"></div>");
}

function fetchSelectedPrediction(){
	//reset index
	positionIndex = 0;
	
	var prevSelected = $(".city-autocomplete div")[positionIndex];
	$(prevSelected).addClass('selected');
}

function activateSearchResult(){
	$("#searchResult").show();

	//jump to div today and adjust window height
	window.location = "index.html#today";
	shiftWindow();
}

//leave space for topnav for every page
function shiftWindow(){
	scrollBy(0,-0.09*0.25*$(document).height());
};

//show topnav background color after a 
//specific height(21% from the top of the html)
function addTopnavEffect(){
	(function($) {          
	    $(document).ready(function(){                   
	        $(window).scroll(function(){                          
	            if ($(this).scrollTop() > $(document).height()*0.21) {
	            	$("#topnavBg").css({"background-color": "#333"});
	                $('#topnavBg').fadeIn(500);
	            } else {
	            	$("#topnavBg").css({"background-color": "transparent"});
	                $('#topnavBg').fadeOut(500);
	            }
	        });
	    });
	})(jQuery);
}

//allowed user use enter key instead of click Search button
function addEntreKeyEvent(buttonID){
	var enter_keyCode = 13;
	$("#searchTextField").keyup(function(event){
	    if(event.keyCode == enter_keyCode){
	    	$('.city-autocomplete').hide();
	       	$(buttonID).click();
	    }
	});
}

//allowed user use up and down arrow to switch predictions
function setUpAndDownKey(){
	var upArror_keyCode = 38;
	var downArror_keyCode = 40;

	$(document).keydown(function(event){
		//remove background color of previous prediction
		var prevSelected = $(".city-autocomplete div")[positionIndex];
		$(prevSelected).removeClass('selected');

		if(event.keyCode == upArror_keyCode){
			if(positionIndex>0) positionIndex--;
		}else if(event.keyCode == downArror_keyCode){
			var l = $(".city-autocomplete div").length;
			if(positionIndex<l-1) positionIndex++;
		}

		//make selected prediction in different background color
		var nextSelected = $(".city-autocomplete div")[positionIndex];
		$(nextSelected).addClass("selected");
	})
}

//block default up and down arrow action
var DisableArrowKeys = function(e){
	var ar = new Array(38, 40);
    if ($.inArray(e.which, ar) > -1) {
        e.preventDefault();
        return false; 
    }
    return true;
}

/*--------------main--------------*/
makeSearch();
addTopnavEffect();

$("#searchResult").hide();
$('#searchTextField').cityAutocomplete();
$(document).bind("keydown", DisableArrowKeys);

setUpAndDownKey();
addEntreKeyEvent("#searchButton");

if(location.hash) shiftWindow();       
window.addEventListener("hashchange",shiftWindow);
