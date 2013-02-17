$(window).load(function(){
	$(window).scroll(
		function(){
			height = $(window).scrollTop();
			if(height == 0){
				$("#nav").css({
					position: "fixed",
					left: "0",
					top: "0px"
				});
			}
			else{
				$("#nav").css({
					position: "absolute",
					left: "0",
					top: height
				});
			}
		}
	);
	
	$("#menu").hover(
		function(){$("#menu-items").slideDown(150)}, 
		function(){$("#menu-items").slideUp(150)}
	);
	
	$("#menu-items").hide();
});