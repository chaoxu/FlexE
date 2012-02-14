$(function(){
	$(".nav ul a:not(.current)").hover(function(){
		$(this).addClass("current");
	},function(){
		$(this).removeClass("current");
	});	
	$(".track1_box tbody tr:odd,.track2_box tbody tr:odd").addClass("tr_bg");	
	$(".leaderboard_tab a").click(function(){
		var index = $(".leaderboard_tab a").index($(this))+1;
		if($(this).hasClass("li_current")){
			return false;
		}else{
			$(this).parent().siblings().children().removeClass("li_current");
			$(this).addClass("li_current");
			$("ul.leaderboard_tab").nextAll().hide();
			//alert(index);
			$(".track"+index+"_box").show();
		}
	});	
	$(".ask_btn").click(function(){
		newModal();
		return false;
	});	
	
	function newModal(){
		var box = new Boxy($("#boxy"),{
			title:"Ask a question",
			closeText:"X",
			modal:true,
			draggable:true
		});
		box.resize(530,335);
	}
	$("#modify_btn").click(function(){
		$(this).text("save");
		
		$("input,textarea")
			.css({"border-color":"#92add6"})
			.focus(function(){
				$(this).select();
			})
			.attr("disabled",false);
		
	});
});
